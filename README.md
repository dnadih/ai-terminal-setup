# ai-terminal-setup

AI in your terminal — a Python script that communicates with the OpenRouter API. Zero dependencies (stdlib only).

## Installation

### 1. Create virtual environment

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.terminal-mcp"
cd "$env:USERPROFILE\.terminal-mcp"
python -m venv venv
```

### 2. Save the script

Copy `mcp_bridge.py` (from this repo) to `%USERPROFILE%\.terminal-mcp\mcp_bridge.py`.

### 3. Set API key

```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "your_key", "User")
```

Close and reopen your terminal.

### 4. Set up the `ai` command

**CMD:** Copy `ai.bat` to `C:\Windows\System32\ai.bat`.

**PowerShell:** Add the contents of `Microsoft.PowerShell_profile.ps1` to `$PROFILE`:

```powershell
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Type File -Force }
notepad $PROFILE
```

Paste the content, save, then reload:

```powershell
. $PROFILE
```

## Usage

```powershell
ai "what is python?"            # direct query
dir | ai "explain this output"  # pipe mode
ai                               # paste mode (Ctrl+Z to finish)
ai -h                            # help
```

The script automatically adds OS and shell info to the system prompt:
- **OS:** detected via `os.name` (Windows / Linux/Mac)
- **Shell:** set via `AI_SHELL` env variable (automatically from `ai.bat` or PS profile)
