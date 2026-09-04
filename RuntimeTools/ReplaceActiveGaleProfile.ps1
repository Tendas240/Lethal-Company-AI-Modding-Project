$root='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles'
$repo='Tendas240/Lethal-Company-AI-Modding-Project'
$headers=@{'User-Agent'='LC-Profile-Updater'}

function Get-GaleAutomationRoot {
    try {
        $proc=@(Get-Process -ErrorAction SilentlyContinue |
            Where-Object { $_.ProcessName -ieq 'gale' -and $_.MainWindowHandle -ne 0 } |
            Sort-Object StartTime -Descending |
            Select-Object -First 1)
        if(!$proc.Count){return $null}
        return [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$proc[0].MainWindowHandle)
    }
    catch {
        return $null
    }
}

function Find-UiaVisibleByName {
    param(
        [Parameter(Mandatory=$true)]$Root,
        [Parameter(Mandatory=$true)][string]$Name
    )

    $out=@()
    try {
        $condition=New-Object System.Windows.Automation.PropertyCondition -ArgumentList @(
            [System.Windows.Automation.AutomationElement]::NameProperty,
            $Name
        )
        $collection=$Root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$condition)
        for($i=0;$i-lt$collection.Count;$i++){
            try {
                $item=$collection.Item($i)
                if($item.Current.IsEnabled -and -not $item.Current.IsOffscreen){
                    $out+=$item
                }
            }
            catch {}
        }
    }
    catch {}
    return $out
}

function Invoke-UiaElement {
    param(
        [Parameter(Mandatory=$true)]$Element,
        [ValidateSet('default','expand','select')][string]$Action='default'
    )

    if($Action -eq 'expand'){
        try {
            $pattern=$Element.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
            $pattern.Expand()
            return $true
        }
        catch {}
    }

    if($Action -eq 'select'){
        try {
            $pattern=$Element.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
            $pattern.Select()
            return $true
        }
        catch {}
    }

    try {
        $pattern=$Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke()
        return $true
    }
    catch {}

    if($Action -ne 'expand'){
        try {
            $pattern=$Element.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
            $pattern.Expand()
            return $true
        }
        catch {}
    }

    return $false
}

function Try-ResolveGaleMissingProfileDialog {
    param(
        [Parameter(Mandatory=$true)][string]$ExpectedProfileName,
        [int]$WaitSeconds=20
    )

    try {
        Add-Type -AssemblyName UIAutomationClient -ErrorAction Stop
        Add-Type -AssemblyName UIAutomationTypes -ErrorAction Stop
    }
    catch {
        return 'uia-unavailable'
    }

    $deadline=[DateTime]::UtcNow.AddSeconds($WaitSeconds)
    $root=$null
    $dialog=@()

    do{
        $root=Get-GaleAutomationRoot
        if($root){
            $dialog=@(Find-UiaVisibleByName -Root $root -Name 'Missing Profiles')
            if($dialog.Count -gt 0){break}
        }
        Start-Sleep -Milliseconds 250
    }while([DateTime]::UtcNow -lt $deadline)

    if(!$root){return 'no-window'}
    if($dialog.Count -eq 0){return 'none'}

    # Fail closed unless the dialog is exactly the simple one-profile case that
    # this helper itself just created. Never auto-delete unrelated missing profiles.
    $profileHits=@(Find-UiaVisibleByName -Root $root -Name $ExpectedProfileName)
    $selectors=@(Find-UiaVisibleByName -Root $root -Name 'Select an action')
    if($profileHits.Count -lt 1 -or $selectors.Count -ne 1){
        return 'ambiguous'
    }

    if(!(Invoke-UiaElement -Element $selectors[0] -Action 'expand')){
        return 'failed'
    }

    $deleteDeadline=[DateTime]::UtcNow.AddSeconds(5)
    $deleteItems=@()
    do{
        $root=Get-GaleAutomationRoot
        if($root){
            $deleteItems=@(Find-UiaVisibleByName -Root $root -Name 'Delete')
            if($deleteItems.Count -eq 1){break}
        }
        Start-Sleep -Milliseconds 100
    }while([DateTime]::UtcNow -lt $deleteDeadline)

    if($deleteItems.Count -ne 1){return 'failed'}
    if(!(Invoke-UiaElement -Element $deleteItems[0] -Action 'select')){
        return 'failed'
    }

    $submitDeadline=[DateTime]::UtcNow.AddSeconds(5)
    $submit=@()
    do{
        $root=Get-GaleAutomationRoot
        if($root){
            $submit=@(Find-UiaVisibleByName -Root $root -Name 'Submit')
            if($submit.Count -eq 1){break}
        }
        Start-Sleep -Milliseconds 100
    }while([DateTime]::UtcNow -lt $submitDeadline)

    if($submit.Count -ne 1){return 'failed'}
    if(!(Invoke-UiaElement -Element $submit[0] -Action 'default')){
        return 'failed'
    }

    $closeDeadline=[DateTime]::UtcNow.AddSeconds(8)
    do{
        Start-Sleep -Milliseconds 150
        $root=Get-GaleAutomationRoot
        if(!$root){continue}
        $remaining=@(Find-UiaVisibleByName -Root $root -Name 'Missing Profiles')
        if($remaining.Count -eq 0){return 'resolved'}
    }while([DateTime]::UtcNow -lt $closeDeadline)

    return 'failed'
}

Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -ieq 'gale' } |
    Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 500

$active=((Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/RuntimeInbox/ACTIVE_BUILD.txt" -Headers $headers).Trim())
if(!$active){throw 'RuntimeInbox/ACTIVE_BUILD.txt ist leer'}
Write-Host "`nAktiver Repository-Build: $active" -ForegroundColor Cyan

$build=Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/Current/AUTO_BUILD_RESULT.json" -Headers $headers
if(([string]$build.build_id) -ne $active){
    throw "AUTO_BUILD_RESULT gehört zu '$($build.build_id)', ACTIVE_BUILD ist aber '$active'. Abbruch aus Sicherheitsgründen"
}

$profilePath=[string]$build.output_profile
$expected=([string]$build.output_sha256).ToLowerInvariant()
if(!$profilePath -or !$expected){throw 'AUTO_BUILD_RESULT enthält keinen gültigen Profilpfad oder SHA-256'}

$profileFile=[IO.Path]::GetFileName($profilePath)
Write-Host "Repository-Profil: $profileFile" -ForegroundColor Cyan
Write-Host "Erwarteter SHA-256: $expected" -ForegroundColor Cyan

$downloads=Join-Path $env:USERPROFILE 'Downloads'
if(!(Test-Path -LiteralPath $downloads)){New-Item -ItemType Directory -Path $downloads | Out-Null}
$dst=Join-Path $downloads $profileFile
if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}

$encodedPath=[Uri]::EscapeUriString($profilePath)
$downloadUrl="https://raw.githubusercontent.com/$repo/main/$encodedPath"
Write-Host "`nLade neues Profil zuerst sicher herunter..." -ForegroundColor Cyan
Invoke-WebRequest -UseBasicParsing -Uri $downloadUrl -OutFile $dst -Headers $headers
if(!(Test-Path -LiteralPath $dst) -or (Get-Item -LiteralPath $dst).Length -le 0){
    throw 'Download fehlgeschlagen oder Datei ist leer'
}

$actual=(Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "Download SHA-256: $actual" -ForegroundColor Cyan
if($actual -ne $expected){
    Remove-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue
    throw "SHA-256-Prüfung fehlgeschlagen. Erwartet: $expected / Erhalten: $actual"
}
Write-Host 'SHA-256 stimmt. Download ist verifiziert.' -ForegroundColor Green

$dirs=@(Get-ChildItem -LiteralPath $root -Directory | Sort-Object Name)
if(!$dirs.Count){
    Remove-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue
    throw "Keine Gale-Profile gefunden unter: $root"
}

Write-Host "`nVerfügbare Gale-Profile:`n" -ForegroundColor Cyan
for($i=0;$i-lt$dirs.Count;$i++){
    Write-Host ("[{0}] {1}" -f ($i+1),$dirs[$i].Name)
}

do{
    $n=Read-Host "`nNummer des Profils, das gelöscht werden soll"
    $parsed=0
    $ok=[int]::TryParse($n,[ref]$parsed) -and $parsed -ge 1 -and $parsed -le $dirs.Count
}until($ok)

$sel=$dirs[$parsed-1]
Write-Host "`nAusgewählt: $($sel.Name)" -ForegroundColor Yellow

do{
    $answer=(Read-Host 'Soll dieses Profil wirklich gelöscht werden? (y/n)').Trim().ToLowerInvariant()
}until($answer -eq 'y' -or $answer -eq 'n')

if($answer -eq 'n'){
    if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}
    Write-Host "`nAbgebrochen. Das lokale Profil wurde nicht gelöscht." -ForegroundColor Yellow
    return
}

Remove-Item -LiteralPath $sel.FullName -Recurse -Force
Write-Host "Gelöscht: $($sel.FullName)" -ForegroundColor Green

Write-Host "`nÖffne neues Profil in Gale..." -ForegroundColor Green
Start-Process -FilePath $dst

$missingResult=Try-ResolveGaleMissingProfileDialog -ExpectedProfileName $sel.Name
switch($missingResult){
    'resolved' {
        Write-Host "Gales 'Missing Profiles'-Dialog wurde gezielt für '$($sel.Name)' auf Delete -> Submit aufgelöst." -ForegroundColor Green
        Start-Sleep -Milliseconds 500
        # Re-send the verified .r2z after the blocking dialog is gone. Gale's import
        # dialog is a singleton, so this safely refreshes/opens the same import flow.
        Start-Process -FilePath $dst
    }
    'none' {
        Write-Host "Kein blockierender 'Missing Profiles'-Dialog erkannt." -ForegroundColor Green
    }
    default {
        Write-Warning "Der 'Missing Profiles'-Dialog konnte nicht eindeutig und sicher automatisiert werden ($missingResult). Es wird nichts blind angeklickt."
        Write-Host "Bitte in Gale für '$($sel.Name)' gezielt Delete auswählen und danach Submit drücken." -ForegroundColor Yellow
        Read-Host 'Wenn der Missing-Profile-Dialog vollständig geschlossen ist, hier ENTER drücken'
        Start-Process -FilePath $dst
    }
}

Write-Host "`nIn Gale jetzt: Advanced options -> Import all files aktivieren -> Import." -ForegroundColor Yellow
Read-Host 'Wenn Gale den Import ERFOLGREICH abgeschlossen hat, hier ENTER drücken'

if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}
Write-Host "Download-Datei entfernt: $dst" -ForegroundColor Green
