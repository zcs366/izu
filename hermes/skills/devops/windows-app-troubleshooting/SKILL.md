---
name: Windows App Troubleshooting from WSL
description: "Diagnose and fix Windows desktop applications entirely from WSL terminal — process discovery, window management, log analysis, application restart, and cross-drive app data location. No GUI required."
---

# Windows App Troubleshooting from WSL

## Overview
When a Windows desktop app isn't working (won't launch, window hidden, can't converse, crashes), you can diagnose and fix it entirely from WSL. This skill covers the standard debugging pipeline.

## Trigger Conditions
- User reports a Windows desktop app not working (e.g. "钉钉怎么无法会话", "微信打不开", "QQ登录不上")
- You need to check process status, logs, or window state of a Windows app from WSL

## Phase 1: Process Discovery

### Check if the app is running
```bash
# All processes
cmd.exe /c "tasklist" 2>/dev/null | grep -i "appname"

# Specific image name
cmd.exe /c "tasklist /FI \"IMAGENAME eq DingTalk.exe\" /FO LIST" 2>/dev/null

# CSV format (for null-safe processing)
cmd.exe /c "tasklist /NH /FO CSV" 2>/dev/null | findstr /i "appname"
```

### Find the application binary
```bash
# Check common locations
cmd.exe /c "dir /s /b \"C:\\*AppName*\" 2>nul" 2>/dev/null
cmd.exe /c "dir /s /b \"D:\\*AppName*\" 2>nul" 2>/dev/null

# Check Program Files
ls /mnt/d/Program\ Files/ 2>/dev/null
ls /mnt/d/Program\ Files\ \(x86\)/ 2>/dev/null

# Check full drive scan (careful: may timeout on large drives)
find /mnt/d -iname "*appname*" 2>/dev/null | head -30
```

### Find application data (often on C: even if program is on D:)
```bash
ls /mnt/c/Users/Administrator/AppData/Local/AppName/ 2>/dev/null
ls /mnt/c/Users/Administrator/AppData/Roaming/AppName/ 2>/dev/null
```

### Check Windows services related to the app
```bash
cmd.exe /c "sc query type=service state=all" 2>/dev/null | grep -i "appname\|keyword"
```

## Phase 2: Diagnose

### Check log files
```bash
# Find most recent logs
ls -lt /mnt/c/Users/Administrator/AppData/Roaming/AppName/log/ 2>/dev/null | head -20

# Check for errors in current log
tail -100 /mnt/c/Users/Administrator/AppData/Roaming/AppName/log/appname.log | grep -i -E "error|fail|exception|timeout|network|connect" | tail -30
```

### Check network connectivity from WSL to app servers
```bash
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 https://app-api.example.com/
cmd.exe /c "ping -n 1 api.server.com 2>nul" 2>/dev/null
```

### Check screen configuration (multi-monitor, off-screen windows)
```powershell
# Via PowerShell script (write to D: drive first)
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::AllScreens | ForEach-Object { Write-Host ($_.DeviceName + '|' + $_.Bounds.ToString()) }"
```

## Phase 3: Window Management

### Enumerate all app windows
Use a PowerShell script saved to `/mnt/d/` (to avoid encoding issues with here-strings via cmd.exe):

```powershell
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win32 {
    [DllImport("user32.dll")] public static extern int EnumWindows(EnumWindowsProc lpEnumFunc, int lParam);
    public delegate bool EnumWindowsProc(IntPtr hWnd, int lParam);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetClassName(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
}
'@
# Filter by class name containing app keyword
```

Or use Get-Process for simple window info:
```powershell
$proc = Get-Process AppName -ErrorAction SilentlyContinue
foreach($p in $proc){
    Write-Host ("PID:" + $p.Id + "|MainTitle:" + $p.MainWindowTitle + "|MainHandle:" + $p.MainWindowHandle.ToString())
}
```

### Check if window is minimized/restored
```powershell
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class W32 {
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr h);
}
'@
$h = [IntPtr]MAIN_HANDLE
Write-Host ("MINIMIZED:" + [W32]::IsIconic($h))
Write-Host ("VISIBLE:" + [W32]::IsWindowVisible($h))
```

### Bring window to foreground
```powershell
$h = [IntPtr]MAIN_HANDLE
if([W32]::IsIconic($h)){
    [W32]::ShowWindow($h, 9)   # SW_RESTORE
} else {
    [W32]::ShowWindow($h, 3)   # SW_MAXIMIZE
}
Start-Sleep -Milliseconds 300
[W32]::SetForegroundWindow($h)
```

## Phase 4: Application Restart

### Kill all instances
```batch
taskkill /F /IM AppName.exe /T
```

### Launch from WSL — write a .bat file to D: drive first (avoid quoting issues)
```batch
"D:\Program Files (x86)\AppFolder\main\current\AppName.exe"
exit
```

Then execute:
```bash
cmd.exe /c "D:\launch_app.bat"
```

**IMPORTANT**: Use `terminal(background=true)` for long-lived processes, then health-check in a follow-up call.

### Launch via launcher (if available)
```bash
cmd.exe /c "start \"\" /D \"D:\\Program Files (x86)\\AppFolder\" AppLauncher.exe"
```

## Phase 5: Verify

After the fix, verify:
```bash
# Process is running
cmd.exe /c "tasklist /FI \"IMAGENAME eq AppName.exe\" /NH"

# Window is not minimized
# API connectivity
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 https://app-api.example.com/
```

## Pitfalls / Known Issues

1. **Chinese character encoding**: When passing Chinese strings through cmd.exe → PowerShell, here-strings (`@'...'@`) and character literals get garbled. Workaround: write `.ps1` files to `/mnt/d/` (Windows-accessible path) and execute via `cmd.exe /c "powershell -ExecutionPolicy Bypass -File D:\script.ps1"`. Use ASCII class names (e.g. `"Qt51518QWindowIcon"`) instead of Chinese window titles when possible.

2. **WSL /tmp/ not accessible from cmd.exe**: `/tmp/` in WSL is not `C:\tmp` on Windows. Always write batch/PowerShell scripts to `/mnt/d/` (or another Windows-mounted drive) when they need to be executed via `cmd.exe`.

3. **Background processes**: The terminal tool rejects `command &` (backgrounding) in foreground calls. Use `terminal(background=true)` for long-lived processes. The foreground terminal tool (`terminal`) is for quick commands. Long-running Windows apps must be launched in the background.

4. **App starts but exits immediately**: Check for "already running" errors in logs (e.g. DingTalk's "nest engine already exist" warning). Use `taskkill /F /IM AppName.exe /T` to force-kill all instances before restarting.

5. **Program on D: drive, data on C: drive**: Many Windows apps install binaries to D: but store AppData to C:. Check both drives.

6. **FindWindow with Chinese window titles**: Hard to match due to encoding issues. Use class name matching (e.g. `"Qt51518QWindowIcon"`, `"Chrome_WidgetWin_0"`, `"StandardFrame_DingTalk"`) instead of window title matching.

7. **PowerShell `Get-Process` can give quick window state**: `$proc.MainWindowHandle` and `$proc.MainWindowTitle` reveal if the process has a visible window and what its title is (encoding garbled but handle is reliable).

## Reference
- `references/dingtalk-troubleshooting-session.md` — Full debugging transcript from the session that spawned this skill
