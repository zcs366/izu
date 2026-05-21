# Workspace Initialization (WSL↔Windows)

## When to Use

- User says "建一个工作区", "给我在 X 建个工作区", "以后读写都在这里"
- Any request to establish a workspace/directory convention

## Workflow

### 1. Resolve the path

Windows paths → WSL paths:
- `I:\hermes` → `/mnt/i/hermes/`
- `C:\Users\xxx` → `/mnt/c/Users/xxx/`
- Always verify the mount exists: `ls /mnt/<drive-letter>/`

### 2. Create the directory structure

```
<workspace-root>/
├── _workspace.md         ← conventions + memory
├── output/               ← files I generate (give to user)
│   ├── pdf/
│   ├── doc/
│   └── img/
├── input/                ← files user gives me (to read/process)
│   ├── pdf/
│   ├── doc/
│   ├── md/
│   ├── img/
│   └── other/
├── work/                 ← temporary working files
└── data/                 ← data files
```

### 3. Write `_workspace.md`

Include:
- Path mapping table (Windows ↔ WSL)
- Directory purpose descriptions
- File format conventions
- Active project list (from existing files)
- Any user-specified preferences

### 4. Save to Hermes memory

Record in memory (compact format):
```
工作区：<Windows-path> (WSL: <WSL-path>)。结构：output/(pdf/doc/img) 我生成的文件；input/(pdf/doc/md/img/other) 用户给我的文件；work/ 临时工作文件；data/。配置见 _workspace.md。
```

### 5. Validate

Confirm the directory structure is visible from both WSL and Windows:
```bash
ls <WSL-path>/    # should show all dirs
```

## Pitfalls

- **Silent mkdir failures**: `mkdir -p` in `execute_code` may fail silently across multiple commands. Use single terminal calls with `&&` chaining or verify with `ls`.
- **Path confusion**: Never use raw `I:\` or `\` in shell commands — always convert to `/mnt/<drive>/`.
- **File overwrite**: If `_workspace.md` already exists, read it first and merge, don't overwrite.
- **Trailing slash**: Remove trailing slashes from user paths before converting.
