$repo='Tendas240/Lethal-Company-AI-Modding-Project'
$headers=@{'User-Agent'='LC-Profile-Updater';'Cache-Control'='no-cache'}
$expectedBaseRevision='$helperRevision=''2026-09-05-import-uia-v2.2-materialization-proof'''
$replacementRevision='$helperRevision=''2026-09-17-import-uia-v2.4.1-diagnostic-build-result-url-delimiting'''

$cache=[DateTime]::UtcNow.Ticks
$baseUrl="https://raw.githubusercontent.com/$repo/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb=$cache"
$source=(Invoke-WebRequest -UseBasicParsing -Uri $baseUrl -Headers $headers).Content
if([string]::IsNullOrWhiteSpace($source)){throw 'Canonical v2.2 Gale helper source could not be loaded'}
if($source.IndexOf($expectedBaseRevision,[System.StringComparison]::Ordinal) -lt 0){
    throw 'Refusing to patch Gale helper: expected v2.2 source revision signature is absent. Repository helper drift must be reviewed first.'
}

$zipTextStartMarker='function Get-ZipEntryText {'
$materializationStartMarker='function Get-RequiredCriticalMaterializationPaths {'
$waitMarker='function Wait-ImportedProfileEvidence {'
$zipTextStart=$source.IndexOf($zipTextStartMarker,[System.StringComparison]::Ordinal)
$materializationStart=$source.IndexOf($materializationStartMarker,[System.StringComparison]::Ordinal)
$waitStart=$source.IndexOf($waitMarker,[System.StringComparison]::Ordinal)
if($zipTextStart -lt 0 -or $materializationStart -le $zipTextStart -or $waitStart -le $materializationStart){
    throw 'Refusing to patch Gale helper: v2.2 export/materialization function boundaries were not found exactly'
}

$newZipTextFunction=@'
function Get-ZipEntryText {
    param([Parameter(Mandatory=$true)][string]$ZipPath,[Parameter(Mandatory=$true)][string]$EntryName)
    Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
    $zip=[System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        $entry=$zip.GetEntry($EntryName)
        if(!$entry){throw "ZIP entry not found: $EntryName"}
        $stream=$entry.Open()
        try {
            # Windows PowerShell 5.1 showed a non-terminating New-Object overload
            # failure for the previous five-argument StreamReader constructor.
            # Select the long-standing four-argument constructor directly instead.
            try {
                $reader=[System.IO.StreamReader]::new($stream,[System.Text.Encoding]::UTF8,$true,4096)
            }
            catch {
                throw "Could not construct StreamReader for ZIP entry '$EntryName': $($_.Exception.Message)"
            }
            try {
                $text=$reader.ReadToEnd()
            }
            finally {$reader.Dispose()}
            if([string]::IsNullOrWhiteSpace($text)){
                throw "ZIP entry '$EntryName' was read as empty/whitespace; refusing to derive dependency contracts"
            }
            return $text
        }
        finally {$stream.Dispose()}
    }
    finally {$zip.Dispose()}
}
'@

$newMaterializationFunctions=@'
function Get-RequiredCriticalMaterializationPaths {
    param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$ExpectedExportText)

    # Gale stores each Thunderstore package below a namespace-package directory and
    # preserves the package's own BepInEx/plugins subtree beneath it. A fixed flat
    # DLL path therefore does not model the real runtime layout. Contracts use
    # "\**\" to mean: exactly one non-empty file with this name must exist
    # recursively below the package root.
    $basePackage='loaforc-loaforcsSoundAPI'
    $lcPackage='loaforc-loaforcsSoundAPI_LethalCompany'
    $hasBase=($ExpectedExportText.IndexOf("- name: $basePackage",[System.StringComparison]::Ordinal) -ge 0)
    $hasLc=($ExpectedExportText.IndexOf("- name: $lcPackage",[System.StringComparison]::Ordinal) -ge 0)

    # Use anchored line patterns for drift detection. The base package name is a
    # prefix of the LC package name, so a plain substring test would misclassify
    # an LC-only export as also explicitly mentioning the base package.
    $baseNamePattern='(?m)^\s*-\s*name:\s*'+[regex]::Escape($basePackage)+'\s*$'
    $lcNamePattern='(?m)^\s*-\s*name:\s*'+[regex]::Escape($lcPackage)+'\s*$'
    $mentionsBase=[regex]::IsMatch($ExpectedExportText,$baseNamePattern)
    $mentionsLc=[regex]::IsMatch($ExpectedExportText,$lcNamePattern)

    # If a package list entry is recognizable with harmless whitespace variance
    # but not by the exact validated canonical form, fail closed for review.
    if($mentionsBase -and -not $hasBase){throw "Export mentions '$basePackage' but its canonical '- name:' entry could not be resolved"}
    if($mentionsLc -and -not $hasLc){throw "Export mentions '$lcPackage' but its canonical '- name:' entry could not be resolved"}

    $required=@()
    # loaforcsSoundAPI_LethalCompany 1.0.2 has loaforcsSoundAPI as a package
    # dependency. Gale export metadata may list only the requested top-level mod,
    # so the base library is mandatory whenever the LC binding is present.
    if($hasBase -or $hasLc){
        $required+='BepInEx\plugins\loaforc-loaforcsSoundAPI\**\me.loaforc.soundapi.dll'
    }
    if($hasLc){
        $required+='BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany\**\me.loaforc.soundapi.lethalcompany.dll'
    }

    $required=@($required | Select-Object -Unique)
    if($hasLc -and $required.Count -ne 2){throw 'LethalCompany SoundAPI binding resolved without exactly two critical materialization contracts'}
    if($hasBase -and -not $hasLc -and $required.Count -ne 1){throw 'Base SoundAPI resolved without exactly one critical materialization contract'}
    return $required
}

function Get-MissingCriticalImportedFiles {
    param([Parameter(Mandatory=$true)][string]$TargetDir,[string[]]$CriticalRelativePaths=@())
    $missing=@()
    $recursiveToken='\**\'

    foreach($contractPath in @($CriticalRelativePaths)){
        $tokenIndex=$contractPath.IndexOf($recursiveToken,[System.StringComparison]::Ordinal)
        if($tokenIndex -lt 0){
            $fullPath=Join-Path $TargetDir $contractPath
            if(!(Test-Path -LiteralPath $fullPath -PathType Leaf)){$missing+=$contractPath;continue}
            try {
                if((Get-Item -LiteralPath $fullPath -ErrorAction Stop).Length -le 0){$missing+=$contractPath}
            } catch {$missing+=$contractPath}
            continue
        }

        $packageRootRelative=$contractPath.Substring(0,$tokenIndex)
        $fileName=$contractPath.Substring($tokenIndex+$recursiveToken.Length)
        $packageRoot=Join-Path $TargetDir $packageRootRelative
        if(!(Test-Path -LiteralPath $packageRoot -PathType Container)){
            $missing+=$contractPath
            continue
        }

        try {
            $hits=@(Get-ChildItem -LiteralPath $packageRoot -File -Recurse -Filter $fileName -ErrorAction Stop)
        }
        catch {
            $missing+=$contractPath
            continue
        }

        # Fail closed on absence, emptiness, or ambiguity. Runtime patchers enumerate
        # package files recursively, so one unique physical DLL inside the package
        # root is the required materialization evidence.
        if($hits.Count -ne 1){$missing+=$contractPath;continue}
        try {
            if($hits[0].Length -le 0){$missing+=$contractPath;continue}
        }
        catch {$missing+=$contractPath;continue}
    }
    return @($missing)
}
'@

$newTargetResolutionBlock=@'
$active=((Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/RuntimeInbox/ACTIVE_BUILD.txt?cb=$cache" -Headers $headers).Trim())
if(!$active){throw 'RuntimeInbox/ACTIVE_BUILD.txt ist leer'}
Write-Host "`nAktiver Repository-Build: $active" -ForegroundColor Cyan

$cache=[DateTime]::UtcNow.Ticks
$build=Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/Current/AUTO_BUILD_RESULT.json?cb=$cache" -Headers $headers
if(([string]$build.build_id) -eq $active){
    $profilePath=[string]$build.output_profile
    $expected=([string]$build.output_sha256).ToLowerInvariant()
    $expectedProfileName=[string]$build.profile_name
    if(!$expectedProfileName){$expectedProfileName=[IO.Path]::GetFileNameWithoutExtension($profilePath)}
    if(!$profilePath -or !$expected -or !$expectedProfileName){throw 'AUTO_BUILD_RESULT enthält keinen gültigen Profilpfad, Profilnamen oder SHA-256'}
}
else {
    $cache=[DateTime]::UtcNow.Ticks
    $state=Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/Current/CURRENT_STATE.json?cb=$cache" -Headers $headers
    if(([string]$state.controllers.runtime_active_build) -ne $active){
        throw "ACTIVE_BUILD '$active' stimmt weder mit AUTO_BUILD_RESULT '$($build.build_id)' noch mit CURRENT_STATE.controllers.runtime_active_build überein"
    }
    $diag=$state.selected_scope.diagnostic_revision
    if($null -eq $diag -or ([string]$diag.build_id) -ne $active){
        throw "ACTIVE_BUILD '$active' ist kein explizit gebundener CURRENT_STATE diagnostic_revision target"
    }
    if(([string]$diag.status) -ne 'PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED'){
        throw "Diagnostic runtime target '$active' hat keinen freigegebenen aktiven Status: '$($diag.status)'"
    }
    if(([string]$diag.base_build_id) -ne ([string]$build.build_id)){
        throw "Diagnostic runtime target '$active' basiert nicht auf AUTO_BUILD_RESULT '$($build.build_id)'"
    }
    if(([string]$diag.base_profile) -ne ([string]$build.output_profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$build.output_sha256).ToLowerInvariant()){
        throw "Diagnostic runtime target '$active' base profile/SHA disagree with AUTO_BUILD_RESULT"
    }

    $buildResultPath=[string]$diag.build_result
    if([string]::IsNullOrWhiteSpace($buildResultPath)){throw "Diagnostic runtime target '$active' hat keinen build_result authority path"}
    $buildResultSegments=@($buildResultPath -split '/')
    if($buildResultSegments.Count -eq 0 -or @($buildResultSegments | Where-Object {[string]::IsNullOrWhiteSpace($_) -or $_ -eq '.' -or $_ -eq '..'}).Count -gt 0){
        throw "Diagnostic runtime target '$active' hat einen ungültigen build_result repository path: '$buildResultPath'"
    }
    $encodedBuildResultPath=(@($buildResultSegments | ForEach-Object {[Uri]::EscapeDataString($_)}) -join '/')
    $cache=[DateTime]::UtcNow.Ticks
    $diagBuildUrl="https://raw.githubusercontent.com/$repo/main/${encodedBuildResultPath}?cb=$cache"
    try {
        $diagBuild=Invoke-RestMethod -UseBasicParsing -Uri $diagBuildUrl -Headers $headers -ErrorAction Stop
    }
    catch {
        throw "Diagnostic build_result konnte nicht geladen werden: '$buildResultPath' ($($_.Exception.Message))"
    }
    if(([string]$diagBuild.build_id) -ne $active){throw "Diagnostic build_result gehört zu '$($diagBuild.build_id)', erwartet '$active'"}
    if(([string]$diagBuild.output_profile) -ne ([string]$diag.profile) -or ([string]$diagBuild.output_sha256).ToLowerInvariant() -ne ([string]$diag.sha256).ToLowerInvariant()){
        throw "Diagnostic build_result profile/SHA disagree with CURRENT_STATE diagnostic_revision"
    }
    if(([string]$diagBuild.base_profile) -ne ([string]$diag.base_profile) -or ([string]$diagBuild.base_sha256).ToLowerInvariant() -ne ([string]$diag.base_sha256).ToLowerInvariant()){
        throw "Diagnostic build_result base profile/SHA disagree with CURRENT_STATE diagnostic_revision"
    }

    $profilePath=[string]$diagBuild.output_profile
    $expected=([string]$diagBuild.output_sha256).ToLowerInvariant()
    $expectedProfileName=[string]$diagBuild.profile_name
    if(!$expectedProfileName){$expectedProfileName=[IO.Path]::GetFileNameWithoutExtension($profilePath)}
    if(!$profilePath -or !$expected -or !$expectedProfileName){throw 'Diagnostic build_result enthält keinen gültigen Profilpfad, Profilnamen oder SHA-256'}
    Write-Host "Expliziter diagnostischer Runtime-Target wurde über CURRENT_STATE + build_result fail-closed verifiziert." -ForegroundColor DarkGray
}
'@

$patched=$source.Substring(0,$zipTextStart)+$newZipTextFunction+"`r`n`r`n"+$newMaterializationFunctions+"`r`n`r`n"+$source.Substring($waitStart)
$patched=$patched.Replace($expectedBaseRevision,$replacementRevision)
if($patched.IndexOf($replacementRevision,[System.StringComparison]::Ordinal) -lt 0){throw 'Failed to stamp v2.4 helper revision'}
if($patched.IndexOf('New-Object System.IO.StreamReader -ArgumentList',[System.StringComparison]::Ordinal) -ge 0){
    throw 'Refusing to launch: legacy StreamReader constructor path survived the v2.4 patch'
}

$targetStartMarker='$active=((Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/RuntimeInbox/ACTIVE_BUILD.txt?cb=$cache" -Headers $headers).Trim())'
$profileFileMarker='$profileFile=[IO.Path]::GetFileName($profilePath)'
$targetStart=$patched.IndexOf($targetStartMarker,[System.StringComparison]::Ordinal)
$profileFileStart=$patched.IndexOf($profileFileMarker,$targetStart,[System.StringComparison]::Ordinal)
if($targetStart -lt 0 -or $profileFileStart -le $targetStart){
    throw 'Refusing to patch Gale helper: v2.2 runtime-target resolution boundaries were not found exactly'
}
$patched=$patched.Substring(0,$targetStart)+$newTargetResolutionBlock+"`r`n`r`n"+$patched.Substring($profileFileStart)
if($patched.IndexOf("AUTO_BUILD_RESULT gehört zu",[System.StringComparison]::Ordinal) -ge 0){
    throw 'Refusing to launch: legacy unconditional ACTIVE_BUILD/AUTO_BUILD_RESULT mismatch abort survived the v2.4 patch'
}

Write-Host 'Launching canonical Gale importer with v2.4.1 fail-closed diagnostic-target URL delimiting, export-read and recursive package-materialization contract...' -ForegroundColor Cyan
Invoke-Expression $patched
