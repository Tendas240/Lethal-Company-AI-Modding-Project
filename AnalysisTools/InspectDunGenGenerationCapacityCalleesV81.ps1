#requires -Version 5.1
[CmdletBinding()]
param([switch]$SelfTest, [switch]$BootstrapSelfTest)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$RepositoryName = 'Tendas240/Lethal-Company-AI-Modding-Project'
$PullRequestNumber = 138
$PullRequestBranch = 'scope/universal-interior-phase-c3a-dawn-tags'
$ExpectedBaseBranch = 'main'
$ExpectedRepositoryMain = '56355ff518ae4301a38d370be9561251f6f963c1'
$EvidenceRoot = 'SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees'
$ReportName = 'DUNGEN_GENERATION_CAPACITY_CROSS_TYPE_CALLEES_FOCUSED_DECOMPILE.txt'

$IlSpyVersion = '11.0.0.9375'
$NuGetSource = 'https://api.nuget.org/v3/index.json'
$SteamAppId = '1966720'
$ExpectedAssemblySha256 = '5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731'
$ExpectedDunGenSha256 = 'd62bbc63eae39ef388797194796ed9cf5a3e7c857fe31f7e5b7310ed78262db6'
$ExpectedExeSha256 = '24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1'
$ExpectedSteamBuildId = '22825947'
$ExpectedAppManifestSha256 = 'fb6750dfe7e6a7dae7f6e6ec77ae522dff95ba0be7aec8f4d379d01bccebe432'
$ReviewedAppManifestSha256 = @(
    $ExpectedAppManifestSha256,
    'b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3',
    '132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e'
)
$ManifestReview = 'AnalysisTools/InspectRoundManagerSpawningV81_PROVENANCE_REVIEW.md'
$PriorManifest = 'SourceEvidence/VanillaV81/DunGenGenerationCapacity/20260922T193336Z-5d63c0ca/MANIFEST.json'
$C3F14Ledger = 'SourceEvidence/UniversalInteriorViability/PhaseC3F14/GENERATION_CAPACITY_IMPLEMENTATION_SYNTHESIS.json'
$ExpectedC3F14ReportSha256 = '602d0294bc852188283b41e94efebf3417a3f0200fd5ab6d42aaa942ef657f8b'
$ForbiddenMethodNames = @()
$ExpectedRootMethods = @(
    'DunGen.DungeonFlow.GetLineAtDepth',
    'DunGen.GraphLine.GetRandomArchetype',
    'DunGen.InjectedTile.ShouldInjectTileAtPoint',
    'DunGen.BranchCountHelper.ComputeBranchCounts',
    'DunGen.DoorwayPairFinder.GetDoorwayPairs'
)
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Write-Step {
    param([string]$Message)
    Write-Host ('[DunGenGenerationCapacityV81] ' + $Message) -ForegroundColor Cyan
}

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-TextSha256 {
    param([Parameter(Mandatory = $true)][string]$Text)
    $hash = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($hash.ComputeHash($Utf8.GetBytes($Text)))).Replace('-', '').ToLowerInvariant()
    }
    finally { $hash.Dispose() }
}

function Get-SteamBuildIdentity {
    param([Parameter(Mandatory = $true)][string]$Text)
    $appMatches = [regex]::Matches($Text, '"appid"\s+"([^"]+)"')
    $buildMatches = [regex]::Matches($Text, '"buildid"\s+"([^"]+)"')
    if ($appMatches.Count -ne 1 -or $buildMatches.Count -ne 1) {
        throw 'Steam appid and buildid must each occur exactly once.'
    }
    return [pscustomobject]@{
        AppId = $appMatches[0].Groups[1].Value
        BuildId = $buildMatches[0].Groups[1].Value
    }
}

function Assert-InstalledGameProvenance {
    param(
        [string]$AssemblySha,
        [string]$DunGenSha,
        [string]$ExeSha,
        [string]$ManifestSha,
        [string]$AppId,
        [string]$BuildId
    )
    if ($AssemblySha -ne $ExpectedAssemblySha256) {
        throw "Installed Assembly-CSharp SHA mismatch: $AssemblySha. Expected $ExpectedAssemblySha256."
    }
    if ($DunGenSha -ne $ExpectedDunGenSha256) {
        throw "Installed DunGen.dll SHA mismatch: $DunGenSha. Expected $ExpectedDunGenSha256."
    }
    if ($ExeSha -ne $ExpectedExeSha256) { throw "Game executable SHA mismatch: $ExeSha." }
    if ($AppId -cne $SteamAppId) { throw "Steam appid mismatch: $AppId." }
    if ($BuildId -cne $ExpectedSteamBuildId) { throw "Steam buildid mismatch: $BuildId." }
    if ($ReviewedAppManifestSha256 -notcontains $ManifestSha) {
        throw "Steam appmanifest SHA mismatch: $ManifestSha. Refusing unreviewed provenance drift."
    }
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

    $programFilesX86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    if ($programFilesX86) {
        $candidate = Join-Path $programFilesX86 'Steam'
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
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $candidates += (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    $unique = @($candidates | Select-Object -Unique)
    if ($unique.Count -eq 0) {
        throw 'Could not locate installed Lethal Company Assembly-CSharp.dll in detected Steam libraries.'
    }
    if ($unique.Count -gt 1) {
        throw ('Multiple Lethal Company Assembly-CSharp.dll candidates were found. Refusing to guess: ' + ($unique -join '; '))
    }
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
        return [pscustomobject]@{
            ExitCode = $process.ExitCode
            StdOut = $stdoutTask.GetAwaiter().GetResult()
            StdErr = $stderrTask.GetAwaiter().GetResult()
        }
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
        throw ($Label + ' failed with exit code ' + $result.ExitCode + '.')
    }
    return $result.StdOut
}

function Get-ExactTypeSuggestion {
    param(
        [Parameter(Mandatory = $true)][string]$DiagnosticText,
        [Parameter(Mandatory = $true)][string]$ClassName
    )
    $pattern = '(?m)^\\s*(?<type>(?:[A-Za-z_][A-Za-z0-9_]*\\.)+' + [regex]::Escape($ClassName) + ')\\s*
    param([Parameter(Mandatory = $true)][string]$TempRoot, [switch]$ForceIsolatedSdk)

    $toolDir = Join-Path $TempRoot 'ilspy-tool'
    New-Item -ItemType Directory -Path $toolDir -Force | Out-Null

    $dotnetExe = $null
    $dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($dotnet -and -not $ForceIsolatedSdk) {
        $sdkResult = Invoke-NativeProcess -FilePath $dotnet.Source -Arguments @('--list-sdks')
        if ($sdkResult.ExitCode -eq 0 -and @($sdkResult.StdOut -split '\r?\n' | Where-Object { $_ -match '^10\.' }).Count -gt 0) {
            $dotnetExe = $dotnet.Source
        }
    }

    if (-not $dotnetExe) {
        Write-Step '.NET 10 SDK not found; bootstrapping an isolated SDK.'
        $dotnetDir = Join-Path $TempRoot 'dotnet'
        $installer = Join-Path $TempRoot 'dotnet-install.ps1'
        Invoke-WebRequest -UseBasicParsing 'https://dot.net/v1/dotnet-install.ps1' -OutFile $installer
        $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
        Invoke-CheckedNativeProcess -FilePath $powershellExe -Arguments @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $installer,
            '-Channel', '10.0', '-InstallDir', $dotnetDir, '-NoPath'
        ) -Label 'Isolated .NET SDK installation' | Out-Null
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

    Invoke-CheckedNativeProcess -FilePath $dotnetExe -Arguments @(
        'tool', 'install', 'ilspycmd', '--tool-path', $toolDir, '--version',
        $IlSpyVersion, '--configfile', $nugetConfig, '--disable-parallel'
    ) -Label 'ILSpy installation' | Out-Null

    $matches = @(Get-ChildItem -LiteralPath $toolDir -Recurse -File -Filter 'ilspycmd.dll')
    if ($matches.Count -ne 1) { throw ('Expected exactly one ilspycmd.dll, found ' + $matches.Count + '.') }
    return [pscustomobject]@{ DotNet = $dotnetExe; IlSpyDll = $matches[0].FullName }
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

function Get-ParsedMethods {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$ClassName
    )
    $mask = Get-CodeMask $Source
    $classMatch = [regex]::Match($mask, ('\bclass\s+' + [regex]::Escape($ClassName) + '\b[^{]*\{'))
    if (-not $classMatch.Success) { throw ($ClassName + ' class declaration absent.') }

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
    $decls = [regex]::Matches(
        $mask,
        '(?m)^[\t ]*(?:public|private|protected|internal)\s+[^\r\n{};=]*?\b(?<name>[A-Za-z_][A-Za-z0-9_]*)\s*\('
    )
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

        $methods += [pscustomobject]@{
            Name = $decl.Groups['name'].Value
            Signature = $Source.Substring($decl.Index, $bodyStart - $decl.Index).Trim()
            Text = $Source.Substring($decl.Index, $end - $decl.Index + 1)
            Body = $mask.Substring($bodyStart + 1, $end - $bodyStart - 1)
            SourceLine = ([regex]::Matches($Source.Substring(0, $decl.Index), '\n')).Count + 1
            Index = $decl.Index
        }
    }

    if ($methods.Count -eq 0) { throw ('No top-level methods were parsed from ' + $ClassName + '.') }
    return $methods
}

function Add-OneHopNeighbors {
    param(
        [Parameter(Mandatory = $true)][object[]]$Methods,
        [Parameter(Mandatory = $true)][object[]]$Roots
    )
    $selected = @($Roots)
    $rootNames = @($Roots | ForEach-Object { $_.Name } | Sort-Object -Unique)

    foreach ($method in $Methods) {
        if (@($selected | Where-Object { $_.Index -eq $method.Index }).Count -gt 0) { continue }

        $isCaller = $false
        foreach ($name in $rootNames) {
            if ($method.Body -match ('\b' + [regex]::Escape($name) + '\s*\(')) {
                $isCaller = $true
                break
            }
        }

        $isCallee = $false
        foreach ($root in $Roots) {
            if ($root.Body -match ('\b' + [regex]::Escape($method.Name) + '\s*\(')) {
                $isCallee = $true
                break
            }
        }

        if ($isCaller -or $isCallee) { $selected += $method }
    }

    return @($selected | Sort-Object Index -Unique)
}


function Assert-MethodSelection {
    param(
        [Parameter(Mandatory = $true)][object[]]$Methods,
        [Parameter(Mandatory = $true)][string]$Label,
        [int]$MaxLines
    )
    if ($Methods.Count -eq 0) { throw ($Label + ' focused extraction is empty.') }
    $lineCount = 0
    foreach ($method in $Methods) {
        if ($ForbiddenMethodNames -contains $method.Name) {
            throw ($Label + ' selected forbidden already-closed method: ' + $method.Name)
        }
        if ($method.Body -match '^\s*throw\s+null\s*;\s*$') {
            throw ('Reference-only throw-null stub rejected: ' + $method.Signature)
        }
        $lineCount += @($method.Text -split '\r?\n').Count
    }
    if ($lineCount -gt $MaxLines) {
        throw ($Label + ' focused extraction is ' + $lineCount + ' lines; limit ' + $MaxLines + '.')
    }
}


function Get-FocusedTypeSelection {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$ClassName,
        [Parameter(Mandatory = $true)][string]$RootName,
        [Parameter(Mandatory = $true)][string]$SignalPattern,
        [switch]$IncludeConstructors,
        [int]$MaxLines = 1200
    )

    $methods = @(Get-ParsedMethods -Source $Source -ClassName $ClassName)
    $roots = @($methods | Where-Object { $_.Name -ceq $RootName })
    if ($roots.Count -eq 0) {
        throw ($ClassName + '.' + $RootName + ' root method absent.')
    }
    if ($roots.Count -gt 3) {
        throw ($ClassName + '.' + $RootName + ' has unexpected overload count ' + $roots.Count + '.')
    }

    $rootText = (($roots | ForEach-Object { $_.Name + [Environment]::NewLine + $_.Body }) -join [Environment]::NewLine)
    if ($rootText -notmatch $SignalPattern) {
        throw ($ClassName + '.' + $RootName + ' lacks required semantic signal: ' + $SignalPattern)
    }

    $seeds = @($roots)
    if ($IncludeConstructors) {
        $constructors = @($methods | Where-Object { $_.Name -ceq $ClassName })
        if ($constructors.Count -eq 0) {
            throw ($ClassName + ' constructor required by focused capture but absent.')
        }
        $seeds += $constructors
    }

    $selected = @($seeds)
    foreach ($method in $methods) {
        if (@($selected | Where-Object { $_.Index -eq $method.Index }).Count -gt 0) { continue }
        foreach ($seed in $seeds) {
            if ($seed.Body -match ('\b' + [regex]::Escape($method.Name) + '\s*\(')) {
                $selected += $method
                break
            }
        }
    }

    $selected = @($selected | Sort-Object Index -Unique)
    Assert-MethodSelection -Methods $selected -Label ($ClassName + '.' + $RootName) -MaxLines $MaxLines

    return [pscustomobject]@{
        Methods = $selected
        RootSignatures = @($roots | ForEach-Object { $_.Signature })
        ConstructorSignatures = @($selected | Where-Object { $_.Name -ceq $ClassName } | ForEach-Object { $_.Signature })
        SelectedSignatures = @($selected | ForEach-Object { $_.Signature })
    }
}

function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Report, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees/[0-9TZ]+-[a-f0-9]+$') {
        throw 'Unexpected publication directory.'
    }
    return @(
        @{ path = ($Directory + '/' + $ReportName); mode = '100644'; type = 'blob'; content = $Report },
        @{ path = ($Directory + '/MANIFEST.json'); mode = '100644'; type = 'blob'; content = $Manifest }
    )
}

function Invoke-ProvenanceSelfTest {
    $valid = @{
        AssemblySha = $ExpectedAssemblySha256
        DunGenSha = $ExpectedDunGenSha256
        ExeSha = $ExpectedExeSha256
        ManifestSha = $ExpectedAppManifestSha256
        AppId = $SteamAppId
        BuildId = $ExpectedSteamBuildId
    }

    foreach ($approved in $ReviewedAppManifestSha256) {
        $valid.ManifestSha = $approved
        Assert-InstalledGameProvenance @valid
    }

    foreach ($key in @('AssemblySha', 'DunGenSha', 'ExeSha', 'ManifestSha', 'AppId', 'BuildId')) {
        $bad = $valid.Clone()
        $bad[$key] = 'unreviewed'
        $failed = $false
        try { Assert-InstalledGameProvenance @bad } catch { $failed = $true }
        if (-not $failed) { throw ('Provenance rejection failed for ' + $key) }
    }
}

function Invoke-ExtractorSelfTest {
    $typeDiagnostic = @'
DunGen.DungeonFlow decompiler stderr:
Could not find a type named 'DunGen.DungeonFlow'.
Did you mean one of the following?
    DunGen.Graph.DungeonFlow
    DunGen.Graph.DungeonFlowBuilder
'@
    $resolved = Get-ExactTypeSuggestion -DiagnosticText $typeDiagnostic -ClassName 'DungeonFlow'
    if ($resolved -cne 'DunGen.Graph.DungeonFlow') { throw 'Exact ILSpy type-suggestion resolution self-test failed.' }

    $failed = $false
    try {
        Get-ExactTypeSuggestion -DiagnosticText @'
    DunGen.A.GraphLine
    DunGen.B.GraphLine
'@ -ClassName 'GraphLine' | Out-Null
    } catch { $failed = $true }
    if (-not $failed) { throw 'Ambiguous ILSpy type-suggestion rejection self-test failed.' }

    $fixtures = @(
        [pscustomobject]@{
            ClassName = 'DungeonFlow'; RootName = 'GetLineAtDepth'; Signal = '\bLines\b'; IncludeConstructors = $false
            Source = @'
public class DungeonFlow
{
    public object[] Lines;
    public object GetLineAtDepth(float depth) { return PickLine(depth, Lines); }
    private object PickLine(float depth, object[] lines) { return null; }
    private void Unrelated() { }
}
'@
            Required = @('GetLineAtDepth','PickLine')
        },
        [pscustomobject]@{
            ClassName = 'GraphLine'; RootName = 'GetRandomArchetype'; Signal = '\bArchetype'; IncludeConstructors = $false
            Source = @'
public class GraphLine
{
    public object[] Archetypes;
    public object GetRandomArchetype(object random, object previous) { return PickArchetype(Archetypes); }
    private object PickArchetype(object[] values) { return null; }
}
'@
            Required = @('GetRandomArchetype','PickArchetype')
        },
        [pscustomobject]@{
            ClassName = 'InjectedTile'; RootName = 'ShouldInjectTileAtPoint'; Signal = '[Dd]epth'; IncludeConstructors = $true
            Source = @'
public class InjectedTile
{
    private float minDepth;
    public InjectedTile(object rule, bool main, object random) { minDepth = BuildDepth(rule); }
    public bool ShouldInjectTileAtPoint(bool main, float pathDepth, float branchDepth) { return CheckDepth(main ? pathDepth : branchDepth); }
    private float BuildDepth(object rule) { return 0f; }
    private bool CheckDepth(float depth) { return depth >= minDepth; }
}
'@
            Required = @('InjectedTile','ShouldInjectTileAtPoint','BuildDepth','CheckDepth')
        },
        [pscustomobject]@{
            ClassName = 'BranchCountHelper'; RootName = 'ComputeBranchCounts'; Signal = '\bBranch'; IncludeConstructors = $false
            Source = @'
public class BranchCountHelper
{
    public static void ComputeBranchCounts(object flow, object random, object dungeon, ref int[] branches) { FillBranches(branches); }
    private static void FillBranches(int[] branches) { }
}
'@
            Required = @('ComputeBranchCounts','FillBranches')
        },
        [pscustomobject]@{
            ClassName = 'DoorwayPairFinder'; RootName = 'GetDoorwayPairs'; Signal = '\bDoorway|\bTileWeights|\bWeight'; IncludeConstructors = $false
            Source = @'
public class DoorwayPairFinder
{
    public object TileWeights;
    public object GetDoorwayPairs(int? maxCount) { return BuildDoorwayPairs(TileWeights); }
    private object BuildDoorwayPairs(object weights) { return null; }
}
'@
            Required = @('GetDoorwayPairs','BuildDoorwayPairs')
        }
    )

    foreach ($fixture in $fixtures) {
        $selection = Get-FocusedTypeSelection -Source $fixture.Source -ClassName $fixture.ClassName -RootName $fixture.RootName -SignalPattern $fixture.Signal -IncludeConstructors:$fixture.IncludeConstructors
        $names = @($selection.Methods | ForEach-Object { $_.Name })
        foreach ($requiredName in $fixture.Required) {
            if ($names -notcontains $requiredName) {
                throw ($fixture.ClassName + ' focused self-test missed ' + $requiredName)
            }
        }
        if ($names -contains 'Unrelated') { throw ($fixture.ClassName + ' selected unrelated method.') }
    }

    $failed = $false
    try {
        Get-FocusedTypeSelection -Source $fixtures[0].Source -ClassName 'DungeonFlow' -RootName 'MissingMethod' -SignalPattern '\bLines\b' | Out-Null
    } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-root rejection self-test failed.' }

    $failed = $false
    try {
        Get-FocusedTypeSelection -Source ($fixtures[1].Source -replace 'Archetypes', 'Choices') -ClassName 'GraphLine' -RootName 'GetRandomArchetype' -SignalPattern '\bArchetype' | Out-Null
    } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-signal rejection self-test failed.' }

    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees/20260922T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs)$' }).Count -ne 0) {
        throw 'Publication allowlist self-test failed.'
    }
}

function Invoke-BootstrapSelfTest {
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-callees-bootstrap-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $temp -Force | Out-Null
    try {
        $tool = Ensure-DotNetAndIlSpy -TempRoot $temp -ForceIsolatedSdk
        $version = Invoke-CheckedNativeProcess -FilePath $tool.DotNet -Arguments @($tool.IlSpyDll, '--version') -Label 'ILSpy version'
        if ($version -notmatch ('(?m)^ilspycmd: ' + [regex]::Escape($IlSpyVersion) + '\s*$')) {
            throw 'Installed ILSpy did not report the pinned version.'
        }
    }
    finally {
        Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function Resolve-GitHubCli {
    $command = Get-Command gh -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }

    $programFilesX86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    $paths = @(
        (Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe'),
        (Join-Path $env:LOCALAPPDATA 'Programs\GitHub CLI\gh.exe')
    )
    if ($programFilesX86) { $paths += (Join-Path $programFilesX86 'GitHub CLI\gh.exe') }

    foreach ($path in $paths) {
        if ($path -and (Test-Path -LiteralPath $path)) { return $path }
    }

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw 'GitHub CLI is missing and winget is unavailable.'
    }
    & winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI installation failed.' }

    foreach ($path in $paths) {
        if ($path -and (Test-Path -LiteralPath $path)) { return $path }
    }
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
    $result = Invoke-CheckedNativeProcess -FilePath $script:GhPath -Arguments $arguments -Label ('GitHub API ' + $Method + ' ' + $Endpoint)
    return ($result | ConvertFrom-Json)
}




if ($SelfTest -and $BootstrapSelfTest) { throw 'Select only one self-test mode.' }
if ($SelfTest) {
    Invoke-ProvenanceSelfTest
    Invoke-ExtractorSelfTest
    Write-Host 'PASS: provenance, focused cross-type callee extractor and publication self-tests.'
    return
}
if ($BootstrapSelfTest) {
    Invoke-BootstrapSelfTest
    Write-Host 'PASS: isolated .NET/ILSpy bootstrap.'
    return
}

$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-callees-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $script:CaptureTempRoot -Force | Out-Null

try {
    Write-Step 'Locating and verifying installed V81 and exact DunGen.dll.'
    $assemblyPath = Resolve-AssemblyPath
    $managedDir = Split-Path -Parent $assemblyPath
    $dunGenPath = Join-Path $managedDir 'DunGen.dll'
    if (-not (Test-Path -LiteralPath $dunGenPath -PathType Leaf)) {
        throw 'Installed DunGen.dll is missing from the exact game Managed directory.'
    }

    $gameRoot = Split-Path -Parent (Split-Path -Parent $managedDir)
    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)
    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    foreach ($path in @($exePath, $appManifest)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw 'Required game provenance file is missing.' }
    }

    $assemblySha = Get-Sha256Lower $assemblyPath
    $dunGenSha = Get-Sha256Lower $dunGenPath
    $exeSha = Get-Sha256Lower $exePath
    $manifestSha = Get-Sha256Lower $appManifest
    $steamIdentity = Get-SteamBuildIdentity -Text (Get-Content -LiteralPath $appManifest -Raw)
    Assert-InstalledGameProvenance -AssemblySha $assemblySha -DunGenSha $dunGenSha -ExeSha $exeSha -ManifestSha $manifestSha -AppId $steamIdentity.AppId -BuildId $steamIdentity.BuildId

    $script:GhPath = Resolve-GitHubCli
    & $script:GhPath auth status --hostname github.com *> $null
    if ($LASTEXITCODE -ne 0) {
        & $script:GhPath auth login --hostname github.com --git-protocol https --web
        if ($LASTEXITCODE -ne 0) { throw 'GitHub authentication failed.' }
    }

    $pullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($pullRequest.state -cne 'open' -or
        $pullRequest.merged -eq $true -or
        $pullRequest.head.ref -cne $PullRequestBranch -or
        $pullRequest.head.repo.full_name -cne $RepositoryName -or
        $pullRequest.base.ref -cne $ExpectedBaseBranch -or
        $pullRequest.base.sha -cne $ExpectedRepositoryMain) {
        throw 'PR #138 is not the expected exact-base open in-repository evidence PR.'
    }

    $repositoryPrHead = $pullRequest.head.sha
    $prHeadCommit = Invoke-RepoApi ('git/commits/' + $repositoryPrHead)
    $repositoryMain = (Invoke-RepoApi 'git/ref/heads/main').object.sha
    if ($repositoryMain -cne $ExpectedRepositoryMain) {
        throw ('Repository main drifted from reviewed base: ' + $repositoryMain)
    }

    $priorFile = Invoke-RepoApi ('contents/' + $PriorManifest + '?ref=' + $repositoryPrHead)
    $priorText = $Utf8.GetString([Convert]::FromBase64String($priorFile.content))
    $prior = $priorText | ConvertFrom-Json
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or
        $prior.dungen_assembly.sha256 -ne $ExpectedDunGenSha256 -or
        $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or
        $prior.steam.buildid -ne $ExpectedSteamBuildId -or
        $prior.steam.app_id -ne $SteamAppId -or
        $prior.report.sha256 -ne $ExpectedC3F14ReportSha256) {
        throw 'C3F14 parent capture manifest disagrees with the pinned installed-game/DunGen/report contract.'
    }

    $ledgerFile = Invoke-RepoApi ('contents/' + $C3F14Ledger + '?ref=' + $repositoryPrHead)
    $ledgerText = $Utf8.GetString([Convert]::FromBase64String($ledgerFile.content))
    $ledger = $ledgerText | ConvertFrom-Json
    if ($ledger.schema_version -cne 'c3f14-generation-capacity-implementation-synthesis-1' -or
        $ledger.aggregate.proof_set_flows -ne 20 -or
        $ledger.aggregate.generated_eligible_positive_three_lower_bound_proven -ne 0) {
        throw 'C3F14 synthesis ledger does not match the reviewed proof boundary.'
    }

    $actualRoots = @($ledger.remaining_cross_type_callees)
    if ($actualRoots.Count -ne $ExpectedRootMethods.Count) { throw 'C3F14 remaining-callee count mismatch.' }
    for ($i = 0; $i -lt $ExpectedRootMethods.Count; $i++) {
        if ($actualRoots[$i] -cne $ExpectedRootMethods[$i]) {
            throw ('C3F14 remaining-callee mismatch at index ' + $i + ': ' + $actualRoots[$i])
        }
    }

    $ilspy = Ensure-DotNetAndIlSpy -TempRoot $script:CaptureTempRoot

    $specs = @(
        [pscustomobject]@{ Type = 'DunGen.DungeonFlow'; Class = 'DungeonFlow'; Root = 'GetLineAtDepth'; Signal = '\bLines\b'; Constructors = $false; MaxLines = 500 },
        [pscustomobject]@{ Type = 'DunGen.GraphLine'; Class = 'GraphLine'; Root = 'GetRandomArchetype'; Signal = '\bArchetype'; Constructors = $false; MaxLines = 700 },
        [pscustomobject]@{ Type = 'DunGen.InjectedTile'; Class = 'InjectedTile'; Root = 'ShouldInjectTileAtPoint'; Signal = '[Dd]epth'; Constructors = $true; MaxLines = 900 },
        [pscustomobject]@{ Type = 'DunGen.BranchCountHelper'; Class = 'BranchCountHelper'; Root = 'ComputeBranchCounts'; Signal = '\bBranch'; Constructors = $false; MaxLines = 900 },
        [pscustomobject]@{ Type = 'DunGen.DoorwayPairFinder'; Class = 'DoorwayPairFinder'; Root = 'GetDoorwayPairs'; Signal = '\bDoorway|\bTileWeights|\bWeight'; Constructors = $false; MaxLines = 1800 }
    )

    $captures = @()
    foreach ($spec in $specs) {
        Write-Step ('Decompiling exact installed ' + $spec.Type + ' locally.')
        $decompile = Invoke-FocusedTypeDecompile -DotNet $ilspy.DotNet -IlSpyDll $ilspy.IlSpyDll -ManagedDir $managedDir -DunGenPath $dunGenPath -PreferredType $spec.Type -ClassName $spec.Class
        $source = $decompile.Source

        $selection = Get-FocusedTypeSelection -Source $source -ClassName $spec.Class -RootName $spec.Root -SignalPattern $spec.Signal -IncludeConstructors:$spec.Constructors -MaxLines $spec.MaxLines
        $captures += [pscustomobject]@{
            RequestedType = $spec.Type
            Type = $decompile.Type
            UsedTypeSuggestion = $decompile.UsedSuggestion
            Class = $spec.Class
            Root = $spec.Root
            FullSourceSha256 = Get-TextSha256 $source
            Selection = $selection
        }
    }

    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 DunGen generation-capacity cross-type callee evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Installed DunGen.dll SHA-256: ' + $dunGenSha)
    [void]$builder.AppendLine('Steam buildid: ' + $steamIdentity.BuildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Repository PR #138 head at capture: ' + $repositoryPrHead)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion)
    [void]$builder.AppendLine('Scope: only the five C3F14 unresolved cross-type roots, plus directly called same-type helpers; InjectedTile additionally includes its constructor(s) and their direct same-type helpers.')
    [void]$builder.AppendLine('Explicit exclusions: previously captured DungeonGenerator cluster, TilePlacementData.NormalizedDepth, Doorway.ProcessDoorwayObjects, DungeonGenerator.ProcessGlobalProps, GameObjectChanceTable.GetRandom, RoundManager.SpawnSyncedProps, binaries and full type decompiles.')

    foreach ($capture in $captures) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('## ' + $capture.Type + '.' + $capture.Root)
        foreach ($method in $capture.Selection.Methods) {
            [void]$builder.AppendLine('')
            [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
            [void]$builder.AppendLine($method.Text)
        }
    }

    $report = $builder.ToString()
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix

    $metadataTypes = @()
    foreach ($capture in $captures) {
        $metadataTypes += [ordered]@{
            requested_type = $capture.RequestedType
            type = $capture.Type
            resolved_from_ilspy_suggestion = $capture.UsedTypeSuggestion
            full_local_type_source_sha256 = $capture.FullSourceSha256
            root_method = $capture.Root
            root_signatures = @($capture.Selection.RootSignatures)
            constructor_signatures = @($capture.Selection.ConstructorSignatures)
            selected_signatures = @($capture.Selection.SelectedSignatures)
            same_type_neighbor_depth = 1
        }
    }

    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Exact installed-V81 DunGen cross-type callees remaining after Universal Interior Viability C3F14'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        pull_request = $PullRequestNumber
        pull_request_branch = $PullRequestBranch
        repository_pr_head_at_capture = $repositoryPrHead
        repository_main_at_capture = $repositoryMain
        expected_repository_main = $ExpectedRepositoryMain
        bound_c3f14_parent_manifest = @{
            path = $PriorManifest
            git_blob_sha = $priorFile.sha
            text_sha256 = (Get-TextSha256 $priorText)
            report_sha256 = $prior.report.sha256
        }
        bound_c3f14_synthesis = @{
            path = $C3F14Ledger
            git_blob_sha = $ledgerFile.sha
            text_sha256 = (Get-TextSha256 $ledgerText)
            schema_version = $ledger.schema_version
            proof_set_flows = $ledger.aggregate.proof_set_flows
            remaining_cross_type_callees = @($actualRoots)
        }
        source_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'; sha256 = $assemblySha }
        dungen_assembly = @{ logical_path = 'Lethal Company_Data/Managed/DunGen.dll'; sha256 = $dunGenSha }
        game_executable = @{ logical_path = 'Lethal Company.exe'; sha256 = $exeSha }
        steam = @{
            app_id = $steamIdentity.AppId
            buildid = $steamIdentity.BuildId
            appmanifest_sha256 = $manifestSha
            prior_appmanifest_sha256 = $ExpectedAppManifestSha256
            matches_prior_appmanifest = ($manifestSha -eq $ExpectedAppManifestSha256)
            manifest_review = $ManifestReview
        }
        decompiler = @{ tool = 'ilspycmd'; version = $IlSpyVersion; types = @($metadataTypes) }
        selection = @{
            exact_root_methods = @($ExpectedRootMethods)
            same_type_direct_callees_only = $true
            injected_tile_constructors_included = $true
            forbidden_recaptures = @(
                'DungeonGenerator generation cluster',
                'TilePlacementData.NormalizedDepth',
                'Doorway.ProcessDoorwayObjects',
                'DungeonGenerator.ProcessGlobalProps',
                'GameObjectChanceTable.GetRandom',
                'RoundManager.SpawnSyncedProps'
            )
        }
        report = @{
            file = $ReportName
            sha256 = (Get-TextSha256 $report)
            excludes = @('game binaries','DunGen.dll','full type decompiles','unrelated methods','absolute local paths','user names')
        }
    }

    $metadataJson = ($metadata | ConvertTo-Json -Depth 20) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)

    Write-Step 'Publishing focused cross-type callee evidence to PR #138.'
    $currentPullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($currentPullRequest.state -cne 'open' -or
        $currentPullRequest.merged -eq $true -or
        $currentPullRequest.head.ref -cne $PullRequestBranch -or
        $currentPullRequest.head.sha -cne $repositoryPrHead -or
        $currentPullRequest.base.ref -cne $ExpectedBaseBranch -or
        $currentPullRequest.base.sha -cne $ExpectedRepositoryMain) {
        throw 'PR #138 changed during capture. Refusing stale write.'
    }
    if ((Invoke-RepoApi 'git/ref/heads/main').object.sha -cne $ExpectedRepositoryMain) {
        throw 'Repository main changed during capture. Refusing stale write.'
    }

    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{
        base_tree = $prHeadCommit.tree.sha
        tree = $entries
    }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{
        message = ('Capture exact V81 DunGen cross-type generation-capacity evidence ' + $stamp)
        tree = $treeResult.sha
        parents = @($repositoryPrHead)
    }
    $refResult = Invoke-RepoApi -Endpoint ('git/refs/heads/' + $PullRequestBranch) -Method 'PATCH' -Body @{
        sha = $commitResult.sha
        force = $false
    }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Updated PR branch response did not match evidence commit.' }

    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Report: https://github.com/' + $RepositoryName + '/blob/' + $commitResult.sha + '/' + $directory + '/' + $ReportName)
    Write-Host 'Only the focused report and manifest were uploaded. No local clone, game/DunGen binary or gameplay run was uploaded.'
}
finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) {
        Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

    $matches = @([regex]::Matches($DiagnosticText, $pattern) | ForEach-Object { $_.Groups['type'].Value } | Select-Object -Unique)
    if ($matches.Count -ne 1) {
        throw ($ClassName + ' type resolution expected exactly one exact ILSpy suggestion, found ' + $matches.Count + '.')
    }
    return $matches[0]
}

function Invoke-FocusedTypeDecompile {
    param(
        [Parameter(Mandatory = $true)][string]$DotNet,
        [Parameter(Mandatory = $true)][string]$IlSpyDll,
        [Parameter(Mandatory = $true)][string]$ManagedDir,
        [Parameter(Mandatory = $true)][string]$DunGenPath,
        [Parameter(Mandatory = $true)][string]$PreferredType,
        [Parameter(Mandatory = $true)][string]$ClassName
    )

    $first = Invoke-NativeProcess -FilePath $DotNet -Arguments @($IlSpyDll, '-t', $PreferredType, '-r', $ManagedDir, $DunGenPath)
    if ($first.ExitCode -eq 0) {
        if ([string]::IsNullOrWhiteSpace($first.StdOut)) { throw ($PreferredType + ' decompiler output is empty.') }
        return [pscustomobject]@{ Type = $PreferredType; Source = $first.StdOut; UsedSuggestion = $false }
    }

    $diagnostic = (($first.StdOut + [Environment]::NewLine + $first.StdErr).Trim())
    $resolvedType = Get-ExactTypeSuggestion -DiagnosticText $diagnostic -ClassName $ClassName
    if ($resolvedType -ceq $PreferredType) {
        throw ($PreferredType + ' decompile failed and ILSpy suggested only the same type.')
    }

    Write-Step ('Resolved installed type ' + $PreferredType + ' -> ' + $resolvedType + ' from ILSpy exact-class suggestion.')
    $second = Invoke-NativeProcess -FilePath $DotNet -Arguments @($IlSpyDll, '-t', $resolvedType, '-r', $ManagedDir, $DunGenPath)
    if ($second.ExitCode -ne 0) {
        if (-not [string]::IsNullOrWhiteSpace($second.StdErr)) { Write-Host $second.StdErr -ForegroundColor Yellow }
        if (-not [string]::IsNullOrWhiteSpace($second.StdOut)) { Write-Host $second.StdOut }
        throw ($resolvedType + ' decompile failed with exit code ' + $second.ExitCode + '.')
    }
    if ([string]::IsNullOrWhiteSpace($second.StdOut)) { throw ($resolvedType + ' decompiler output is empty.') }
    return [pscustomobject]@{ Type = $resolvedType; Source = $second.StdOut; UsedSuggestion = $true }
}

function Ensure-DotNetAndIlSpy {
    param([Parameter(Mandatory = $true)][string]$TempRoot, [switch]$ForceIsolatedSdk)

    $toolDir = Join-Path $TempRoot 'ilspy-tool'
    New-Item -ItemType Directory -Path $toolDir -Force | Out-Null

    $dotnetExe = $null
    $dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($dotnet -and -not $ForceIsolatedSdk) {
        $sdkResult = Invoke-NativeProcess -FilePath $dotnet.Source -Arguments @('--list-sdks')
        if ($sdkResult.ExitCode -eq 0 -and @($sdkResult.StdOut -split '\r?\n' | Where-Object { $_ -match '^10\.' }).Count -gt 0) {
            $dotnetExe = $dotnet.Source
        }
    }

    if (-not $dotnetExe) {
        Write-Step '.NET 10 SDK not found; bootstrapping an isolated SDK.'
        $dotnetDir = Join-Path $TempRoot 'dotnet'
        $installer = Join-Path $TempRoot 'dotnet-install.ps1'
        Invoke-WebRequest -UseBasicParsing 'https://dot.net/v1/dotnet-install.ps1' -OutFile $installer
        $powershellExe = (Get-Command powershell.exe -ErrorAction Stop).Source
        Invoke-CheckedNativeProcess -FilePath $powershellExe -Arguments @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $installer,
            '-Channel', '10.0', '-InstallDir', $dotnetDir, '-NoPath'
        ) -Label 'Isolated .NET SDK installation' | Out-Null
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

    Invoke-CheckedNativeProcess -FilePath $dotnetExe -Arguments @(
        'tool', 'install', 'ilspycmd', '--tool-path', $toolDir, '--version',
        $IlSpyVersion, '--configfile', $nugetConfig, '--disable-parallel'
    ) -Label 'ILSpy installation' | Out-Null

    $matches = @(Get-ChildItem -LiteralPath $toolDir -Recurse -File -Filter 'ilspycmd.dll')
    if ($matches.Count -ne 1) { throw ('Expected exactly one ilspycmd.dll, found ' + $matches.Count + '.') }
    return [pscustomobject]@{ DotNet = $dotnetExe; IlSpyDll = $matches[0].FullName }
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

function Get-ParsedMethods {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$ClassName
    )
    $mask = Get-CodeMask $Source
    $classMatch = [regex]::Match($mask, ('\bclass\s+' + [regex]::Escape($ClassName) + '\b[^{]*\{'))
    if (-not $classMatch.Success) { throw ($ClassName + ' class declaration absent.') }

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
    $decls = [regex]::Matches(
        $mask,
        '(?m)^[\t ]*(?:public|private|protected|internal)\s+[^\r\n{};=]*?\b(?<name>[A-Za-z_][A-Za-z0-9_]*)\s*\('
    )
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

        $methods += [pscustomobject]@{
            Name = $decl.Groups['name'].Value
            Signature = $Source.Substring($decl.Index, $bodyStart - $decl.Index).Trim()
            Text = $Source.Substring($decl.Index, $end - $decl.Index + 1)
            Body = $mask.Substring($bodyStart + 1, $end - $bodyStart - 1)
            SourceLine = ([regex]::Matches($Source.Substring(0, $decl.Index), '\n')).Count + 1
            Index = $decl.Index
        }
    }

    if ($methods.Count -eq 0) { throw ('No top-level methods were parsed from ' + $ClassName + '.') }
    return $methods
}

function Add-OneHopNeighbors {
    param(
        [Parameter(Mandatory = $true)][object[]]$Methods,
        [Parameter(Mandatory = $true)][object[]]$Roots
    )
    $selected = @($Roots)
    $rootNames = @($Roots | ForEach-Object { $_.Name } | Sort-Object -Unique)

    foreach ($method in $Methods) {
        if (@($selected | Where-Object { $_.Index -eq $method.Index }).Count -gt 0) { continue }

        $isCaller = $false
        foreach ($name in $rootNames) {
            if ($method.Body -match ('\b' + [regex]::Escape($name) + '\s*\(')) {
                $isCaller = $true
                break
            }
        }

        $isCallee = $false
        foreach ($root in $Roots) {
            if ($root.Body -match ('\b' + [regex]::Escape($method.Name) + '\s*\(')) {
                $isCallee = $true
                break
            }
        }

        if ($isCaller -or $isCallee) { $selected += $method }
    }

    return @($selected | Sort-Object Index -Unique)
}


function Assert-MethodSelection {
    param(
        [Parameter(Mandatory = $true)][object[]]$Methods,
        [Parameter(Mandatory = $true)][string]$Label,
        [int]$MaxLines
    )
    if ($Methods.Count -eq 0) { throw ($Label + ' focused extraction is empty.') }
    $lineCount = 0
    foreach ($method in $Methods) {
        if ($ForbiddenMethodNames -contains $method.Name) {
            throw ($Label + ' selected forbidden already-closed method: ' + $method.Name)
        }
        if ($method.Body -match '^\s*throw\s+null\s*;\s*$') {
            throw ('Reference-only throw-null stub rejected: ' + $method.Signature)
        }
        $lineCount += @($method.Text -split '\r?\n').Count
    }
    if ($lineCount -gt $MaxLines) {
        throw ($Label + ' focused extraction is ' + $lineCount + ' lines; limit ' + $MaxLines + '.')
    }
}


function Get-FocusedTypeSelection {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$ClassName,
        [Parameter(Mandatory = $true)][string]$RootName,
        [Parameter(Mandatory = $true)][string]$SignalPattern,
        [switch]$IncludeConstructors,
        [int]$MaxLines = 1200
    )

    $methods = @(Get-ParsedMethods -Source $Source -ClassName $ClassName)
    $roots = @($methods | Where-Object { $_.Name -ceq $RootName })
    if ($roots.Count -eq 0) {
        throw ($ClassName + '.' + $RootName + ' root method absent.')
    }
    if ($roots.Count -gt 3) {
        throw ($ClassName + '.' + $RootName + ' has unexpected overload count ' + $roots.Count + '.')
    }

    $rootText = (($roots | ForEach-Object { $_.Name + [Environment]::NewLine + $_.Body }) -join [Environment]::NewLine)
    if ($rootText -notmatch $SignalPattern) {
        throw ($ClassName + '.' + $RootName + ' lacks required semantic signal: ' + $SignalPattern)
    }

    $seeds = @($roots)
    if ($IncludeConstructors) {
        $constructors = @($methods | Where-Object { $_.Name -ceq $ClassName })
        if ($constructors.Count -eq 0) {
            throw ($ClassName + ' constructor required by focused capture but absent.')
        }
        $seeds += $constructors
    }

    $selected = @($seeds)
    foreach ($method in $methods) {
        if (@($selected | Where-Object { $_.Index -eq $method.Index }).Count -gt 0) { continue }
        foreach ($seed in $seeds) {
            if ($seed.Body -match ('\b' + [regex]::Escape($method.Name) + '\s*\(')) {
                $selected += $method
                break
            }
        }
    }

    $selected = @($selected | Sort-Object Index -Unique)
    Assert-MethodSelection -Methods $selected -Label ($ClassName + '.' + $RootName) -MaxLines $MaxLines

    return [pscustomobject]@{
        Methods = $selected
        RootSignatures = @($roots | ForEach-Object { $_.Signature })
        ConstructorSignatures = @($selected | Where-Object { $_.Name -ceq $ClassName } | ForEach-Object { $_.Signature })
        SelectedSignatures = @($selected | ForEach-Object { $_.Signature })
    }
}

function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Report, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees/[0-9TZ]+-[a-f0-9]+$') {
        throw 'Unexpected publication directory.'
    }
    return @(
        @{ path = ($Directory + '/' + $ReportName); mode = '100644'; type = 'blob'; content = $Report },
        @{ path = ($Directory + '/MANIFEST.json'); mode = '100644'; type = 'blob'; content = $Manifest }
    )
}

function Invoke-ProvenanceSelfTest {
    $valid = @{
        AssemblySha = $ExpectedAssemblySha256
        DunGenSha = $ExpectedDunGenSha256
        ExeSha = $ExpectedExeSha256
        ManifestSha = $ExpectedAppManifestSha256
        AppId = $SteamAppId
        BuildId = $ExpectedSteamBuildId
    }

    foreach ($approved in $ReviewedAppManifestSha256) {
        $valid.ManifestSha = $approved
        Assert-InstalledGameProvenance @valid
    }

    foreach ($key in @('AssemblySha', 'DunGenSha', 'ExeSha', 'ManifestSha', 'AppId', 'BuildId')) {
        $bad = $valid.Clone()
        $bad[$key] = 'unreviewed'
        $failed = $false
        try { Assert-InstalledGameProvenance @bad } catch { $failed = $true }
        if (-not $failed) { throw ('Provenance rejection failed for ' + $key) }
    }
}

function Invoke-ExtractorSelfTest {
    $fixtures = @(
        [pscustomobject]@{
            ClassName = 'DungeonFlow'; RootName = 'GetLineAtDepth'; Signal = '\bLines\b'; IncludeConstructors = $false
            Source = @'
public class DungeonFlow
{
    public object[] Lines;
    public object GetLineAtDepth(float depth) { return PickLine(depth, Lines); }
    private object PickLine(float depth, object[] lines) { return null; }
    private void Unrelated() { }
}
'@
            Required = @('GetLineAtDepth','PickLine')
        },
        [pscustomobject]@{
            ClassName = 'GraphLine'; RootName = 'GetRandomArchetype'; Signal = '\bArchetype'; IncludeConstructors = $false
            Source = @'
public class GraphLine
{
    public object[] Archetypes;
    public object GetRandomArchetype(object random, object previous) { return PickArchetype(Archetypes); }
    private object PickArchetype(object[] values) { return null; }
}
'@
            Required = @('GetRandomArchetype','PickArchetype')
        },
        [pscustomobject]@{
            ClassName = 'InjectedTile'; RootName = 'ShouldInjectTileAtPoint'; Signal = '[Dd]epth'; IncludeConstructors = $true
            Source = @'
public class InjectedTile
{
    private float minDepth;
    public InjectedTile(object rule, bool main, object random) { minDepth = BuildDepth(rule); }
    public bool ShouldInjectTileAtPoint(bool main, float pathDepth, float branchDepth) { return CheckDepth(main ? pathDepth : branchDepth); }
    private float BuildDepth(object rule) { return 0f; }
    private bool CheckDepth(float depth) { return depth >= minDepth; }
}
'@
            Required = @('InjectedTile','ShouldInjectTileAtPoint','BuildDepth','CheckDepth')
        },
        [pscustomobject]@{
            ClassName = 'BranchCountHelper'; RootName = 'ComputeBranchCounts'; Signal = '\bBranch'; IncludeConstructors = $false
            Source = @'
public class BranchCountHelper
{
    public static void ComputeBranchCounts(object flow, object random, object dungeon, ref int[] branches) { FillBranches(branches); }
    private static void FillBranches(int[] branches) { }
}
'@
            Required = @('ComputeBranchCounts','FillBranches')
        },
        [pscustomobject]@{
            ClassName = 'DoorwayPairFinder'; RootName = 'GetDoorwayPairs'; Signal = '\bDoorway|\bTileWeights|\bWeight'; IncludeConstructors = $false
            Source = @'
public class DoorwayPairFinder
{
    public object TileWeights;
    public object GetDoorwayPairs(int? maxCount) { return BuildDoorwayPairs(TileWeights); }
    private object BuildDoorwayPairs(object weights) { return null; }
}
'@
            Required = @('GetDoorwayPairs','BuildDoorwayPairs')
        }
    )

    foreach ($fixture in $fixtures) {
        $selection = Get-FocusedTypeSelection -Source $fixture.Source -ClassName $fixture.ClassName -RootName $fixture.RootName -SignalPattern $fixture.Signal -IncludeConstructors:$fixture.IncludeConstructors
        $names = @($selection.Methods | ForEach-Object { $_.Name })
        foreach ($requiredName in $fixture.Required) {
            if ($names -notcontains $requiredName) {
                throw ($fixture.ClassName + ' focused self-test missed ' + $requiredName)
            }
        }
        if ($names -contains 'Unrelated') { throw ($fixture.ClassName + ' selected unrelated method.') }
    }

    $failed = $false
    try {
        Get-FocusedTypeSelection -Source $fixtures[0].Source -ClassName 'DungeonFlow' -RootName 'MissingMethod' -SignalPattern '\bLines\b' | Out-Null
    } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-root rejection self-test failed.' }

    $failed = $false
    try {
        Get-FocusedTypeSelection -Source ($fixtures[1].Source -replace 'Archetypes', 'Choices') -ClassName 'GraphLine' -RootName 'GetRandomArchetype' -SignalPattern '\bArchetype' | Out-Null
    } catch { $failed = $true }
    if (-not $failed) { throw 'Missing-signal rejection self-test failed.' }

    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees/20260922T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs)$' }).Count -ne 0) {
        throw 'Publication allowlist self-test failed.'
    }
}

function Invoke-BootstrapSelfTest {
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-callees-bootstrap-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $temp -Force | Out-Null
    try {
        $tool = Ensure-DotNetAndIlSpy -TempRoot $temp -ForceIsolatedSdk
        $version = Invoke-CheckedNativeProcess -FilePath $tool.DotNet -Arguments @($tool.IlSpyDll, '--version') -Label 'ILSpy version'
        if ($version -notmatch ('(?m)^ilspycmd: ' + [regex]::Escape($IlSpyVersion) + '\s*$')) {
            throw 'Installed ILSpy did not report the pinned version.'
        }
    }
    finally {
        Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function Resolve-GitHubCli {
    $command = Get-Command gh -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }

    $programFilesX86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    $paths = @(
        (Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe'),
        (Join-Path $env:LOCALAPPDATA 'Programs\GitHub CLI\gh.exe')
    )
    if ($programFilesX86) { $paths += (Join-Path $programFilesX86 'GitHub CLI\gh.exe') }

    foreach ($path in $paths) {
        if ($path -and (Test-Path -LiteralPath $path)) { return $path }
    }

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw 'GitHub CLI is missing and winget is unavailable.'
    }
    & winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI installation failed.' }

    foreach ($path in $paths) {
        if ($path -and (Test-Path -LiteralPath $path)) { return $path }
    }
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
    $result = Invoke-CheckedNativeProcess -FilePath $script:GhPath -Arguments $arguments -Label ('GitHub API ' + $Method + ' ' + $Endpoint)
    return ($result | ConvertFrom-Json)
}




if ($SelfTest -and $BootstrapSelfTest) { throw 'Select only one self-test mode.' }
if ($SelfTest) {
    Invoke-ProvenanceSelfTest
    Invoke-ExtractorSelfTest
    Write-Host 'PASS: provenance, focused cross-type callee extractor and publication self-tests.'
    return
}
if ($BootstrapSelfTest) {
    Invoke-BootstrapSelfTest
    Write-Host 'PASS: isolated .NET/ILSpy bootstrap.'
    return
}

$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-callees-v81-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $script:CaptureTempRoot -Force | Out-Null

try {
    Write-Step 'Locating and verifying installed V81 and exact DunGen.dll.'
    $assemblyPath = Resolve-AssemblyPath
    $managedDir = Split-Path -Parent $assemblyPath
    $dunGenPath = Join-Path $managedDir 'DunGen.dll'
    if (-not (Test-Path -LiteralPath $dunGenPath -PathType Leaf)) {
        throw 'Installed DunGen.dll is missing from the exact game Managed directory.'
    }

    $gameRoot = Split-Path -Parent (Split-Path -Parent $managedDir)
    $exePath = Join-Path $gameRoot 'Lethal Company.exe'
    $steamApps = Split-Path -Parent (Split-Path -Parent $gameRoot)
    $appManifest = Join-Path $steamApps ('appmanifest_' + $SteamAppId + '.acf')
    foreach ($path in @($exePath, $appManifest)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw 'Required game provenance file is missing.' }
    }

    $assemblySha = Get-Sha256Lower $assemblyPath
    $dunGenSha = Get-Sha256Lower $dunGenPath
    $exeSha = Get-Sha256Lower $exePath
    $manifestSha = Get-Sha256Lower $appManifest
    $steamIdentity = Get-SteamBuildIdentity -Text (Get-Content -LiteralPath $appManifest -Raw)
    Assert-InstalledGameProvenance -AssemblySha $assemblySha -DunGenSha $dunGenSha -ExeSha $exeSha -ManifestSha $manifestSha -AppId $steamIdentity.AppId -BuildId $steamIdentity.BuildId

    $script:GhPath = Resolve-GitHubCli
    & $script:GhPath auth status --hostname github.com *> $null
    if ($LASTEXITCODE -ne 0) {
        & $script:GhPath auth login --hostname github.com --git-protocol https --web
        if ($LASTEXITCODE -ne 0) { throw 'GitHub authentication failed.' }
    }

    $pullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($pullRequest.state -cne 'open' -or
        $pullRequest.merged -eq $true -or
        $pullRequest.head.ref -cne $PullRequestBranch -or
        $pullRequest.head.repo.full_name -cne $RepositoryName -or
        $pullRequest.base.ref -cne $ExpectedBaseBranch -or
        $pullRequest.base.sha -cne $ExpectedRepositoryMain) {
        throw 'PR #138 is not the expected exact-base open in-repository evidence PR.'
    }

    $repositoryPrHead = $pullRequest.head.sha
    $prHeadCommit = Invoke-RepoApi ('git/commits/' + $repositoryPrHead)
    $repositoryMain = (Invoke-RepoApi 'git/ref/heads/main').object.sha
    if ($repositoryMain -cne $ExpectedRepositoryMain) {
        throw ('Repository main drifted from reviewed base: ' + $repositoryMain)
    }

    $priorFile = Invoke-RepoApi ('contents/' + $PriorManifest + '?ref=' + $repositoryPrHead)
    $priorText = $Utf8.GetString([Convert]::FromBase64String($priorFile.content))
    $prior = $priorText | ConvertFrom-Json
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or
        $prior.dungen_assembly.sha256 -ne $ExpectedDunGenSha256 -or
        $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or
        $prior.steam.buildid -ne $ExpectedSteamBuildId -or
        $prior.steam.app_id -ne $SteamAppId -or
        $prior.report.sha256 -ne $ExpectedC3F14ReportSha256) {
        throw 'C3F14 parent capture manifest disagrees with the pinned installed-game/DunGen/report contract.'
    }

    $ledgerFile = Invoke-RepoApi ('contents/' + $C3F14Ledger + '?ref=' + $repositoryPrHead)
    $ledgerText = $Utf8.GetString([Convert]::FromBase64String($ledgerFile.content))
    $ledger = $ledgerText | ConvertFrom-Json
    if ($ledger.schema_version -cne 'c3f14-generation-capacity-implementation-synthesis-1' -or
        $ledger.aggregate.proof_set_flows -ne 20 -or
        $ledger.aggregate.generated_eligible_positive_three_lower_bound_proven -ne 0) {
        throw 'C3F14 synthesis ledger does not match the reviewed proof boundary.'
    }

    $actualRoots = @($ledger.remaining_cross_type_callees)
    if ($actualRoots.Count -ne $ExpectedRootMethods.Count) { throw 'C3F14 remaining-callee count mismatch.' }
    for ($i = 0; $i -lt $ExpectedRootMethods.Count; $i++) {
        if ($actualRoots[$i] -cne $ExpectedRootMethods[$i]) {
            throw ('C3F14 remaining-callee mismatch at index ' + $i + ': ' + $actualRoots[$i])
        }
    }

    $ilspy = Ensure-DotNetAndIlSpy -TempRoot $script:CaptureTempRoot

    $specs = @(
        [pscustomobject]@{ Type = 'DunGen.DungeonFlow'; Class = 'DungeonFlow'; Root = 'GetLineAtDepth'; Signal = '\bLines\b'; Constructors = $false; MaxLines = 500 },
        [pscustomobject]@{ Type = 'DunGen.GraphLine'; Class = 'GraphLine'; Root = 'GetRandomArchetype'; Signal = '\bArchetype'; Constructors = $false; MaxLines = 700 },
        [pscustomobject]@{ Type = 'DunGen.InjectedTile'; Class = 'InjectedTile'; Root = 'ShouldInjectTileAtPoint'; Signal = '[Dd]epth'; Constructors = $true; MaxLines = 900 },
        [pscustomobject]@{ Type = 'DunGen.BranchCountHelper'; Class = 'BranchCountHelper'; Root = 'ComputeBranchCounts'; Signal = '\bBranch'; Constructors = $false; MaxLines = 900 },
        [pscustomobject]@{ Type = 'DunGen.DoorwayPairFinder'; Class = 'DoorwayPairFinder'; Root = 'GetDoorwayPairs'; Signal = '\bDoorway|\bTileWeights|\bWeight'; Constructors = $false; MaxLines = 1800 }
    )

    $captures = @()
    foreach ($spec in $specs) {
        Write-Step ('Decompiling exact installed ' + $spec.Type + ' locally.')
        $source = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
            $ilspy.IlSpyDll, '-t', $spec.Type, '-r', $managedDir, $dunGenPath
        ) -Label ($spec.Type + ' decompile')
        if ([string]::IsNullOrWhiteSpace($source)) { throw ($spec.Type + ' decompiler output is empty.') }

        $selection = Get-FocusedTypeSelection -Source $source -ClassName $spec.Class -RootName $spec.Root -SignalPattern $spec.Signal -IncludeConstructors:$spec.Constructors -MaxLines $spec.MaxLines
        $captures += [pscustomobject]@{
            Type = $spec.Type
            Class = $spec.Class
            Root = $spec.Root
            FullSourceSha256 = Get-TextSha256 $source
            Selection = $selection
        }
    }

    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 DunGen generation-capacity cross-type callee evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Installed DunGen.dll SHA-256: ' + $dunGenSha)
    [void]$builder.AppendLine('Steam buildid: ' + $steamIdentity.BuildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Repository PR #138 head at capture: ' + $repositoryPrHead)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion)
    [void]$builder.AppendLine('Scope: only the five C3F14 unresolved cross-type roots, plus directly called same-type helpers; InjectedTile additionally includes its constructor(s) and their direct same-type helpers.')
    [void]$builder.AppendLine('Explicit exclusions: previously captured DungeonGenerator cluster, TilePlacementData.NormalizedDepth, Doorway.ProcessDoorwayObjects, DungeonGenerator.ProcessGlobalProps, GameObjectChanceTable.GetRandom, RoundManager.SpawnSyncedProps, binaries and full type decompiles.')

    foreach ($capture in $captures) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('## ' + $capture.Type + '.' + $capture.Root)
        foreach ($method in $capture.Selection.Methods) {
            [void]$builder.AppendLine('')
            [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
            [void]$builder.AppendLine($method.Text)
        }
    }

    $report = $builder.ToString()
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix

    $metadataTypes = @()
    foreach ($capture in $captures) {
        $metadataTypes += [ordered]@{
            type = $capture.Type
            full_local_type_source_sha256 = $capture.FullSourceSha256
            root_method = $capture.Root
            root_signatures = @($capture.Selection.RootSignatures)
            constructor_signatures = @($capture.Selection.ConstructorSignatures)
            selected_signatures = @($capture.Selection.SelectedSignatures)
            same_type_neighbor_depth = 1
        }
    }

    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Exact installed-V81 DunGen cross-type callees remaining after Universal Interior Viability C3F14'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        pull_request = $PullRequestNumber
        pull_request_branch = $PullRequestBranch
        repository_pr_head_at_capture = $repositoryPrHead
        repository_main_at_capture = $repositoryMain
        expected_repository_main = $ExpectedRepositoryMain
        bound_c3f14_parent_manifest = @{
            path = $PriorManifest
            git_blob_sha = $priorFile.sha
            text_sha256 = (Get-TextSha256 $priorText)
            report_sha256 = $prior.report.sha256
        }
        bound_c3f14_synthesis = @{
            path = $C3F14Ledger
            git_blob_sha = $ledgerFile.sha
            text_sha256 = (Get-TextSha256 $ledgerText)
            schema_version = $ledger.schema_version
            proof_set_flows = $ledger.aggregate.proof_set_flows
            remaining_cross_type_callees = @($actualRoots)
        }
        source_assembly = @{ logical_path = 'Lethal Company_Data/Managed/Assembly-CSharp.dll'; sha256 = $assemblySha }
        dungen_assembly = @{ logical_path = 'Lethal Company_Data/Managed/DunGen.dll'; sha256 = $dunGenSha }
        game_executable = @{ logical_path = 'Lethal Company.exe'; sha256 = $exeSha }
        steam = @{
            app_id = $steamIdentity.AppId
            buildid = $steamIdentity.BuildId
            appmanifest_sha256 = $manifestSha
            prior_appmanifest_sha256 = $ExpectedAppManifestSha256
            matches_prior_appmanifest = ($manifestSha -eq $ExpectedAppManifestSha256)
            manifest_review = $ManifestReview
        }
        decompiler = @{ tool = 'ilspycmd'; version = $IlSpyVersion; types = @($metadataTypes) }
        selection = @{
            exact_root_methods = @($ExpectedRootMethods)
            same_type_direct_callees_only = $true
            injected_tile_constructors_included = $true
            forbidden_recaptures = @(
                'DungeonGenerator generation cluster',
                'TilePlacementData.NormalizedDepth',
                'Doorway.ProcessDoorwayObjects',
                'DungeonGenerator.ProcessGlobalProps',
                'GameObjectChanceTable.GetRandom',
                'RoundManager.SpawnSyncedProps'
            )
        }
        report = @{
            file = $ReportName
            sha256 = (Get-TextSha256 $report)
            excludes = @('game binaries','DunGen.dll','full type decompiles','unrelated methods','absolute local paths','user names')
        }
    }

    $metadataJson = ($metadata | ConvertTo-Json -Depth 20) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)

    Write-Step 'Publishing focused cross-type callee evidence to PR #138.'
    $currentPullRequest = Invoke-RepoApi ('pulls/' + $PullRequestNumber)
    if ($currentPullRequest.state -cne 'open' -or
        $currentPullRequest.merged -eq $true -or
        $currentPullRequest.head.ref -cne $PullRequestBranch -or
        $currentPullRequest.head.sha -cne $repositoryPrHead -or
        $currentPullRequest.base.ref -cne $ExpectedBaseBranch -or
        $currentPullRequest.base.sha -cne $ExpectedRepositoryMain) {
        throw 'PR #138 changed during capture. Refusing stale write.'
    }
    if ((Invoke-RepoApi 'git/ref/heads/main').object.sha -cne $ExpectedRepositoryMain) {
        throw 'Repository main changed during capture. Refusing stale write.'
    }

    $treeResult = Invoke-RepoApi -Endpoint 'git/trees' -Method 'POST' -Body @{
        base_tree = $prHeadCommit.tree.sha
        tree = $entries
    }
    $commitResult = Invoke-RepoApi -Endpoint 'git/commits' -Method 'POST' -Body @{
        message = ('Capture exact V81 DunGen cross-type generation-capacity evidence ' + $stamp)
        tree = $treeResult.sha
        parents = @($repositoryPrHead)
    }
    $refResult = Invoke-RepoApi -Endpoint ('git/refs/heads/' + $PullRequestBranch) -Method 'PATCH' -Body @{
        sha = $commitResult.sha
        force = $false
    }
    if ($refResult.object.sha -ne $commitResult.sha) { throw 'Updated PR branch response did not match evidence commit.' }

    Write-Host ''
    Write-Host 'SUCCESS' -ForegroundColor Green
    Write-Host ('Evidence commit: ' + $commitResult.sha)
    Write-Host ('Report: https://github.com/' + $RepositoryName + '/blob/' + $commitResult.sha + '/' + $directory + '/' + $ReportName)
    Write-Host 'Only the focused report and manifest were uploaded. No local clone, game/DunGen binary or gameplay run was uploaded.'
}
finally {
    if (Test-Path -LiteralPath $script:CaptureTempRoot) {
        Remove-Item -LiteralPath $script:CaptureTempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
