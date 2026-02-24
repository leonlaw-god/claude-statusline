# Claude Statusline Installer for Windows
# Usage: irm https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main/install.ps1 | iex

param()

$ErrorActionPreference = "Stop"

$RepoUrl = "https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main"
$ClaudeDir = "$env:USERPROFILE\.claude"
$ScriptName = "statusline-enhanced.py"

Write-Host "🔧 Installing Claude Statusline..." -ForegroundColor Cyan

# Create .claude directory if not exists
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
}

# Download the script
Write-Host "📥 Downloading statusline script..." -ForegroundColor Yellow
$ScriptPath = "$ClaudeDir\$ScriptName"
Invoke-WebRequest -Uri "$RepoUrl/$ScriptName" -OutFile $ScriptPath

# Update settings.json
$SettingsFile = "$ClaudeDir\settings.json"
Write-Host "📝 Updating settings.json..." -ForegroundColor Yellow

$StatusLineConfig = @{
    type = "command"
    command = "py $ScriptPath"
}

if (Test-Path $SettingsFile) {
    $Settings = Get-Content $SettingsFile -Raw | ConvertFrom-Json

    # Add or update statusLine
    if ($Settings.PSObject.Properties.Match("statusLine")) {
        $Settings.statusLine = $StatusLineConfig
    } else {
        $Settings | Add-Member -MemberType NoteProperty -Name "statusLine" -Value $StatusLineConfig
    }

    $Settings | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
    Write-Host "✅ Updated settings.json" -ForegroundColor Green
} else {
    # Create new settings.json
    $NewSettings = @{
        statusLine = $StatusLineConfig
    }
    $NewSettings | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
    Write-Host "✅ Created new settings.json" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Restart Claude Code to see the new statusline." -ForegroundColor Cyan
Write-Host ""
Write-Host "Features:" -ForegroundColor Yellow
Write-Host "  • Model name display"
Write-Host "  • Token usage (Tok/Out)"
Write-Host "  • Cost tracking (`$)"
Write-Host "  • Context usage percentage (Ctx)"
Write-Host "  • Git status (branch, changes, conflicts)"
Write-Host "  • Full directory path"
