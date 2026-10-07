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
$RequiredSeedControlTokens = @('overrideRandomSeed','overrideSeedNumber','LoadNewLevel')
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
    $oldDecompile = @'
    Write-Step 'Extracting the exact RoundManager type locally.'
    $source = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', 'RoundManager', '-r', $managedDir, $assemblyPath
    ) -Label 'RoundManager decompile'
    if ([string]::IsNullOrWhiteSpace($source)) { throw 'Decompiler returned empty source.' }
    $methods = @(Get-FocusedMethods -Source $source -Required $RequiredMethods)
'@ -replace "`r`n","`n"
    $newDecompile = @'
    Write-Step 'Extracting the exact StartOfRound type locally.'
    $source = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', 'StartOfRound', '-r', $managedDir, $assemblyPath
    ) -Label 'StartOfRound decompile'
    if ([string]::IsNullOrWhiteSpace($source)) { throw 'Decompiler returned empty source.' }
    $methods = @(Get-FocusedMethods -Source $source -Required $RequiredMethods)
    foreach ($token in $RequiredSeedControlTokens) {
        if (-not $source.Contains($token)) { throw ('StartOfRound source is missing required seed-control token: ' + $token) }
    }
    $referenceLines = New-Object System.Collections.Generic.List[string]
    $sourceLines = @($source -split "`r?`n")
    $localTokenCounts = @{}
    foreach ($token in @('overrideRandomSeed','overrideSeedNumber')) {
        $matches = @()
        for ($lineIndex = 0; $lineIndex -lt $sourceLines.Count; $lineIndex++) {
            if ($sourceLines[$lineIndex].Contains($token)) { $matches += $lineIndex }
        }
        if ($matches.Count -lt 2) { throw ('Expected declaration plus at least one StartOfRound reference for ' + $token + ', found ' + $matches.Count + '.') }
        $localTokenCounts[$token] = $matches.Count
        foreach ($lineIndex in $matches) {
            $from = [Math]::Max(0,$lineIndex-2); $to = [Math]::Min($sourceLines.Count-1,$lineIndex+2)
            [void]$referenceLines.Add(('--- StartOfRound ' + $token + ' context / local type line ' + ($lineIndex+1) + ' ---'))
            for ($contextIndex=$from; $contextIndex -le $to; $contextIndex++) { [void]$referenceLines.Add($sourceLines[$contextIndex]) }
        }
    }
    $loadMatches = @($methods | Where-Object { $_.Text -match '\bLoadNewLevel\s*\(' })
    if ($loadMatches.Count -eq 0) { throw 'Focused StartOfRound methods do not contain the RoundManager.LoadNewLevel handoff.' }

    Write-Step 'Scanning exact Assembly-CSharp decompile for assembly-wide override-field references.'
    $assemblyProjectDir = Join-Path $script:CaptureTempRoot 'assembly-reference-scan'
    New-Item -ItemType Directory -Path $assemblyProjectDir -Force | Out-Null
    $projectOutput = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-p', '-o', $assemblyProjectDir, '-r', $managedDir, $assemblyPath
    ) -Label 'Assembly-CSharp project decompile'
    if (-not [string]::IsNullOrWhiteSpace($projectOutput)) { Write-Host $projectOutput }
    $assemblyCsFiles = @(Get-ChildItem -LiteralPath $assemblyProjectDir -Recurse -File -Filter '*.cs' | Sort-Object FullName)
    if ($assemblyCsFiles.Count -eq 0) { throw 'Assembly-wide decompile produced no C# source files.' }
    $assemblyReferenceLines = New-Object System.Collections.Generic.List[string]
    $assemblyTokenCounts = @{}
    foreach ($token in @('overrideRandomSeed','overrideSeedNumber')) {
        $tokenCount = 0
        foreach ($file in $assemblyCsFiles) {
            $fileLines = [IO.File]::ReadAllLines($file.FullName)
            for ($lineIndex = 0; $lineIndex -lt $fileLines.Count; $lineIndex++) {
                if ($fileLines[$lineIndex] -notmatch ('\b' + [regex]::Escape($token) + '\b')) { continue }
                $tokenCount++
                $relativePath = $file.FullName.Substring($assemblyProjectDir.Length).TrimStart([char[]]"\/") -replace '\\','/'
                $from = [Math]::Max(0,$lineIndex-6); $to = [Math]::Min($fileLines.Count-1,$lineIndex+6)
                [void]$assemblyReferenceLines.Add(('--- Assembly-CSharp ' + $token + ' context / ' + $relativePath + ':' + ($lineIndex+1) + ' ---'))
                for ($contextIndex=$from; $contextIndex -le $to; $contextIndex++) { [void]$assemblyReferenceLines.Add($fileLines[$contextIndex]) }
            }
        }
        if ($tokenCount -lt $localTokenCounts[$token]) { throw ('Assembly-wide reference scan found fewer ' + $token + ' occurrences than the StartOfRound type: ' + $tokenCount + ' < ' + $localTokenCounts[$token] + '.') }
        $assemblyTokenCounts[$token] = $tokenCount
    }
'@ -replace "`r`n","`n"
    $oldReportTail = @'
    foreach ($method in $methods) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
        [void]$builder.AppendLine($method.Text)
    }
    $report = $builder.ToString()
'@ -replace "`r`n","`n"
    $newReportTail = @'
    foreach ($method in $methods) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
        [void]$builder.AppendLine($method.Text)
    }
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Direct StartOfRound override-field reference contexts')
    [void]$builder.AppendLine('These bounded contexts enumerate every direct occurrence of overrideRandomSeed and overrideSeedNumber in the exact decompiled StartOfRound type, including declarations and reads/writes.')
    foreach ($referenceLine in $referenceLines) { [void]$builder.AppendLine($referenceLine) }
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Assembly-wide override-field reference contexts')
    [void]$builder.AppendLine('The exact Assembly-CSharp.dll was also decompiled as a temporary local project. The contexts below enumerate every decompiled C# occurrence of overrideRandomSeed and overrideSeedNumber across that assembly; only these bounded contexts are published, not the full project.')
    foreach ($referenceLine in $assemblyReferenceLines) { [void]$builder.AppendLine($referenceLine) }
    $report = $builder.ToString()
'@ -replace "`r`n","`n"
    $oldExtractorFixture = @'
public class RoundManager {
    public void SpawnEnemyGameObject(int number = 0)
'@ -replace "`r`n","`n"
    $newExtractorFixture = @'
public class StartOfRound {
    public void SpawnEnemyGameObject(int number = 0)
'@ -replace "`r`n","`n"
    $oldStubFixture = '$stub = ''public class RoundManager {'' + [char]10 + ''public void SpawnEnemyGameObject() { throw null; }'' + [char]10 + ''}'''
    $newStubFixture = '$stub = ''public class StartOfRound {'' + [char]10 + ''public void SpawnEnemyGameObject() { throw null; }'' + [char]10 + ''}'''
    $oldDecompilerMetadata = @'
        decompiler = @{ tool = 'ilspycmd'; version = $IlSpyVersion; type = 'RoundManager'; full_local_type_source_sha256 = (Get-TextSha256 $source) }
'@ -replace "`r`n","`n"
    $newDecompilerMetadata = @'
        decompiler = @{ tool = 'ilspycmd'; version = $IlSpyVersion; type = 'StartOfRound'; full_local_type_source_sha256 = (Get-TextSha256 $source) }
        assembly_reference_scan = @{ mode = 'ilspycmd project decompile'; source_file_count = $assemblyCsFiles.Count; overrideRandomSeed_occurrences = $assemblyTokenCounts['overrideRandomSeed']; overrideSeedNumber_occurrences = $assemblyTokenCounts['overrideSeedNumber'] }
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
      @($oldExtractorFixture,$newExtractorFixture,'extractor fixture class'),
      @($oldStubFixture,$newStubFixture,'stub fixture class'),
      @($oldDecompile,$newDecompile,'capture decompile block'),
      @('^SourceEvidence/VanillaV81/RoundManagerGeneration/[0-9TZ]+-[a-f0-9]+$','^SourceEvidence/VanillaV81/StartOfRoundSeedControl/[0-9TZ]+-[a-f0-9]+$','publication allowlist'),
      @('SourceEvidence/VanillaV81/RoundManagerGeneration/20260920T000000Z-abcdef12','SourceEvidence/VanillaV81/StartOfRoundSeedControl/20260920T000000Z-abcdef12','publication self-test path'),
      @('lc-roundmanager-generation-v81-','lc-startofround-seed-control-v81-','temp prefix'),
      @('# Installed Lethal Company V81 RoundManager generation-gate evidence','# Installed Lethal Company V81 StartOfRound seed-control evidence','heading'),
      @('Scope: GenerateNewLevelClientRpc, GenerateNewFloor and one-hop direct callers within RoundManager.','Scope: StartGame, ChooseNewRandomMapSeed, OpenShipDoors and one-hop direct callers within StartOfRound, plus every decompiled Assembly-CSharp occurrence of overrideRandomSeed and overrideSeedNumber and the focused RoundManager.LoadNewLevel handoff.','scope'),
      @($oldReportTail,$newReportTail,'override reference report'),
      @('source-evidence/roundmanager-generation-v81-','source-evidence/startofround-seed-control-v81-','branch prefix'),
      @('Native V81 RoundManager generation-gate evidence for Universal Interior Viability Phase C3E3F','Native V81 StartOfRound map-seed origin, override ownership and RoundManager handoff evidence for S1.42AK-BMDSFIX1 regular map-seed control analysis','manifest purpose'),
      @($oldDecompilerMetadata,$newDecompilerMetadata,'manifest decompiler type'),
      @('Capture exact V81 RoundManager generation-gate evidence ','Capture exact V81 StartOfRound seed-control evidence ','commit message')
    )
    foreach($r in $replacements){ $text = Replace-ExactlyOnce -Text $text -Old $r[0] -New $r[1] -Label $r[2] }
    foreach($token in @('StartGame','ChooseNewRandomMapSeed','OpenShipDoors','overrideRandomSeed','overrideSeedNumber','LoadNewLevel','Assembly-CSharp project decompile','assembly_reference_scan','StartOfRoundSeedControl','4974c9249f249053275d93a5ba4f68e92346c1cfa09e89e6fce0b860c0c306a7')){
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
