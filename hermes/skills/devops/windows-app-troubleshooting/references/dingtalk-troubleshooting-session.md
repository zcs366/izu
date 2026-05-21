# DingTalk Troubleshooting Session (2026-05-16)

## Problem
User: "钉钉怎么无法会话" — DingTalk can't have conversations.

## Discovery Path

### 1. Process Check
```bash
cmd.exe /c "tasklist /FI \"IMAGENAME eq dingtalk.exe\" /FO LIST" 2>/dev/null
# → No DingTalk process found (initially)
```

### 2. Binary Location
```bash
cmd.exe /c "dir /s /b \"C:\\*DingTalk*\" 2>nul" 2>/dev/null
# → Nothing on C:
ls /mnt/d/Program\ Files\ \(x86\)/ 2>/dev/null
# → Found "DingDing" folder (not "DingTalk"!)
```

### 3. Application Data Location
Data on C:, program on D::
```bash
ls /mnt/c/Users/Administrator/AppData/Roaming/DingTalk/ 2>/dev/null
# → Found logs, config, etc.
```

### 4. Launch Attempt — First Try
```bash
# Simple start failed (quoting issue with nested quotes)
cmd.exe /c "start /B \"\" \"D:\\Program Files (x86)\\DingDing\\main\\current\\DingTalk.exe""
# → bash quoting error

# Solution: write a .bat file to D: drive
# launch_dingtalk.bat:
#   start "" "D:\Program Files (x86)\DingDing\main\current\DingTalk.exe"
#   exit
cmd.exe /c "D:\launch_dingtalk.bat"
# → Process launched but exited immediately
```

### 5. Direct Execution Debug
```batch
"D:\Program Files (x86)\DingDing\main\current\DingTalk.exe" 2>&1
echo EXIT_CODE=%ERRORLEVEL%
pause
```
Output showed:
```
[ERROR:early_gray_v2.cc(234)] ExportEnvToMemory process bool failed
[WARNING:nest_engine_ex.cc(259)] nest engine already exist.
```
**Key insight**: "nest engine already exist" — a background service/process was already running, preventing a clean launch.

### 6. Process Rediscovery
```bash
cmd.exe /c "tasklist" 2>/dev/null | grep -i "ding"
# → 10 DingTalk.exe processes found!
```

### 7. Window Enumeration
```powershell
# Wrote dingtalk_enum.ps1 to D: drive
# Found DingTalk windows:
# - Qt51518QWindowIcon|钉钉 - (163720)|visible=True  ← MAIN WINDOW
# - Multiple Qt51511QWindowIcon|DingTalk|visible=False
# - StandardFrame_DingTalk|visible=True
```
The main window was visible but the `Get-Process` showed PID 6124 had `MainWindowHandle=331680`.

### 8. Window State Check
```powershell
$h = [IntPtr]331680
[W32]::IsIconic($h)  # → True! Window was MINIMIZED
```

### 9. Fix: Restart
```batch
taskkill /F /IM DingTalk.exe /T
timeout /t 3
start "" "D:\Program Files (x86)\DingDing\main\current\DingTalk.exe"
```
→ Killed 10 processes, waited 3s, relaunched.
→ 6 processes came up (main PID 6124).

### 10. Fix: Bring Window to Foreground
```powershell
$h = [IntPtr]331680
[W32]::ShowWindow($h, 9)  # SW_RESTORE
[W32]::SetForegroundWindow($h)
```

### 11. Verification
```powershell
$h = [IntPtr]331680
[W32]::IsWindow($h)       # → True
[W32]::IsIconic($h)       # → False (not minimized anymore)
[W32]::IsWindowVisible($h) # → True
curl https://oapi.dingtalk.com/  # → 200 OK
```

## Technical Notes
- **DingTalk install path**: `D:\Program Files (x86)\DingDing\main\current\DingTalk.exe`
- **DingTalk main executable class**: `Qt51518QWindowIcon`
- **Main window title pattern**: `"钉钉 - (163720)"` (app name + workspace code)
- **Other window classes**: `Qt51511QWindowIcon`, `StandardFrame_DingTalk`, `DingMenuWnd`
- **AppData path**: `C:\Users\Administrator\AppData\Roaming\DingTalk\`
- **Log path**: `C:\Users\Administrator\AppData\Roaming\DingTalk\log\gaea.log.YYYY-MM-DD`
- **Key log pattern**: Look for "nest engine already exist" — means a previous instance is still running
- **Normal startup**: ~10 seconds from launch to process list update
- **Process count**: ~6 core processes when running cleanly
