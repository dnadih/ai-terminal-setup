# ai-terminal-setup

AI in your terminal — a Python script that communicates with the OpenRouter API. Zero dependencies (stdlib only).

## 🤨 Name Origins
You may have noticed the script is called `mcp_bridge.py`. Yes, "MCP" as in **Model Context Protocol** — the fancy Anthropic standard for letting LLMs interact with tools and servers.

This script does **none of that**. It's literally `urllib.request` → OpenRouter → print. No protocol, no tools, no server, no ceremony.

**The backstory:** I originally planned to build a proper LLM harness — maybe something like a Codex bridge, maybe a real MCP server that could list files, run commands, and fetch context. Then I looked at the actual use case ("explain this error", "what does this command do") and realized I was designing a space station to boil an egg.

So I threw out the harness, kept the name, and called it a day. `mcp_bridge.py` is now a **monument to abandoned ambition** — a reminder that sometimes the best architecture is the one you don't build. It's the software equivalent of naming your cat "Panther" because you *planned* to get a panther but ended up with a stray tabby that refuses to hunt mice.

Works great though. 🚀

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
ai -m                            # change the LLM model (change is peristant)
```

The script automatically adds OS and shell info to the system prompt:
- **OS:** detected via `os.name` (Windows / Linux/Mac)
- **Shell:** set via `AI_SHELL` env variable (automatically from `ai.bat` or PS profile)
