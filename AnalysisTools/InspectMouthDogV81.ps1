[CmdletBinding()]
param(
    [string]$AssemblyPath
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$Repository = 'https://github.com/Tendas240/Lethal-Company-AI-Modding-Project.git'
$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$IlSpyVersion = '11.0.0.9375'
$SteamAppId = '1966720'
$EvidenceRoot = 'SourceEvidence/VanillaV81/MouthDogAI'

function Write-Step {
    param([string]$Message)
    Write-Host ('[MouthDogV81] ' + $Message) -ForegroundColor Cyan
}

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-SteamRoots {
    $roots = New-Object System.Collections.Generic.List[string]

    try {
        $steam = Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -ErrorAction Stop
        if ($steam.SteamPath) {
            $roots.Add([IO.Path]::GetFullPath(($steam.SteamPath -replace '/', '\')))
        }
    }
    catch { }

    $common = @(
        (Join-Path ${env:ProgramFiles(x86)} 'Steam'),
        (Join-Path $env:ProgramFiles 'Steam')
    )

    foreach ($candidate in $common) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            $roots.Add([IO.Path]::GetFullPath($candidate))
        }
    }

    $expanded = New-Object System.Collections.Generic.List[string]
    foreach ($root in ($roots | Select-Object -Unique)) {
        $expanded.Add($root)
        $vdf = Join-Path $root 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf) {
            $text = Get-Content -LiteralPath $vdf -Raw
            foreach ($match in [regex]::Matches($text, '"path"\s+"([^"]+)"')) {
                $library = $match.Groups[1].Value -replace '\\\\', '\'
                if ($library) {
                    $expanded.Add([IO.Path]::GetFullPath($library))
                }
            }
        }
    }

    return @($expanded | Select-Object -Unique)
}

function Resolve-AssemblyPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        if (-not (Test-Path -LiteralPath $RequestedPath -PathType Leaf)) {
            throw "AssemblyPath does not exist: $RequestedPath"
        }
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }

    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($root in (Get-SteamRoots)) {
        $candidate = Join-Path $root 'steamapps\common\Lethal Company\Lethal Company_Data\Managed\Assembly-CSharp.dll'
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $candidates.Add((Resolve-Path -LiteralPath $candidate).Path)
        }
    }

    $unique = @($candidates | Select-Object -Unique)
    if ($unique.Count -eq 0) {
        throw 'Could not locate Lethal Company_Data\Managed\Assembly-CSharp.dll in any detected Steam library. Re-run with -AssemblyPath <full path>.'
    }

    if ($unique.Count -gt 1) {
        Write-Step 'Multiple Lethal Company installs were found. Selecting the newest Assembly-CSharp.dll by LastWriteTimeUtc:'
        foreach ($path in $unique) {
            Write-Host ('  ' + $path)
        }
        return ($unique | Sort-Object { (Get-Item -LiteralPath $_).LastWriteTimeUtc } -Descending | Select-Object -First 1)
    }

    return $unique[0]
}

function Ensure-DotNetAndIlSpy {
    param([Parameter(Mandatory = $true)][string]$TempRoot)

    $toolDir = Join-Path $TempRoot 'ilspy-tool'
    New-Item -ItemType Directory -Path $toolDir -Force | Out-Null

    $dotnetExe = $null
    $dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($dotnet) {
        $sdkList = & $dotnet.Source --list-sdks 2>$null
        if ($LASTEXITCODE -eq 0 -and ($sdkList | Where-Object { $_ -match '^10\.' })) {
            $dotnetExe = $dotnet.Source
        }
    }

    if (-not $dotnetExe) {
        Write-Step '.NET 10 SDK not found; bootstrapping an isolated SDK under the temporary directory.'
        $dotnetDir = Join-Path $TempRoot 'dotnet'
        $installer = Join-Path $TempRoot 'dotnet-install.ps1'
        Invoke-WebRequest -UseBasicParsing 'https://dot.net/v1/dotnet-install.ps1' -OutFile $installer
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer -Channel '10.0' -InstallDir $dotnetDir -NoPath
        if ($LASTEXITCODE -ne 0) {
            throw 'Failed to bootstrap the temporary .NET 10 SDK.'
        }
        $dotnetExe = Join-Path $dotnetDir 'dotnet.exe'
    }

    Write-Step "Installing isolated ilspycmd $IlSpyVersion."
    & $dotnetExe tool install ilspycmd --tool-path $toolDir --version $IlSpyVersion --disable-parallel 2>&1 | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install ilspycmd $IlSpyVersion."
    }

    $ilspy = Join-Path $toolDir 'ilspycmd.exe'
    if (-not (Test-Path -LiteralPath $ilspy -PathType Leaf)) {
        throw 'ilspycmd installation completed without producing ilspycmd.exe.'
    }

    return $ilspy
}

function Find-MouthDogTypeName {
    param(
        [Parameter(Mandatory = $true)][string]$IlSpy,
        [Parameter(Mandatory = $true)][string]$Assembly
    )

    $listing = & $IlSpy -l c $Assembly 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw 'ilspycmd could not list classes from Assembly-CSharp.dll.'
    }

    $matches = @($listing | Where-Object { $_ -match 'MouthDogAI' })
    foreach ($line in $matches) {
        $text = [string]$line
        if ($text -match '^\s*(?:Class|class)\s+(.+?MouthDogAI)\s*$') {
            return $matches[0] -replace '^\s*(?:Class|class)\s+', ''
        }
        if ($text -match '([A-Za-z_][A-Za-z0-9_\.\+`]*MouthDogAI)') {
            return $Matches[1]
        }
    }

    # Runtime evidence names the loaded type MouthDogAI; try that exact global-namespace name
    # before failing. This is not a fallback patch target; it is only a decompiler lookup.
    return 'MouthDogAI'
}

function Get-EnclosingMethodRange {
    param(
        [Parameter(Mandatory = $true)][string[]]$Lines,
        [Parameter(Mandatory = $true)][int]$HitIndex
    )

    $start = -1
    $scanStart = [Math]::Max(0, $HitIndex - 80)
    for ($i = $HitIndex; $i -ge $scanStart; $i--) {
        $line = $Lines[$i]
        if ($line -match '^\s*(public|private|protected|internal)\b.*\(' -and
            $line -notmatch '^\s*(public|private|protected|internal)\s+(class|struct|interface|enum)\b') {
            $start = $i
            break
        }
    }

    if ($start -lt 0) {
        return $null
    }

    $openLine = -1
    for ($i = $start; $i -lt [Math]::Min($Lines.Count, $start + 25); $i++) {
        if ($Lines[$i].Contains('{')) {
            $openLine = $i
            break
        }
        if ($Lines[$i].TrimEnd().EndsWith(';')) {
            break
        }
    }

    if ($openLine -lt 0) {
        return $null
    }

    $depth = 0
    $seenOpen = $false
    $end = -1
    for ($i = $openLine; $i -lt $Lines.Count; $i++) {
        $chars = $Lines[$i].ToCharArray()
        foreach ($ch in $chars) {
            if ($ch -eq '{') {
                $depth++
                $seenOpen = $true
            }
            elseif ($ch -eq '}') {
                $depth--
            }
        }
        if ($seenOpen -and $depth -le 0) {
            $end = $i
            break
        }
    }

    if ($end -lt 0) {
        return $null
    }

    return [pscustomobject]@{ Start = $start; End = $end }
}

function Build-FocusedReport {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][hashtable]$Provenance
    )

    $lines = @($Source -split "`r?`n")
    $patterns = @(
        'Heard noise!',
        'Mouth dog targetPos',
        'lastheardnoisePosition',
        'DetectNoise',
        'EnterLunge',
        'OnCollideWithEnemy',
        'OnCollideWithPlayer'
    )

    $ranges = New-Object System.Collections.Generic.List[object]
    $markerHits = New-Object System.Collections.Generic.List[object]

    for ($i = 0; $i -lt $lines.Count; $i++) {
        foreach ($pattern in $patterns) {
            if ($lines[$i].IndexOf($pattern, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $markerHits.Add([pscustomobject]@{ Marker = $pattern; Line = ($i + 1) })
                $range = Get-EnclosingMethodRange -Lines $lines -HitIndex $i
                if ($range) {
                    $ranges.Add($range)
                }
            }
        }
    }

    if ($markerHits.Count -eq 0) {
        throw 'Focused MouthDogAI decompile contained none of the required marker/method names.'
    }

    $uniqueRanges = @($ranges | Sort-Object Start, End -Unique)
    $selectedLineCount = 0
    foreach ($range in $uniqueRanges) {
        $selectedLineCount += ($range.End - $range.Start + 1)
    }

    # Keep public repository evidence focused. Full MouthDogAI source remains only in memory/temp.
    if ($selectedLineCount -gt 650) {
        throw "Focused extraction expanded to $selectedLineCount source lines, above the 650-line safety ceiling. Refusing to publish an over-broad decompile."
    }

    $builder = New-Object System.Text.StringBuilder
    [void]$builder.AppendLine('# Lethal Company V81 MouthDogAI focused source evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Purpose: resolve the exact native Mouth Dog perception/target/lunge/collision boundary exposed by S1.42AG without publishing Assembly-CSharp.dll or a full game decompile.')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Provenance')
    [void]$builder.AppendLine(('- Assembly: `Lethal Company_Data/Managed/Assembly-CSharp.dll`'))
    [void]$builder.AppendLine(('- Assembly SHA-256: `' + $Provenance.AssemblySha256 + '`'))
    [void]$builder.AppendLine(('- Assembly size: `' + $Provenance.AssemblySize + '` bytes'))
    [void]$builder.AppendLine(('- Assembly LastWriteTimeUtc: `' + $Provenance.AssemblyLastWriteUtc + '`'))
    [void]$builder.AppendLine(('- Lethal Company executable SHA-256: `' + $Provenance.ExeSha256 + '`'))
    [void]$builder.AppendLine(('- Steam appmanifest buildid: `' + $Provenance.SteamBuildId + '`'))
    [void]$builder.AppendLine(('- Steam appmanifest SHA-256: `' + $Provenance.AppManifestSha256 + '`'))
    [void]$builder.AppendLine(('- Decompiler: `ilspycmd ' + $Provenance.IlSpyVersion + '`'))
    [void]$builder.AppendLine(('- Decompiled type: `' + $Provenance.TypeName + '`'))
    [void]$builder.AppendLine(('- Full local type-decompile SHA-256: `' + $Provenance.FullTypeSourceSha256 + '`'))
    [void]$builder.AppendLine(('- Capture UTC: `' + $Provenance.CaptureUtc + '`'))
    [void]$builder.AppendLine(('- Repository main at capture: `' + $Provenance.RepositoryMain + '`'))
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Absolute local paths and Windows user names are intentionally omitted.')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Marker index')
    foreach ($hit in $markerHits) {
        [void]$builder.AppendLine(('- `' + $hit.Marker + '` at local focused-type line ' + $hit.Line))
    }
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Focused method blocks')
    [void]$builder.AppendLine('Only methods containing the requested perception/target/lunge/collision markers are retained below. Unrelated MouthDogAI source is not included.')

    $blockNumber = 0
    foreach ($range in $uniqueRanges) {
        $blockNumber++
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine(('--- BLOCK ' + $blockNumber + ' / local lines ' + ($range.Start + 1) + '-' + ($range.End + 1) + ' ---'))
        for ($i = $range.Start; $i -le $range.End; $i++) {
            [void]$builder.AppendLine(('{0,5}: {1}' -f ($i + 1), $lines[$i]))
        }
    }

    return $builder.ToString()
}

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-mouthdog-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

try {
    Write-Step 'Locating local Lethal Company Assembly-CSharp.dll.'
    $resolvedAssembly = Resolve-AssemblyPath -RequestedPath $AssemblyPath
    $assemblyInfo = Get-Item -LiteralPath $resolvedAssembly
    $managedDir = Split-Path -Parent $resolvedAssembly
    $dataDir = Split-Path -Parent $managedDir
    $gameRoot = Split-Path -Parent $dataDir
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)

    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    $exeSha = 'NOT_FOUND'
    if (Test-Path -LiteralPath $exePath -PathType Leaf) {
        $exeSha = Get-Sha256Lower -Path $exePath
    }

    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    $appManifestSha = 'NOT_FOUND'
    $steamBuildId = 'UNKNOWN'
    if (Test-Path -LiteralPath $appManifest -PathType Leaf) {
        $appManifestSha = Get-Sha256Lower -Path $appManifest
        $manifestText = Get-Content -LiteralPath $appManifest -Raw
        if ($manifestText -match '"buildid"\s+"([0-9]+)"') {
            $steamBuildId = $Matches[1]
        }
    }

    $assemblySha = Get-Sha256Lower -Path $resolvedAssembly
    Write-Step ('Assembly SHA-256: ' + $assemblySha)

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'Git is required to publish the focused evidence branch, but git.exe is not available on PATH.'
    }

    $ilspy = Ensure-DotNetAndIlSpy -TempRoot $tempRoot
    $ilspyVersionText = (& $ilspy --version 2>&1 | Out-String).Trim()

    $typeName = Find-MouthDogTypeName -IlSpy $ilspy -Assembly $resolvedAssembly
    Write-Step ('Decompiling only type: ' + $typeName)
    $source = (& $ilspy -t $typeName -r $managedDir $resolvedAssembly 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0 -or -not $source.Trim()) {
        throw "Focused ilspycmd decompile failed for type '$typeName'."
    }

    $sourceBytes = [Text.Encoding]::UTF8.GetBytes($source)
    $sha256 = [Security.Cryptography.SHA256]::Create()
    try {
        $fullTypeSourceSha = ([BitConverter]::ToString($sha256.ComputeHash($sourceBytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $sha256.Dispose()
    }

    $captureUtc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')

    Write-Step 'Creating temporary shallow repository clone for provenance and evidence branch publication.'
    $cloneDir = Join-Path $tempRoot 'repo'
    & git clone --quiet --depth 1 --branch main $Repository $cloneDir
    if ($LASTEXITCODE -ne 0) {
        throw 'Failed to clone repository main.'
    }

    Push-Location $cloneDir
    try {
        $repoMain = (& git rev-parse HEAD).Trim()
        if (-not $repoMain) {
            throw 'Could not resolve repository main commit in temporary clone.'
        }

        $branch = 'source-evidence/mouthdog-v81-' + $stamp.ToLowerInvariant()
        & git checkout -q -b $branch
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create evidence branch $branch."
        }

        $provenance = @{
            AssemblySha256 = $assemblySha
            AssemblySize = $assemblyInfo.Length
            AssemblyLastWriteUtc = $assemblyInfo.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ss.fffffffZ')
            ExeSha256 = $exeSha
            SteamBuildId = $steamBuildId
            AppManifestSha256 = $appManifestSha
            IlSpyVersion = $IlSpyVersion
            IlSpyVersionOutput = $ilspyVersionText
            TypeName = $typeName
            FullTypeSourceSha256 = $fullTypeSourceSha
            CaptureUtc = $captureUtc
            RepositoryMain = $repoMain
        }

        $report = Build-FocusedReport -Source $source -Provenance $provenance
        $reportBytes = [Text.Encoding]::UTF8.GetBytes($report)
        $reportShaObj = [Security.Cryptography.SHA256]::Create()
        try {
            $reportSha = ([BitConverter]::ToString($reportShaObj.ComputeHash($reportBytes))).Replace('-', '').ToLowerInvariant()
        }
        finally {
            $reportShaObj.Dispose()
        }

        $relativeDir = ($EvidenceRoot + '/' + $stamp)
        $evidenceDir = Join-Path $cloneDir ($relativeDir -replace '/', '\')
        New-Item -ItemType Directory -Path $evidenceDir -Force | Out-Null

        $reportPath = Join-Path $evidenceDir 'MOUTHDOGAI_FOCUSED_DECOMPILE.txt'
        [IO.File]::WriteAllText($reportPath, $report, (New-Object Text.UTF8Encoding($false)))

        $manifest = [ordered]@{
            schema_version = 1
            purpose = 'V81 MouthDogAI focused native source evidence for S1.42AG remaining targeting-path analysis'
            capture_utc = $captureUtc
            repository = $RepositoryName
            repository_main_at_capture = $repoMain
            game_contract = 'Lethal Company V81 project-local installation; Steam buildid is recorded for independent provenance checking'
            source_assembly = [ordered]@{
                logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'
                sha256 = $assemblySha
                size_bytes = $assemblyInfo.Length
                last_write_utc = $assemblyInfo.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ss.fffffffZ')
            }
            game_executable = [ordered]@{
                logical_path = 'Lethal Company.exe'
                sha256 = $exeSha
            }
            steam = [ordered]@{
                app_id = $SteamAppId
                appmanifest_logical_name = ('appmanifest_' + $SteamAppId + '.acf')
                appmanifest_sha256 = $appManifestSha
                buildid = $steamBuildId
            }
            decompiler = [ordered]@{
                tool = 'ilspycmd'
                package_version = $IlSpyVersion
                version_output = $ilspyVersionText
                type = $typeName
                full_local_type_decompile_sha256 = $fullTypeSourceSha
            }
            published_evidence = [ordered]@{
                file = 'MOUTHDOGAI_FOCUSED_DECOMPILE.txt'
                sha256 = $reportSha
                scope = @('Heard noise!', 'Mouth dog targetPos', 'lastheardnoisePosition', 'DetectNoise', 'EnterLunge', 'OnCollideWithEnemy', 'OnCollideWithPlayer')
                excludes = @('Assembly-CSharp.dll', 'full Assembly-CSharp decompile', 'absolute local paths', 'Windows user name')
            }
        }

        $manifestPath = Join-Path $evidenceDir 'MANIFEST.json'
        $manifestJson = $manifest | ConvertTo-Json -Depth 8
        [IO.File]::WriteAllText($manifestPath, ($manifestJson + "`n"), (New-Object Text.UTF8Encoding($false)))

        & git add -- $relativeDir
        if ($LASTEXITCODE -ne 0) {
            throw 'Failed to stage focused source evidence.'
        }

        $staged = @(& git diff --cached --name-only)
        if ($staged.Count -ne 2) {
            throw ('Safety check failed: expected exactly two staged evidence files, got: ' + ($staged -join ', '))
        }
        foreach ($path in $staged) {
            if ($path -notlike ($EvidenceRoot + '/*') -or $path -match '\.(dll|exe|cs|zip|r2z)$') {
                throw ('Safety check refused staged path: ' + $path)
            }
        }

        $userName = (& git config user.name 2>$null | Out-String).Trim()
        $userEmail = (& git config user.email 2>$null | Out-String).Trim()
        if (-not $userName) {
            & git config user.name 'Tendas240'
        }
        if (-not $userEmail) {
            & git config user.email '71498430+Tendas240@users.noreply.github.com'
        }

        & git commit -q -m ('Capture V81 MouthDogAI focused source evidence ' + $stamp)
        if ($LASTEXITCODE -ne 0) {
            throw 'Failed to commit focused source evidence.'
        }

        Write-Step ('Pushing temporary evidence branch: ' + $branch)
        & git push -q -u origin $branch
        if ($LASTEXITCODE -ne 0) {
            throw 'Evidence branch push failed. No Assembly-CSharp.dll or full decompile was staged; check Git credentials and retry.'
        }

        $evidenceCommit = (& git rev-parse HEAD).Trim()
        Write-Host ''
        Write-Host 'SUCCESS' -ForegroundColor Green
        Write-Host ('Evidence branch : ' + $branch)
        Write-Host ('Evidence commit : ' + $evidenceCommit)
        Write-Host ('Assembly SHA-256: ' + $assemblySha)
        Write-Host ('Steam buildid    : ' + $steamBuildId)
        Write-Host 'Only the focused report and manifest were pushed. The game DLL and complete decompile were not uploaded.'
    }
    finally {
        Pop-Location
    }
}
finally {
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
