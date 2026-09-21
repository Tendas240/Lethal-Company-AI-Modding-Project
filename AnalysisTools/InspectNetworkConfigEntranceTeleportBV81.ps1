#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest, [switch]$DependencySelfTest, [switch]$PythonBootstrapSelfTest)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$SteamAppId = '1966720'
$ExpectedAssemblySha256 = '5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731'
$ExpectedExeSha256 = '24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1'
$ExpectedSteamBuildId = '22825947'
$ExpectedAppManifestSha256 = 'fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432'
$ReviewedAppManifestSha256 = @(
    $ExpectedAppManifestSha256,
    'b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3',
    '132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e'
)
$ManifestReview = 'AnalysisTools/InspectRoundManagerSpawningV81_PROVENANCE_REVIEW.md'
$PriorManifest = 'SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json'
$PullRequestNumber = 138
$PullRequestBranch = 'scope/universal-interior-phase-c3a-dawn-tags'
$ScannerRepositoryPath = 'AnalysisTools/inspect_v81_networkconfig_prefab.py'
$EvidenceRoot = 'SourceEvidence/VanillaV81/NetworkConfigEntranceTeleportB'
$CaptureName = 'NETWORK_CONFIG_PREFAB_CAPTURE.json'
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$RequiredPythonPackages = @('UnityPy==1.25.3', 'dnfile==0.18.0', 'dncil==1.0.2', 'TypeTreeGeneratorAPI==0.0.10')
$BootstrapPythonVersion = '3.11.9'
$BootstrapPythonUrl = 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.zip'
$BootstrapPythonSha256 = '4ba90a4ab8990891033d37ff04d2047fdae8948d0d2729a68d3a6a17c585b681'
$BootstrapPythonManifest = 'https://www.python.org/ftp/python/3.11.9/windows-3.11.9.json'

function Write-Step { param([string]$Message) Write-Host ('[NetworkConfigEntranceTeleportBV81] ' + $Message) -ForegroundColor Cyan }
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
function Get-SteamBuildIdentity {
    param([Parameter(Mandatory = $true)][string]$Text)
    $appMatches = [regex]::Matches($Text, '"appid"\s+"([^"]+)"')
    $buildMatches = [regex]::Matches($Text, '"buildid"\s+"([^"]+)"')
    if ($appMatches.Count -ne 1 -or $buildMatches.Count -ne 1) {
        throw 'Steam appid and buildid must each occur exactly once.'
    }
    return [pscustomobject]@{ AppId = $appMatches[0].Groups[1].Value; BuildId = $buildMatches[0].Groups[1].Value }
}
function Assert-InstalledGameProvenance {
    param([string]$AssemblySha, [string]$ExeSha, [string]$ManifestSha, [string]$AppId, [string]$BuildId)
    if ($AssemblySha -ne $ExpectedAssemblySha256) { throw "Installed Assembly-CSharp SHA mismatch: $AssemblySha. Expected $ExpectedAssemblySha256." }
    if ($ExeSha -ne $ExpectedExeSha256) { throw "Game executable SHA mismatch: $ExeSha." }
    if ($AppId -cne $SteamAppId) { throw "Steam appid mismatch: $AppId." }
    if ($BuildId -cne $ExpectedSteamBuildId) { throw "Steam buildid mismatch: $BuildId." }
    if ($ReviewedAppManifestSha256 -notcontains $ManifestSha) { throw "Steam appmanifest SHA mismatch: $ManifestSha. Refusing unreviewed provenance drift." }
}

function Get-SteamRoots {
    $roots = @()
    try {
        $steam = Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -ErrorAction Stop
        if ($steam.SteamPath) { $roots += [IO.Path]::GetFullPath(($steam.SteamPath -replace '/', '\')) }
    } catch { }
    if (${env:ProgramFiles(x86)}) {
        $candidate = Join-Path ${env:ProgramFiles(x86)} 'Steam'
        if (Test-Path -LiteralPath $candidate) { $roots += [IO.Path]::GetFullPath($candidate) }
    }
    if ($env:ProgramFiles) {
        $candidate = Join-Path $env:ProgramFiles 'Steam'
        if (Test-Path -LiteralPath $candidate) { $roots += [IO.Path]::GetFullPath($candidate) }
    }
    $expanded = @()
    foreach ($root in ($roots | Select-Object -Unique)) {
        $expanded += $root
        $vdf = Join-Path $root 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf -PathType Leaf) {
            $text = Get-Content -LiteralPath $vdf -Raw
            foreach ($match in [regex]::Matches($text, '"path"\s+"([^"]+)"')) {
                $library = $match.Groups[1].Value -replace '\\\\', '\'
                if ($library) { $expanded += [IO.Path]::GetFullPath($library) }
            }
        }
    }
    return @($expanded | Select-Object -Unique)
}
function Resolve-AssemblyPath {
    $candidates = @()
    foreach ($root in (Get-SteamRoots)) {
        $candidate = Join-Path $root 'steamapps\common\Lethal Company\Lethal Company_Data\Managed\Assembly-CSharp.dll'
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { $candidates += (Resolve-Path -LiteralPath $candidate).Path }
    }
    $unique = @($candidates | Select-Object -Unique)
    if ($unique.Count -eq 0) { throw 'Could not locate the installed Lethal Company Assembly-CSharp.dll in detected Steam libraries.' }
    if ($unique.Count -gt 1) { throw ('Multiple Lethal Company installations found. Refusing to guess: ' + ($unique -join '; ')) }
    return $unique[0]
}

function ConvertTo-NativeArgument {
    param([AllowEmptyString()][string]$Value)
    $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
    return '"' + [regex]::Replace($escaped, '(\\+)$', '$1$1') + '"'
}
function Invoke-NativeProcess {
    param([string]$FilePath, [string[]]$Arguments)
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $FilePath
    $start.Arguments = (($Arguments | ForEach-Object { ConvertTo-NativeArgument $_ }) -join ' ')
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { throw ('Failed to start native executable: ' + $FilePath) }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        return [pscustomobject]@{ ExitCode = $process.ExitCode; StdOut = $stdoutTask.GetAwaiter().GetResult(); StdErr = $stderrTask.GetAwaiter().GetResult() }
    } finally { $process.Dispose() }
}
function Invoke-CheckedNativeProcess {
    param([string]$FilePath, [string[]]$Arguments, [string]$Label)
    $result = Invoke-NativeProcess -FilePath $FilePath -Arguments $Arguments
    if (-not [string]::IsNullOrWhiteSpace($result.StdErr)) {
        Write-Host ($Label + ' stderr:') -ForegroundColor Yellow
        Write-Host $result.StdErr
    }
    if ($result.ExitCode -ne 0) {
        if (-not [string]::IsNullOrWhiteSpace($result.StdOut)) { Write-Host $result.StdOut }
        throw ($Label + ' failed with exit code ' + $result.ExitCode + '.')
    }
    return $result.StdOut
}
function Test-PythonCandidate {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    try {
        $version = Invoke-NativeProcess -FilePath $Path -Arguments @('--version')
        $text = ($version.StdOut + $version.StdErr).Trim()
        if ($version.ExitCode -eq 0 -and $text -match '^Python 3\.(\d+)\.(\d+)') {
            if ([int]$matches[1] -ge 10) { return (Resolve-Path -LiteralPath $Path).Path }
        }
    } catch { }
    return $null
}
function Get-PythonCandidatePaths {
    $candidates = @()

    foreach ($name in @('python.exe', 'python', 'python3.exe', 'python3')) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source) { $candidates += $cmd.Source }
    }

    $py = Get-Command py.exe -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
    if ($py -and $py.Source) {
        try {
            $listed = Invoke-NativeProcess -FilePath $py.Source -Arguments @('-0p')
            foreach ($match in [regex]::Matches(($listed.StdOut + [Environment]::NewLine + $listed.StdErr), '([A-Za-z]:\\[^\r\n]*?python(?:\.exe)?)\s*$','Multiline')) {
                $candidates += $match.Groups[1].Value.Trim()
            }
        } catch { }
    }

    foreach ($root in @(
        'HKCU:\Software\Python\PythonCore',
        'HKLM:\Software\Python\PythonCore',
        'HKLM:\Software\WOW6432Node\Python\PythonCore'
    )) {
        try {
            if (-not (Test-Path -LiteralPath $root)) { continue }
            foreach ($versionKey in (Get-ChildItem -LiteralPath $root -ErrorAction Stop)) {
                $installKeyPath = $versionKey.PSPath + '\InstallPath'
                if (-not (Test-Path -LiteralPath $installKeyPath)) { continue }
                $installKey = Get-Item -LiteralPath $installKeyPath -ErrorAction Stop
                $exe = [string]$installKey.GetValue('ExecutablePath')
                if ([string]::IsNullOrWhiteSpace($exe)) {
                    $base = [string]$installKey.GetValue('')
                    if (-not [string]::IsNullOrWhiteSpace($base)) { $exe = Join-Path $base 'python.exe' }
                }
                if (-not [string]::IsNullOrWhiteSpace($exe)) { $candidates += $exe }
            }
        } catch { }
    }

    foreach ($root in @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Python'),
        $env:ProgramFiles,
        [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    )) {
        if ([string]::IsNullOrWhiteSpace($root) -or -not (Test-Path -LiteralPath $root -PathType Container)) { continue }
        try {
            if ((Split-Path -Leaf $root) -eq 'Python') {
                $candidates += @(Get-ChildItem -LiteralPath $root -Directory -ErrorAction Stop | ForEach-Object { Join-Path $_.FullName 'python.exe' })
            } else {
                $candidates += @(Get-ChildItem -LiteralPath $root -Directory -Filter 'Python*' -ErrorAction Stop | ForEach-Object { Join-Path $_.FullName 'python.exe' })
            }
        } catch { }
    }

    return @($candidates | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
}
function Install-IsolatedPythonRuntime {
    param([Parameter(Mandatory = $true)][string]$TempRoot)

    $archive = Join-Path $TempRoot ('python-' + $BootstrapPythonVersion + '-amd64.zip')
    $runtimeDir = Join-Path $TempRoot ('python-' + $BootstrapPythonVersion + '-portable')
    Write-Step ('No suitable existing Python was resolved; bootstrapping hash-pinned portable CPython ' + $BootstrapPythonVersion + '.')

    $priorProtocol = [Net.ServicePointManager]::SecurityProtocol
    try {
        [Net.ServicePointManager]::SecurityProtocol = $priorProtocol -bor [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -UseBasicParsing $BootstrapPythonUrl -OutFile $archive
    }
    finally {
        [Net.ServicePointManager]::SecurityProtocol = $priorProtocol
    }

    if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) { throw 'Pinned portable CPython download did not produce an archive.' }
    $archiveSha = Get-Sha256Lower $archive
    if ($archiveSha -cne $BootstrapPythonSha256) {
        throw ('Portable CPython archive SHA-256 mismatch: ' + $archiveSha + '. Expected ' + $BootstrapPythonSha256 + '.')
    }

    New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
    Expand-Archive -LiteralPath $archive -DestinationPath $runtimeDir -Force

    $python = Join-Path $runtimeDir 'python.exe'
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
        $pythonFiles = @(Get-ChildItem -LiteralPath $runtimeDir -Recurse -File -Filter 'python.exe' -ErrorAction Stop)
        if ($pythonFiles.Count -ne 1) {
            throw ('Portable CPython archive produced ' + $pythonFiles.Count + ' python.exe candidates; expected exactly one.')
        }
        $python = $pythonFiles[0].FullName
    }

    $version = Invoke-CheckedNativeProcess -FilePath $python -Arguments @('--version') -Label 'Portable CPython version verification'
    if ($version.Trim() -cne ('Python ' + $BootstrapPythonVersion)) {
        throw ('Portable CPython version mismatch: ' + $version.Trim())
    }
    return $python
}
function Resolve-Python {
    param([Parameter(Mandatory = $true)][string]$TempRoot, [switch]$ForceBootstrap)

    if (-not $ForceBootstrap) {
        foreach ($candidate in (Get-PythonCandidatePaths)) {
            $resolved = Test-PythonCandidate -Path $candidate
            if ($resolved) {
                Write-Step ('Using existing Python runtime: ' + $resolved)
                return $resolved
            }
        }
    }

    return Install-IsolatedPythonRuntime -TempRoot $TempRoot
}
function New-IsolatedPythonEnvironment {
    param(
        [Parameter(Mandatory = $true)][string]$TempRoot,
        [Parameter(Mandatory = $true)][string]$ScannerPath,
        [switch]$ForcePythonBootstrap
    )
    $python = Resolve-Python -TempRoot $TempRoot -ForceBootstrap:$ForcePythonBootstrap
    $venv = Join-Path $TempRoot 'pyenv'
    Invoke-CheckedNativeProcess -FilePath $python -Arguments @('-m', 'venv', $venv) -Label 'Python venv creation' | Out-Null
    $venvPython = Join-Path $venv 'Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) { throw 'Isolated Python executable was not created.' }
    Invoke-CheckedNativeProcess -FilePath $venvPython -Arguments (@('-m', 'pip', 'install', '--disable-pip-version-check', '--no-input') + $RequiredPythonPackages) -Label 'Pinned Python dependency installation' | Out-Null
    $selfTest = Invoke-CheckedNativeProcess -FilePath $venvPython -Arguments @($ScannerPath, '--self-test') -Label 'NetworkConfig scanner self-test'
    Write-Host $selfTest
    return $venvPython
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
        [IO.File]::WriteAllText($requestPath, ($Body | ConvertTo-Json -Depth 30 -Compress), $Utf8)
        $arguments += @('--input', $requestPath)
    }
    $output = & $script:GhPath @arguments
    if ($LASTEXITCODE -ne 0) { throw ('GitHub API operation failed: ' + $Method + ' ' + $Endpoint + '. No repository ref write was attempted.') }
    return (($output -join [Environment]::NewLine) | ConvertFrom-Json)
}
function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Capture, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/NetworkConfigEntranceTeleportB/[0-9TZ]+-[a-f0-9]+$') { throw 'Unexpected publication directory.' }
    return @(
        @{ path = ($Directory + '/' + $CaptureName); mode = '100644'; type = 'blob'; content = $Capture },
        @{ path = ($Directory + '/MANIFEST.json'); mode = '100644'; type = 'blob'; content = $Manifest }
    )
}

function Invoke-SelfTest {
    $valid = @{ AssemblySha = $ExpectedAssemblySha256; ExeSha = $ExpectedExeSha256; ManifestSha = $ExpectedAppManifestSha256; AppId = $SteamAppId; BuildId = $ExpectedSteamBuildId }
    foreach ($approved in $ReviewedAppManifestSha256) {
        $valid.ManifestSha = $approved
        Assert-InstalledGameProvenance @valid
    }
    $rejected = $false
    try { Assert-InstalledGameProvenance -AssemblySha 'wrong' -ExeSha $ExpectedExeSha256 -ManifestSha $ExpectedAppManifestSha256 -AppId $SteamAppId -BuildId $ExpectedSteamBuildId } catch { $rejected = $true }
    if (-not $rejected) { throw 'Wrong Assembly-CSharp hash was accepted.' }
    $identity = Get-SteamBuildIdentity -Text ('"appid" "' + $SteamAppId + '" "buildid" "' + $ExpectedSteamBuildId + '"')
    if ($identity.AppId -cne $SteamAppId -or $identity.BuildId -cne $ExpectedSteamBuildId) { throw 'Steam identity self-test failed.' }
    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/NetworkConfigEntranceTeleportB/20260921T000000Z-abcdef12' -Capture '{}' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|assets)$' }).Count -ne 0) { throw 'Publication allowlist self-test failed.' }
    Write-Host 'PASS: provenance allowlist, Steam identity and two-file publication contract.'
}

$selectedSelfTestModes = ([int][bool]$SelfTest) + ([int][bool]$DependencySelfTest) + ([int][bool]$PythonBootstrapSelfTest)
if ($selectedSelfTestModes -gt 1) { throw 'Select only one self-test mode.' }
if ($SelfTest) { Invoke-SelfTest; return }
if ($DependencySelfTest -or $PythonBootstrapSelfTest) {
    $localScanner = Join-Path (Get-Location) $ScannerRepositoryPath
    if (-not (Test-Path -LiteralPath $localScanner -PathType Leaf)) { throw 'Run dependency/bootstrap self-test from a repository checkout containing the scanner.' }
    $prefix = if ($PythonBootstrapSelfTest) { 'lc-networkconfig-python-bootstrap-' } else { 'lc-networkconfig-deps-' }
    $script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ($prefix + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $script:CaptureTempRoot -Force | Out-Null
    try {
        $venvPython = New-IsolatedPythonEnvironment -TempRoot $script:CaptureTempRoot -ScannerPath $localScanner -ForcePythonBootstrap:$PythonBootstrapSelfTest
        if ($PythonBootstrapSelfTest) {
            $fullTemp = [IO.Path]::GetFullPath($script:CaptureTempRoot).TrimEnd('\') + '\'
            $fullPython = [IO.Path]::GetFullPath($venvPython)
            if (-not $fullPython.StartsWith($fullTemp, [StringComparison]::OrdinalIgnoreCase)) { throw 'Forced Python bootstrap did not remain inside the temporary capture root.' }
            Write-Host ('PASS: hash-pinned portable CPython ' + $BootstrapPythonVersion + ' bootstrap, venv creation, pinned dependencies and scanner execution.')
        } else {
            Write-Host 'PASS: isolated pinned Python dependency bootstrap and scanner execution.'
        }
    } finally { Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue }
    return
}

$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-networkconfig-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $script:CaptureTempRoot -Force | Out-Null
try {
    Write-Step 'Locating and verifying the installed V81 game.'
    $assemblyPath = Resolve-AssemblyPath
    $managedDir = Split-Path -Parent $assemblyPath
    $dataRoot = Split-Path -Parent $managedDir
    $gameRoot = Split-Path -Parent $dataRoot
    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    $netcodePath = Join-Path $managedDir 'Unity.Netcode.Runtime.dll'
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)
    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    foreach ($path in @($exePath, $netcodePath, $appManifest)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('Required V81 provenance/input file missing: ' + $path) }
    }
    $assemblySha = Get-Sha256Lower $assemblyPath
    $exeSha = Get-Sha256Lower $exePath
    $netcodeSha = Get-Sha256Lower $netcodePath
    $manifestSha = Get-Sha256Lower $appManifest
    $manifestText = Get-Content -LiteralPath $appManifest -Raw
    $steamIdentity = Get-SteamBuildIdentity -Text $manifestText
    Assert-InstalledGameProvenance -AssemblySha $assemblySha -ExeSha $exeSha -ManifestSha $manifestSha -AppId $steamIdentity.AppId -BuildId $steamIdentity.BuildId

    $script:GhPath = Resolve-GitHubCli
    & $script:GhPath auth status --hostname github.com *> $null
    if ($LASTEXITCODE -ne 0) {
        & $script:GhPath auth login --hostname github.com --git-protocol https --web
        if ($LASTEXITCODE -ne 0) { throw 'GitHub authentication failed.' }
    }

    $pullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($pullRequest.state -cne 'open' -or $pullRequest.merged -eq $true -or $pullRequest.head.ref -cne $PullRequestBranch -or $pullRequest.head.repo.full_name -cne $RepositoryName) {
        throw 'PR #138 is not the expected open in-repository evidence PR. Refusing publication.'
    }
    $repositoryPrHead = $pullRequest.head.sha
    $prHeadCommit = Invoke-RepoApi ('git/commits/' + $repositoryPrHead)
    $mainRef = Invoke-RepoApi 'git/ref/heads/main'
    $repositoryMain = $mainRef.object.sha
    $priorFile = Invoke-RepoApi ('contents/' + $PriorManifest + '?ref=' + $repositoryMain)
    $prior = $Utf8.GetString([Convert]::FromBase64String($priorFile.content)) | ConvertFrom-Json
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or $prior.steam.buildid -ne $ExpectedSteamBuildId -or $prior.steam.app_id -ne $SteamAppId -or $prior.steam.appmanifest_sha256 -ne $ExpectedAppManifestSha256) {
        throw 'Current repository prior evidence disagrees with the pinned installed-game contract.'
    }

    Write-Step 'Fetching the exact scanner from the current PR head and creating an isolated parser environment.'
    $scannerFile = Invoke-RepoApi ('contents/' + $ScannerRepositoryPath + '?ref=' + $repositoryPrHead)
    if ($scannerFile.type -cne 'file' -or [string]::IsNullOrWhiteSpace($scannerFile.content)) { throw 'Exact PR-head scanner file could not be fetched.' }
    $scannerText = $Utf8.GetString([Convert]::FromBase64String(($scannerFile.content -replace '\s', '')))
    $scannerPath = Join-Path $script:CaptureTempRoot 'inspect_v81_networkconfig_prefab.py'
    [IO.File]::WriteAllText($scannerPath, $scannerText, $Utf8)
    $scannerSha = Get-Sha256Lower $scannerPath
    $python = New-IsolatedPythonEnvironment -TempRoot $script:CaptureTempRoot -ScannerPath $scannerPath

    Write-Step 'Scanning only the installed base-game NetworkConfig prefab graph and exact Netcode metadata/IL.'
    $capturePath = Join-Path $script:CaptureTempRoot $CaptureName
    $scanOutput = Invoke-CheckedNativeProcess -FilePath $python -Arguments @(
        $scannerPath,
        '--data-root', $dataRoot,
        '--netcode-dll', $netcodePath,
        '--out', $capturePath
    ) -Label 'V81 NetworkConfig static capture'
    Write-Host $scanOutput
    if (-not (Test-Path -LiteralPath $capturePath -PathType Leaf)) { throw 'Scanner did not produce the expected capture JSON.' }
    $capture = Get-Content -LiteralPath $capturePath -Raw
    $captureObject = $capture | ConvertFrom-Json
    if ($captureObject.schema_version -cne 'v81-networkconfig-entranceteleportb-6') { throw 'Unexpected capture schema.' }
    $allowedStatus = @('REGISTERED_SURFACE_PROVEN', 'REGISTERED_SURFACE_INCOMPLETE', 'EXACT_NAME_NOT_REGISTERED', 'AMBIGUOUS_MULTIPLE_EXACT_MATCHES')
    if ($allowedStatus -notcontains $captureObject.assets.target_status) { throw ('Unexpected target status: ' + $captureObject.assets.target_status) }
    if ($captureObject.netcode.dll_sha256 -ne $netcodeSha) { throw 'Scanner Netcode SHA disagrees with wrapper hash.' }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix
    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Exact installed-V81 NetworkConfig EntranceTeleportB registration/component-surface evidence for Universal Interior Viability C3F10C'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        pull_request = $PullRequestNumber
        pull_request_branch = $PullRequestBranch
        repository_pr_head_at_capture = $repositoryPrHead
        repository_main_at_capture = $repositoryMain
        bound_prior_evidence = $PriorManifest
        source_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'; sha256 = $assemblySha }
        netcode_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Unity.Netcode.Runtime.dll'; sha256 = $netcodeSha; size_bytes = (Get-Item -LiteralPath $netcodePath).Length }
        game_executable = @{ logical_path = 'Lethal Company.exe'; sha256 = $exeSha }
        steam = @{ app_id = $steamIdentity.AppId; buildid = $steamIdentity.BuildId; appmanifest_sha256 = $manifestSha; prior_appmanifest_sha256 = $ExpectedAppManifestSha256; matches_prior_appmanifest = ($manifestSha -eq $ExpectedAppManifestSha256); manifest_review = $ManifestReview }
        scanner = @{ repository_path = $ScannerRepositoryPath; github_blob_sha = $scannerFile.sha; sha256 = $scannerSha }
        target = @{ exact_name = 'EntranceTeleportB'; status = $captureObject.assets.target_status; required_component_surface = @('EntranceTeleport', 'InteractTrigger', 'Unity.Netcode.NetworkObject') }
        published_evidence = @{ file = $CaptureName; sha256 = (Get-TextSha256 $capture); excludes = @('game binaries', 'Unity asset payloads', 'full managed decompiles', 'absolute local paths', 'user names') }
    }
    $metadataJson = ($metadata | ConvertTo-Json -Depth 15) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Capture $capture -Manifest $metadataJson)

    Write-Step 'Re-checking PR head immediately before the atomic evidence publication.'
    $currentPullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($currentPullRequest.state -cne 'open' -or $currentPullRequest.merged -eq $true -or $currentPullRequest.head.ref -cne $PullRequestBranch -or $currentPullRequest.head.sha -cne $repositoryPrHead) {
        throw 'PR #138 head changed during capture. Refusing stale write.'
    }
    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{ base_tree = $prHeadCommit.tree.sha; tree = $entries }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{ message = ('Capture exact V81 NetworkConfig EntranceTeleportB evidence ' + $stamp); tree = $treeResult.sha; parents = @($repositoryPrHead) }
    $refResult = Invoke-RepoApi -Endpoint ('git/refs/heads/' + $PullRequestBranch) -Method 'PATCH' -Body @{ sha = $commitResult.sha; force = $false }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Updated PR branch response did not match the evidence commit.' }

    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Target status: ' + $captureObject.assets.target_status)
    Write-Host ('Evidence directory: ' + $directory)
    Write-Host 'Only compact JSON evidence and a manifest were uploaded. No game binary, Unity asset payload, local clone or gameplay run was uploaded.'
} finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) { Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
