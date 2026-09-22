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
$EvidenceRoot = 'SourceEvidence/VanillaV81/DunGenGenerationCapacity'
$ReportName = 'DUNGEN_GENERATION_CAPACITY_FOCUSED_DECOMPILE.txt'

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
$PriorManifest = 'SourceEvidence/VanillaV81/DunGenChanceSpawnSynced/20260922T185024Z-e0d76674/MANIFEST.json'
$DungeonGeneratorType = 'DunGen.DungeonGenerator'
$TileType = 'DunGen.Tile'
$DoorwayType = 'DunGen.Doorway'
$C3F13Ledger = 'SourceEvidence/UniversalInteriorViability/PhaseC3F13/GENERATED_CAPACITY_FEASIBILITY_LEDGER.json'
$ForbiddenMethodNames = @('ProcessGlobalProps')
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

function Get-DungeonGeneratorSelection {
    param([Parameter(Mandatory = $true)][string]$Source, [int]$MaxLines = 3600)

    $methods = @(Get-ParsedMethods -Source $Source -ClassName 'DungeonGenerator')
    $signalGroups = @(
        [pscustomobject]@{ Name = 'flow_graph'; Pattern = '\bDungeonFlow\s*\.\s*(?:Length|Lines|Nodes)\b' },
        [pscustomobject]@{ Name = 'archetype_tileset'; Pattern = '\bDungeonArchetype[A-Za-z0-9_]*\b|\bTileSet[A-Za-z0-9_]*\b' },
        [pscustomobject]@{ Name = 'tile_weights'; Pattern = '\bTileWeights\b' },
        [pscustomobject]@{ Name = 'required_injection'; Pattern = '\bTileInjectionRules\b|\bIsRequired\b' },
        [pscustomobject]@{ Name = 'branch_cap'; Pattern = '\bBranch[A-Za-z0-9_]*\b|\bCap[A-Za-z0-9_]*\b' }
    )

    $roots = @()
    $coverage = @()
    foreach ($group in $signalGroups) {
        $matches = @($methods | Where-Object {
            ($ForbiddenMethodNames -notcontains $_.Name) -and
            (($_.Name + [Environment]::NewLine + $_.Body) -match $group.Pattern)
        })
        if ($matches.Count -eq 0) {
            throw ('DungeonGenerator signal group absent: ' + $group.Name + ' / ' + $group.Pattern)
        }
        $roots += $matches
        $coverage += [pscustomobject]@{
            Name = $group.Name
            Pattern = $group.Pattern
            Methods = @($matches | ForEach-Object { $_.Name } | Sort-Object -Unique)
        }
    }

    $roots = @($roots | Sort-Object Index -Unique)
    $selected = @(Add-OneHopNeighbors -Methods $methods -Roots $roots | Where-Object {
        $ForbiddenMethodNames -notcontains $_.Name
    })
    Assert-MethodSelection -Methods $selected -Label 'DungeonGenerator' -MaxLines $MaxLines

    if (@($selected | Where-Object {
        (($_.Name + [Environment]::NewLine + $_.Body) -match '\bRepeat[A-Za-z0-9_]*\b|\bReuse[A-Za-z0-9_]*\b|\bTileWeights\b')
    }).Count -eq 0) {
        throw 'DungeonGenerator focused neighborhood does not expose tile-weight/repeat/reuse semantics.'
    }

    return [pscustomobject]@{
        Methods = $selected
        Coverage = $coverage
        RootSignatures = @($roots | ForEach-Object { $_.Signature })
    }
}

function Get-SignalMemberLines {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$SignalPattern,
        [int]$MaxLines = 40
    )
    $sourceLines = @($Source -split '\r?\n')
    $maskLines = @((Get-CodeMask $Source) -split '\r?\n')
    if ($sourceLines.Count -ne $maskLines.Count) { throw 'Signal-member mask line count mismatch.' }
    $signalMembers = @()
    for ($i = 0; $i -lt $maskLines.Count; $i++) {
        if ($maskLines[$i] -match $SignalPattern -and $maskLines[$i] -notmatch '\(') {
            $signalMembers += [pscustomobject]@{ Line = $i + 1; Text = $sourceLines[$i].TrimEnd() }
        }
    }
    if ($signalMembers.Count -gt $MaxLines) { throw 'Signal-member extraction exceeded its line limit.' }
    return $signalMembers
}

function Resolve-PlacementTypeName {
    param([Parameter(Mandatory = $true)][string]$TileSource)

    $mask = Get-CodeMask $TileSource
    $matches = [regex]::Matches(
        $mask,
        '(?m)^[\t ]*(?:public|private|protected|internal)\s+(?<type>(?:global::)?[A-Za-z_][A-Za-z0-9_.]*)\s+Placement\b'
    )
    $types = @($matches | ForEach-Object {
        $_.Groups['type'].Value -replace '^global::', ''
    } | Sort-Object -Unique)
    if ($types.Count -ne 1) {
        throw ('Expected exactly one Tile.Placement declaration type, found ' + $types.Count + '.')
    }
    $type = $types[0]
    if ($type -notmatch '\.') { $type = 'DunGen.' + $type }
    return $type
}

function Get-NamedMemberBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$MemberName,
        [int]$MaxLines = 120
    )

    $mask = Get-CodeMask $Source
    $pattern = '(?m)^[\t ]*(?:public|private|protected|internal)\s+[^\r\n]*\b' + [regex]::Escape($MemberName) + '\b[^\r\n]*'
    $matches = [regex]::Matches($mask, $pattern)
    if ($matches.Count -ne 1) {
        throw ('Expected exactly one declaration for ' + $MemberName + ', found ' + $matches.Count + '.')
    }

    $decl = $matches[0]
    $lineStart = $decl.Index
    $lineEnd = $mask.IndexOf([char]10, $lineStart)
    if ($lineEnd -lt 0) { $lineEnd = $mask.Length }
    $lineMask = $mask.Substring($lineStart, $lineEnd - $lineStart)
    if ($lineMask -match '=>.*;' -or ($lineMask -match ';\s*$' -and $lineMask -notmatch '\{')) {
        $text = $Source.Substring($lineStart, $lineEnd - $lineStart).TrimEnd()
        return [pscustomobject]@{
            Text = $text
            SourceLine = ([regex]::Matches($Source.Substring(0, $lineStart), '\n')).Count + 1
        }
    }

    $open = $mask.IndexOf('{', $decl.Index)
    if ($open -lt 0) { throw ($MemberName + ' declaration has no supported body.') }

    $depth = 1
    $pos = $open + 1
    while ($pos -lt $mask.Length -and $depth -gt 0) {
        if ($mask[$pos] -eq '{') { $depth++ }
        elseif ($mask[$pos] -eq '}') { $depth-- }
        $pos++
    }
    if ($depth -ne 0) { throw ($MemberName + ' member body did not close.') }

    $text = $Source.Substring($lineStart, $pos - $lineStart)
    $lineCount = @($text -split '\r?\n').Count
    if ($lineCount -gt $MaxLines) { throw ($MemberName + ' member block exceeded ' + $MaxLines + ' lines.') }
    return [pscustomobject]@{
        Text = $text
        SourceLine = ([regex]::Matches($Source.Substring(0, $lineStart), '\n')).Count + 1
    }
}

function Get-DoorwaySelection {
    param([Parameter(Mandatory = $true)][string]$Source, [int]$MaxLines = 800)

    $methods = @(Get-ParsedMethods -Source $Source -ClassName 'Doorway')
    $roots = @($methods | Where-Object {
        ($ForbiddenMethodNames -notcontains $_.Name) -and
        (($_.Name + [Environment]::NewLine + $_.Body) -match '\bBlockerPrefabWeights\b')
    })
    if ($roots.Count -eq 0) { throw 'No DunGen.Doorway method consumes BlockerPrefabWeights.' }

    $selected = @(Add-OneHopNeighbors -Methods $methods -Roots $roots | Where-Object {
        $ForbiddenMethodNames -notcontains $_.Name
    })
    Assert-MethodSelection -Methods $selected -Label 'Doorway' -MaxLines $MaxLines

    if (@($selected | Where-Object {
        $_.Body -match '\bInstantiate\b|\bSetActive\b|\bSetDoorwayBlocked\b|\bSpawn\b'
    }).Count -eq 0) {
        throw 'Doorway BlockerPrefabWeights neighborhood does not expose blocker materialization/activation semantics.'
    }
    return $selected
}

function New-EvidenceTreeEntries {
    param([string]$Directory, [string]$Report, [string]$Manifest)
    if ($Directory -notmatch '^SourceEvidence/VanillaV81/DunGenGenerationCapacity/[0-9TZ]+-[a-f0-9]+$') {
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
    $generatorFixture = @'
public class DungeonGenerator
{
    public object DungeonFlow;

    private void BuildMainPath()
    {
        var length = DungeonFlow.Length;
        var lines = DungeonFlow.Lines;
        var nodes = DungeonFlow.Nodes;
        DungeonArchetype archetype = PickArchetype();
        TileSet set = archetype.TileSets[0];
        PickTile(set);
    }

    private void PickTile(TileSet set)
    {
        var choices = set.TileWeights;
        if (AllowTileRepeat) { choices = set.TileWeights; }
    }

    private void InjectRequired()
    {
        foreach (var rule in TileInjectionRules)
        {
            if (rule.IsRequired) { PlaceTile(); }
        }
    }

    private void GenerateBranch()
    {
        PlaceCap();
    }

    private void PlaceCap()
    {
        var cap = CapTileSet.TileWeights;
    }

    public void Generate()
    {
        BuildMainPath();
        InjectRequired();
        GenerateBranch();
    }

    private void ProcessGlobalProps()
    {
        var ignored = DungeonFlow.Length;
    }

    private DungeonArchetype PickArchetype() { return null; }
    private void PlaceTile() { }
}
'@
    $selection = Get-DungeonGeneratorSelection -Source $generatorFixture
    $names = @($selection.Methods | ForEach-Object { $_.Name })
    foreach ($requiredName in @('BuildMainPath','PickTile','InjectRequired','GenerateBranch','PlaceCap','Generate')) {
        if ($names -notcontains $requiredName) { throw ('DungeonGenerator self-test missed ' + $requiredName) }
    }
    if ($names -contains 'ProcessGlobalProps') { throw 'Forbidden ProcessGlobalProps was selected.' }
    if ($selection.Coverage.Count -ne 5) { throw 'DungeonGenerator signal coverage count mismatch.' }

    $tileFixture = @'
public class Tile
{
    public TilePlacementData Placement;
    public object Other;
}
'@
    $placementType = Resolve-PlacementTypeName -TileSource $tileFixture
    if ($placementType -cne 'DunGen.TilePlacementData') { throw 'Tile.Placement type resolution failed.' }
    $tileLines = @(Get-SignalMemberLines -Source $tileFixture -SignalPattern '\bPlacement\b')
    if ($tileLines.Count -ne 1) { throw 'Tile.Placement declaration extraction failed.' }

    $placementFixture = @'
public class TilePlacementData
{
    public bool IsOnMainPath;
    public float PathDepth;
    public float BranchDepth;

    public float NormalizedDepth
    {
        get
        {
            return IsOnMainPath ? PathDepth : BranchDepth;
        }
    }
}
'@
    $normalized = Get-NamedMemberBlock -Source $placementFixture -MemberName 'NormalizedDepth'
    if ($normalized.Text -notmatch 'PathDepth' -or $normalized.Text -notmatch 'BranchDepth') {
        throw 'NormalizedDepth member extraction failed.'
    }

    $doorwayFixture = @'
public class Doorway
{
    private object SelectBlocker()
    {
        var prefab = BlockerPrefabWeights.GetRandom();
        return Materialize(prefab);
    }

    private object Materialize(object prefab)
    {
        return Instantiate(prefab);
    }

    public void Refresh()
    {
        SelectBlocker();
    }
}
'@
    $doorway = @(Get-DoorwaySelection -Source $doorwayFixture)
    $doorNames = @($doorway | ForEach-Object { $_.Name })
    if ($doorNames -notcontains 'SelectBlocker' -or $doorNames -notcontains 'Materialize' -or $doorNames -notcontains 'Refresh') {
        throw 'Doorway root/caller/callee extraction self-test failed.'
    }

    $failed = $false
    try { Get-DungeonGeneratorSelection -Source ($generatorFixture -replace 'TileInjectionRules', 'OtherRules' -replace 'IsRequired', 'Optional') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing injection signal group was not rejected.' }

    $failed = $false
    try { Get-DoorwaySelection -Source ($doorwayFixture -replace 'BlockerPrefabWeights', 'OtherWeights') | Out-Null } catch { $failed = $true }
    if (-not $failed) { throw 'Missing Doorway BlockerPrefabWeights signal was not rejected.' }

    $entries = @(New-EvidenceTreeEntries -Directory 'SourceEvidence/VanillaV81/DunGenGenerationCapacity/20260922T000000Z-abcdef12' -Report 'report' -Manifest '{}')
    if ($entries.Count -ne 2 -or @($entries | Where-Object { $_.path -match '\.(dll|exe|zip|r2z|cs)$' }).Count -ne 0) {
        throw 'Publication allowlist self-test failed.'
    }
}
function Invoke-BootstrapSelfTest {
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-bootstrap-' + [guid]::NewGuid().ToString('N'))
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
    Write-Host 'PASS: provenance, focused generation-capacity extractor and publication self-tests.'
    return
}
if ($BootstrapSelfTest) {
    Invoke-BootstrapSelfTest
    Write-Host 'PASS: isolated .NET/ILSpy bootstrap.'
    return
}

$script:CaptureTempRoot = Join-Path ([IO.Path]::GetTempPath()) ('lc-dungen-generation-capacity-v81-' + [guid]::NewGuid().ToString('N'))
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
    $prior = $Utf8.GetString([Convert]::FromBase64String($priorFile.content)) | ConvertFrom-Json
    if ($prior.source_assembly.sha256 -ne $ExpectedAssemblySha256 -or
        $prior.dungen_assembly.sha256 -ne $ExpectedDunGenSha256 -or
        $prior.game_executable.sha256 -ne $ExpectedExeSha256 -or
        $prior.steam.buildid -ne $ExpectedSteamBuildId -or
        $prior.steam.app_id -ne $SteamAppId) {
        throw 'C3F12 manifest disagrees with the pinned installed-game/DunGen contract.'
    }

    $ledgerFile = Invoke-RepoApi ('contents/' + $C3F13Ledger + '?ref=' + $repositoryPrHead)
    $ledgerText = $Utf8.GetString([Convert]::FromBase64String($ledgerFile.content))
    $ledger = $ledgerText | ConvertFrom-Json
    if ($ledger.schema_version -cne 'c3f13-generated-capacity-feasibility-ledger-1' -or
        $ledger.aggregate.proof_set_flows -ne 20 -or
        $ledger.aggregate.direct_tile_descendant_flows -ne 17 -or
        $ledger.aggregate.indirect_doorway_blocker_flows -ne 3) {
        throw 'C3F13 capacity ledger does not match the reviewed 20-flow proof boundary.'
    }

    $ilspy = Ensure-DotNetAndIlSpy -TempRoot $script:CaptureTempRoot

    Write-Step 'Decompiling exact installed DunGen.DungeonGenerator locally.'
    $generatorSource = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', $DungeonGeneratorType, '-r', $managedDir, $dunGenPath
    ) -Label 'DunGen.DungeonGenerator decompile'
    if ([string]::IsNullOrWhiteSpace($generatorSource)) { throw 'DungeonGenerator decompiler output is empty.' }
    $generatorSelection = Get-DungeonGeneratorSelection -Source $generatorSource
    $generatorMethods = @($generatorSelection.Methods)

    Write-Step 'Resolving Tile.Placement and exact NormalizedDepth implementation.'
    $tileSource = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', $TileType, '-r', $managedDir, $dunGenPath
    ) -Label 'DunGen.Tile decompile'
    if ([string]::IsNullOrWhiteSpace($tileSource)) { throw 'Tile decompiler output is empty.' }
    $placementLines = @(Get-SignalMemberLines -Source $tileSource -SignalPattern '\bPlacement\b')
    if ($placementLines.Count -eq 0) { throw 'DunGen.Tile does not expose a Placement declaration.' }
    $placementType = Resolve-PlacementTypeName -TileSource $tileSource

    $placementSource = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', $placementType, '-r', $managedDir, $dunGenPath
    ) -Label ($placementType + ' decompile')
    if ([string]::IsNullOrWhiteSpace($placementSource)) { throw 'Placement-type decompiler output is empty.' }
    $normalizedDepth = Get-NamedMemberBlock -Source $placementSource -MemberName 'NormalizedDepth'

    Write-Step 'Decompiling exact installed DunGen.Doorway blocker-selection surface locally.'
    $doorwaySource = Invoke-CheckedNativeProcess -FilePath $ilspy.DotNet -Arguments @(
        $ilspy.IlSpyDll, '-t', $DoorwayType, '-r', $managedDir, $dunGenPath
    ) -Label 'DunGen.Doorway decompile'
    if ([string]::IsNullOrWhiteSpace($doorwaySource)) { throw 'Doorway decompiler output is empty.' }
    $doorwayMethods = @(Get-DoorwaySelection -Source $doorwaySource)

    $builder = New-Object Text.StringBuilder
    [void]$builder.AppendLine('# Installed Lethal Company V81 DunGen generation-capacity evidence')
    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('Source Assembly-CSharp SHA-256: ' + $assemblySha)
    [void]$builder.AppendLine('Installed DunGen.dll SHA-256: ' + $dunGenSha)
    [void]$builder.AppendLine('Steam buildid: ' + $steamIdentity.BuildId)
    [void]$builder.AppendLine('Repository main at capture: ' + $repositoryMain)
    [void]$builder.AppendLine('Repository PR #138 head at capture: ' + $repositoryPrHead)
    [void]$builder.AppendLine('Decompiler: ilspycmd ' + $IlSpyVersion)
    [void]$builder.AppendLine('Scope A: DungeonGenerator roots located by exact C3F13 graph/archetype/TileWeights/injection/branch-cap signals plus one-hop same-type callers/callees.')
    [void]$builder.AppendLine('Scope B: Tile.Placement declaration and the exact resolved NormalizedDepth member implementation.')
    [void]$builder.AppendLine('Scope C: Doorway BlockerPrefabWeights roots plus one-hop same-type callers/callees for the three indirect flows.')
    [void]$builder.AppendLine('Explicit exclusions: DungeonGenerator.ProcessGlobalProps, GameObjectChanceTable.GetRandom, RoundManager.SpawnSyncedProps, binaries and full type decompiles.')

    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## DunGen.DungeonGenerator focused methods')
    foreach ($method in $generatorMethods) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
        [void]$builder.AppendLine($method.Text)
    }

    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## DunGen.Tile Placement declaration')
    foreach ($member in $placementLines) {
        [void]$builder.AppendLine(('line ' + $member.Line + ': ' + $member.Text))
    }

    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## ' + $placementType + '.NormalizedDepth')
    [void]$builder.AppendLine('--- local type line ' + $normalizedDepth.SourceLine + ' ---')
    [void]$builder.AppendLine($normalizedDepth.Text)

    [void]$builder.AppendLine('')
    [void]$builder.AppendLine('## DunGen.Doorway focused blocker methods')
    foreach ($method in $doorwayMethods) {
        [void]$builder.AppendLine('')
        [void]$builder.AppendLine('--- ' + $method.Signature + ' / local type line ' + $method.SourceLine + ' ---')
        [void]$builder.AppendLine($method.Text)
    }

    $report = $builder.ToString()
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $directory = $EvidenceRoot + '/' + $stamp + '-' + $suffix

    $metadata = [ordered]@{
        schema_version = 1
        purpose = 'Exact installed-V81 DunGen generation-capacity semantics required by Universal Interior Viability C3F13'
        capture_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
        repository = $RepositoryName
        pull_request = $PullRequestNumber
        pull_request_branch = $PullRequestBranch
        repository_pr_head_at_capture = $repositoryPrHead
        repository_main_at_capture = $repositoryMain
        expected_repository_main = $ExpectedRepositoryMain
        bound_c3f12_manifest = $PriorManifest
        bound_c3f13_ledger = @{
            path = $C3F13Ledger
            git_blob_sha = $ledgerFile.sha
            text_sha256 = (Get-TextSha256 $ledgerText)
            schema_version = $ledger.schema_version
            proof_set_flows = $ledger.aggregate.proof_set_flows
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
        decompiler = @{
            tool = 'ilspycmd'
            version = $IlSpyVersion
            dungeon_generator_type = $DungeonGeneratorType
            dungeon_generator_full_local_type_source_sha256 = (Get-TextSha256 $generatorSource)
            tile_type = $TileType
            tile_full_local_type_source_sha256 = (Get-TextSha256 $tileSource)
            resolved_placement_type = $placementType
            placement_full_local_type_source_sha256 = (Get-TextSha256 $placementSource)
            doorway_type = $DoorwayType
            doorway_full_local_type_source_sha256 = (Get-TextSha256 $doorwaySource)
        }
        selection = @{
            dungeon_generator_signal_coverage = @($generatorSelection.Coverage | ForEach-Object {
                @{ name = $_.Name; pattern = $_.Pattern; methods = @($_.Methods) }
            })
            dungeon_generator_root_signatures = @($generatorSelection.RootSignatures)
            dungeon_generator_selected_signatures = @($generatorMethods | ForEach-Object { $_.Signature })
            tile_placement_declaration_lines = @($placementLines | ForEach-Object { @{ line = $_.Line; text = $_.Text } })
            normalized_depth_member_source_line = $normalizedDepth.SourceLine
            doorway_required_signal = 'BlockerPrefabWeights'
            doorway_selected_signatures = @($doorwayMethods | ForEach-Object { $_.Signature })
            forbidden_recaptures = @('DungeonGenerator.ProcessGlobalProps','GameObjectChanceTable.GetRandom','RoundManager.SpawnSyncedProps')
            same_type_neighbor_depth = 1
            max_source_lines = @{ dungeon_generator = 3600; doorway = 800; normalized_depth_member = 120 }
        }
        report = @{
            file = $ReportName
            sha256 = (Get-TextSha256 $report)
            excludes = @('game binaries','DunGen.dll','full type decompiles','unrelated methods','absolute local paths','user names')
        }
    }
    $metadataJson = ($metadata | ConvertTo-Json -Depth 16) + [Environment]::NewLine
    $entries = @(New-EvidenceTreeEntries -Directory $directory -Report $report -Manifest $metadataJson)

    Write-Step ('Publishing focused generation-capacity evidence to PR #138.')
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
        message = ('Capture exact V81 DunGen generation-capacity evidence ' + $stamp)
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
