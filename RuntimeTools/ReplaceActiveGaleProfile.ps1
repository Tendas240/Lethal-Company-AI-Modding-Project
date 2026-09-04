$root='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles'
$repo='Tendas240/Lethal-Company-AI-Modding-Project'
$headers=@{'User-Agent'='LC-Profile-Updater'}

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
Write-Host "`nIn Gale jetzt: Advanced options -> Import all files aktivieren -> Import." -ForegroundColor Yellow
Read-Host 'Wenn Gale den Import ERFOLGREICH abgeschlossen hat, hier ENTER drücken'

if(Test-Path -LiteralPath $dst){Remove-Item -LiteralPath $dst -Force}
Write-Host "Download-Datei entfernt: $dst" -ForegroundColor Green
