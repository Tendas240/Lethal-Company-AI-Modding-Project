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
$ReportName = 'V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt'
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

function Get-IlTypeModel {
    param([Parameter(Mandatory = $true)][string]$Il, [Parameter(Mandatory = $true)][string]$TypeName)
    $endPattern = '(?m)^[\t ]*\}\s*// end of method ' + [regex]::Escape($TypeName) + '::(?<name>[^\r\n]+?)\s*$'
    $endMatches = [regex]::Matches($Il, $endPattern)
    if ($endMatches.Count -eq 0) { throw ($TypeName + ': no exact IL method end markers were found.') }
    $methods = @()
    foreach ($endMatch in $endMatches) {
        $prefix = $Il.Substring(0, $endMatch.Index)
        $starts = [regex]::Matches($prefix, '(?m)^[\t ]*\.method\b')
        if ($starts.Count -eq 0) { throw ($TypeName + ': IL method start missing before ' + $endMatch.Groups['name'].Value + '.') }
        $start = $starts[$starts.Count - 1].Index
        $end = $endMatch.Index + $endMatch.Length
        $text = $Il.Substring($start, $end - $start)
        $brace = $text.IndexOf('{')
        if ($brace -lt 0) { throw ($TypeName + ': IL method body opener missing for ' + $endMatch.Groups['name'].Value + '.') }
        $methods += [pscustomobject]@{
            Name = $endMatch.Groups['name'].Value.Trim()
            Signature = $text.Substring(0, $brace).Trim()
            Text = $text
            Body = $text.Substring($brace + 1)
            SourceLine = ([regex]::Matches($Il.Substring(0, $start), '\n')).Count + 1
            Index = $start
        }
    }
    $headerMatch = [regex]::Match($Il, '(?ms)^[\t ]*\.class\b.*?\b' + [regex]::Escape($TypeName) + '\b.*?^[\t ]*\{')
    $header = if ($headerMatch.Success) { $headerMatch.Value.TrimEnd('{').Trim() } else { '.class ' + $TypeName }
    return [pscustomobject]@{ TypeName = $TypeName; Header = $header; Methods = @($methods) }
}
function Get-ExactIlMethod {
    param([Parameter(Mandatory = $true)]$Model, [Parameter(Mandatory = $true)][string]$Name, [Parameter(Mandatory = $true)][string]$SignaturePattern)
    $found = @($Model.Methods | Where-Object { $_.Name -eq $Name -and $_.Signature -match $SignaturePattern })
    if ($found.Count -ne 1) { throw ($Model.TypeName + ': expected exactly one exact IL method ' + $Name + ', found ' + $found.Count + '.') }
    return $found[0]
}
function Get-IlOneHopContext {
    param([Parameter(Mandatory = $true)]$Model, [Parameter(Mandatory = $true)][object[]]$Seeds, [int]$MaxLines = 1600)
    $selected = @{}
    foreach ($seed in $Seeds) { $selected[[string]$seed.Index] = $seed }
    foreach ($candidate in $Model.Methods) {
        if ($selected.ContainsKey([string]$candidate.Index)) { continue }
        $include = $false
        foreach ($seed in $Seeds) {
            $seedPattern = '::' + [regex]::Escape($seed.Name) + '\s*\('
            $candidatePattern = '::' + [regex]::Escape($candidate.Name) + '\s*\('
            if ($candidate.Body -match $seedPattern -or $seed.Body -match $candidatePattern) { $include = $true; break }
        }
        if ($include) { $selected[[string]$candidate.Index] = $candidate }
    }
    $result = @($selected.Values | Sort-Object Index)
    $lineCount = 0
    foreach ($method in $result) { $lineCount += @($method.Text -split '\r?\n').Count }
    if ($lineCount -gt $MaxLines) { throw ($Model.TypeName + ': focused IL extraction is ' + $lineCount + ' lines; limit ' + $MaxLines + '. No evidence was uploaded.') }
    if ($result.Count -eq 0) { throw ($Model.TypeName + ': focused IL extraction is empty.') }
    return $result
}
function Get-IlLifecycleSeeds {
    param([Parameter(Mandatory = $true)]$Model)
    $awake = @($Model.Methods | Where-Object { $_.Name -eq 'Awake' })
    if ($awake.Count -ne 1) { throw ($Model.TypeName + ': expected exactly one declared IL Awake method, found ' + $awake.Count + '.') }
    $seeds = @($Model.Methods | Where-Object { $LifecycleNames -contains $_.Name })
    if (@($seeds | Where-Object { $_.Name -eq 'Awake' }).Count -ne 1) { throw ($Model.TypeName + ': Awake was not retained in IL lifecycle selection.') }
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
.class public auto ansi beforefieldinit RoundManager extends [mscorlib]System.Object
{
    .method public hidebysig instance bool AssignRandomEnemyToVent (class EnemyVent vent, float32 spawnTime) cil managed
    {
        IL_0000: ldarg.0
        IL_0001: call instance bool RoundManager::PickEnemy(class EnemyVent)
        IL_0006: ret
    } // end of method RoundManager::AssignRandomEnemyToVent
    .method public hidebysig instance bool AssignRandomEnemyToVent (int32 fake) cil managed
    {
        IL_0000: ldc.i4.0
        IL_0001: ret
    } // end of method RoundManager::AssignRandomEnemyToVent
    .method private hidebysig instance bool PickEnemy (class EnemyVent vent) cil managed
    {
        IL_0000: ldc.i4.1
        IL_0001: ret
    } // end of method RoundManager::PickEnemy
    .method private hidebysig instance void BeginEnemySpawning () cil managed
    {
        IL_0000: ldarg.0
        IL_0001: ldnull
        IL_0002: ldc.r4 1
        IL_0007: call instance bool RoundManager::AssignRandomEnemyToVent(class EnemyVent, float32)
        IL_000c: pop
        IL_000d: ret
    } // end of method RoundManager::BeginEnemySpawning
}
'@
    $round = Get-IlTypeModel -Il $roundFixture -TypeName 'RoundManager'
    $assign = Get-ExactIlMethod -Model $round -Name 'AssignRandomEnemyToVent' -SignaturePattern '\(\s*class EnemyVent\b[^,]*,\s*float32\b'
    $roundContext = @(Get-IlOneHopContext -Model $round -Seeds @($assign))
    $roundNames = @($roundContext | ForEach-Object { $_.Name })
    foreach ($required in @('AssignRandomEnemyToVent', 'PickEnemy', 'BeginEnemySpawning')) { if ($roundNames -notcontains $required) { throw ('RoundManager IL context missing ' + $required) } }
    if (@($roundContext | Where-Object { $_.Signature -match '\(\s*int32\b' }).Count -ne 0) { throw 'Wrong RoundManager overload leaked into IL exact selection.' }

    $nestFixture = @'
.class public auto ansi beforefieldinit EnemyAINestSpawnObject extends [mscorlib]System.Object
{
    .method private hidebysig instance void Awake () cil managed
    {
        IL_0000: ldarg.0
        IL_0001: call instance void EnemyAINestSpawnObject::RegisterNest()
        IL_0006: ret
    } // end of method EnemyAINestSpawnObject::Awake
    .method private hidebysig instance void OnDestroy () cil managed
    {
        IL_0000: ldarg.0
        IL_0001: call instance void EnemyAINestSpawnObject::CleanupNest()
        IL_0006: ret
    } // end of method EnemyAINestSpawnObject::OnDestroy
    .method private hidebysig instance void RegisterNest () cil managed
    {
        IL_0000: ret
    } // end of method EnemyAINestSpawnObject::RegisterNest
    .method private hidebysig instance void CleanupNest () cil managed
    {
        IL_0000: ret
    } // end of method EnemyAINestSpawnObject::CleanupNest
}
'@
    $nest = Get-IlTypeModel -Il $nestFixture -TypeName 'EnemyAINestSpawnObject'
    $nestSeeds = @(Get-IlLifecycleSeeds -Model $nest)
    $nestContext = @(Get-IlOneHopContext -Model $nest -Seeds $nestSeeds)
    $nestNames = @($nestContext | ForEach-Object { $_.Name })
    foreach ($required in @('Awake', 'OnDestroy', 'RegisterNest', 'CleanupNest')) { if ($nestNames -notcontains $required) { throw ('Nest IL lifecycle context missing ' + $required) } }
    $missingAwake = $nestFixture -replace '(?ms)\s*\.method private hidebysig instance void Awake \(\) cil managed.*?// end of method EnemyAINestSpawnObject::Awake\s*', "`n"
    $failed = $false
    try { Get-IlLifecycleSeeds -Model (Get-IlTypeModel -Il $missingAwake -TypeName 'EnemyAINestSpawnObject') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing declared IL Awake rejection failed.' }

    $enemyFixture = @'
.class public auto ansi beforefieldinit EnemyAI extends [mscorlib]System.Object
{
    .method public hidebysig instance void UseNestSpawnObject (class EnemyAINestSpawnObject nest) cil managed
    {
        IL_0000: ldarg.0
        IL_0001: call instance void EnemyAI::ReleasePreviousNest()
        IL_0006: ret
    } // end of method EnemyAI::UseNestSpawnObject
    .method public hidebysig instance void UseNestSpawnObject (int32 fake) cil managed
    {
        IL_0000: ret
    } // end of method EnemyAI::UseNestSpawnObject
    .method private hidebysig instance void Start () cil managed
    {
        IL_0000: ldarg.0
        IL_0001: ldnull
        IL_0002: call instance void EnemyAI::UseNestSpawnObject(class EnemyAINestSpawnObject)
        IL_0007: ret
    } // end of method EnemyAI::Start
    .method private hidebysig instance void ReleasePreviousNest () cil managed
    {
        IL_0000: ret
    } // end of method EnemyAI::ReleasePreviousNest
}
'@
    $enemy = Get-IlTypeModel -Il $enemyFixture -TypeName 'EnemyAI'
    $useNest = Get-ExactIlMethod -Model $enemy -Name 'UseNestSpawnObject' -SignaturePattern '\(\s*class EnemyAINestSpawnObject\b'
    $enemyContext = @(Get-IlOneHopContext -Model $enemy -Seeds @($useNest))
    $enemyNames = @($enemyContext | ForEach-Object { $_.Name })
    foreach ($required in @('UseNestSpawnObject', 'Start', 'ReleasePreviousNest')) { if ($enemyNames -notcontains $required) { throw ('EnemyAI IL context missing ' + $required) } }

    $failed = $false
    try { Get-ExactIlMethod -Model $round -Name 'Missing' -SignaturePattern 'Missing' | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing IL target rejection failed.' }
    $failed = $false
    try { Get-IlOneHopContext -Model $round -Seeds @($assign) -MaxLines 1 | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'IL size-limit rejection failed.' }
    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/VentNestLifecycle/20260911T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs|il)$' }).Count -ne 0) { throw 'Publication allowlist test failed.' }
    Write-Host 'PASS: IL exact overloads, declared Awake lifecycle, one-hop caller/downstream context, limits and two-file publication.'
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
    $ilByType = @{}
    $modelByType = @{}
    foreach ($typeName in @('RoundManager', 'EnemyAINestSpawnObject', 'EnemyAI')) {
        Write-Step ('Decompiling exact installed IL type ' + $typeName + '.')
        $il = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @($ilspy.IlSpyDll, '-il', '-t', $typeName, '-r', $managedDir, $assemblyPath) -Label ($typeName + ' IL decompile')
        if ([string]::IsNullOrWhiteSpace($il)) { throw ($typeName + ': IL decompiler returned empty source.') }
        $ilByType[$typeName] = $il
        $modelByType[$typeName] = Get-IlTypeModel -Il $il -TypeName $typeName
    }

    $assign = Get-ExactIlMethod -Model $modelByType['RoundManager'] -Name 'AssignRandomEnemyToVent' -SignaturePattern '\(\s*class EnemyVent\b[^,]*,\s*float32\b'
    $roundContext = @(Get-IlOneHopContext -Model $modelByType['RoundManager'] -Seeds @($assign))
    $nestSeeds = @(Get-IlLifecycleSeeds -Model $modelByType['EnemyAINestSpawnObject'])
    $nestContext = @(Get-IlOneHopContext -Model $modelByType['EnemyAINestSpawnObject'] -Seeds $nestSeeds)
    $useNest = Get-ExactIlMethod -Model $modelByType['EnemyAI'] -Name 'UseNestSpawnObject' -SignaturePattern '\(\s*class EnemyAINestSpawnObject\b'
    $enemyContext = @(Get-IlOneHopContext -Model $modelByType['EnemyAI'] -Seeds @($useNest))

    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 vent/nest lifecycle IL evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Steam buildid: ' + $steamIdentity.BuildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion + ' IL mode')
    [void]$builder.AppendLine('Scope: exact AssignRandomEnemyToVent(EnemyVent,float), declared EnemyAINestSpawnObject lifecycle including exact Awake, exact EnemyAI.UseNestSpawnObject(EnemyAINestSpawnObject), and one-hop same-type caller/downstream context only.')
    [void]$builder.AppendLine('IL is used deliberately so a valid declared Unity lifecycle method cannot be lost because of C# rendering/parser shape.')
    [void]$builder.AppendLine('This supplements the completed 27-block RoundManager capture; it does not repeat that capture and is not gameplay acceptance.')
    [void]$builder.AppendLine('Game binaries, full type IL decompiles, absolute local paths and user names are excluded.')

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
            [void]$builder.AppendLine('--- ' + ($method.Signature -replace '\r?\n', ' ') + ' / local IL line ' + $method.SourceLine + ' ---')
            [void]$builder.AppendLine($method.Text)
        }
    }
    $report = $builder.ToString()
    if (@($report -split '\r?\n').Count -gt 1800) { throw 'Combined focused IL report exceeded 1800 lines. No evidence was uploaded.' }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix
    $branch = 'source-evidence/v81-vent-nest-' + $stamp.ToLowerInvariant() + '-' + $suffix
    $metadata = [ordered]@{
        schema_version = 2
        purpose = 'Supplemental installed V81 vent assignment and nest lifecycle IL evidence for S1.42AI-DIAG1 patch safety'
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
            mode = 'IL'
            types = @(
                @{ name = 'RoundManager'; full_local_type_il_sha256 = (Get-TextSha256 $ilByType['RoundManager']) },
                @{ name = 'EnemyAINestSpawnObject'; full_local_type_il_sha256 = (Get-TextSha256 $ilByType['EnemyAINestSpawnObject']) },
                @{ name = 'EnemyAI'; full_local_type_il_sha256 = (Get-TextSha256 $ilByType['EnemyAI']) }
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
        report = @{ file = $ReportName; sha256 = (Get-TextSha256 $report); excludes = @('game binaries', 'full type IL decompiles', 'absolute local paths', 'user names') }
    }
    $metadataJson = ($metadata | ConvertTo-Json -Depth 12) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)

    Write-Step ('Publishing focused vent/nest IL evidence on new branch ' + $branch + '.')
    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{ base_tree = $mainCommit.tree.sha; tree = $entries }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{ message = ('Capture exact V81 vent and nest lifecycle IL evidence ' + $stamp); tree = $treeResult.sha; parents = @($repositoryMain) }
    $refResult = Invoke-RepoApi -Endpoint 'git/refs' -Method 'POST' -Body @{ ref = ('refs/heads/' + $branch); sha = $commitResult.sha }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Published branch response did not match the evidence commit.' }

    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence branch: ' + $branch)
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Report: https://github.com/' + $RepositoryName + '/blob/' + $commitResult.sha + '/' + $directory + '/' + $ReportName)
    Write-Host 'Only the focused IL text report and manifest were uploaded. No gameplay run, local repository clone, profile build, or controller change was performed.'
}
finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) { Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
