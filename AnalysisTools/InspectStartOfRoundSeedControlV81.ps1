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

function Write-Step { param([string]$Message) Write-Host ('[StartOfRoundSeedControlV81] ' + $Message) -ForegroundColor Cyan }
function Replace-ExactlyOnce {
    param([string]$Text,[string]$Old,[string]$New,[string]$Label)
    $matches = [regex]::Matches($Text,[regex]::Escape($Old))
    if ($matches.Count -ne 1) { throw "Base-helper contract drift for ${Label}: expected exactly one match, found $($matches.Count)." }
    return $Text.Replace($Old,$New)
}
function Get-PinnedBaseHelper {
    $escapedPath = [Uri]::EscapeDataString($BaseHelperPath) -replace '%2F','/'
    $uri = 'https://api.github.com/repos/' + $RepositoryName + '/contents/' + $escapedPath + '?ref=' + $BaseCommit
    $headers = @{ Accept='application/vnd.github+json'; 'User-Agent'='Lethal-Company-AI-Modding-Project-StartOfRoundSeedControlCapture'; 'X-GitHub-Api-Version'='2022-11-28' }
    Write-Step ('Fetching pinned generation helper at ' + $BaseCommit + '.')
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
    if ($response.sha -cne $BaseHelperBlobSha) { throw "Pinned base-helper blob mismatch: $($response.sha). Expected $BaseHelperBlobSha." }
    if ([string]::IsNullOrWhiteSpace($response.content)) { throw 'Pinned base-helper response did not contain file content.' }
    $bytes = [Convert]::FromBase64String(($response.content -replace '\s',''))
    return ((($Utf8.GetString($bytes)) -replace "`r`n","`n") -replace "`r","`n")
}
function New-StartOfRoundHelperText {
    param([string]$BaseText)
    $text = $BaseText
    $oldRequired = @'
$RequiredMethods = @(
    'GenerateNewLevelClientRpc',
    'GenerateNewFloor'
)
'@ -replace "`r`n","`n"
    $newRequired = @'
$RequiredMethods = @(
    'StartGame',
    'ChooseNewRandomMapSeed',
    'OpenShipDoors'
)
'@ -replace "`r`n","`n"
    $oldReviewed = @'
$ReviewedAppManifestSha256 = @(
    $ExpectedAppManifestSha256,
    'b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3',
    '132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e'
)
'@ -replace "`r`n","`n"
    $newReviewed = @'
$ReviewedAppManifestSha256 = @(
    $ExpectedAppManifestSha256,
    'b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3',
    '132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e',
    '4974c9249f249053275d93a5ba4f68e92346c1cfa09e89e6fce0b860c0c306a7'
)
'@ -replace "`r`n","`n"
    $replacements = @(
      @('$EvidenceRoot = ''SourceEvidence/VanillaV81/RoundManagerGeneration''','$EvidenceRoot = ''SourceEvidence/VanillaV81/StartOfRoundSeedControl''','evidence root'),
      @('$ReportName = ''ROUNDMANAGER_GENERATION_FOCUSED_DECOMPILE.txt''','$ReportName = ''STARTOFROUND_SEED_CONTROL_FOCUSED_DECOMPILE.txt''','report name'),
      @($oldReviewed,$newReviewed,'reviewed appmanifest allowlist'),
      @('$ManifestReview = ''AnalysisTools/InspectRoundManagerSpawningV81_PROVENANCE_REVIEW.md''','$ManifestReview = ''AnalysisTools/InspectRoundManagerSeedControlV81_PROVENANCE_REVIEW.md''','manifest review'),
      @($oldRequired,$newRequired,'required methods'),
      @('[RoundManagerGenerationV81] ','[StartOfRoundSeedControlV81] ','step prefix'),
      @('\bclass\s+RoundManager\b[^{]*\{','\bclass\s+StartOfRound\b[^{]*\{','class extractor'),
      @('RoundManager class declaration absent.','StartOfRound class declaration absent.','class failure'),
      @('RoundManager','StartOfRound','ILSpy target type'),
      @('^SourceEvidence/VanillaV81/RoundManagerGeneration/[0-9TZ]+-[a-f0-9]+$','^SourceEvidence/VanillaV81/StartOfRoundSeedControl/[0-9TZ]+-[a-f0-9]+$','publication allowlist'),
      @('SourceEvidence/VanillaV81/RoundManagerGeneration/20260920T000000Z-abcdef12','SourceEvidence/VanillaV81/StartOfRoundSeedControl/20260920T000000Z-abcdef12','publication self-test path'),
      @('lc-roundmanager-generation-v81-','lc-startofround-seed-control-v81-','temp prefix'),
      @('# Installed Lethal Company V81 RoundManager generation-gate evidence','# Installed Lethal Company V81 StartOfRound seed-control evidence','heading'),
      @('Scope: GenerateNewLevelClientRpc, GenerateNewFloor and one-hop direct callers within RoundManager.','Scope: StartGame, ChooseNewRandomMapSeed, OpenShipDoors and one-hop direct callers within StartOfRound; focused source also captures overrideRandomSeed, overrideSeedNumber and the RoundManager.LoadNewLevel handoff when present.','scope'),
      @('source-evidence/roundmanager-generation-v81-','source-evidence/startofround-seed-control-v81-','branch prefix'),
      @('Native V81 RoundManager generation-gate evidence for Universal Interior Viability Phase C3E3F','Native V81 StartOfRound map-seed origin, override ownership and RoundManager handoff evidence for S1.42AK-BMDSFIX1 regular map-seed control analysis','manifest purpose'),
      @('Capture exact V81 RoundManager generation-gate evidence ','Capture exact V81 StartOfRound seed-control evidence ','commit message')
    )
    foreach($r in $replacements){ $text = Replace-ExactlyOnce -Text $text -Old $r[0] -New $r[1] -Label $r[2] }
    foreach($token in @('StartGame','ChooseNewRandomMapSeed','OpenShipDoors','StartOfRoundSeedControl','4974c9249f249053275d93a5ba4f68e92346c1cfa09e89e6fce0b860c0c306a7')){
        if(-not $text.Contains($token)){ throw "Derived helper missing required contract token: $token" }
    }
    return $text
}
if($SelfTest -and $BootstrapSelfTest){ throw 'Select only one self-test mode.' }
$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-startofround-seed-control-wrapper-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
try {
    $derivedText = New-StartOfRoundHelperText -BaseText (Get-PinnedBaseHelper)
    $derivedPath = Join-Path $tempRoot 'InspectStartOfRoundSeedControlV81.derived.ps1'
    [IO.File]::WriteAllText($derivedPath,$derivedText,$Utf8)
    Write-Step 'Pinned generation-helper contract and deterministic StartOfRound transformation validated.'
    $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
    $arguments = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$derivedPath)
    if($SelfTest){$arguments += '-SelfTest'} elseif($BootstrapSelfTest){$arguments += '-BootstrapSelfTest'}
    & $powershellExe @arguments
    if($LASTEXITCODE -ne 0){ throw ('Derived StartOfRound helper failed with exit code ' + $LASTEXITCODE + '.') }
    if($SelfTest){ Write-Host 'PASS: pinned generation-helper identity, StartOfRound transformation and inherited self-tests.' -ForegroundColor Green }
    elseif($BootstrapSelfTest){ Write-Host 'PASS: pinned generation-helper identity, StartOfRound transformation and inherited isolated bootstrap self-test.' -ForegroundColor Green }
}
finally { Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue }
