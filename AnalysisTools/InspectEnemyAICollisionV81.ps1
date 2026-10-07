#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$Repository = 'https://github.com/Tendas240/Lethal-Company-AI-Modding-Project.git'
$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$IlSpyVersion = '11.0.0.9375'
$NuGetSource = 'https://api.nuget.org/v3/index.json'
$SteamAppId = '1966720'
$ExpectedAssemblySha256 = '5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731'
$ExpectedExeSha256 = '24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1'
$ExpectedSteamBuildId = '22825947'
$ExpectedAppManifestSha256 = 'fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432'
$ExistingMouthDogManifest = 'SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json'
$EvidenceRoot = 'SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy'
$ReportName = 'ENEMYAI_ONCOLLIDEWITHENEMY_FOCUSED_DECOMPILE.txt'

function Write-Step {
    param([string]$Message)
    Write-Host ('[EnemyAICollisionV81] ' + $Message) -ForegroundColor Cyan
}

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-SteamRoots {
    $roots = @()

    try {
        $steam = Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -ErrorAction Stop
        if ($steam.SteamPath) {
            $roots += [IO.Path]::GetFullPath(($steam.SteamPath -replace '/', '\'))
        }
    }
    catch { }

    if (${env:ProgramFiles(x86)}) {
        $candidate = Join-Path ${env:ProgramFiles(x86)} 'Steam'
        if (Test-Path -LiteralPath $candidate) {
            $roots += [IO.Path]::GetFullPath($candidate)
        }
    }
    if ($env:ProgramFiles) {
        $candidate = Join-Path $env:ProgramFiles 'Steam'
        if (Test-Path -LiteralPath $candidate) {
            $roots += [IO.Path]::GetFullPath($candidate)
        }
    }

    $expanded = @()
    foreach ($root in ($roots | Select-Object -Unique)) {
        $expanded += $root
        $vdf = Join-Path $root 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf -PathType Leaf) {
            $text = Get-Content -LiteralPath $vdf -Raw
            foreach ($match in [regex]::Matches($text, '"path"\s+"([^"]+)"')) {
                $library = $match.Groups[1].Value -replace '\\\\', '\'
                if ($library) {
                    $expanded += [IO.Path]::GetFullPath($library)
                }
            }
        }
    }

    return @($expanded | Select-Object -Unique)
}

function Resolve-AssemblyPath {
    $candidates = @()
    foreach ($root in (Get-SteamRoots)) {
        $candidate = Join-Path $root 'steamapps\common\Lethal Company\Lethal Company_Data\Managed\Assembly-CSharp.dll'
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $candidates += (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    $unique = @($candidates | Select-Object -Unique)
    if ($unique.Count -eq 0) {
        throw 'Could not locate the installed Lethal Company Assembly-CSharp.dll in detected Steam libraries.'
    }
    if ($unique.Count -gt 1) {
        throw ('Multiple Lethal Company Assembly-CSharp.dll candidates were found. Refusing to guess: ' + ($unique -join '; '))
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
        if ($LASTEXITCODE -eq 0 -and @($sdkList | Where-Object { $_ -match '^10\.' }).Count -gt 0) {
            $dotnetExe = $dotnet.Source
        }
    }

    if (-not $dotnetExe) {
        Write-Step '.NET 10 SDK not found; bootstrapping an isolated SDK in the temporary directory.'
        $dotnetDir = Join-Path $TempRoot 'dotnet'
        $installer = Join-Path $TempRoot 'dotnet-install.ps1'
        Invoke-WebRequest -UseBasicParsing 'https://dot.net/v1/dotnet-install.ps1' -OutFile $installer
        $dotnetInstallOutput = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer -Channel '10.0' -InstallDir $dotnetDir -NoPath 2>&1)
        $dotnetInstallExitCode = $LASTEXITCODE
        foreach ($line in $dotnetInstallOutput) {
            Write-Host ([string]$line)
        }
        if ($dotnetInstallExitCode -ne 0) {
            throw 'Failed to bootstrap the temporary .NET 10 SDK.'
        }
        $dotnetExe = Join-Path $dotnetDir 'dotnet.exe'
    }

    $nugetConfig = Join-Path $TempRoot 'nuget.config'
    $nugetConfigText = @"
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="$NuGetSource" protocolVersion="3" />
  </packageSources>
</configuration>
"@
    [IO.File]::WriteAllText($nugetConfig, $nugetConfigText, (New-Object Text.UTF8Encoding($false)))

    Write-Step "Installing isolated ilspycmd $IlSpyVersion using an isolated NuGet config."
    & $dotnetExe tool install ilspycmd --tool-path $toolDir --version $IlSpyVersion --configfile $nugetConfig --disable-parallel 2>&1 | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install ilspycmd $IlSpyVersion from explicit source $NuGetSource."
    }

    $ilspyDllMatches = @(Get-ChildItem -LiteralPath $toolDir -Recurse -File -Filter 'ilspycmd.dll')
    if ($ilspyDllMatches.Count -ne 1) {
        throw ('Expected exactly one ilspycmd.dll in the isolated tool directory, found: ' + $ilspyDllMatches.Count)
    }

    $launcher = Join-Path $TempRoot 'run-ilspycmd.cmd'
    $launcherText = "@echo off`r`n`"$dotnetExe`" `"$($ilspyDllMatches[0].FullName)`" %*`r`nexit /b %ERRORLEVEL%`r`n"
    [IO.File]::WriteAllText($launcher, $launcherText, (New-Object Text.ASCIIEncoding))
    return $launcher
}

function Find-MethodStart {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyString()][string[]]$Lines,
        [Parameter(Mandatory = $true)][int]$HitIndex
    )

    $floor = [Math]::Max(0, $HitIndex - 100)
    for ($i = $HitIndex; $i -ge $floor; $i--) {
        $line = $Lines[$i]
        if ($line -match '^\s*(public|private|protected|internal)\b.*\(' -and
            $line -notmatch '^\s*(public|private|protected|internal)\s+(class|struct|interface|enum)\b') {
            return $i
        }
    }
    throw ('Could not find a method declaration before focused source line ' + ($HitIndex + 1))
}

function Find-MethodEnd {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyString()][string[]]$Lines,
        [Parameter(Mandatory = $true)][int]$StartIndex
    )

    $depth = 0
    $sawOpeningBrace = $false
    for ($i = $StartIndex; $i -lt $Lines.Count; $i++) {
        $opens = ([regex]::Matches($Lines[$i], '\{')).Count
        $closes = ([regex]::Matches($Lines[$i], '\}')).Count
        if ($opens -gt 0) {
            $sawOpeningBrace = $true
        }
        if ($sawOpeningBrace) {
            $depth += ($opens - $closes)
            if ($depth -eq 0) {
                return $i
            }
        }
    }
    throw ('Could not find the end of focused method beginning at source line ' + ($StartIndex + 1))
}

function Build-FocusedReport {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][hashtable]$Provenance
    )

    $lines = @($Source -split "`r?`n")
    $patterns = @('OnCollideWithEnemy', 'MeetsStandardEnemyCollisionConditions')
    $hits = @()
    $blocksByStart = @{}

    for ($i = 0; $i -lt $lines.Count; $i++) {
        foreach ($pattern in $patterns) {
            if ($lines[$i].IndexOf($pattern, [StringComparison]::Ordinal) -ge 0) {
                $hits += [pscustomobject]@{ Marker = $pattern; Line = ($i + 1) }
                $start = Find-MethodStart -Lines $lines -HitIndex $i
                $end = Find-MethodEnd -Lines $lines -StartIndex $start
                $blocksByStart[[string]$start] = $end
            }
        }
    }

    $collisionHits = @($hits | Where-Object { $_.Marker -eq 'OnCollideWithEnemy' })
    if ($collisionHits.Count -eq 0) {
        throw 'Exact EnemyAI decompile did not contain OnCollideWithEnemy. Refusing to publish incomplete evidence.'
    }

    $selectedLineCount = 0
    foreach ($startKey in $blocksByStart.Keys) {
        $selectedLineCount += ([int]$blocksByStart[$startKey] - [int]$startKey + 1)
    }
    if ($selectedLineCount -gt 300) {
        throw "Focused EnemyAI collision extraction expanded to $selectedLineCount source lines, above the 300-line safety ceiling. Refusing to publish an over-broad decompile."
    }

    $builder = New-Object System.Text.StringBuilder
    [void]$builder.AppendLine('# Lethal Company V81 EnemyAI collision focused source evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Purpose: prove the exact Vanilla V81 EnemyAI.OnCollideWithEnemy() base contract and any directly named standard enemy-collision helper before a MouthDogAI collision Harmony boundary is considered.')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Provenance')
    [void]$builder.AppendLine('- Assembly: `Lethal Company_Data/Managed/Assembly-CSharp.dll`')
    [void]$builder.AppendLine(('- Assembly SHA-256: `' + $Provenance.AssemblySha256 + '`'))
    [void]$builder.AppendLine(('- Lethal Company executable SHA-256: `' + $Provenance.ExeSha256 + '`'))
    [void]$builder.AppendLine(('- Steam appmanifest buildid: `' + $Provenance.SteamBuildId + '`'))
    [void]$builder.AppendLine(('- Steam appmanifest SHA-256: `' + $Provenance.AppManifestSha256 + '`'))
    [void]$builder.AppendLine(('- Decompiler: `ilspycmd ' + $Provenance.IlSpyVersion + '`'))
    [void]$builder.AppendLine('- Decompiled type: `EnemyAI`')
    [void]$builder.AppendLine(('- Full local type-decompile SHA-256: `' + $Provenance.FullTypeSourceSha256 + '`'))
    [void]$builder.AppendLine(('- Capture UTC: `' + $Provenance.CaptureUtc + '`'))
    [void]$builder.AppendLine(('- Repository main at capture: `' + $Provenance.RepositoryMain + '`'))
    [void]$builder.AppendLine(('- Bound to prior MouthDog capture manifest: `' + $ExistingMouthDogManifest + '`'))
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Absolute local paths, Windows user names, Assembly-CSharp.dll and the full EnemyAI type decompile are intentionally excluded.')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Marker index')
    foreach ($hit in $hits) {
        [void]$builder.AppendLine(('- `' + $hit.Marker + '` at local EnemyAI type line ' + $hit.Line))
    }
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## Exact focused method blocks')

    $block = 0
    foreach ($start in @($blocksByStart.Keys | ForEach-Object { [int]$_ } | Sort-Object)) {
        $block++
        $end = [int]$blocksByStart[[string]$start]
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine(('--- BLOCK ' + $block + ' / local lines ' + ($start + 1) + '-' + ($end + 1) + ' ---'))
        for ($i = $start; $i -le $end; $i++) {
            [void]$builder.AppendLine(('{0,5}: {1}' -f ($i + 1), $lines[$i]))
        }
    }

    return $builder.ToString()
}

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-enemyai-collision-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

try {
    Write-Step 'Locating the installed Lethal Company Assembly-CSharp.dll.'
    $resolvedAssembly = Resolve-AssemblyPath
    $assemblyInfo = Get-Item -LiteralPath $resolvedAssembly
    $managedDir = Split-Path -Parent $resolvedAssembly
    $dataDir = Split-Path -Parent $managedDir
    $gameRoot = Split-Path -Parent $dataDir
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)

    $assemblySha = Get-Sha256Lower -Path $resolvedAssembly
    if ($assemblySha -ne $ExpectedAssemblySha256) {
        throw "Installed Assembly-CSharp.dll SHA-256 is $assemblySha, expected proven V81 capture SHA-256 $ExpectedAssemblySha256. Refusing cross-build evidence."
    }

    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) {
        throw 'Lethal Company.exe was not found beside the proven Assembly-CSharp.dll.'
    }
    $exeSha = Get-Sha256Lower -Path $exePath
    if ($exeSha -ne $ExpectedExeSha256) {
        throw "Lethal Company.exe SHA-256 is $exeSha, expected $ExpectedExeSha256. Refusing cross-build evidence."
    }

    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    if (-not (Test-Path -LiteralPath $appManifest -PathType Leaf)) {
        throw "Steam appmanifest_$SteamAppId.acf was not found."
    }
    $appManifestSha = Get-Sha256Lower -Path $appManifest
    if ($appManifestSha -ne $ExpectedAppManifestSha256) {
        throw "Steam appmanifest SHA-256 is $appManifestSha, expected $ExpectedAppManifestSha256. Refusing cross-build evidence."
    }
    $manifestText = Get-Content -LiteralPath $appManifest -Raw
    if ($manifestText -notmatch '"buildid"\s+"([0-9]+)"') {
        throw 'Steam appmanifest did not contain a buildid.'
    }
    $steamBuildId = $Matches[1]
    if ($steamBuildId -ne $ExpectedSteamBuildId) {
        throw "Steam buildid is $steamBuildId, expected proven buildid $ExpectedSteamBuildId. Refusing cross-build evidence."
    }

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git.exe is required to publish the focused evidence branch, but Git is not available on PATH.'
    }

    $ilspyResult = @(Ensure-DotNetAndIlSpy -TempRoot $tempRoot)
    if ($ilspyResult.Count -ne 1) {
        throw ('Ensure-DotNetAndIlSpy returned an unexpected output count: ' + $ilspyResult.Count)
    }
    $ilspy = [string]$ilspyResult[0]
    $ilspyVersionText = (& $ilspy --version 2>&1 | Out-String).Trim()

    Write-Step 'Decompiling only exact native type EnemyAI.'
    $source = (& $ilspy -t 'EnemyAI' -r $managedDir $resolvedAssembly 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0 -or -not $source.Trim()) {
        throw 'Focused ilspycmd decompile failed for exact type EnemyAI.'
    }
    if ($source -notmatch '\bclass\s+EnemyAI\b' -or $source -notmatch '\bOnCollideWithEnemy\b') {
        throw 'Decompiled output did not validate as EnemyAI with OnCollideWithEnemy().'
    }

    $sourceBytes = [Text.Encoding]::UTF8.GetBytes($source)
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        $fullTypeSourceSha = ([BitConverter]::ToString($hash.ComputeHash($sourceBytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $hash.Dispose()
    }

    $captureUtc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')

    Write-Step 'Creating a temporary shallow clone for provenance and evidence publication.'
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

        $priorManifestPath = Join-Path $cloneDir ($ExistingMouthDogManifest -replace '/', '\')
        if (-not (Test-Path -LiteralPath $priorManifestPath -PathType Leaf)) {
            throw "Prior proven MouthDog manifest is missing from main: $ExistingMouthDogManifest"
        }
        $priorManifest = Get-Content -LiteralPath $priorManifestPath -Raw | ConvertFrom-Json
        if ([string]$priorManifest.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or
            [string]$priorManifest.steam.buildid -ne $ExpectedSteamBuildId -or
            [string]$priorManifest.game_executable.sha256 -ne $ExpectedExeSha256) {
            throw 'Prior MouthDog provenance manifest no longer matches the pinned V81 assembly/build/executable contract. Refusing publication.'
        }

        $provenance = @{
            AssemblySha256 = $assemblySha
            ExeSha256 = $exeSha
            SteamBuildId = $steamBuildId
            AppManifestSha256 = $appManifestSha
            IlSpyVersion = $IlSpyVersion
            FullTypeSourceSha256 = $fullTypeSourceSha
            CaptureUtc = $captureUtc
            RepositoryMain = $repoMain
        }
        $report = Build-FocusedReport -Source $source -Provenance $provenance

        $reportBytes = [Text.Encoding]::UTF8.GetBytes($report)
        $reportHash = [Security.Cryptography.SHA256]::Create()
        try {
            $reportSha = ([BitConverter]::ToString($reportHash.ComputeHash($reportBytes))).Replace('-', '').ToLowerInvariant()
        }
        finally {
            $reportHash.Dispose()
        }

        $branch = 'source-evidence/enemyai-collision-v81-' + $stamp.ToLowerInvariant()
        & git checkout -q -b $branch
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create evidence branch $branch."
        }

        $relativeDir = $EvidenceRoot + '/' + $stamp
        $evidenceDir = Join-Path $cloneDir ($relativeDir -replace '/', '\')
        New-Item -ItemType Directory -Path $evidenceDir -Force | Out-Null

        $reportPath = Join-Path $evidenceDir $ReportName
        [IO.File]::WriteAllText($reportPath, $report, (New-Object Text.UTF8Encoding($false)))

        $manifest = [ordered]@{
            schema_version = 1
            purpose = 'V81 EnemyAI.OnCollideWithEnemy focused native source evidence for MouthDog pre-successor base-method safety analysis'
            capture_utc = $captureUtc
            repository = $RepositoryName
            repository_main_at_capture = $repoMain
            bound_prior_evidence = $ExistingMouthDogManifest
            game_contract = 'Exact same Lethal Company V81 assembly/build/executable provenance as the successful MouthDogAI capture; mismatches fail closed before publication.'
            source_assembly = [ordered]@{
                logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'
                sha256 = $assemblySha
                size_bytes = $assemblyInfo.Length
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
                package_source = $NuGetSource
                version_output = $ilspyVersionText
                type = 'EnemyAI'
                full_local_type_decompile_sha256 = $fullTypeSourceSha
            }
            published_evidence = [ordered]@{
                file = $ReportName
                sha256 = $reportSha
                scope = @('EnemyAI.OnCollideWithEnemy', 'MeetsStandardEnemyCollisionConditions when present in exact EnemyAI type')
                excludes = @('Assembly-CSharp.dll', 'full Assembly-CSharp decompile', 'full EnemyAI type decompile', 'absolute local paths', 'Windows user name')
            }
        }

        $manifestPath = Join-Path $evidenceDir 'MANIFEST.json'
        $manifestJson = $manifest | ConvertTo-Json -Depth 8
        [IO.File]::WriteAllText($manifestPath, ($manifestJson + "`n"), (New-Object Text.UTF8Encoding($false)))

        & git add -- $relativeDir
        if ($LASTEXITCODE -ne 0) {
            throw 'Failed to stage focused EnemyAI collision source evidence.'
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
        if (-not $userName) { & git config user.name 'Tendas240' }
        if (-not $userEmail) { & git config user.email '71498430+Tendas240@users.noreply.github.com' }

        & git commit -q -m ('Capture V81 EnemyAI collision focused source evidence ' + $stamp)
        if ($LASTEXITCODE -ne 0) {
            throw 'Failed to commit focused EnemyAI collision source evidence.'
        }

        Write-Step ('Pushing temporary evidence branch: ' + $branch)
        & git push -q -u origin $branch
        if ($LASTEXITCODE -ne 0) {
            throw 'Evidence branch push failed. No game DLL or full decompile was staged; check Git credentials and retry.'
        }

        $evidenceCommit = (& git rev-parse HEAD).Trim()
        Write-Host ''
        Write-Host 'SUCCESS' -ForegroundColor Green
        Write-Host ('Evidence branch : ' + $branch)
        Write-Host ('Evidence commit : ' + $evidenceCommit)
        Write-Host ('Assembly SHA-256: ' + $assemblySha)
        Write-Host ('Steam buildid    : ' + $steamBuildId)
        Write-Host 'Only the focused EnemyAI collision report and manifest were pushed. Assembly-CSharp.dll and full decompiles were not uploaded.'
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
