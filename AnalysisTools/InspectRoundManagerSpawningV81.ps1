#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$IlSpyVersion = '11.0.0.9375'
$NuGetSource = 'https://api.nuget.org/v3/index.json'
$SteamAppId = '1966720'
$ExpectedAssemblySha256 = '5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731'
$ExpectedExeSha256 = '24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1'
$ExpectedSteamBuildId = '22825947'
$ExpectedAppManifestSha256 = 'fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432'
$PriorManifest = 'SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json'
$EvidenceRoot = 'SourceEvidence/VanillaV81/RoundManagerSpawning'
$ReportName = 'ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt'
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$RequiredMethods = @(
    'FinishGeneratingNewLevelClientRpc', 'PredictAllOutsideEnemies',
    'SpawnNestObjectForOutsideEnemy', 'ResetEnemySpawningVariables', 'BeginEnemySpawning',
    'SpawnEnemiesOutside', 'SpawnWeedEnemies', 'SpawnRandomWeedEnemy',
    'SpawnDaytimeEnemiesOutside', 'SpawnRandomDaytimeEnemy', 'SpawnRandomOutsideEnemy',
    'PlotOutEnemiesForNextHour', 'SpawnEnemyFromVent', 'SpawnEnemyOnServer',
    'SpawnEnemyServerRpc', 'SpawnEnemyGameObject', 'DespawnEnemyOnServer',
    'DespawnEnemyServerRpc', 'DespawnEnemyGameObject'
)
function Write-Step { param([string]$Message) Write-Host ('[RoundManagerV81] ' + $Message) -ForegroundColor Cyan }
function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Get-TextSha256 {
    param([Parameter(Mandatory = $true)][string]$Text)
    $hash = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hash.ComputeHash($Utf8.GetBytes($Text)))).Replace('-', '').ToLowerInvariant() }
    finally { $hash.Dispose() }
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


function Get-CodeMask {
    param([Parameter(Mandatory = $true)][string]$Text)
    if ($Text.Contains('"""')) { throw 'Raw C# strings are outside this focused extractor contract.' }
    $pattern = @'
(?s)/\*.*?\*/|//[^\r\n]*|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'
'@
    return [regex]::Replace($Text, $pattern.Trim(), [System.Text.RegularExpressions.MatchEvaluator]{
        param($m)
        return [regex]::Replace($m.Value, '[^\r\n]', ' ')
    })
}
function Get-FocusedMethods {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string[]]$Required,
        [int]$MaxLines = 3000
    )
    $mask = Get-CodeMask $Source
    $classMatch = [regex]::Match($mask, '\bclass\s+RoundManager\b[^{]*\{')
    if (-not $classMatch.Success) { throw 'RoundManager class declaration absent.' }
    $depths = New-Object 'int[]' ($mask.Length + 1)
    $depth = 0
    for ($i = 0; $i -lt $mask.Length; $i++) {
        $depths[$i] = $depth
        if ($mask[$i] -eq '{') { $depth++ }
        elseif ($mask[$i] -eq '}') { $depth-- }
        if ($depth -lt 0) { throw 'Unbalanced C# braces.' }
    }
    $depths[$mask.Length] = $depth
    if ($depth -ne 0) { throw 'Unbalanced C# braces at end of source.' }
    $classBrace = $classMatch.Index + $classMatch.Length - 1
    $methodDepth = $depths[$classBrace] + 1
    $decls = [regex]::Matches($mask, '(?m)^[\t ]*(?:public|private|protected|internal)\s+[^\r\n{};=]*?\b(?<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(')
    $methods = @()
    foreach ($decl in $decls) {
        if ($depths[$decl.Index] -ne $methodDepth) { continue }
        $openParen = $decl.Index + $decl.Length - 1
        $paren = 1
        $pos = $openParen + 1
        while ($pos -lt $mask.Length -and $paren -gt 0) {
            if ($mask[$pos] -eq '(') { $paren++ }
            elseif ($mask[$pos] -eq ')') { $paren-- }
            $pos++
        }
        if ($paren -ne 0) { throw 'Unbalanced method signature.' }
        while ($pos -lt $mask.Length -and [char]::IsWhiteSpace($mask[$pos])) { $pos++ }
        if ($pos -ge $mask.Length -or $mask[$pos] -ne '{') { continue }
        $bodyStart = $pos
        $end = $bodyStart + 1
        while ($end -lt $mask.Length -and -not ($mask[$end] -eq '}' -and $depths[$end] -eq ($methodDepth + 1))) { $end++ }
        if ($end -ge $mask.Length) { throw 'Method body did not close.' }
        $text = $Source.Substring($decl.Index, $end - $decl.Index + 1)
        $body = $mask.Substring($bodyStart + 1, $end - $bodyStart - 1)
        $methods += [pscustomobject]@{
            Name = $decl.Groups['name'].Value
            Signature = $Source.Substring($decl.Index, $bodyStart - $decl.Index).Trim()
            Text = $text
            Body = $body
            SourceLine = ([regex]::Matches($Source.Substring(0, $decl.Index), '\n')).Count + 1
            Index = $decl.Index
        }
    }
    foreach ($name in $Required) {
        $found = @($methods | Where-Object { $_.Name -eq $name })
        if ($found.Count -eq 0) { throw ('Required declared method absent or unsupported: ' + $name) }
        foreach ($method in $found) {
            if ($method.Body -match '^\s*throw\s+null\s*;\s*$') { throw ('Reference-only throw-null stub rejected: ' + $name) }
        }
    }
    $selected = @($methods | Where-Object { $Required -contains $_.Name })
    $callPattern = '\b(?:' + (($Required | ForEach-Object { [regex]::Escape($_) }) -join '|') + ')\s*\('
    foreach ($method in $methods) {
        if ($Required -contains $method.Name) { continue }
        if ($method.Body -match $callPattern) { $selected += $method }
    }
    $selected = @($selected | Sort-Object Index)
    $lineCount = 0
    foreach ($method in $selected) { $lineCount += @($method.Text -split '\r?\n').Count }
    if ($lineCount -gt $MaxLines) { throw "Focused extraction is $lineCount lines; limit $MaxLines. No evidence was uploaded." }
    if ($selected.Count -eq 0) { throw 'Focused extraction is empty.' }
    return $selected
}
function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Report, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/RoundManagerSpawning/[0-9TZ]+-[a-f0-9]+$') { throw 'Unexpected publication directory.' }
    return @(
        @{ path = ($Directory + '/' + $ReportName); mode = '100644'; type = 'blob'; content = $Report },
        @{ path = ($Directory + '/MANIFEST.json'); mode = '100644'; type = 'blob'; content = $Manifest }
    )
}
function Invoke-ExtractorSelfTest {
    $fixture = @'
public class RoundManager {
    public void SpawnEnemyGameObject(int number = 0)
    {
        var x = "} // not a comment";
        var y = @"{""quoted""}";
        var z = $"{number} {{literal}}";
        char c = '}';
        /* } */
        // {
        if (number > 0) { number--; }
    }
    private void DirectCaller()
    {
        SpawnEnemyGameObject(1);
    }
    private void Unrelated()
    {
        var text = "SpawnEnemyGameObject(9)";
    }
    private class Nested {
        public void SpawnEnemyGameObject() { throw null; }
    }
}
'@
    $result = @(Get-FocusedMethods -Source $fixture -Required @('SpawnEnemyGameObject'))
    if ($result.Count -ne 2 -or $result[0].Name -ne 'SpawnEnemyGameObject' -or $result[1].Name -ne 'DirectCaller') { throw 'Method/caller selection self-test failed.' }
    if (-not $result[0].Text.TrimEnd().EndsWith('}')) { throw 'Unclosed method selection.' }
    $failed = $false
    try { Get-FocusedMethods -Source $fixture -Required @('Absent') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-target rejection failed.' }
    $stub = 'public class RoundManager {' + [char]10 + 'public void SpawnEnemyGameObject() { throw null; }' + [char]10 + '}'
    $failed = $false
    try { Get-FocusedMethods -Source $stub -Required @('SpawnEnemyGameObject') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Stub rejection failed.' }
    $failed = $false
    try { Get-FocusedMethods -Source $fixture -Required @('SpawnEnemyGameObject') -MaxLines 1 | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Size-limit rejection failed.' }
    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs)$' }).Count -ne 0) { throw 'Publication allowlist test failed.' }
    $roundtrip = @{tree = $entries} | ConvertTo-Json -Depth 12 | ConvertFrom-Json
    if ($roundtrip.tree.Count -ne 2) { throw 'JSON tree roundtrip failed.' }
    Write-Host 'PASS: extractor, callers, string/comment braces, nested exclusion, missing/stub/size rejection and two-file publication.'
}

function Resolve-GitHubCli {
    $command = Get-Command gh -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    $x86Root = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    $paths = @("$env:ProgramFiles\GitHub CLI\gh.exe", "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe", "$x86Root\GitHub CLI\gh.exe")
    foreach ($path in $paths) { if (Test-Path -LiteralPath $path) { return $path } }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'GitHub CLI is missing and winget is unavailable.' }
    & winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI installation failed.' }
    foreach ($path in $paths) { if (Test-Path -LiteralPath $path) { return $path } }
    throw 'GitHub CLI could not be resolved after installation.'
}
function Invoke-RepoApi {
    param([string]$Endpoint, [string]$Method = 'GET', [object]$Body = $null)
    $arguments = @('api', '--hostname', 'github.com', ('repos/' + $RepositoryName + '/' + $Endpoint), '--method', $Method)
    if ($null -ne $Body) {
        $requestPath = Join-Path $script:CaptureTempRoot 'request.json'
        [IO.File]::WriteAllText($requestPath, ($Body | ConvertTo-Json -Depth 20 -Compress), $Utf8)
        $arguments += @('--input', $requestPath)
    }
    $errorPath = Join-Path $script:CaptureTempRoot 'api-error.txt'
    $output = & $script:GhPath @arguments 2>$errorPath
    if ($LASTEXITCODE -ne 0) { throw ('GitHub API operation failed: ' + $Method + ' ' + $Endpoint + '. No main-branch write was attempted.') }
    return (($output -join [Environment]::NewLine) | ConvertFrom-Json)
}
if ($SelfTest) { Invoke-ExtractorSelfTest; return }
$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-roundmanager-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $script:CaptureTempRoot -Force | Out-Null
try {
    Write-Step 'Locating and verifying the installed V81 game.'
    $assemblyPath = Resolve-AssemblyPath
    $managedDir = Split-Path -Parent $assemblyPath
    $gameRoot = Split-Path -Parent (Split-Path -Parent $managedDir)
    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)
    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    foreach ($path in @($exePath, $appManifest)) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw 'Required game provenance file is missing.' } }
    $assemblySha = Get-Sha256Lower $assemblyPath
    $exeSha = Get-Sha256Lower $exePath
    $manifestSha = Get-Sha256Lower $appManifest
    if ($assemblySha -ne $ExpectedAssemblySha256) { throw "Installed Assembly-CSharp SHA mismatch: $assemblySha. Expected $ExpectedAssemblySha256." }
    if ($exeSha -ne $ExpectedExeSha256) { throw "Game executable SHA mismatch: $exeSha." }
    if ($manifestSha -ne $ExpectedAppManifestSha256) { throw "Steam appmanifest SHA mismatch: $manifestSha. Refusing unreviewed provenance drift." }
    $manifestText = Get-Content -LiteralPath $appManifest -Raw
    if ($manifestText -notmatch '"buildid"\s+"([0-9]+)"') { throw 'Steam buildid is absent.' }
    $buildId = $Matches[1]
    if ($buildId -ne $ExpectedSteamBuildId) { throw "Steam buildid mismatch: $buildId." }
    $script:GhPath = Resolve-GitHubCli
    & $script:GhPath auth status --hostname github.com *> $null
    if ($LASTEXITCODE -ne 0) {
        & $script:GhPath auth login --hostname github.com --git-protocol https --web
        if ($LASTEXITCODE -ne 0) { throw 'GitHub authentication failed.' }
    }
    $mainRef = Invoke-RepoApi 'git/ref/heads/main'
    $repositoryMain = $mainRef.object.sha
    $mainCommit = Invoke-RepoApi ('git/commits/' + $repositoryMain)
    $priorFile = Invoke-RepoApi ('contents/' + $PriorManifest + '?ref=' + $repositoryMain)
    $prior = $Utf8.GetString([Convert]::FromBase64String($priorFile.content)) | ConvertFrom-Json
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or $prior.steam.buildid -ne $ExpectedSteamBuildId) { throw 'Current repository prior evidence disagrees with the pinned installed-game contract.' }
    $ilspyResult = @(Ensure-DotNetAndIlSpy -TempRoot $script:CaptureTempRoot)
    if ($ilspyResult.Count -ne 1) { throw 'Decompiler bootstrap returned unexpected output.' }
    $ilspy = [string]$ilspyResult[0]
    Write-Step 'Extracting the exact RoundManager type locally.'
    $stderr = Join-Path $script:CaptureTempRoot 'decompiler-error.txt'
    $sourceLines = & $ilspy -t 'RoundManager' -r $managedDir $assemblyPath 2>$stderr
    if ($LASTEXITCODE -ne 0) { throw 'RoundManager decompile failed. No evidence was uploaded.' }
    $source = $sourceLines -join [Environment]::NewLine
    if ([string]::IsNullOrWhiteSpace($source)) { throw 'Decompiler returned empty source.' }
    $methods = @(Get-FocusedMethods -Source $source -Required $RequiredMethods)
    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 RoundManager spawn evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Steam buildid: ' + $buildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion)
    [void]$builder.AppendLine('Scope: required declared spawn/despawn methods and one-hop direct callers within RoundManager.')
    [void]$builder.AppendLine('This is source evidence, not gameplay acceptance. Full type source and binaries are excluded.')
    foreach ($method in $methods) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
        [void]$builder.AppendLine($method.Text)
    }
    $report = $builder.ToString()
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix
    $branch = 'source-evidence/roundmanager-v81-' + $stamp.ToLowerInvariant() + '-' + $suffix
    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Native V81 spawn method and direct-caller evidence for S1.42AI-DIAG1 safety review'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        repository_main_at_capture = $repositoryMain
        bound_prior_evidence = $PriorManifest
        source_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'; sha256 = $assemblySha }
        game_executable = @{ logical_path = 'Lethal Company.exe'; sha256 = $exeSha }
        steam = @{ app_id = $SteamAppId; buildid = $buildId; appmanifest_sha256 = $manifestSha }
        decompiler = @{ tool = 'ilspycmd'; version = $IlSpyVersion; type = 'RoundManager'; full_local_type_source_sha256 = (Get-TextSha256 $source) }
        selection = @{ required_methods = $RequiredMethods; selected_signatures = @($methods | ForEach-Object { $_.Signature }); max_source_lines = 3000; direct_caller_depth = 1 }
        report = @{ file = $ReportName; sha256 = (Get-TextSha256 $report); excludes = @('game binaries', 'full type decompile', 'absolute local paths', 'user names') }
    }
    $metadataJson = ($metadata | ConvertTo-Json -Depth 12) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)
    Write-Step ('Publishing ' + $methods.Count + ' method blocks and provenance on a new evidence branch.')
    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{ base_tree = $mainCommit.tree.sha; tree = $entries }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{
        message = ('Capture exact V81 RoundManager spawn evidence ' + $stamp)
        tree = $treeResult.sha
        parents = @($repositoryMain)
    }
    $refResult = Invoke-RepoApi -Endpoint 'git/refs' -Method 'POST' -Body @{ ref = ('refs/heads/' + $branch); sha = $commitResult.sha }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Published branch response did not match the evidence commit.' }
    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence branch: ' + $branch)
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Report: https://github.com/' + $RepositoryName + '/blob/' + $commitResult.sha + '/' + $directory + '/' + $ReportName)
    Write-Host 'Only the focused text report and manifest were uploaded. No local repository clone or gameplay run was required.'
}
finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) { Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
