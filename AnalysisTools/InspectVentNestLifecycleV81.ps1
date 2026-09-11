#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest, [switch]$BootstrapSelfTest)
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
$ReviewedAppManifestSha256 = @(
    $ExpectedAppManifestSha256,
    'b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3'
)
$ManifestReview = 'AnalysisTools/InspectRoundManagerSpawningV81_PROVENANCE_REVIEW.md'
$PriorManifest = 'SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/MANIFEST.json'
$EvidenceRoot = 'SourceEvidence/VanillaV81/VentNestLifecycle'
$ReportName = 'V81_VENT_NEST_LIFECYCLE_FOCUSED_DECOMPILE.txt'
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$LifecycleNames = @('Awake', 'Start', 'Update', 'LateUpdate', 'FixedUpdate', 'OnEnable', 'OnDisable', 'OnDestroy', 'OnNetworkSpawn', 'OnNetworkDespawn')

function Write-Step { param([string]$Message) Write-Host ('[VentNestV81] ' + $Message) -ForegroundColor Cyan }
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
    if ($appMatches.Count -ne 1 -or $buildMatches.Count -ne 1) { throw 'Steam appid and buildid must each occur exactly once.' }
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
    }
    catch { }
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
    if ($unique.Count -gt 1) { throw ('Multiple Lethal Company Assembly-CSharp.dll candidates were found. Refusing to guess: ' + ($unique -join '; ')) }
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
    }
    finally { $process.Dispose() }
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
        throw ($Label + ' failed with exit code ' + $result.ExitCode + '. See captured output above.')
    }
    return $result.StdOut
}
function Ensure-DotNetAndIlSpy {
    param([Parameter(Mandatory = $true)][string]$TempRoot, [switch]$ForceIsolatedSdk)
    $toolDir = Join-Path $TempRoot 'ilspy-tool'
    New-Item -ItemType Directory -Path $toolDir -Force | Out-Null
    $dotnetExe = $null
    $dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($dotnet -and -not $ForceIsolatedSdk) {
        $sdkResult = Invoke-NativeProcess -FilePath $dotnet.Source -Arguments @('--list-sdks')
        $sdkList = $sdkResult.StdOut -split '\r?\n'
        if ($sdkResult.ExitCode -eq 0 -and @($sdkList | Where-Object { $_ -match '^10\.' }).Count -gt 0) { $dotnetExe = $dotnet.Source }
    }
    if (-not $dotnetExe) {
        Write-Step '.NET 10 SDK not found; bootstrapping an isolated SDK in the temporary directory.'
        $dotnetDir = Join-Path $TempRoot 'dotnet'
        $installer = Join-Path $TempRoot 'dotnet-install.ps1'
        Invoke-WebRequest -UseBasicParsing 'https://dot.net/v1/dotnet-install.ps1' -OutFile $installer
        $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
        $installOutput = Invoke-CheckedNativeProcess -FilePath $powershellExe -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $installer, '-Channel', '10.0', '-InstallDir', $dotnetDir, '-NoPath') -Label 'Isolated .NET SDK installation'
        Write-Host $installOutput
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
    [IO.File]::WriteAllText($nugetConfig, $nugetConfigText, $Utf8)
    Write-Step "Installing isolated ilspycmd $IlSpyVersion using an isolated NuGet config."
    $toolInstallOutput = Invoke-CheckedNativeProcess -FilePath $dotnetExe -Arguments @('tool', 'install', 'ilspycmd', '--tool-path', $toolDir, '--version', $IlSpyVersion, '--configfile', $nugetConfig, '--disable-parallel') -Label 'ILSpy installation'
    Write-Host $toolInstallOutput
    $ilspyDllMatches = @(Get-ChildItem -LiteralPath $toolDir -Recurse -File -Filter 'ilspycmd.dll')
    if ($ilspyDllMatches.Count -ne 1) { throw ('Expected exactly one ilspycmd.dll in the isolated tool directory, found: ' + $ilspyDllMatches.Count) }
    return [pscustomobject]@{ DotNet = $dotnetExe; IlSpyDll = $ilspyDllMatches[0].FullName }
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
function Get-TypeModel {
    param([Parameter(Mandatory = $true)][string]$Source, [Parameter(Mandatory = $true)][string]$TypeName)
    $mask = Get-CodeMask $Source
    $typePattern = '\bclass\s+' + [regex]::Escape($TypeName) + '\b[^\{]*\{'
    $classMatch = [regex]::Match($mask, $typePattern)
    if (-not $classMatch.Success) { throw ($TypeName + ' class declaration absent.') }
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
        if ($paren -ne 0) { throw ($TypeName + ': unbalanced method signature.') }
        while ($pos -lt $mask.Length -and [char]::IsWhiteSpace($mask[$pos])) { $pos++ }
        if ($pos -ge $mask.Length -or $mask[$pos] -ne '{') { continue }
        $bodyStart = $pos
        $end = $bodyStart + 1
        while ($end -lt $mask.Length -and -not ($mask[$end] -eq '}' -and $depths[$end] -eq ($methodDepth + 1))) { $end++ }
        if ($end -ge $mask.Length) { throw ($TypeName + ': method body did not close.') }
        $methods += [pscustomobject]@{
            Name = $decl.Groups['name'].Value
            Signature = $Source.Substring($decl.Index, $bodyStart - $decl.Index).Trim()
            Text = $Source.Substring($decl.Index, $end - $decl.Index + 1)
            Body = $mask.Substring($bodyStart + 1, $end - $bodyStart - 1)
            SourceLine = ([regex]::Matches($Source.Substring(0, $decl.Index), '\n')).Count + 1
            Index = $decl.Index
        }
    }
    return [pscustomobject]@{
        TypeName = $TypeName
        Header = $Source.Substring($classMatch.Index, $classBrace - $classMatch.Index + 1).Trim()
        Methods = @($methods)
    }
}
function Get-ExactMethod {
    param([Parameter(Mandatory = $true)]$Model, [Parameter(Mandatory = $true)][string]$Name, [Parameter(Mandatory = $true)][string]$SignaturePattern)
    $found = @($Model.Methods | Where-Object { $_.Name -eq $Name -and $_.Signature -match $SignaturePattern })
    if ($found.Count -ne 1) { throw ($Model.TypeName + ': expected exactly one exact method ' + $Name + ', found ' + $found.Count + '.') }
    if ($found[0].Body -match '^\s*throw\s+null\s*;\s*$') { throw ($Model.TypeName + ': reference-only throw-null stub rejected: ' + $found[0].Signature) }
    return $found[0]
}
function Get-OneHopContext {
    param([Parameter(Mandatory = $true)]$Model, [Parameter(Mandatory = $true)][object[]]$Seeds, [int]$MaxLines = 1600)
    $selected = @{}
    foreach ($seed in $Seeds) { $selected[[string]$seed.Index] = $seed }
    foreach ($candidate in $Model.Methods) {
        if ($selected.ContainsKey([string]$candidate.Index)) { continue }
        $include = $false
        foreach ($seed in $Seeds) {
            if ($candidate.Body -match ('\b' + [regex]::Escape($seed.Name) + '\s*\(')) { $include = $true; break }
            if ($seed.Body -match ('\b' + [regex]::Escape($candidate.Name) + '\s*\(')) { $include = $true; break }
        }
        if ($include) { $selected[[string]$candidate.Index] = $candidate }
    }
    $result = @($selected.Values | Sort-Object Index)
    $lineCount = 0
    foreach ($method in $result) { $lineCount += @($method.Text -split '\r?\n').Count }
    if ($lineCount -gt $MaxLines) { throw ($Model.TypeName + ': focused extraction is ' + $lineCount + ' lines; limit ' + $MaxLines + '. No evidence was uploaded.') }
    if ($result.Count -eq 0) { throw ($Model.TypeName + ': focused extraction is empty.') }
    return $result
}
function Get-LifecycleSeeds {
    param([Parameter(Mandatory = $true)]$Model)
    $awake = Get-ExactMethod -Model $Model -Name 'Awake' -SignaturePattern 'Awake\s*\(\s*\)'
    $seeds = @($Model.Methods | Where-Object { $LifecycleNames -contains $_.Name })
    if (@($seeds | Where-Object { $_.Index -eq $awake.Index }).Count -ne 1) { throw ($Model.TypeName + ': Awake was not retained in lifecycle selection.') }
    foreach ($seed in $seeds) {
        if ($seed.Body -match '^\s*throw\s+null\s*;\s*$') { throw ($Model.TypeName + ': lifecycle throw-null stub rejected: ' + $seed.Signature) }
    }
    return $seeds
}
function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Report, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/VentNestLifecycle/[0-9TZ]+-[a-f0-9]+$') { throw 'Unexpected publication directory.' }
    return @(
        @{ path = ($Directory + '/' + $ReportName); mode = '100644'; type = 'blob'; content = $Report },
        @{ path = ($Directory + '/MANIFEST.json'); mode = '100644'; type = 'blob'; content = $Manifest }
    )
}

function Invoke-NativeProcessSelfTest {
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('lc-ventnest-native-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $temp -Force | Out-Null
    try {
        $fixture = Join-Path $temp 'native fixture.ps1'
        $fixtureText = @'
param([int]$Code, [string]$Value)
[Console]::Out.WriteLine('OUT:' + $Value)
[Console]::Error.WriteLine('ERR:diagnostic')
exit $Code
'@
        [IO.File]::WriteAllText($fixture, $fixtureText, $Utf8)
        $exe = (Get-Command powershell.exe -ErrorAction Stop).Source
        foreach ($value in @('', 'space value', 'a"b', 'trailing\')) {
            $result = Invoke-NativeProcess -FilePath $exe -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $fixture, '-Code', '0', '-Value', $value)
            if ($result.ExitCode -ne 0 -or $result.StdOut.TrimEnd() -cne ('OUT:' + $value) -or $result.StdErr.TrimEnd() -cne 'ERR:diagnostic') { throw 'Native stdout/stderr/argument preservation test failed.' }
        }
        $failed = $false
        try { Invoke-CheckedNativeProcess -FilePath $exe -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $fixture, '-Code', '7', '-Value', 'x') -Label 'Failure fixture' | Out-Null } catch { if ($_.Exception.Message -match 'exit code 7') { $failed = $true } else { throw } }
        if (-not $failed) { throw 'Nonzero native exit was not rejected.' }
        Write-Host 'PASS: native process argument/stdout/stderr and nonzero-exit handling.'
    }
    finally { Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue }
}
function Invoke-ProvenanceSelfTest {
    foreach ($manifest in $ReviewedAppManifestSha256) {
        Assert-InstalledGameProvenance -AssemblySha $ExpectedAssemblySha256 -ExeSha $ExpectedExeSha256 -ManifestSha $manifest -AppId $SteamAppId -BuildId $ExpectedSteamBuildId
    }
    foreach ($key in @('AssemblySha', 'ExeSha', 'ManifestSha', 'AppId', 'BuildId')) {
        $args = @{ AssemblySha = $ExpectedAssemblySha256; ExeSha = $ExpectedExeSha256; ManifestSha = $ExpectedAppManifestSha256; AppId = $SteamAppId; BuildId = $ExpectedSteamBuildId }
        $args[$key] = 'unreviewed'
        $failed = $false
        try { Assert-InstalledGameProvenance @args } catch { $failed = $true }
        if (-not $failed) { throw ('Provenance rejection failed for ' + $key) }
    }
    Write-Host 'PASS: reviewed provenance variants and fail-closed mismatch rejection.'
}
function Invoke-ExtractorSelfTest {
    $roundFixture = @'
public class RoundManager {
    public int AssignRandomEnemyToVent(EnemyVent vent, float spawnTime) {
        return PickEnemy(vent);
    }
    public int AssignRandomEnemyToVent(int fake) { return fake; }
    private int PickEnemy(EnemyVent vent) { return 1; }
    private void BeginEnemySpawning() { AssignRandomEnemyToVent(null, 1f); }
    private void Unrelated() { var x = "AssignRandomEnemyToVent(null, 2f)"; }
}
'@
    $round = Get-TypeModel -Source $roundFixture -TypeName 'RoundManager'
    $assign = Get-ExactMethod -Model $round -Name 'AssignRandomEnemyToVent' -SignaturePattern 'AssignRandomEnemyToVent\s*\(\s*EnemyVent\b[^,]*,\s*float\b[^\)]*\)'
    $roundContext = @(Get-OneHopContext -Model $round -Seeds @($assign))
    $roundNames = @($roundContext | ForEach-Object { $_.Name })
    foreach ($required in @('AssignRandomEnemyToVent', 'PickEnemy', 'BeginEnemySpawning')) { if ($roundNames -notcontains $required) { throw ('RoundManager context missing ' + $required) } }
    if (@($roundContext | Where-Object { $_.Signature -match 'AssignRandomEnemyToVent\s*\(\s*int\b' }).Count -ne 0) { throw 'Wrong overload leaked into exact selection.' }

    $nestFixture = @'
public class EnemyAINestSpawnObject : NetworkBehaviour {
    private void Awake() { RegisterNest(); }
    private void OnDestroy() { CleanupNest(); }
    private void RegisterNest() { }
    private void CleanupNest() { }
    private void Utility() { }
}
'@
    $nest = Get-TypeModel -Source $nestFixture -TypeName 'EnemyAINestSpawnObject'
    $lifecycle = @(Get-LifecycleSeeds -Model $nest)
    $nestContext = @(Get-OneHopContext -Model $nest -Seeds $lifecycle)
    $nestNames = @($nestContext | ForEach-Object { $_.Name })
    foreach ($required in @('Awake', 'OnDestroy', 'RegisterNest', 'CleanupNest')) { if ($nestNames -notcontains $required) { throw ('Nest lifecycle context missing ' + $required) } }

    $enemyFixture = @'
public class EnemyAI : NetworkBehaviour {
    public void UseNestSpawnObject(EnemyAINestSpawnObject nest) { ReleasePreviousNest(); }
    public void UseNestSpawnObject(int fake) { }
    private void Start() { UseNestSpawnObject(null); }
    private void ReleasePreviousNest() { }
    private void Unrelated() { }
}
'@
    $enemy = Get-TypeModel -Source $enemyFixture -TypeName 'EnemyAI'
    $useNest = Get-ExactMethod -Model $enemy -Name 'UseNestSpawnObject' -SignaturePattern 'UseNestSpawnObject\s*\(\s*EnemyAINestSpawnObject\b[^\)]*\)'
    $enemyContext = @(Get-OneHopContext -Model $enemy -Seeds @($useNest))
    $enemyNames = @($enemyContext | ForEach-Object { $_.Name })
    foreach ($required in @('UseNestSpawnObject', 'Start', 'ReleasePreviousNest')) { if ($enemyNames -notcontains $required) { throw ('EnemyAI context missing ' + $required) } }

    $failed = $false
    try { Get-ExactMethod -Model $round -Name 'Missing' -SignaturePattern 'Missing\s*\(' | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-target rejection failed.' }
    $failed = $false
    try { Get-OneHopContext -Model $round -Seeds @($assign) -MaxLines 1 | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Size-limit rejection failed.' }
    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/VentNestLifecycle/20260911T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs)$' }).Count -ne 0) { throw 'Publication allowlist test failed.' }
    Write-Host 'PASS: exact overloads, lifecycle selection, one-hop caller/downstream context, limits and two-file publication.'
}
function Invoke-BootstrapSelfTest {
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('lc-ventnest-bootstrap-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $temp -Force | Out-Null
    try {
        $tool = Ensure-DotNetAndIlSpy -TempRoot $temp -ForceIsolatedSdk
        $version = Invoke-CheckedNativeProcess -FilePath $tool.DotNet -Arguments @($tool.IlSpyDll, '--version') -Label 'ILSpy version'
        Write-Host $version
        if ($version -notmatch ('(?m)^ilspycmd: ' + [regex]::Escape($IlSpyVersion) + '\s*$')) { throw 'Installed ILSpy did not report the pinned version.' }
        Write-Host 'PASS: isolated .NET 10 SDK and pinned ILSpy bootstrap.'
    }
    finally { Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue }
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

if ($SelfTest -and $BootstrapSelfTest) { throw 'Select only one self-test mode.' }
if ($SelfTest) { Invoke-NativeProcessSelfTest; Invoke-ProvenanceSelfTest; Invoke-ExtractorSelfTest; return }
if ($BootstrapSelfTest) { Invoke-BootstrapSelfTest; return }

$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-vent-nest-v81-' + [guid]::NewGuid().ToString('N'))
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
    $manifestText = Get-Content -LiteralPath $appManifest -Raw
    $steamIdentity = Get-SteamBuildIdentity -Text $manifestText
    Assert-InstalledGameProvenance -AssemblySha $assemblySha -ExeSha $exeSha -ManifestSha $manifestSha -AppId $steamIdentity.AppId -BuildId $steamIdentity.BuildId

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
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or $prior.steam.buildid -ne $ExpectedSteamBuildId -or $prior.steam.app_id -ne $SteamAppId -or $ReviewedAppManifestSha256 -notcontains $prior.steam.appmanifest_sha256) { throw 'Current repository prior V81 evidence disagrees with the pinned installed-game contract.' }

    $ilspy = Ensure-DotNetAndIlSpy -TempRoot $script:CaptureTempRoot
    $sourceByType = @{}
    $modelByType = @{}
    foreach ($typeName in @('RoundManager', 'EnemyAINestSpawnObject', 'EnemyAI')) {
        Write-Step ('Decompiling exact type ' + $typeName + '.')
        $source = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @($ilspy.IlSpyDll, '-t', $typeName, '-r', $managedDir, $assemblyPath) -Label ($typeName + ' decompile')
        if ([string]::IsNullOrWhiteSpace($source)) { throw ($typeName + ': decompiler returned empty source.') }
        $sourceByType[$typeName] = $source
        $modelByType[$typeName] = Get-TypeModel -Source $source -TypeName $typeName
    }

    $assign = Get-ExactMethod -Model $modelByType['RoundManager'] -Name 'AssignRandomEnemyToVent' -SignaturePattern 'AssignRandomEnemyToVent\s*\(\s*EnemyVent\b[^,]*,\s*float\b[^\)]*\)'
    $roundContext = @(Get-OneHopContext -Model $modelByType['RoundManager'] -Seeds @($assign))
    $nestSeeds = @(Get-LifecycleSeeds -Model $modelByType['EnemyAINestSpawnObject'])
    $nestContext = @(Get-OneHopContext -Model $modelByType['EnemyAINestSpawnObject'] -Seeds $nestSeeds)
    $useNest = Get-ExactMethod -Model $modelByType['EnemyAI'] -Name 'UseNestSpawnObject' -SignaturePattern 'UseNestSpawnObject\s*\(\s*EnemyAINestSpawnObject\b[^\)]*\)'
    $enemyContext = @(Get-OneHopContext -Model $modelByType['EnemyAI'] -Seeds @($useNest))

    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 vent/nest lifecycle evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Steam buildid: ' + $steamIdentity.BuildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion)
    [void]$builder.AppendLine('Scope: exact AssignRandomEnemyToVent(EnemyVent,float), EnemyAINestSpawnObject lifecycle including Awake, exact EnemyAI.UseNestSpawnObject(EnemyAINestSpawnObject), and one-hop same-type caller/downstream context only.')
    [void]$builder.AppendLine('This supplements the completed 27-block RoundManager capture; it does not repeat that capture and is not gameplay acceptance.')
    [void]$builder.AppendLine('Game binaries, full type decompiles and absolute local paths are excluded.')

    $groups = @(
        [pscustomobject]@{ Name = 'RoundManager'; Model = $modelByType['RoundManager']; Methods = $roundContext },
        [pscustomobject]@{ Name = 'EnemyAINestSpawnObject'; Model = $modelByType['EnemyAINestSpawnObject']; Methods = $nestContext },
        [pscustomobject]@{ Name = 'EnemyAI'; Model = $modelByType['EnemyAI']; Methods = $enemyContext }
    )
    foreach ($group in $groups) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('=== TYPE ' + $group.Name + ' ===')
        [void]$builder.AppendLine($group.Model.Header)
        foreach ($method in $group.Methods) {
            [void]$builder.AppendLine('')
            [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
            [void]$builder.AppendLine($method.Text)
        }
    }
    $report = $builder.ToString()
    if (@($report -split '\r?\n').Count -gt 1800) { throw 'Combined focused report exceeded 1800 lines. No evidence was uploaded.' }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix
    $branch = 'source-evidence/v81-vent-nest-' + $stamp.ToLowerInvariant() + '-' + $suffix
    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Supplemental installed V81 vent assignment and nest lifecycle evidence for S1.42AI-DIAG1 patch safety'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        repository_main_at_capture = $repositoryMain
        bound_prior_evidence = $PriorManifest
        source_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'; sha256 = $assemblySha }
        game_executable = @{ logical_path = 'Lethal Company.exe'; sha256 = $exeSha }
        steam = @{ app_id = $steamIdentity.AppId; buildid = $steamIdentity.BuildId; appmanifest_sha256 = $manifestSha; reviewed_manifest_hashes = $ReviewedAppManifestSha256; manifest_review = $ManifestReview }
        decompiler = @{
            tool = 'ilspycmd'
            version = $IlSpyVersion
            types = @(
                @{ name = 'RoundManager'; full_local_type_source_sha256 = (Get-TextSha256 $sourceByType['RoundManager']) },
                @{ name = 'EnemyAINestSpawnObject'; full_local_type_source_sha256 = (Get-TextSha256 $sourceByType['EnemyAINestSpawnObject']) },
                @{ name = 'EnemyAI'; full_local_type_source_sha256 = (Get-TextSha256 $sourceByType['EnemyAI']) }
            )
        }
        selection = @{
            caller_downstream_depth = 1
            roundmanager_exact_signature = $assign.Signature
            roundmanager_selected_signatures = @($roundContext | ForEach-Object { $_.Signature })
            nest_lifecycle_seed_signatures = @($nestSeeds | ForEach-Object { $_.Signature })
            nest_selected_signatures = @($nestContext | ForEach-Object { $_.Signature })
            enemyai_exact_signature = $useNest.Signature
            enemyai_selected_signatures = @($enemyContext | ForEach-Object { $_.Signature })
            per_type_max_source_lines = 1600
            combined_max_report_lines = 1800
        }
        report = @{ file = $ReportName; sha256 = (Get-TextSha256 $report); excludes = @('game binaries', 'full type decompiles', 'absolute local paths', 'user names') }
    }
    $metadataJson = ($metadata | ConvertTo-Json -Depth 12) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)

    Write-Step ('Publishing focused vent/nest evidence on new branch ' + $branch + '.')
    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{ base_tree = $mainCommit.tree.sha; tree = $entries }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{ message = ('Capture exact V81 vent and nest lifecycle evidence ' + $stamp); tree = $treeResult.sha; parents = @($repositoryMain) }
    $refResult = Invoke-RepoApi -Endpoint 'git/refs' -Method 'POST' -Body @{ ref = ('refs/heads/' + $branch); sha = $commitResult.sha }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Published branch response did not match the evidence commit.' }

    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence branch: ' + $branch)
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Report: https://github.com/' + $RepositoryName + '/blob/' + $commitResult.sha + '/' + $directory + '/' + $ReportName)
    Write-Host 'Only the focused text report and manifest were uploaded. No gameplay run, local repository clone, profile build, or controller change was performed.'
}
finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) { Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
