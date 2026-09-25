#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest, [switch]$BootstrapSelfTest)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$BaseCommit = 'e376e09e09454b4c25b578626fafc9c721f27cda'
$BaseHelperPath = 'AnalysisTools/InspectRoundManagerGenerationV81.ps1'
$BaseHelperBlobSha = '51a577179f17343411cbdb05506cc374334497e7'
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Write-Step {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host ('[RoundManagerSeedControlV81] ' + $Message) -ForegroundColor Cyan
}

function Replace-ExactlyOnce {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Old,
        [Parameter(Mandatory = $true)][string]$New,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $matches = [regex]::Matches($Text, [regex]::Escape($Old))
    if ($matches.Count -ne 1) {
        throw "Base-helper contract drift for ${Label}: expected exactly one match, found $($matches.Count)."
    }
    return $Text.Replace($Old, $New)
}

function Get-PinnedBaseHelper {
    $escapedPath = [Uri]::EscapeDataString($BaseHelperPath) -replace '%2F', '/'
    $uri = 'https://api.github.com/repos/' + $RepositoryName + '/contents/' + $escapedPath + '?ref=' + $BaseCommit
    $headers = @{
        Accept = 'application/vnd.github+json'
        'User-Agent' = 'Lethal-Company-AI-Modding-Project-SeedControlCapture'
        'X-GitHub-Api-Version' = '2022-11-28'
    }

    Write-Step ('Fetching pinned base helper at ' + $BaseCommit + '.')
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    if ($response.sha -cne $BaseHelperBlobSha) {
        throw "Pinned base-helper blob mismatch: $($response.sha). Expected $BaseHelperBlobSha."
    }
    if ([string]::IsNullOrWhiteSpace($response.content)) {
        throw 'Pinned base-helper response did not contain file content.'
    }

    $bytes = [Convert]::FromBase64String(($response.content -replace '\s', ''))
    $text = $Utf8.GetString($bytes)
    return (($text -replace "`r`n", "`n") -replace "`r", "`n")
}

function New-SeedControlHelperText {
    param([Parameter(Mandatory = $true)][string]$BaseText)

    $text = $BaseText

    $oldRequired = @'
$RequiredMethods = @(
    'GenerateNewLevelClientRpc',
    'GenerateNewFloor'
)
'@ -replace "`r`n", "`n"
    $newRequired = @'
$RequiredMethods = @(
    'LoadNewLevelWait',
    'InitializeRandomNumberGenerators',
    'GetRandomWeightedIndex'
)
'@ -replace "`r`n", "`n"

    $replacements = @(
        [pscustomobject]@{ Old = '$EvidenceRoot = ''SourceEvidence/VanillaV81/RoundManagerGeneration'''; New = '$EvidenceRoot = ''SourceEvidence/VanillaV81/RoundManagerSeedControl'''; Label = 'evidence root' },
        [pscustomobject]@{ Old = '$ReportName = ''ROUNDMANAGER_GENERATION_FOCUSED_DECOMPILE.txt'''; New = '$ReportName = ''ROUNDMANAGER_SEED_CONTROL_FOCUSED_DECOMPILE.txt'''; Label = 'report name' },
        [pscustomobject]@{ Old = $oldRequired; New = $newRequired; Label = 'required method set' },
        [pscustomobject]@{ Old = '[RoundManagerGenerationV81] '; New = '[RoundManagerSeedControlV81] '; Label = 'step prefix' },
        [pscustomobject]@{ Old = '^SourceEvidence/VanillaV81/RoundManagerGeneration/[0-9TZ]+-[a-f0-9]+$'; New = '^SourceEvidence/VanillaV81/RoundManagerSeedControl/[0-9TZ]+-[a-f0-9]+$'; Label = 'publication allowlist' },
        [pscustomobject]@{ Old = 'SourceEvidence/VanillaV81/RoundManagerGeneration/20260920T000000Z-abcdef12'; New = 'SourceEvidence/VanillaV81/RoundManagerSeedControl/20260920T000000Z-abcdef12'; Label = 'publication self-test path' },
        [pscustomobject]@{ Old = 'lc-roundmanager-generation-v81-'; New = 'lc-roundmanager-seed-control-v81-'; Label = 'temporary directory prefix' },
        [pscustomobject]@{ Old = '# Installed Lethal Company V81 RoundManager generation-gate evidence'; New = '# Installed Lethal Company V81 RoundManager seed-control evidence'; Label = 'report heading' },
        [pscustomobject]@{ Old = 'Scope: GenerateNewLevelClientRpc, GenerateNewFloor and one-hop direct callers within RoundManager.'; New = 'Scope: LoadNewLevelWait, InitializeRandomNumberGenerators, GetRandomWeightedIndex and one-hop direct callers within RoundManager.'; Label = 'report scope' },
        [pscustomobject]@{ Old = 'source-evidence/roundmanager-generation-v81-'; New = 'source-evidence/roundmanager-seed-control-v81-'; Label = 'evidence branch prefix' },
        [pscustomobject]@{ Old = 'Native V81 RoundManager generation-gate evidence for Universal Interior Viability Phase C3E3F'; New = 'Native V81 RoundManager map-seed origin and RNG evidence for S1.42AK-BMDSFIX1 regular map-seed control analysis'; Label = 'manifest purpose' },
        [pscustomobject]@{ Old = 'Capture exact V81 RoundManager generation-gate evidence '; New = 'Capture exact V81 RoundManager seed-control evidence '; Label = 'evidence commit message' }
    )

    if ($replacements.Count -ne 12) {
        throw "Seed-control replacement contract expected 12 records, found $($replacements.Count)."
    }
    foreach ($replacement in $replacements) {
        if ([string]::IsNullOrEmpty([string]$replacement.Old) -or
            [string]::IsNullOrEmpty([string]$replacement.New) -or
            [string]::IsNullOrEmpty([string]$replacement.Label)) {
            throw 'Seed-control replacement contract contains an empty Old/New/Label value.'
        }
        $text = Replace-ExactlyOnce -Text $text -Old $replacement.Old -New $replacement.New -Label $replacement.Label
    }

    foreach ($required in @('LoadNewLevelWait', 'InitializeRandomNumberGenerators', 'GetRandomWeightedIndex')) {
        if ($text -notmatch [regex]::Escape("'$required'")) {
            throw "Derived helper is missing required method target: $required."
        }
    }
    if ($text.Contains($oldRequired)) {
        throw 'Derived helper retained the old generation-gate required-method block.'
    }
    if ($text -notmatch [regex]::Escape("$" + "EvidenceRoot = 'SourceEvidence/VanillaV81/RoundManagerSeedControl'")) {
        throw 'Derived helper evidence root assertion failed.'
    }

    return $text
}

if ($SelfTest -and $BootstrapSelfTest) {
    throw 'Select only one self-test mode.'
}

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-roundmanager-seed-control-wrapper-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
try {
    $baseText = Get-PinnedBaseHelper
    $derivedText = New-SeedControlHelperText -BaseText $baseText
    $derivedPath = Join-Path $tempRoot 'InspectRoundManagerSeedControlV81.derived.ps1'
    [IO.File]::WriteAllText($derivedPath, $derivedText, $Utf8)

    Write-Step 'Pinned base-helper contract and deterministic seed-control transformation validated.'
    $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
    $arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $derivedPath)
    if ($SelfTest) {
        $arguments += '-SelfTest'
    }
    elseif ($BootstrapSelfTest) {
        $arguments += '-BootstrapSelfTest'
    }

    & $powershellExe @arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('Derived seed-control helper failed with exit code ' + $LASTEXITCODE + '.')
    }

    if ($SelfTest) {
        Write-Host 'PASS: pinned helper identity, exact transformation contract and inherited helper self-tests.' -ForegroundColor Green
    }
    elseif ($BootstrapSelfTest) {
        Write-Host 'PASS: pinned helper identity, exact transformation contract and inherited isolated bootstrap self-test.' -ForegroundColor Green
    }
}
finally {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}
