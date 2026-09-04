$root='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles'
$repo='Tendas240/Lethal-Company-AI-Modding-Project'
$headers=@{'User-Agent'='LC-Profile-Updater';'Cache-Control'='no-cache'}
$helperRevision='2026-09-04-import-uia-v2-single-open-evidence'

function Get-GaleAutomationRoot {
    try {
        $proc=@(Get-Process -ErrorAction SilentlyContinue |
            Where-Object { $_.ProcessName -ieq 'gale' -and $_.MainWindowHandle -ne 0 } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1)
        if(!$proc.Count){return $null}
        return [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$proc[0].MainWindowHandle)
    }
    catch { return $null }
}

function Find-UiaVisibleByName {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)][string]$Name)
    $out=@()
    try {
        $condition=New-Object System.Windows.Automation.PropertyCondition -ArgumentList @(
            [System.Windows.Automation.AutomationElement]::NameProperty,$Name)
        $collection=$Root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$condition)
        for($i=0;$i-lt$collection.Count;$i++){
            try {
                $item=$collection.Item($i)
                if($item.Current.IsEnabled -and -not $item.Current.IsOffscreen){$out+=$item}
            } catch {}
        }
    } catch {}
    return $out
}

function Find-UiaVisibleByNames {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)][string[]]$Names)
    $out=@()
    foreach($name in $Names){$out+=@(Find-UiaVisibleByName -Root $Root -Name $name)}
    return $out
}

function Test-UiaPattern {
    param([Parameter(Mandatory=$true)]$Element,[Parameter(Mandatory=$true)]$Pattern)
    try {$null=$Element.GetCurrentPattern($Pattern);return $true}catch{return $false}
}

function Find-UiaVisibleByPattern {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)]$Pattern)
    $out=@()
    try {
        $collection=$Root.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
        for($i=0;$i-lt$collection.Count;$i++){
            try {
                $item=$collection.Item($i)
                if($item.Current.IsEnabled -and -not $item.Current.IsOffscreen -and (Test-UiaPattern -Element $item -Pattern $Pattern)){$out+=$item}
            } catch {}
        }
    } catch {}
    return $out
}

function Find-UiaVisibleByNameAndPattern {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)][string]$Name,[Parameter(Mandatory=$true)]$Pattern)
    return @(Find-UiaVisibleByName -Root $Root -Name $Name | Where-Object {Test-UiaPattern -Element $_ -Pattern $Pattern})
}

function Find-UiaVisibleByNamesAndPattern {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)][string[]]$Names,[Parameter(Mandatory=$true)]$Pattern)
    $out=@()
    foreach($name in $Names){$out+=@(Find-UiaVisibleByNameAndPattern -Root $Root -Name $name -Pattern $Pattern)}
    return $out
}

function Find-UiaVisibleByValue {
    param([Parameter(Mandatory=$true)]$Root,[Parameter(Mandatory=$true)][string]$Value)
    $out=@()
    foreach($item in @(Find-UiaVisibleByPattern -Root $Root -Pattern ([System.Windows.Automation.ValuePattern]::Pattern))){
        try {
            $pattern=$item.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
            if(([string]$pattern.Current.Value) -eq $Value){$out+=$item}
        } catch {}
    }
    return $out
}

function Get-UiaParent {
    param([Parameter(Mandatory=$true)]$Element)
    try {
        $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
        return $walker.GetParent($Element)
    } catch {return $null}
}

function Invoke-UiaElement {
    param([Parameter(Mandatory=$true)]$Element,[ValidateSet('default','expand','select')][string]$Action='default')
    if($Action -eq 'expand'){
        try {
            $pattern=$Element.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
            if($pattern.Current.ExpandCollapseState -ne [System.Windows.Automation.ExpandCollapseState]::Expanded){$pattern.Expand()}
            return $true
        } catch {}
    }
    if($Action -eq 'select'){
        try {$Element.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern).Select();return $true}catch{}
    }
    try {$Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke();return $true}catch{}
    return $false
}

function Test-MissingProfilesVisible {
    $rootElement=Get-GaleAutomationRoot
    if(!$rootElement){return $false}
    return (@(Find-UiaVisibleByName -Root $rootElement -Name 'Missing Profiles').Count -gt 0)
}

function Wait-MissingProfilesClosed {
    param([int]$WaitSeconds=120)
    $deadline=[DateTime]::UtcNow.AddSeconds($WaitSeconds)
    do {
        if(!(Test-MissingProfilesVisible)){return $true}
        Start-Sleep -Milliseconds 200
    } while([DateTime]::UtcNow -lt $deadline)
    return $false
}

function Try-ResolveGaleMissingProfileDialog {
    param([Parameter(Mandatory=$true)][string]$ExpectedProfileName,[int]$WaitSeconds=20)
    try {
        Add-Type -AssemblyName UIAutomationClient -ErrorAction Stop
        Add-Type -AssemblyName UIAutomationTypes -ErrorAction Stop
    } catch {return 'uia-unavailable'}

    $deadline=[DateTime]::UtcNow.AddSeconds($WaitSeconds)
    $rootElement=$null
    $missing=@()
    do {
        $rootElement=Get-GaleAutomationRoot
        if($rootElement){$missing=@(Find-UiaVisibleByName -Root $rootElement -Name 'Missing Profiles');if($missing.Count -gt 0){break}}
        Start-Sleep -Milliseconds 250
    } while([DateTime]::UtcNow -lt $deadline)

    if(!$rootElement){return 'no-window'}
    if($missing.Count -eq 0){return 'none'}

    $selectors=@(Find-UiaVisibleByNameAndPattern -Root $rootElement -Name 'Select an action' -Pattern ([System.Windows.Automation.ExpandCollapsePattern]::Pattern))
    if($selectors.Count -ne 1){
        Write-Host "UIA diagnostic: actionable missing-profile selectors = $($selectors.Count)" -ForegroundColor DarkYellow
        return 'ambiguous'
    }

    $profileHits=@(Find-UiaVisibleByName -Root $rootElement -Name $ExpectedProfileName)
    Write-Host "UIA diagnostic: exact profile-name nodes for '$ExpectedProfileName' = $($profileHits.Count)" -ForegroundColor DarkGray

    if(!(Invoke-UiaElement -Element $selectors[0] -Action expand)){return 'failed'}

    $deleteDeadline=[DateTime]::UtcNow.AddSeconds(5)
    $deleteItems=@()
    do {
        $rootElement=Get-GaleAutomationRoot
        if($rootElement){$deleteItems=@(Find-UiaVisibleByNameAndPattern -Root $rootElement -Name 'Delete' -Pattern ([System.Windows.Automation.SelectionItemPattern]::Pattern))}
        if($deleteItems.Count -eq 1){break}
        Start-Sleep -Milliseconds 100
    } while([DateTime]::UtcNow -lt $deleteDeadline)
    if($deleteItems.Count -ne 1){Write-Host "UIA diagnostic: actionable Delete items = $($deleteItems.Count)" -ForegroundColor DarkYellow;return 'failed'}
    if(!(Invoke-UiaElement -Element $deleteItems[0] -Action select)){return 'failed'}

    $submitDeadline=[DateTime]::UtcNow.AddSeconds(5)
    $submit=@()
    do {
        $rootElement=Get-GaleAutomationRoot
        if($rootElement){$submit=@(Find-UiaVisibleByNameAndPattern -Root $rootElement -Name 'Submit' -Pattern ([System.Windows.Automation.InvokePattern]::Pattern))}
        if($submit.Count -eq 1){break}
        Start-Sleep -Milliseconds 100
    } while([DateTime]::UtcNow -lt $submitDeadline)
    if($submit.Count -ne 1){Write-Host "UIA diagnostic: actionable Submit buttons = $($submit.Count)" -ForegroundColor DarkYellow;return 'failed'}
    if(!(Invoke-UiaElement -Element $submit[0])){return 'failed'}

    if(Wait-MissingProfilesClosed -WaitSeconds 8){return 'resolved'}
    return 'failed'
}

function Find-GaleImportDialogScope {
    param([Parameter(Mandatory=$true)]$Root)
    $titleNames=@('Import profile','Profil importieren')
    $advancedNames=@('Advanced options','Erweiterte Optionen')
    $importNames=@('Import','Importieren')
    foreach($title in @(Find-UiaVisibleByNames -Root $Root -Names $titleNames)){
        $node=$title
        for($depth=0;$depth-lt 14 -and $node;$depth++){
            $advanced=@(Find-UiaVisibleByNames -Root $node -Names $advancedNames)
            $buttons=@(Find-UiaVisibleByNamesAndPattern -Root $node -Names $importNames -Pattern ([System.Windows.Automation.InvokePattern]::Pattern))
            if($advanced.Count -ge 1 -and $buttons.Count -ge 1){return $node}
            $node=Get-UiaParent -Element $node
        }
    }
    return $null
}

function Try-AutomateGaleProfileImport {
    param([Parameter(Mandatory=$true)][string]$ExpectedProfileName,[int]$WaitSeconds=60)
    try {
        Add-Type -AssemblyName UIAutomationClient -ErrorAction Stop
        Add-Type -AssemblyName UIAutomationTypes -ErrorAction Stop
    } catch {return 'uia-unavailable'}

    $deadline=[DateTime]::UtcNow.AddSeconds($WaitSeconds)
    $rootElement=$null
    $scope=$null
    do {
        $rootElement=Get-GaleAutomationRoot
        if($rootElement){$scope=Find-GaleImportDialogScope -Root $rootElement;if($scope){break}}
        Start-Sleep -Milliseconds 250
    } while([DateTime]::UtcNow -lt $deadline)
    if(!$rootElement){return 'no-window'}
    if(!$scope){return 'none'}

    $nameNodes=@(Find-UiaVisibleByName -Root $scope -Name $ExpectedProfileName)
    $valueNodes=@(Find-UiaVisibleByValue -Root $scope -Value $ExpectedProfileName)
    if(($nameNodes.Count+$valueNodes.Count) -lt 1){
        Write-Host "UIA diagnostic: expected import profile identity '$ExpectedProfileName' not exposed." -ForegroundColor DarkYellow
        return 'ambiguous'
    }

    $toggleControls=@(Find-UiaVisibleByPattern -Root $scope -Pattern ([System.Windows.Automation.TogglePattern]::Pattern))
    if($toggleControls.Count -eq 0){
        $advancedNames=@('Advanced options','Erweiterte Optionen')
        $advanced=@(Find-UiaVisibleByNamesAndPattern -Root $scope -Names $advancedNames -Pattern ([System.Windows.Automation.ExpandCollapsePattern]::Pattern))
        if($advanced.Count -eq 1){if(!(Invoke-UiaElement -Element $advanced[0] -Action expand)){return 'failed'}}
        else {
            $advanced=@(Find-UiaVisibleByNamesAndPattern -Root $scope -Names $advancedNames -Pattern ([System.Windows.Automation.InvokePattern]::Pattern))
            if($advanced.Count -ne 1){Write-Host "UIA diagnostic: actionable Advanced options controls = $($advanced.Count)" -ForegroundColor DarkYellow;return 'ambiguous'}
            if(!(Invoke-UiaElement -Element $advanced[0])){return 'failed'}
        }
        $toggleDeadline=[DateTime]::UtcNow.AddSeconds(5)
        do {
            Start-Sleep -Milliseconds 100
            $rootElement=Get-GaleAutomationRoot
            if(!$rootElement){continue}
            $scope=Find-GaleImportDialogScope -Root $rootElement
            if(!$scope){continue}
            $toggleControls=@(Find-UiaVisibleByPattern -Root $scope -Pattern ([System.Windows.Automation.TogglePattern]::Pattern))
            if($toggleControls.Count -gt 0){break}
        } while([DateTime]::UtcNow -lt $toggleDeadline)
    }

    if($toggleControls.Count -ne 1){Write-Host "UIA diagnostic: visible toggle controls inside import dialog = $($toggleControls.Count)" -ForegroundColor DarkYellow;return 'ambiguous'}
    try {
        $toggle=$toggleControls[0].GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
        if($toggle.Current.ToggleState -eq [System.Windows.Automation.ToggleState]::Off){$toggle.Toggle();Start-Sleep -Milliseconds 150;$toggle=$toggleControls[0].GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)}
        if($toggle.Current.ToggleState -ne [System.Windows.Automation.ToggleState]::On){return 'failed'}
    } catch {return 'failed'}

    $importNames=@('Import','Importieren')
    $importButtons=@(Find-UiaVisibleByNamesAndPattern -Root $scope -Names $importNames -Pattern ([System.Windows.Automation.InvokePattern]::Pattern))
    if($importButtons.Count -ne 1){Write-Host "UIA diagnostic: actionable Import buttons inside import dialog = $($importButtons.Count)" -ForegroundColor DarkYellow;return 'ambiguous'}
    if(!(Invoke-UiaElement -Element $importButtons[0])){return 'failed'}
    return 'started'
}

function Get-ZipEntrySha256 {
    param([Parameter(Mandatory=$true)][string]$ZipPath,[Parameter(Mandatory=$true)][string]$EntryName)
    Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
    $zip=[System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        $entry=$zip.GetEntry($EntryName)
        if(!$entry){throw "ZIP entry not found: $EntryName"}
        $stream=$entry.Open()
        try {
            $sha=[System.Security.Cryptography.SHA256]::Create()
            try {return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant()}
            finally {$sha.Dispose()}
        }
        finally {$stream.Dispose()}
    }
    finally {$zip.Dispose()}
}

function Wait-ImportedProfileEvidence {
    param([Parameter(Mandatory=$true)][string]$TargetDir,[Parameter(Mandatory=$true)][string]$ExpectedExportSha,[int]$WaitSeconds=300)
    $exportPath=Join-Path $TargetDir 'export.r2x'
    $deadline=[DateTime]::UtcNow.AddSeconds($WaitSeconds)
    do {
        if(Test-Path -LiteralPath $exportPath){
            try {
                $actualExport=(Get-FileHash -LiteralPath $exportPath -Algorithm SHA256).Hash.ToLowerInvariant()
                if($actualExport -eq $ExpectedExportSha){return 'completed'}
            } catch {}
        }
        Start-Sleep -Milliseconds 250
    } while([DateTime]::UtcNow -lt $deadline)
    return 'unconfirmed'
}

Write-Host "Helper revision: $helperRevision" -ForegroundColor DarkGray

Get-Process -ErrorAction SilentlyContinue | Where-Object {$_.ProcessName -ieq 'gale'} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 500

$cache=[DateTime]::UtcNow.Ticks
$active=((Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/RuntimeInbox/ACTIVE_BUILD.txt?cb=$cache" -Headers $headers).Trim())
if(!$active){throw 'RuntimeInbox/ACTIVE_BUILD.txt ist leer'}
Write-Host "`nAktiver Repository-Build: $active" -ForegroundColor Cyan

$cache=[DateTime]::UtcNow.Ticks
$build=Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/Current/AUTO_BUILD_RESULT.json?cb=$cache" -Headers $headers
if(([string]$build.build_id) -ne $active){throw "AUTO_BUILD_RESULT gehört zu '$($build.build_id)', ACTIVE_BUILD ist aber '$active'. Abbruch aus Sicherheitsgründen"}

$profilePath=[string]$build.output_profile
$expected=([string]$build.output_sha256).ToLowerInvariant()
$expectedProfileName=[string]$build.profile_name
if(!$expectedProfileName){$expectedProfileName=[IO.Path]::GetFileNameWithoutExtension($profilePath)}
if(!$profilePath -or !$expected -or !$expectedProfileName){throw 'AUTO_BUILD_RESULT enthält keinen gültigen Profilpfad, Profilnamen oder SHA-256'}

$profileFile=[IO.Path]::GetFileName($profilePath)
Write-Host "Repository-Profil: $profileFile" -ForegroundColor Cyan
Write-Host "Zielprofilname: $expectedProfileName" -ForegroundColor Cyan
Write-Host "Erwarteter SHA-256: $expected" -ForegroundColor Cyan

$downloads=Join-Path $env:USERPROFILE 'Downloads'
if(!(Test-Path -LiteralPath $downloads)){New-Item -ItemType Directory -Path $downloads | Out-Null}
$dst=Join-Path $downloads $profileFile
if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}

$encodedPath=[Uri]::EscapeUriString($profilePath)
$downloadUrl="https://raw.githubusercontent.com/$repo/main/$encodedPath?cb=$([DateTime]::UtcNow.Ticks)"
Write-Host "`nLade neues Profil zuerst sicher herunter..." -ForegroundColor Cyan
Invoke-WebRequest -UseBasicParsing -Uri $downloadUrl -OutFile $dst -Headers $headers
if(!(Test-Path -LiteralPath $dst) -or (Get-Item -LiteralPath $dst).Length -le 0){throw 'Download fehlgeschlagen oder Datei ist leer'}

$actual=(Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "Download SHA-256: $actual" -ForegroundColor Cyan
if($actual -ne $expected){Remove-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue;throw "SHA-256-Prüfung fehlgeschlagen. Erwartet: $expected / Erhalten: $actual"}
$expectedExportSha=Get-ZipEntrySha256 -ZipPath $dst -EntryName 'export.r2x'
Write-Host "SHA-256 stimmt. Download ist verifiziert." -ForegroundColor Green
Write-Host "export.r2x Evidenz-SHA-256: $expectedExportSha" -ForegroundColor DarkGray

$dirs=@(Get-ChildItem -LiteralPath $root -Directory | Sort-Object Name)
if(!$dirs.Count){Remove-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue;throw "Keine Gale-Profile gefunden unter: $root"}
Write-Host "`nVerfügbare Gale-Profile:`n" -ForegroundColor Cyan
for($i=0;$i-lt$dirs.Count;$i++){Write-Host ("[{0}] {1}" -f ($i+1),$dirs[$i].Name)}

do {
    $n=Read-Host "`nNummer des Profils, das gelöscht werden soll"
    $parsed=0
    $ok=[int]::TryParse($n,[ref]$parsed) -and $parsed -ge 1 -and $parsed -le $dirs.Count
} until($ok)

$sel=$dirs[$parsed-1]
Write-Host "`nAusgewählt: $($sel.Name)" -ForegroundColor Yellow
$targetDir=Join-Path $root $expectedProfileName
if((Test-Path -LiteralPath $targetDir) -and ([IO.Path]::GetFullPath($targetDir) -ne [IO.Path]::GetFullPath($sel.FullName))){Remove-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue;throw "Das Zielprofil '$expectedProfileName' existiert bereits lokal. Abbruch, damit kein anderes Profil unbeabsichtigt überschrieben wird."}

do {$answer=(Read-Host 'Soll dieses Profil wirklich gelöscht werden? (y/n)').Trim().ToLowerInvariant()} until($answer -eq 'y' -or $answer -eq 'n')
if($answer -eq 'n'){if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force};Write-Host "`nAbgebrochen. Das lokale Profil wurde nicht gelöscht." -ForegroundColor Yellow;return}

Remove-Item -LiteralPath $sel.FullName -Recurse -Force
Write-Host "Gelöscht: $($sel.FullName)" -ForegroundColor Green

Write-Host "`nÖffne das verifizierte Profil genau einmal in Gale..." -ForegroundColor Green
Start-Process -FilePath $dst

$missingResult=Try-ResolveGaleMissingProfileDialog -ExpectedProfileName $sel.Name
if($missingResult -eq 'resolved'){
    Write-Host "Gales 'Missing Profiles'-Dialog wurde gezielt für '$($sel.Name)' auf Delete -> Submit aufgelöst." -ForegroundColor Green
}
elseif($missingResult -eq 'none'){
    Write-Host "Kein blockierender 'Missing Profiles'-Dialog erkannt." -ForegroundColor Green
}
else {
    Write-Warning "Der 'Missing Profiles'-Dialog konnte nicht eindeutig und sicher automatisiert werden ($missingResult). Es wird nichts blind angeklickt."
    Write-Host "Bitte in Gale für '$($sel.Name)' gezielt Delete auswählen und danach Submit drücken. PowerShell wartet automatisch auf das Schließen des Dialogs." -ForegroundColor Yellow
    if(!(Wait-MissingProfilesClosed -WaitSeconds 120)){throw 'Missing-Profile-Dialog wurde nicht innerhalb des Zeitlimits geschlossen'}
}

Write-Host "`nWarte auf den bereits durch den EINMALIGEN .r2z-Aufruf geladenen Profil-Importdialog..." -ForegroundColor Cyan
$importResult=Try-AutomateGaleProfileImport -ExpectedProfileName $expectedProfileName -WaitSeconds 60
if($importResult -eq 'started'){
    Write-Host "'Import all files' wurde aktiviert und der Import ausgelöst." -ForegroundColor Green
}
else {
    Write-Warning "Der Importdialog konnte nicht eindeutig und sicher automatisiert werden ($importResult). Es wird nichts blind angeklickt."
    Write-Host "Bitte in Gale manuell: Advanced options -> Import all files aktivieren -> Import. PowerShell wartet automatisch auf die importierte Profil-Evidenz." -ForegroundColor Yellow
}

Write-Host "Prüfe Importabschluss über die tatsächliche lokale export.r2x des Zielprofils..." -ForegroundColor Cyan
$completion=Wait-ImportedProfileEvidence -TargetDir $targetDir -ExpectedExportSha $expectedExportSha -WaitSeconds 300
if($completion -ne 'completed'){
    Write-Warning "Der Import konnte innerhalb des Zeitlimits nicht über die Zielprofil-Evidenz bestätigt werden. Die heruntergeladene .r2z bleibt zur Sicherheit erhalten: $dst"
    return
}

Write-Host "Import verifiziert: '$expectedProfileName' enthält exakt die erwartete export.r2x aus dem SHA-geprüften Build." -ForegroundColor Green
if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}
Write-Host "Download-Datei entfernt: $dst" -ForegroundColor Green
