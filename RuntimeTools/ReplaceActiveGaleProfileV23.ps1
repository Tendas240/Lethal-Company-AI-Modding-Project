$repo='Tendas240/Lethal-Company-AI-Modding-Project'
$headers=@{'User-Agent'='LC-Profile-Updater';'Cache-Control'='no-cache'}
$expectedBaseRevision="$helperRevision='2026-09-05-import-uia-v2.2-materialization-proof'"
$replacementRevision="$helperRevision='2026-09-05-import-uia-v2.3-recursive-package-materialization-proof'"

$cache=[DateTime]::UtcNow.Ticks
$baseUrl="https://raw.githubusercontent.com/$repo/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb=$cache"
$source=(Invoke-WebRequest -UseBasicParsing -Uri $baseUrl -Headers $headers).Content
if([string]::IsNullOrWhiteSpace($source)){throw 'Canonical v2.2 Gale helper source could not be loaded'}
if($source.IndexOf($expectedBaseRevision,[System.StringComparison]::Ordinal) -lt 0){
    throw 'Refusing to patch Gale helper: expected v2.2 source revision signature is absent. Repository helper drift must be reviewed first.'
}

$startMarker='function Get-RequiredCriticalMaterializationPaths {'
$endMarker='function Wait-ImportedProfileEvidence {'
$start=$source.IndexOf($startMarker,[System.StringComparison]::Ordinal)
$end=$source.IndexOf($endMarker,[System.StringComparison]::Ordinal)
if($start -lt 0 -or $end -le $start){throw 'Refusing to patch Gale helper: materialization function boundaries were not found exactly'}

$newMaterializationFunctions=@'
function Get-RequiredCriticalMaterializationPaths {
    param([Parameter(Mandatory=$true)][string]$ExpectedExportText)

    # Gale stores each Thunderstore package below a namespace-package directory and
    # preserves the package's own BepInEx/plugins subtree beneath it. A fixed flat
    # DLL path therefore does not model the real runtime layout. Contracts use
    # "\**\" to mean: exactly one non-empty file with this name must exist
    # recursively below the package root.
    $basePackage='loaforc-loaforcsSoundAPI'
    $lcPackage='loaforc-loaforcsSoundAPI_LethalCompany'
    $hasBase=($ExpectedExportText.IndexOf("- name: $basePackage",[System.StringComparison]::Ordinal) -ge 0)
    $hasLc=($ExpectedExportText.IndexOf("- name: $lcPackage",[System.StringComparison]::Ordinal) -ge 0)

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
    return @($required | Select-Object -Unique)
}

function Get-MissingCriticalImportedFiles {
    param([Parameter(Mandatory=$true)][string]$TargetDir,[string[]]$CriticalRelativePaths=@())
    $missing=@()
    $recursiveToken='\**\'

    foreach($contractPath in @($CriticalRelativePaths)){
        $tokenIndex=$contractPath.IndexOf($recursiveToken,[System.StringComparison]::Ordinal)
        if($tokenIndex -lt 0){
            # Compatibility fallback for any exact-path contract carried by a
            # future helper revision.
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

        # Fail closed on absence, emptiness, or ambiguity. The runtime patchers
        # enumerate package files recursively, so one unique physical DLL inside
        # the package root is the materialization evidence we actually need.
        if($hits.Count -ne 1){$missing+=$contractPath;continue}
        try {
            if($hits[0].Length -le 0){$missing+=$contractPath;continue}
        }
        catch {$missing+=$contractPath;continue}
    }
    return @($missing)
}
'@

$patched=$source.Substring(0,$start)+$newMaterializationFunctions+"`r`n`r`n"+$source.Substring($end)
$patched=$patched.Replace($expectedBaseRevision,$replacementRevision)
if($patched.IndexOf($replacementRevision,[System.StringComparison]::Ordinal) -lt 0){throw 'Failed to stamp v2.3 helper revision'}

Write-Host 'Launching canonical Gale importer with v2.3 recursive package-materialization contract...' -ForegroundColor Cyan
Invoke-Expression $patched
