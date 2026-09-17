```markdown
<p align="center">
  <img
    src="https://files.catbox.moe/c0px9v.gif"
    alt="Pirate - ☠️"
    width="900"
  />
</p>

<h1 align="center"><strong>Pirate - ☠️</strong></h1>

<p align="center">
  <strong>Y-SHAHEEN PARROTSHELL ULTRA — Script 15</strong>
</p>

<p align="center">
  Advanced Termux / Android ARM64 development, Linux, automation,
  security-lab, storage, database and productivity environment.
</p>

<p align="center">
  <a href="https://t.me/mafia_4O4">Telegram Channel</a>
  ·
  <a href="https://t.me/MA_Boss_Bot">Telegram Bot</a>
  ·
  <a href="https://www.facebook.com/share/19FsAxNz4o/">Facebook</a>
</p>

---

## 📌 Project Overview

**Pirate - ☠️** is the project identity for the Y-SHAHEEN PARROTSHELL ULTRA
environment developed around Termux on Android ARM64/aarch64.

The project is designed as a modular environment for:

- Termux automation
- Linux PRoot environments
- Development
- Build systems
- Productivity
- Databases
- Storage and synchronization
- Cryptography
- Networking
- Security testing in authorized laboratories
- Telegram-based control
- GUI environments
- Project management
- Git/GitHub workflows
- System diagnostics
- Backup and restoration
- Cloud-oriented workflows

The project does **not** claim that every listed tool is installed natively
on Termux. Tools are classified according to their actual environment:

- Native Termux
- Python
- Node.js
- Go
- Rust
- PRoot/Linux
- GUI environment
- External service/platform
- Laboratory-only integration
- Planned/optional

---

# 🧭 Environment

| Component | Environment |
|---|---|
| Host | Android |
| Architecture | ARM64 / aarch64 |
| Terminal | Termux |
| Root | Not required |
| Linux isolation | PRoot |
| Terminal multiplexer | tmux |
| Primary shell | Bash |
| Python | Python 3 |
| Package manager | Termux `pkg` |
| Linux package manager | `apt` inside Debian/Kali/Ubuntu |
| Source control | Git |
| Remote source control | GitHub |
| Automation | Bash + Python |
| GUI target | XFCE |
| GUI transport | VNC / Termux:X11 integration |
| Telegram | Telegram Bot API |
| Storage | Local + rclone + Telegram workflows |

---

# 🏗️ Architecture

```text
Pirate - ☠️
│
├── Termux
│   ├── Bash
│   ├── Python
│   ├── Git
│   ├── tmux
│   ├── rclone
│   ├── OpenSSH
│   ├── OpenSSL
│   ├── GnuPG
│   ├── SQLite
│   ├── networking tools
│   └── development toolchains
│
├── PRoot
│   ├── Debian
│   ├── Ubuntu
│   ├── Kali Linux
│   ├── Alpine Linux
│   ├── Parrot OS [optional]
│   └── NixOS [optional]
│
├── GUI
│   ├── XFCE
│   ├── XFCE Goodies
│   ├── dbus-x11
│   ├── TigerVNC
│   └── Termux:X11 integration
│
├── Y-SHAHEEN Script 15
│   ├── core/
│   ├── bin/
│   ├── config/
│   ├── bot/
│   ├── scripts/
│   ├── reports/
│   ├── logs/
│   └── locks/
│
└── Telegram Control Layer
    ├── System
    ├── Storage
    ├── Distros
    ├── Tools
    ├── Rclone
    ├── GPG
    ├── Web Server
    ├── Upload
    ├── Tmux
    ├── Processes
    ├── Update
    ├── BOT
    ├── Kali GUI
    └── All Commands
```

---

📁 Project Structure

```text
.
├── VERSION
├── README.md
├── .gitignore
│
├── bin/
│   ├── ys15
│   ├── ys15-install
│   ├── ys15-scan
│   └── ys15-update
│
├── core/
│   ├── core.py
│   ├── dependencies.py
│   ├── installer.py
│   ├── registry.py
│   ├── scanner.py
│   ├── utils.py
│   └── verifier.py
│
├── config/
│   ├── registry.json
│   └── categories.json
│
├── bot/
│   ├── bot.py
│   └── README.md
│
├── scripts/
│   └── update.sh
│
├── reports/
├── logs/
├── locks/
└── tests/
```

---

🧰 Core Termux Packages

The environment is designed around the following Termux packages.

Shell and system

```text
bash
coreutils
findutils
grep
sed
gawk
tar
gzip
bzip2
xz-utils
zip
unzip
procps
ncurses-utils
file
tree
which
```

Networking

```text
curl
wget
openssh
nmap
netcat
netcat-openbsd
tor
aria2
```

Development

```text
git
gh
python
python-pip
clang
make
cmake
pkg-config
nodejs
npm
golang
rust
rustc
cargo
openjdk
```

Data and databases

```text
sqlite
postgresql
mariadb
redis
```

Storage and synchronization

```text
rclone
rsync
syncthing
squashfs-tools
```

Security and cryptography

```text
openssl
gnupg
clamav
inotify-tools
aide
```

Terminal productivity

```text
tmux
fzf
zsh
neovim
micro
htop
glances
git-delta
tldr
```

Archive/media/build utilities

```text
ffmpeg
qemu-utils
qemu-system-aarch64
```

Availability depends on the current Termux repository and ARM64 support. The project intentionally detects unavailable packages instead of pretending that every package is installed.

---

🐍 Python Ecosystem

Python is one of the primary automation languages in the project.

Used for:

· Y-SHAHEEN core
· Telegram Bot API integration
· scanners
· registry management
· dependency checks
· verification
· automation
· project utilities

Related Python tools and projects:

· Aider
· SQLMap
· Mitmproxy
· Puppeteer-related automation through Python/Node workflows
· Textual
· Flet

Aider

Aider was evaluated for ARM64 Termux.

Native installation can encounter Android-specific dependency issues, especially packages requiring unsupported native builds.

The recommended deployment model is:

```text
Termux
└── PRoot Ubuntu/Debian
    └── Python 3.12
        └── virtual environment
            └── Aider
```

Aider should therefore be considered a Linux/PRoot development component unless native ARM64 Termux dependencies are confirmed.

---

🟢 JavaScript / Node.js

Supported development ecosystem:

· Node.js
· npm
· pnpm
· Bun
· Puppeteer
· Puppeteer-core
· JavaScript automation
· web tooling

Puppeteer/Puppeteer-core requires a compatible browser executable.

---

🦀 Rust

Rust tooling included in the environment design:

· rust
· rustc
· cargo

Rust is useful for:

· native utilities
· high-performance command-line tools
· ARM64 development
· security tooling
· systems development

---

🐹 Go

Go tooling:

· golang
· go

Used for the Go ecosystem and tools such as:

· Naabu
· Nuclei
· Subfinder
· ffuf
· other Go-based CLI utilities

---

🐧 Linux Distributions

The PRoot environment supports the following distribution targets.

Debian

debian

General-purpose Linux development environment.

---

Ubuntu

ubuntu

General-purpose development, Python, cloud and server environment.

---

Kali Linux

kali-rolling

Security laboratory environment.

Use only against systems and targets for which you have authorization.

---

Alpine Linux

alpine

Lightweight Linux environment.

---

Parrot OS

parrot

Optional target.

It must not be considered installed unless:

```bash
proot-distro list --quiet
```

actually reports it.

---

NixOS

nixos

Optional target.

It must not be considered installed unless it is actually available and registered in the local PRoot environment.

---

🖥️ Graphical Environment

The project includes a Linux GUI deployment path.

Kali GUI

The tested GUI deployment path uses:

· XFCE4
· xfce4-goodies
· dbus-x11
· TigerVNC

Example environment:

```text
Kali Linux
   │
   ├── XFCE4
   ├── XFCE Goodies
   ├── DBus
   └── TigerVNC
```

Example startup:

```bash
vncserver :1 -geometry 1280x720 -depth 24
```

Display:

```text
:1
```

VNC port:

```text
5901
```

Stop:

```bash
vncserver -kill :1
```

---

📱 Termux:X11

The project is designed to support integration between:

```text
Termux
    ↓
PRoot Linux
    ↓
XFCE
    ↓
Termux:X11
```

A dedicated integration/startup script can be used to prepare the Linux GUI environment when Termux:X11 is available.

The GUI layer must be treated separately from the base Termux environment.

---

🗄️ Databases

The project includes a database-oriented development layer.

SQLite

Lightweight embedded database:

```text
sqlite3
```

Suitable for:

· local state
· metadata
· small projects
· automation
· test databases

---

PostgreSQL

Server-grade relational database:

```text
psql
postgres
```

Used for:

· application development
· backend testing
· relational workloads

Requires initialization and server startup before use.

---

MariaDB

MySQL-compatible relational database:

```text
mariadb
```

Used for:

· web development
· backend applications
· SQL testing

Requires initialization and server startup.

---

Redis

In-memory data store:

```text
redis-server
redis-cli
```

Used for:

· caching
· queues
· sessions
· development environments

Requires the Redis server process to be running.

---

🐳 Docker

Docker is included in the project's infrastructure/tool registry.

Important distinction:

```text
Docker CLI
≠
Docker daemon
```

Standard non-root Android Termux does not provide the same Docker daemon environment as a normal Linux host.

Possible deployment models include:

· PRoot/Linux
· Remote Linux VM
· Cloud server
· Rootless-compatible environment

Docker should therefore be treated as an optional infrastructure component, not assumed to be natively available on every Termux installation.

---

☁️ Cloud / Infrastructure

The project is designed to work with external infrastructure where available.

Tools and technologies include:

· GitHub
· Git
· GitHub CLI
· Rclone
· OpenSSH
· Kubernetes-related tooling
· kubectl
· Helm
· Terraform
· Ansible
· Docker
· QEMU
· Crossplane
· KubeVirt
· cloud/VPS environments

The project does not claim that Termux itself magically provides a free remote cloud server.

A cloud server requires an actual provider or remote infrastructure.

---

🧱 Infrastructure Projects

The broader Y-SHAHEEN environment has also investigated:

Kubernetes

Container orchestration platform.

---

Crossplane

Infrastructure control plane for managing cloud and infrastructure resources through Kubernetes APIs.

---

KubeVirt

Virtual machine management on Kubernetes.

---

Firecracker

Lightweight microVM technology suitable for isolated workloads.

These projects are infrastructure/server-side components and should not be considered native Termux packages.

---

🔐 Cryptography and Security

Security and cryptography layer:

· OpenSSL
· GnuPG / GPG
· ClamAV
· AIDE
· shred
· srm
· GoCryptFS
· Cryptomator
· VeraCrypt
· EDS
· iShredder
· rclone crypt
· encryption/decryption workflows
· SHA-256 verification

Important

Not every cryptography product listed above is a native Termux package.

Some are:

· Android applications
· Linux applications
· external tools
· PRoot-compatible software
· optional components

The registry should report their actual status.

---

🛡️ Security Laboratory Tools

The security registry contains tools intended for authorized testing and educational laboratories.

Network discovery

· Nmap
· Naabu

Vulnerability research / assessment

· Nuclei
· SQLMap
· RouterSploit
· Metasploit

Content discovery / fuzzing

· ffuf
· Gobuster
· Fuzzing tools

Enumeration

· Subfinder

Proxy / traffic analysis

· Mitmproxy
· Wireshark
· Tshark
· Bettercap

Tunneling / networking

· Tor
· Xray-core
· Sing-box
· Iodine

Web/security research

· WebSploit

Social-engineering simulation

· SEToolkit
· GoPhish
· phishing simulators

Honeypot / defensive research

· Cowrie

Vulnerability education

· Log4Shell laboratory

Browser/privacy

· Mullvad Browser

---

⚠️ Security Usage Policy

Security tools are intended for:

· owned systems
· authorized penetration tests
· CTFs
· Hack The Box
· TryHackMe
· local laboratories
· defensive research
· educational environments

The project does not provide authorization to attack third-party systems.

The Telegram control layer intentionally avoids unrestricted remote shell execution.

---

🧪 Security Training Platforms

The registry includes integrations/references for:

· Hack The Box
· TryHackMe
· Log4Shell laboratory
· fuzzing laboratories

These are external platforms/environments and are not installed as Termux packages.

---

📦 Tool Registry

The project registry separates tools into categories.

· Networking
· Security
· Cryptography
· Development
· Databases
· Storage
· Cloud
· Linux
· GUI
· Productivity
· Automation
· Laboratory
· External Platforms

The scanner should distinguish:

```text
INSTALLED
MISSING
EXTERNAL
LAB
OPTIONAL
```

This prevents a registry entry from being mistaken for a successfully installed executable.

---

🤖 Telegram Bot

Telegram control is an important part of the environment.

Bot:

@MA_Boss_Bot

https://t.me/MA_Boss_Bot

Channel:

https://t.me/mafia_4O4

Telegram account:

@II_4O4

---

🎛️ Telegram Main Menu

The intended main Telegram interface is:

```text
🤖 Y-SHAHEEN BOT

⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔

🟢 SYSTEM ONLINE

[ Termux-Ys 000 ]

┌─────────────────────────────┐
│ 🖥 System    │ 💾 Storage    │
├─────────────────────────────┤
│ 📦 Distros   │ 🧰 Tools      │
├─────────────────────────────┤
│ ☁️ Rclone    │ 🔐 GPG        │
├─────────────────────────────┤
│ 🌐 Web       │ 📤 Upload     │
├─────────────────────────────┤
│ 🖥 Tmux      │ 📊 Processes  │
├─────────────────────────────┤
│ 🔄 Update    │ 🟢 BOT        │
├─────────────────────────────┤
│ 🎨 Kali GUI  │ 📚 Commands   │
└─────────────────────────────┘
```

---

🖥️ System Button

Displays:

· Android architecture
· Termux environment
· memory
· storage
· running processes
· uptime/status
· CPU information
· installed core tools

---

💾 Storage Button

Storage operations include:

· local storage status
· backup information
· restore information
· checksum verification
· Rclone status
· Telegram storage workflows

The project previously validated a Telegram channel upload/download workflow using a manifest and SHA-256 verification.

---

📦 Distros Button

The Telegram distro menu:

· 🐧 Debian
· 🟠 Ubuntu
· 🛡 Kali Linux
· 🦜 Parrot OS
· ⚡ Alpine
· ❄️ NixOS

Each distro should show its actual installation state.

The bot must not pretend that an uninstalled distribution exists.

---

🧰 Tools Button

The Tools screen displays the detected state of registered tools.

Example:

```text
🟢 nmap
🟢 git
🟢 python
🟢 tmux
🟢 rclone

🔴 sqlmap
🔴 nuclei
🔴 naabu
🔴 subfinder
🔴 ffuf
🔴 gobuster
```

For optional tools, the interface can provide:

```text
[ Install ]
```

beside the tool.

---

📥 Install Buttons

The intended Telegram tool interface is:

```text
🧰 TOOL
Nmap
Status: Installed

[ Reinstall / Update ]
```

or:

```text
🧰 TOOL
Nuclei
Status: Missing

[ Install ]
```

or:

```text
🧰 TOOL
Hack The Box
Status: External

[ Open Platform ]
```

The Install button must only execute a known registry installation action.

It must not execute arbitrary commands received from Telegram.

---

🛡️ Security Tools Menu

Example layout:

```text
🛡 SECURITY LAB

Nmap
[ Install ]

Naabu
[ Install ]

Nuclei
[ Install ]

Subfinder
[ Install ]

ffuf
[ Install ]

Gobuster
[ Install ]

SQLMap
[ Install ]

Metasploit
[ Install ]

Mitmproxy
[ Install ]

Tshark
[ Install ]

Bettercap
[ Install ]

RouterSploit
[ Install ]

Tor
[ Install ]
```

Tools that require a different environment are marked accordingly instead of being falsely reported as installed.

---

🎨 Kali GUI Button

The GUI control provides information for:

· Kali Linux
· XFCE4
· XFCE Goodies
· DBus
· TigerVNC

Example:

```text
🎨 KALI GUI

Status: READY / NOT READY

[ Install GUI ]
[ Start GUI ]
[ Stop GUI ]
[ GUI Status ]
```

The GUI installation path is intended for the installed kali-rolling PRoot environment.

---

☁️ Rclone Button

Rclone functionality:

· remote configuration
· storage listing
· upload
· download
· sync
· encrypted crypt remotes
· storage diagnostics

Example:

```text
☁️ RCLONE

[ Remotes ]
[ List ]
[ Upload ]
[ Download ]
[ Sync ]
[ Crypt ]
```

Rclone encryption protects data on the configured remote; it does not itself create additional physical storage.

---

🔐 GPG Button

GPG functions:

```text
🔐 GPG

[ Generate Key ]
[ List Keys ]
[ Encrypt ]
[ Decrypt ]
[ Sign ]
[ Verify ]
```

Sensitive private keys must never be committed to Git.

---

🌐 Web Server Button

Development web-server controls can include:

· local HTTP server
· project server
· status
· port information
· stop/start controls

Only registered/safe operations should be exposed through Telegram.

---

📤 Upload Button

Upload workflows can include:

```text
📤 UPLOAD

[ Telegram ]
[ Rclone ]
[ Project Artifact ]
[ Backup ]
```

Files should be verified using hashes where appropriate.

---

🖥️ Tmux Button

Tmux operations:

```text
🖥 TMUX

[ Sessions ]
[ Attach ]
[ Create ]
[ Stop ]
[ Status ]
```

The Telegram interface should expose only predefined session operations.

---

📊 Processes Button

Process monitoring can expose:

· CPU
· RAM
· process count
· tmux sessions
· bot status
· system load

Possible local tools:

```text
htop
glances
ps
top
```

---

🔄 Update Button

Update functionality includes:

· Termux packages
· Project files
· Git repository
· Tool registry

Example:

```text
🔄 UPDATE

[ Check ]
[ Update Termux ]
[ Update Project ]
[ Update Registry ]
```

Updates should be explicit and auditable.

---

🟢 BOT Button

The BOT status page displays:

```text
🟢 TELEGRAM BOT

API: Connected
Polling: Active
Process: Running
tmux: ys-bot
```

The bot token is never displayed.

---

📚 All Commands Button

The command reference contains the project's safe local commands.

Examples:

```bash
ys15
ys15-install
ys15-scan
ys15-update
```

and diagnostic commands such as:

```bash
proot-distro list --quiet
tmux ls
git status
python --version
rclone version
```

---

🧩 Y-SHAHEEN Script 15

The Script 15 runtime is organized into:

```text
core/
    core.py
    dependencies.py
    installer.py
    registry.py
    scanner.py
    utils.py
    verifier.py

bin/
    ys15
    ys15-install
    ys15-scan
    ys15-update

config/
    registry.json
    categories.json
```

---

🔍 Scanner

The scanner checks real executables rather than relying only on registry entries.

Example categories:

```text
INSTALLED
MISSING
EXTERNAL
LAB
OPTIONAL
```

Example:

```text
✓ nmap
✓ tor

✗ sqlmap
✗ naabu
✗ nuclei
✗ subfinder
✗ ffuf
✗ gobuster
✗ mitmproxy
✗ tshark
✗ bettercap
✗ iodine
✗ websploit
✗ routersploit
```

Actual status depends on the current device.

---

🧠 Core Components

core.py

Main project coordination layer.

registry.py

Tool and component registry.

installer.py

Installation logic for supported registry components.

dependencies.py

Dependency detection.

scanner.py

Environment/tool scanning.

verifier.py

Verification and validation.

utils.py

Shared utilities.

---

🔒 Security Model

The project follows several rules:

1. Secrets are stored outside Git.
2. Telegram tokens are never printed.
3. Telegram administrative access must be restricted.
4. Arbitrary remote shell execution is disabled.
5. Security tools are intended for authorized environments.
6. Destructive PRoot operations require explicit user action.
7. Existing files should be preserved before repair.
8. Installation state must be detected rather than assumed.
9. Tool registry entries do not automatically mean installation success.
10. Reports should identify actual runtime state.

---

🔑 Secrets

Telegram configuration belongs outside the repository.

Example:

```text
~/.ys-ultra15/secrets/telegram.env
```

or the runtime secret location configured by the deployed bot.

Never commit:

```text
.env
.env.*
telegram.env
private keys
API keys
bot tokens
passwords
certificates
```

Recommended permissions:

```bash
chmod 700 ~/.ys-ultra15
chmod 700 ~/.ys-ultra15/secrets
chmod 600 ~/.ys-ultra15/secrets/telegram.env
```

---

🧪 Validation

Before a release:

```bash
python -m py_compile core/*.py
```

Shell validation:

```bash
bash -n bin/ys15
bash -n bin/ys15-install
bash -n bin/ys15-scan
bash -n bin/ys15-update
bash -n scripts/update.sh
```

Git validation:

```bash
git status
git log --oneline -5
```

PRoot validation:

```bash
proot-distro list --quiet
```

Tmux validation:

```bash
tmux ls
```

Telegram bot validation:

```bash
python -u bot/bot.py
```

---

🧰 Additional Development Tools

The broader environment includes support/planned integration for:

· Git
· GitHub CLI
· uv
· npm
· pnpm
· Bun
· Go
· Rust
· Clang
· CMake
· Make
· Terraform
· Ansible
· Helm
· kubectl
· Cookiecutter
· Copier
· Hygen
· Plop
· Neovim
· LazyVim
· Micro
· Zsh
· Oh My Zsh
· fzf
· tldr
· git-delta
· HTTPie
· ngrok
· OpenSSH
· Textual
· Flet

Availability depends on the execution environment and ARM64 compatibility.

---

🌐 Networking Tools

Registered networking tools include:

```text
curl
wget
ssh
OpenSSH
nmap
netcat
aria2
tor
rclone
rsync
syncthing
```

Advanced networking/lab registry:

```text
Xray-core
Sing-box
Iodine
WebSploit
Bettercap
Mitmproxy
Tshark
Wireshark
```

---

📦 Storage and Backup

Storage ecosystem:

· Rclone
· Rclone Crypt
· Syncthing
· rsync
· SQLite
· SquashFS
· Telegram file storage workflow
· SHA-256 verification
· GPG encryption

Telegram channel storage was tested with:

```text
UPLOAD      : OK
MANIFEST    : OK
FILE_ID     : OK
DOWNLOAD    : OK
SHA-256     : VERIFIED
```

---

🧱 Build and Packaging

The project can support project workflows such as:

```text
Detect
   ↓
Dependencies
   ↓
Tests
   ↓
Build
   ↓
Package
   ↓
Encrypt
   ↓
Upload
```

Supported project ecosystems can include:

· Python
· Node.js
· Go
· Rust
· C/C++

depending on available manifests and toolchains.

---

🖥️ Productivity Environment

Terminal productivity layer:

```text
tmux
fzf
zsh
Oh My Zsh
Neovim
LazyVim
Micro
tldr
git-delta
htop
glances
```

---

🔬 Laboratory Environments

The project can be used with:

· Hack The Box
· TryHackMe
· CTF environments
· Local vulnerable VMs
· Local containers
· Authorized security labs

---

🧪 Security Research Components

The registry includes references to:

· Metasploit
· Nmap
· SQLMap
· Naabu
· Nuclei
· Subfinder
· ffuf
· Gobuster
· RouterSploit
· Mitmproxy
· Tshark
· Wireshark
· Bettercap
· Tor
· Xray-core
· Sing-box
· Iodine
· WebSploit
· SET
· GoPhish
· Cowrie
· Log4Shell laboratory

Some components are intended for Linux/PRoot or external laboratory environments rather than direct native Termux installation.

---

📱 Android Integration

The host environment is:

```text
Android
   ↓
Termux
   ↓
PRoot
   ↓
Linux
   ↓
GUI / Development / Security Lab
```

The architecture is designed to operate without requiring Android root.

---

🚫 What This Project Does Not Claim

This README intentionally does not claim that:

· every listed tool is installed
· every tool supports Android ARM64 natively
· Docker daemon works natively inside standard Termux
· Parrot OS is installed automatically
· NixOS is installed automatically
· Aider is natively functional on Termux
· every GUI component is always running
· every database server is permanently running
· every external platform is embedded locally
· a free cloud server is magically created by Termux

Actual installation status should be obtained from the project's scanner.

---

👤 Owner

Telegram Channel

Mafia 4O4

https://t.me/mafia_4O4

Telegram Account

@II_4O4

Telegram Bot

@MA_Boss_Bot

https://t.me/MA_Boss_Bot

Facebook

Yousef Z. A. Shaheen

https://www.facebook.com/share/19FsAxNz4o/

---

🏴 Project Identity

Pirate - ☠️

Y-SHAHEEN PARROTSHELL ULTRA
Script 15

Termux
Android ARM64
PRoot
Linux
GUI
Development
Databases
Storage
Security Labs
Telegram Automation

---

📜 Safe Usage

This project is intended for:

· personal development
· system administration
· authorized security testing
· educational laboratories
· CTFs
· development environments
· automation
· infrastructure experimentation

Users are responsible for obtaining authorization before testing systems that they do not own or administer.

---

🚀 Quick Start

Clone the repository and enter it:

```bash
git clone <repository-url>
cd <repository-directory>
```

Check the environment:

```bash
proot-distro list --quiet
```

Check the project:

```bash
git status
```

Check Python:

```bash
python --version
```

Check Script 15:

```bash
./bin/ys15
```

Run the scanner:

```bash
./bin/ys15-scan
```

Update:

```bash
./bin/ys15-update
```

---

🩺 Diagnostics

```bash
python -m py_compile core/*.py

bash -n bin/ys15
bash -n bin/ys15-install
bash -n bin/ys15-scan
bash -n bin/ys15-update

proot-distro list --quiet

tmux ls

git status
```

---

📊 Status Philosophy

The project intentionally distinguishes between:

Status Meaning
🟢 Installed Executable/component detected
🟡 Optional Supported but not required
🔴 Missing Registry entry exists but component is absent
🔵 External External service/platform
🧪 Lab Intended for an authorized lab
🐧 PRoot Linux environment component
🎨 GUI Graphical environment component

This keeps the README and Telegram interface honest about the actual state of the device.

---

⭐ Project Goals

The long-term goals are:

· one unified Termux environment
· modular tool registry
· ARM64 awareness
· PRoot Linux environments
· GUI support
· database support
· development toolchains
· secure storage
· backup/restore
· Telegram administration
· automated diagnostics
· GitHub synchronization
· reproducible installation
· clear separation between installed and optional components

---

<p align="center">
  <strong>Pirate - ☠️</strong>
</p>
<p align="center">
  Y-SHAHEEN PARROTSHELL ULTRA
</p>
<p align="center">
  Termux • Android ARM64 • Linux • Development • Automation • Security Labs
</p>
