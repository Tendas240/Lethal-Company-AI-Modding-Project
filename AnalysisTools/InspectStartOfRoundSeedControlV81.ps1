#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest, [switch]$BootstrapSelfTest)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$BaseCommit = 'a8a3bafa7896775aecca73a670f5a459e3b59251'
$BaseHelperPath = 'AnalysisTools/InspectRoundManagerSeedControlV81.ps1'
$BaseHelperBlobSha = 'bdb8c4e743bea26a2a328275dda3777ceb3125c6'
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Write-Step {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host ('[StartOfRoundSeedControlV81] ' + $Message) -ForegroundColor Cyan
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
        'User-Agent' = 'Lethal-Company-AI-Modding-Project-StartOfRoundSeedControlCapture'
        'X-GitHub-Api-Version' = '2022-11-28'
    }
    Write-Step ('Fetching pinned seed-control helper at ' + $BaseCommit + '.')
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    if ($response.sha -cne $BaseHelperBlobSha) {
        throw "Pinned base-helper blob mismatch: $($response.sha). Expected $BaseHelperBlobSha."
    }
    if ([string]::IsNullOrWhiteSpace($response.content)) { throw 'Pinned base-helper response did not contain file content.' }
    $bytes = [Convert]::FromBase64String(($response.content -replace '\s', ''))
    return ((($Utf8.GetString($bytes)) -replace "`r`n", "`n") -replace "`r", "`n")
}

function New-StartOfRoundHelperText {
    param([Parameter(Mandatory = $true)][string]$BaseText)

    $text = $BaseText
    $oldRequired = @'
$RequiredMethods = @(
    'LoadNewLevelWait',
    'InitializeRandomNumberGenerators',
    'GetRandomWeightedIndex'
)
'@ -replace "`r`n", "`n"
    $newRequired = @'
$RequiredMethods = @(
    'StartGame',
    'ChooseNewRandomMapSeed',
    'OpenShipDoors'
)
'@ -replace "`r`n", "`n"

    $replacements = @(
        [pscustomobject]@{ Old = '$EvidenceRoot = ''SourceEvidence/VanillaV81/RoundManagerSeedControl'''; New = '$EvidenceRoot = ''SourceEvidence/VanillaV81/StartOfRoundSeedControl'''; Label = 'evidence root' },
        [pscustomobject]@{ Old = '$ReportName = ''ROUNDMANAGER_SEED_CONTROL_FOCUSED_DECOMPILE.txt'''; New = '$ReportName = ''STARTOFROUND_SEED_CONTROL_FOCUSED_DECOMPILE.txt'''; Label = 'report name' },
        [pscustomobject]@{ Old = $oldRequired; New = $newRequired; Label = 'required method set' },
        [pscustomobject]@{ Old = '[RoundManagerSeedControlV81] '; New = '[StartOfRoundSeedControlV81] '; Label = 'step prefix' },
        [pscustomobject]@{ Old = '^SourceEvidence/VanillaV81/RoundManagerSeedControl/[0-9TZ]+-[a-f0-9]+$'; New = '^SourceEvidence/VanillaV81/StartOfRoundSeedControl/[0-9TZ]+-[a-f0-9]+$'; Label = 'publication allowlist' },
        [pscustomobject]@{ Old = 'SourceEvidence/VanillaV81/RoundManagerSeedControl/20260920T000000Z-abcdef12'; New = 'SourceEvidence/VanillaV81/StartOfRoundSeedControl/20260920T000000Z-abcdef12'; Label = 'publication self-test path' },
        [pscustomobject]@{ Old = 'lc-roundmanager-seed-control-v81-'; New = 'lc-startofround-seed-control-v81-'; Label = 'temporary directory prefix' },
        [pscustomobject]@{ Old = '# Installed Lethal Company V81 RoundManager seed-control evidence'; New = '# Installed Lethal Company V81 StartOfRound seed-control evidence'; Label = 'report heading' },
        [pscustomobject]@{ Old = 'Scope: LoadNewLevelWait, InitializeRandomNumberGenerators, GetRandomWeightedIndex and one-hop direct callers within RoundManager.'; New = 'Scope: StartOfRound.StartGame, ChooseNewRandomMapSeed, OpenShipDoors and one-hop direct callers; include direct assembly references needed to classify overrideRandomSeed and overrideSeedNumber ownership and the handoff to RoundManager.LoadNewLevel.'; Label = 'report scope' },
        [pscustomobject]@{ Old = 'source-evidence/roundmanager-seed-control-v81-'; New = 'source-evidence/startofround-seed-control-v81-'; Label = 'evidence branch prefix' },
        [pscustomobject]@{ Old = 'Native V81 RoundManager map-seed origin and RNG evidence for S1.42AK-BMDSFIX1 regular map-seed control analysis'; New = 'Native V81 StartOfRound map-seed origin, override ownership and RoundManager handoff evidence for S1.42AK-BMDSFIX1 regular map-seed control analysis'; Label = 'manifest purpose' },
        [pscustomobject]@{ Old = 'Capture exact V81 RoundManager seed-control evidence '; New = 'Capture exact V81 StartOfRound seed-control evidence '; Label = 'evidence commit message' }
    )

    if ($replacements.Count -ne 12) { throw "StartOfRound replacement contract expected 12 records, found $($replacements.Count)." }
    foreach ($replacement in $replacements) {
        $text = Replace-ExactlyOnce -Text $text -Old $replacement.Old -New $replacement.New -Label $replacement.Label
    }

    # The inherited extractor is type-focused on RoundManager. Change only its type anchor,
    # retaining the proven decompiler/bootstrap/provenance/publication machinery.
    $text = Replace-ExactlyOnce -Text $text -Old '$type = $module.Types | Where-Object { $_.Name -eq ''RoundManager'' } | Select-Object -First 1' -New '$type = $module.Types | Where-Object { $_.Name -eq ''StartOfRound'' } | Select-Object -First 1' -Label 'target type'
    $text = Replace-ExactlyOnce -Text $text -Old "throw 'RoundManager type not found.'" -New "throw 'StartOfRound type not found.'" -Label 'target type failure'

    # Extend the focused evidence with explicit field/reference searches without modifying gameplay.
    $oldWriteReport = '[IO.File]::WriteAllText($reportPath, ($report -join "`n"), $Utf8)'
    $newWriteReport = @'
$report += ''
$report += '=== STARTOFROUND OVERRIDE FIELD / ASSEMBLY REFERENCE SEARCH ==='
foreach ($fieldName in @('overrideRandomSeed', 'overrideSeedNumber')) {
    $field = $type.Fields | Where-Object { $_.Name -ceq $fieldName } | Select-Object -First 1
    if ($null -eq $field) { throw "Required StartOfRound field not found: $fieldName" }
    $report += ('FIELD ' + $field.FullName)
    foreach ($candidateType in $module.Types) {
        foreach ($method in $candidateType.Methods) {
            if (-not $method.HasBody) { continue }
            foreach ($instruction in $method.Body.Instructions) {
                if ($null -ne $instruction.Operand -and $instruction.Operand.ToString().Contains($fieldName)) {
                    $report += ('REF ' + $candidateType.FullName + '::' + $method.Name + ' | ' + $instruction.ToString())
                }
            }
        }
    }
}
[IO.File]::WriteAllText($reportPath, ($report -join "`n"), $Utf8)
'@ -replace "`r`n", "`n"
    $text = Replace-ExactlyOnce -Text $text -Old $oldWriteReport -New $newWriteReport -Label 'override reference report extension'

    foreach ($required in @('StartGame', 'ChooseNewRandomMapSeed', 'OpenShipDoors', 'overrideRandomSeed', 'overrideSeedNumber', 'StartOfRoundSeedControl')) {
        if (-not $text.Contains($required)) { throw "Derived helper is missing required StartOfRound contract token: $required" }
    }
    return $text
}

if ($SelfTest -and $BootstrapSelfTest) { throw 'Select only one self-test mode.' }
$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-startofround-seed-control-wrapper-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
try {
    $baseText = Get-PinnedBaseHelper
    $derivedText = New-StartOfRoundHelperText -BaseText $baseText
    $derivedPath = Join-Path $tempRoot 'InspectStartOfRoundSeedControlV81.derived.ps1'
    [IO.File]::WriteAllText($derivedPath, $derivedText, $Utf8)
    Write-Step 'Pinned base-helper contract and deterministic StartOfRound transformation validated.'
    $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
    $arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $derivedPath)
    if ($SelfTest) { $arguments += '-SelfTest' }
    elseif ($BootstrapSelfTest) { $arguments += '-BootstrapSelfTest' }
    & $powershellExe @arguments
    if ($LASTEXITCODE -ne 0) { throw ('Derived StartOfRound helper failed with exit code ' + $LASTEXITCODE + '.') }
    if ($SelfTest) { Write-Host 'PASS: pinned helper identity, exact StartOfRound transformation contract and inherited helper self-tests.' -ForegroundColor Green }
    elseif ($BootstrapSelfTest) { Write-Host 'PASS: pinned helper identity, exact StartOfRound transformation contract and inherited isolated bootstrap self-test.' -ForegroundColor Green }
}
finally {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}
