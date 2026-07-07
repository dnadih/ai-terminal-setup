function ai_naredba {
    $env:AI_SHELL = "powershell"
    $pitanje = "$args"

    if ($pitanje -like "error:*") {
        $cisto_pitanje = $pitanje -replace "^error:\s*", ""
        $pitanje = "$cisto_pitanje

[ZADNJA GREŠKA IZ SUSTAVA]:
$Error[0]"
    }

    if ($input) {
        $input | Out-String | & C:\Users\dinko\.terminal-mcp\venv\Scripts\python.exe C:\Users\dinko\.terminal-mcp\mcp_bridge.py $pitanje
    } elseif ([string]::IsNullOrWhiteSpace($pitanje)) {
        & C:\Users\dinko\.terminal-mcp\venv\Scripts\python.exe C:\Users\dinko\.terminal-mcp\mcp_bridge.py
    } else {
        & C:\Users\dinko\.terminal-mcp\venv\Scripts\python.exe C:\Users\dinko\.terminal-mcp\mcp_bridge.py $pitanje
    }
}
Set-Alias ai ai_naredba
