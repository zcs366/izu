# Node.js Version Management (for WSL/restricted environments)

Install or upgrade Node.js when `sudo` is unavailable, `curl | bash` installers are blocked, or you need to pin a specific version. All steps work in WSL without sudo.

## Quick Reference: Latest Version Lines

| Branch | Type | Status |
|--------|------|--------|
| v22 (Jod) | LTS | EOL Mar 2026 |
| v24 (Krypton) | Active LTS | ✅ Recommended — support until Apr 2028 |
| v25 | Current | ⚡ Latest features, not LTS |
| v26 | Current | 🆕 Released Apr 2026 |

Fetch latest exact version numbers:
```bash
# Latest LTS
curl -sL https://nodejs.org/dist/index.json | python3 -c "import json,sys; versions=[v for v in json.load(sys.stdin) if v['lts']]; print(versions[0]['version'])"

# Latest Current
curl -sL https://nodejs.org/dist/index.json | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['version'])"
```

## Binary Download (No sudo, No nvm — most reliable)

```bash
VERSION=v24.15.0
ARCH=linux-x64
curl -fsSL "https://nodejs.org/dist/$VERSION/node-$VERSION-$ARCH.tar.xz" -o /tmp/node.tar.xz
mkdir -p ~/.local/node
tar -xf /tmp/node.tar.xz -C ~/.local/node --strip-components=1
echo 'export PATH="$HOME/.local/node/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
node --version
```

## Using nvm (If Available)

```bash
# Download then execute (avoids pipe-to-bash blocks)
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh -o /tmp/nvm-install.sh
bash /tmp/nvm-install.sh
source ~/.bashrc
nvm install 24
nvm alias default 24
```

## Using fnm (Faster Alternative)

```bash
curl -fsSL https://github.com/Schniz/fnm/releases/latest/download/fnm-linux.zip -o /tmp/fnm.zip
unzip /tmp/fnm.zip -d ~/.local/bin
chmod +x ~/.local/bin/fnm
fnm install 24
fnm default 24
fnm use 24
```

## WSL-Specific Pitfalls

### `npm install` hangs/times out
Windows `.npmrc` at `/mnt/c/Users/<user>/.npmrc` interferes with WSL npm:
```bash
npm install --ignore-scripts    # skip postinstall
```

### `npm error config prefix cannot be changed`
Artifact of npm picking up Windows home directory settings. Fix:
```bash
npm config set prefix ""
```

### Systemd services don't inherit shell PATH
When running Node.js via systemd, set absolute PATH in the service file:
```ini
[Service]
Environment="PATH=/home/user/.local/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

## Verification

```bash
node --version    # expected version
npm --version     # should be compatible
which node        # should point to ~/.local/node/bin/node
```
