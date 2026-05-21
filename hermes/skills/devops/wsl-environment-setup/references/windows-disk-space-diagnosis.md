# Windows Disk Space Diagnosis from WSL

Diagnose and reclaim Windows drive space entirely from WSL terminal. Uses PowerShell commands (fast, native Windows filesystem) rather than WSL `du` over `/mnt/c/` (extremely slow for recursive scans, especially FUSE-layer).

## Quick State Check

```bash
# Overall usage for all mounted Windows drives
df -h /mnt/c /mnt/d /mnt/e 2>/dev/null
```

**Caveat:** `df` shows available space, but 100% doesn't mean the drive is broken; it's critically full.

## Hierarchical Scan Strategy

Start broad, then drill in. Never run `du -sh /mnt/c/*/` — it'll take minutes and may time out.

### 1. Root-level system files (hiberfil.sys, pagefile.sys, swapfile.sys)

These are invisible from WSL `ls` (Permission denied) — use PowerShell:

```powershell
powershell.exe -Command "
Get-ChildItem 'C:\' -Force -ErrorAction SilentlyContinue |
    Where-Object { -not $_.PSIsContainer -and $_.Length -gt 100MB } |
    Sort-Object Length -Descending |
    ForEach-Object { '{0,8:N0} MB  {1}' -f [math]::Round($_.Length/1MB), $_.Name }
"
```

**Pitfall — `-Force` is required:** Without it, hidden system files (hiberfil.sys, pagefile.sys, swapfile.sys) don't appear.

### 2. Top-level directories (both C: and D:)

```powershell
powershell.exe -Command "
Get-ChildItem 'C:\' -Directory -ErrorAction SilentlyContinue |
    ForEach-Object {
        $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 1GB) {
            '{0,8:N0} MB  {1}' -f [math]::Round($size/1MB), $_.Name
        }
    } | Sort-Object -Descending
"
```

Same pattern for `D:\`.

**Pitfall — `Measure-Object -Property Length -Sum` fails on directories:** Directories don't have a `Length` property. Always append `-ErrorAction SilentlyContinue` to `Measure-Object`. If you omit it, the entire recursive scan fails with `PSArgumentException` garbled in Chinese/WSL output.

**Pitfall — Chinese-named directories display garbled:** From WSL PowerShell, Chinese characters like `张市历年` or `国学迷` show as `????????`. Use `wmic` as fallback:
```bash
powershell.exe -Command "wmic logicaldisk get DeviceID,Size,FreeSpace"
```
Or accept the encoding limitation — the file listing still works, just the display is garbled.

### 3. Drill into user profile

```powershell
powershell.exe -Command "
\$profile = 'C:\Users\Administrator'
Get-ChildItem \$profile -Directory -ErrorAction SilentlyContinue |
    ForEach-Object {
        \$size = (Get-ChildItem \$_.FullName -Recurse -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if (\$size -gt 500MB) {
            '{0,8:N0} MB  {1}' -f [math]::Round(\$size/1MB), \$_.Name
        }
    } | Sort-Object -Descending
"
```

Then drill into `AppData\Local` and `AppData\Roaming` with the same pattern — they're usually the biggest consumers (WSL VHDX, caches, program data).

### 4. Find the Windows user profile name

```bash
ls /mnt/c/Users/
# Or from PowerShell:
powershell.exe -Command "Get-ChildItem 'C:\Users' -Directory | Select-Object Name"
```

The Windows username may differ from the WSL username.

## Multi-Drive Discovery

Don't assume only C: and D: exist. Use `wmic` to discover ALL drives:

```bash
cmd.exe /c "wmic logicaldisk get DeviceID,VolumeName,Size,FreeSpace"
```

Common results include:
- SSD drives (C:, D:) — fast, limited space, where programs live
- Mechanical drives (E:, F:, G:, H:, ...) — slow, spacious, for storage
- External USB drives — variable

**If there are mechanical drives with free space:** Before deleting anything, consider migrating large static data (AI models, old project files, media) to those drives instead. Mechanical drives are slower for inference but fine for storage.

**Pitfall — user may not remember they have extra drives:** The `wmic` output can surprise the user. List all drives proactively rather than asking "do you have other drives?".

## Multi-Drive Scanning

When both C: and D: (or more drives) are full:

1. **Scan each drive independently** — don't assume the user's data is only on C:
2. **Check for cross-drive duplication** — especially AI model files (ollama on C:, lmstudio on D:)
3. **Look for "hidden" root-level dirs** — `.ollama`, `.lmstudio`, `.android` at `C:\` and `D:\` root, not under Users

## GPU-Aware AI Model Audit

When AI models (Ollama, LM Studio, Stable Diffusion, ComfyUI) are consuming hundreds of GB, the key question is not "how much space" but "can the GPU run these models?"

### Step 1: Check GPU VRAM

```bash
# From WSL, get accurate VRAM and running processes
cmd.exe /c "nvidia-smi"
# Key fields:
#   GPU Memory: XXXXMiB / YYYYMiB  ← YYYY is total VRAM
#   Processes list shows what's using GPU now
```

**Pitfall — WMI reports wrong VRAM:** `Get-CimInstance Win32_VideoController | Select-Object AdapterRAM` often reports 4GB for cards that actually have 11GB+ (WMI reporting bug). Always use **nvidia-smi** for accurate VRAM.

### Step 2: Check Current Processes Using GPU

```powershell
powershell.exe -Command "Get-Process | Where-Object { \$_.ProcessName -match 'ollama|lmstudio|docker|python|comfy' } | Select-Object ProcessName, Id, @{n='MemMB';e={[math]::Round(\$_.WorkingSet64/1MB,1)}}"
```

Also from nvidia-smi output: check the `Processes` section for which apps are using GPU.

### Step 3: Determine Which Models Actually Fit

**GGUF model size formula (Q4_K_M quantization):**
| Model Size | Q4_K_M Size | Fits 11GB VRAM? |
|-----------|------------|-----------------|
| 7B | ~4.5 GB | ✅ Full GPU |
| 8B | ~5.5 GB | ✅ Full GPU |
| 12-14B | ~8-9 GB | ✅ Full GPU |
| 20B | ~12 GB | ⚠️ Needs offloading |
| 24B | ~14 GB | ❌ Mainly CPU |
| 32B | ~18-19 GB | ❌ CPU only, 2-3 t/s |

**Common mistake:** Users download 32B models their GPU can't run, wonder why inference is too slow to use, then leave the models sitting unused. The models become "space decorations."

### Step 4: Cross-Tool Duplication Detection

Check for **the same model family across multiple tools**:

| Tool | Storage Path | Typical Size Range |
|------|-------------|-------------------|
| Ollama | `C:\.ollama\models\blobs` (content-addressed blobs) | 50-200 GB |
| LM Studio | `D:\.lmstudio\models\{publisher}\{model-name}\` | 100-400 GB |
| SD WebUI | `I:\Stable Diffusion\*\models\{type}\` | 50-300 GB |
| ComfyUI | `I:\ComfyUI\*\models\{type}\` | 50-200 GB |

**Signs of duplication:**
- Same model family (Qwen, GLM, DeepSeek, Mistral, Gemma) appears in both Ollama's manifest list AND LM Studio's publisher directories
- SD and ComfyUI share the same checkpoint file downloaded twice
- Multiple quantization levels of the same model (Q4 + Q8 + F16)

**Recommendation strategy for rarely-used AI tools:**
- If user rarely uses any — keep ONE tool platform (Ollama is best for headless API integration)
- Delete the other tools' models entirely (they can be re-downloaded when needed)
- Replace oversized models (32B) with GPU-fitting ones (7B-14B) — 10-20x faster inference
- Downloading a 14B model takes 3-5 minutes; keeping 200GB "in case" is wasting space for the sake of avoiding a 5-minute wait

### Step 5: Pre-Deletion Audit (User Requirement)

**Before deleting ANY AI tool or model, audit each item:**

```
AUDIT CHECKLIST:
□ Is the tool process currently running? (nvidia-smi + Get-Process)
□ Does another tool depend on this one? (e.g., Open WebUI → Ollama)
□ Are there user conversations or data worth backing up?
□ Is the tool registered in Windows (Appwiz.cpl / registry)?
□ Could this deletion affect WSL or WSL-adjacent services?
```

**Risk ratings to present to user:**
| Rating | Meaning | Example |
|--------|---------|---------|
| 🟢 No dependencies | Standalone, re-downloadable | AI model files, temp files |
| 🟡 Ask user | Needs user decision | Docker images, Open WebUI data |
| 🔴 Require backup | Has user data worth keeping | LM Studio conversations, SD outputs |
| ⚫ Don't touch | System-critical | Windows/Program Files system components |

**Workflow for each deletion candidate:**
1. Check if process is running (`Get-Process | Where-Object Name -match '...'`)
2. Check if other tools reference its data (e.g., Open WebUI's vector_db referencing Ollama)
3. Check for user-created content (conversations, generated images, configs)
4. Present risk rating + size to user
5. Only delete after user explicitly approves

**Pitfall — checking process state is not enough:** A tool might not be RUNNING but still actively needed (e.g., Docker Desktop isn't running now but the user plans to start it tomorrow). Always ask the user about "future usage intent" before removing large tool installations.

## Docker Audit When Docker Isn't Running

`docker system prune` requires Docker Desktop to be running. When it's not:

### Check Docker's On-Disk Data Directly

```bash
# Default Docker Desktop WSL data location
ls -la /mnt/d/Docker/    # (or wherever Docker was installed)
# Look for:
#   DockerDesktopWSL/  →  WSL2 virtual disk (typically 20-60 GB)
#   open-webui/        →  Open WebUI user data (chat history, vector DB, uploads)
#   lobe-chat-db/      →  LobeChat database
```

### Direct Directory Audit

Check what's inside Docker data directories before recommending deletion:

```bash
# Check Open WebUI data content
ls /mnt/d/Docker/open-webui/    # chat history, vector_db, uploads, cache
# Check if it's actively useful or just cached data
```

### Present With Context

When reporting Docker's disk usage:
- State whether Docker Desktop is currently running
- List what containers/services are stored (Open WebUI, LobeChat, etc.)
- Note: user may not KNOW what's in there — ask if they still use these services
- Directories like `open-webui/cache/` (800MB+) are safe to delete; `open-webui/vector_db/` and `uploads/` contain user data

## Stable Diffusion / ComfyUI Model Auditing

These tools (often on I: or other large drives) are especially prone to "install once, never use again" bloat.

### Internal Structure

```
Stable Diffusion/
├── sd-webui-aki-v4.10/        ← The webui installation
│   ├── models/                ← 290 GB (checkpoints, LoRAs, VAE, embeddings)
│   ├── extensions/            ← ~16 GB (extensions)
│   ├── outputs/               ← ~5 GB (generated images)
│   ├── python/                ← ~7 GB (bundled Python env)
│   └── .cache/                ← ~5 GB
└── 兔兔/ 资料/ 教程/         ← User documentation, small files
ComfyUI/
├── ComfyUI_windows_portable/
│   └── ComfyUI/
│       ├── models/            ← ~188 GB
│       ├── custom_nodes/      ← ~600 MB
│       ├── output/            ← ~133 MB
│       └── input/             ← ~1 MB
```

### Classification Strategy

When user says "吃了灰" (collecting dust), classify each category:

| Category | Re-download? | Keep? |
|---------|-------------|-------|
| Base checkpoint (SDXL, SD1.5) | Slow (5-10GB) | Consider keeping 1 |
| LoRA/Embeddings | Fast (<500MB each) | Delete, re-download if needed |
| VAE | Fast (<1GB) | Keep 1, delete rest |
| ControlNet | Medium (1-2GB each) | Delete if not used |
| Extensions | Fast | Delete, re-install if needed |
| Bundled Python | Slow (7GB) | Keep (part of installation) |
| Outputs/Generated images | User data | Ask user if they want them |
| .cache/ | 0 cost | Delete freely |

**Recommended "skeleton" setup** for occasional SD/ComfyUI use: ~50 GB total (1 checkpoint + 1 VAE + essential extensions + Python env). Down from 290/188 GB.

## AI Model Duplication Detection

This is the single biggest category overlooked in standard disk cleanups:

| Location | Typical Tool | Typical Size |
|----------|-------------|-------------|
| `C:\.ollama\models\blobs` | Ollama GGUF blobs | 50-200 GB |
| `D:\.lmstudio\models` | LM Studio model files | 100-400 GB |
| `C:\Users\*\AppData\Local\lm-studio-updater` | LM Studio updates cache | 0.5-1 GB |
| `C:\Users\*\.lmstudio\models` | (rare, but check) | 0-10 GB |

**Signs of duplication:**
- Both ollama AND lmstudio are installed
- Same model families appear in both (Qwen, GLM, Phi, Mistral, DeepSeek)
- One tool keeps blobs on C:, the other stores unpacked models on D:

**Questions to ask user:**
1. "Which AI model tool do you actively use — ollama or LM Studio?"
2. "Are these models still needed or can they be purged?"
3. "Can the remaining tool's models be migrated to one drive?"

## Common Space Hogs (Complete Reference)

| Item | Typical Size | Action |
|------|-------------|--------|
| `hiberfil.sys` | **15-30 GB** | `powercfg /h off` (disable hibernation) |
| `C:\.ollama\models\blobs` | **50-200 GB** | Remove unused models; uninstall Ollama if using LM Studio |
| `D:\.lmstudio\models` | **100-400 GB** | Remove unused models; uninstall LM Studio if using Ollama |
| `AppData\Local\wsl\` | **30-60 GB** | Compact VHDX after cleaning WSL |
| `C:\Windows\WinSxS` | **15-30 GB** | `DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase` |
| Docker images/volumes | **10-60 GB** | `docker system prune -a -f` |
| `C:\Windows\Temp` | 1-5 GB | `Remove-Item 'C:\Windows\Temp\*' -Recurse -Force` |
| `AppData\Local\Temp` | 1-5 GB | `Remove-Item 'C:\Users\*\AppData\Local\Temp\*' -Recurse -Force -ErrorAction SilentlyContinue` |
| `C:\ProgramData\Package Cache` | **1-3 GB** | MSI installer cache — safe to delete |
| `C:\Users\*\AppData\Local\pip\cache` | 1-5 GB | `pip cache purge` |
| `C:\Users\*\AppData\Local\npm-cache` | 1-5 GB | `npm cache clean --force` |
| pip cache (inside WSL) | 1-5 GB | `pip cache purge` (frees VHDX interior) |
| npm cache (inside WSL) | 1-5 GB | `npm cache clean --force` |
| `C:\Windows.old` | 10-30 GB | Disk Cleanup → Clean up system files |
| App caches (NetEase, Tencent) | 2-10 GB each | User decision |
| `C:\Users\*\AppData\Local\Programs` | 5-15 GB | Various installed components |
| `C:\Users\*\.lmstudio\extensions` | 5-10 GB | LM Studio runtime extensions |
| `C:\ProgramData\Microsoft\Windows\WER` | 0-2 GB | Windows Error Reporting (safe to clean) |
| `C:\Config.Msi` | 0-1 GB | MSI config cache |

## Hibernation Management

```bash
# Check current state
powershell.exe -Command "powercfg /a"

# Disable (frees hiberfil.sys immediately — 15-30 GB)
powershell.exe -Command "powercfg /h off"

# Verify removal
powershell.exe -Command "if (Test-Path 'C:\hiberfil.sys') { 'still exists' } else { 'removed' }"
```

⚠ May require admin rights. If `powercfg /h off` fails from WSL, run from elevated Windows PowerShell directly.

## WinSxS Cleanup via DISM

```powershell
# Analyze component store (read-only)
DISM /Online /Cleanup-Image /AnalyzeComponentStore

# Clean up superseded components (safe to run, reclaims 5-10 GB)
DISM /Online /Cleanup-Image /StartComponentCleanup

# Aggressive: reset base (removes ALL previous component versions)
# ⚠ After this, you CANNOT uninstall Windows updates
# Only run if confident updates are stable
DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

Run from elevated PowerShell (Windows → right-click → Run as Administrator). From WSL:
```bash
powershell.exe -Command "Start-Process powershell -Verb RunAs -ArgumentList 'DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase'"
```
But elevation dialog appears on Windows desktop — the user must click Yes.

## WSL VHDX Compaction Without Hyper-V

After cleaning files inside WSL (pip cache, npm cache, temp), the `ext4.vhdx` file on C: drive doesn't shrink automatically.

**If Optimize-VHD is available** (Windows Pro with Hyper-V enabled):
```powershell
# In Windows PowerShell as Administrator:
wsl --shutdown
Optimize-VHD -Path "$env:LOCALAPPDATA\wsl\{<distro-guid>}\ext4.vhdx" -Mode Full
```

**If Optimize-VHD is NOT available** (Windows Home, or Hyper-V not enabled) — use diskpart:
```powershell
# In Windows PowerShell as Administrator:
wsl --shutdown
diskpart
```
Inside diskpart:
```
select vdisk file="C:\Users\<YourUser>\AppData\Local\wsl\{<distro-guid>}\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

Find the GUID from WSL: `ls /mnt/c/Users/*/AppData/Local/wsl/`.

**Pitfall — Optimize-VHD path format:** The `-Path` parameter requires a **space** between the flag and the value: `-Path "C:\..."` not `-Path"C:\..."`. Missing space causes "不支持给定路径的格式" error.

**Pitfall — detach vdisk required:** After diskpart compaction, the VHDX must be properly detached or WSL won't mount it on next boot. If you forget, run `wsl --shutdown` again, re-enter diskpart, `select vdisk file="..."`, `detach vdisk`, `exit`.

**Pitfall — run fstrim first:** Before compaction, run `sudo fstrim /` inside WSL to mark freed blocks. Without it, the VHDX has no free space to compact.

## Cleanup Sequence (Recommended Order)

1. **Decide on AI model tool** — pick Ollama or LM Studio, purge the other's models (50-400 GB)
2. **Disable hibernation** — single biggest guaranteed gain (15-30 GB)
3. **Docker system prune** — `docker system prune -a -f` (5-30 GB)
4. **Clear Temp files** — Windows Temp + User Temp (~2-5 GB)
5. **Run Disk Cleanup (cleanmgr)** — check "Clean up system files" for WinSxS, Windows.old
6. **DISM /StartComponentCleanup** — WinSxS reduction (5-10 GB, needs admin)
7. **Clear pip/npm cache** — frees WSL VHDX interior space (~2-10 GB)
8. **Delete `C:\ProgramData\Package Cache`** — MSI cache (~2 GB)
9. **Compact WSL VHDX** — reclaim freed WSL space to C: drive
10. **App caches** — ask user about NetEase, Tencent, browser caches

## Key Principles

- **Always use PowerShell from WSL** for disk scans — 100x faster than `du` over `/mnt/c/`
- **Prioritize hiberfil.sys** — it's the single biggest always-reclaimable block
- **But prioritize AI model deduplication first** — it's usually 10x bigger than hiberfil.sys
- **Clean inside WSL → compact VHDX** — two separate steps; the first frees VHDX interior space, the second returns it to C: drive
- **Ask before Docker prune** — confirm with user before removing tagged images
- **Ask before removing AI models** — they may be actively used; determine the primary tool first
- **Temp files are always safe** — Windows and user Temp directories are purely cache
- **When both C: and D: are full, check both** — AI models often live on D: while system files bloat C:
- **Root-level dot-directories** — `.ollama`, `.lmstudio`, `.conda`, `.android` at drive root — these are the most commonly overlooked space hogs
