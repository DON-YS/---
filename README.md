<p align="center">
  <img src="https://i.postimg.cc/0jHTtdRW/92aa1dd070ba0f22c4ca02c08131f6c4-ezgif-com-resize.gif" alt="Pirate animated identity" width="420">
</p>

<h1 align="center">Pirate - ☠️</h1>

<p align="center"><strong>CLI-only Termux automation and authorized security-lab tool catalog</strong></p>

<p align="center">
  <a href="https://github.com/DON-YS/Pirate">Repository</a> ·
  <a href="https://t.me/mafia_4O4">Telegram Channel</a> ·
  <a href="https://t.me/MA_Boss_Bot">Telegram Bot</a>
</p>

> **Important:** Pirate is **CLI-only — not a Railway Web Service**. It does not contain an HTTP server, web dashboard, database, or live Telegram polling implementation.

## Table of Contents

- [About](#about)
- [Architecture](#architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running the Project](#running-the-project)
- [Configuration](#configuration)
- [Tools & Dependencies](#tools--dependencies)
- [Termux](#termux)
- [Linux Environments](#linux-environments)
- [Kali Linux](#kali-linux)
- [Termux + Linux Userspaces](#termux--linux-userspaces)
- [Railway Deployment](#railway-deployment)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Testing and Verification](#testing-and-verification)
- [Roadmap and Limitations](#roadmap-and-limitations)
- [Contact](#contact)

## About

Pirate is a small, registry-driven command-line toolkit for Termux and other Unix-like environments. It scans whether registered commands, Python modules, and files are available, displays installation metadata, and can run an explicitly registered installer after the user requests a tool.

The repository's current version is `15.0.0`. The implementation uses Bash launchers and Python's standard library. It is intended for local administration and authorized security laboratories only.

### What it solves

Pirate keeps a catalog of optional tools in one readable JSON file and provides a consistent CLI for checking their local availability. It does not replace those tools, provide a hosted scanning service, or collect credentials.

### Current runtime classification

- **Runtime:** synchronous CLI process
- **Primary entrypoint:** `bin/ys15` for the interactive menu
- **Direct entrypoint:** `core/core.py`
- **Bot status:** `bot/bot.py` is a placeholder that prints a readiness message and exits; it is not connected to Telegram
- **Worker status:** no long-running worker is currently implemented
- **Web status:** no web server or HTTP endpoint is implemented

## Architecture

```text
bin/ys15                  Interactive Bash menu
bin/ys15-scan             Bash wrapper for the scanner
bin/ys15-install          Bash wrapper for installation
bin/ys15-update           Bash wrapper for update checks
        |
        v
core/core.py              CLI dispatcher: status / install <tool>
        |
        +--> core/scanner.py       Reads registry and checks local capabilities
        +--> core/installer.py     Validates a name and runs its registered command
        +--> core/verifier.py      Verifies a command exists
        +--> core/dependencies.py  Prints basic command availability
        |
        v
config/registry.json      Tool definitions, checks, and installer metadata
security/policy.json      Authorized-lab safety policy
```

The standard CLI reads local files and invokes local commands. `core/installer.py` intentionally runs the command declared in the trusted registry through `bash -lc`; review registry changes before executing them. There is no database, ORM, migration system, API layer, frontend, queue, cache, or AI/LLM pipeline.

## Features

- Interactive Termux-oriented menu through `bin/ys15`.
- Registry-driven tool status scanning.
- Checks for commands, Python modules, and files.
- Explicit tool-name validation before installation.
- Informational entries for external and lab-only tools.
- Optional version/update workflow controlled by `YS15_REPO`.
- Defensive policy requiring authorization and prohibiting arbitrary remote shell, credential collection, real-world phishing, and destructive actions.

## Requirements

- Python 3 (standard library only for the repository core).
- Bash and a Unix-like environment.
- Git only for the optional update workflow.
- Termux is the primary documented target for the `bin/` launchers.
- Individual catalog entries may require their own tools, network access, Go, or Termux packages; they are not core Python dependencies.

No `requirements.txt`, `pyproject.toml`, `poetry.lock`, `Pipfile`, `package.json`, Dockerfile, or Railway configuration currently exists in the repository. Do not install a dependency file that is not present.

## Installation

### Local Linux or macOS-like Unix shell

```bash
git clone https://github.com/DON-YS/Pirate.git
cd Pirate
python3 -m unittest discover -s tests -p 'test_*.py'
python3 core/core.py status
```

### Termux

```bash
pkg update
pkg install -y git python

git clone https://github.com/DON-YS/Pirate.git
cd Pirate
python core/core.py status
```

The existing interactive wrappers expect the repository to be installed at `$HOME/.ys-ultra15`. To use them exactly as designed, run the repository's installer/update workflow that copies the project into that location, then launch `$HOME/.ys-ultra15/bin/ys15`. Running `core/core.py` directly from a clone is the simplest supported validation path.

## Quick Start

```bash
git clone https://github.com/DON-YS/Pirate.git
cd Pirate
python3 core/core.py status
```

To install a registered entry, inspect `config/registry.json` first and then run:

```bash
python3 core/core.py install <registered-tool-name>
```

Only use security tools against systems and environments you own or are explicitly authorized to test.

## Running the Project

### Direct CLI

```bash
python3 core/core.py status
python3 core/core.py install sqlmap
```

Use `python` instead of `python3` where that is the interpreter name in your environment.

### Interactive launcher

```bash
bin/ys15
```

This launcher is Termux-oriented and uses `$HOME/.ys-ultra15` as its installation base. `bin/ys15-scan` and `bin/ys15-install` are non-interactive wrappers for the scanner and installer when the project is installed at that base path.

### Update workflow

```bash
YS15_REPO=https://github.com/DON-YS/Pirate.git bash scripts/update.sh
```

The update script clones the configured HTTPS GitHub repository and copies files to `$HOME/.ys-ultra15`. It expects a remote `install.sh` when the separate interactive update path performs an installation; this repository currently does not contain `install.sh`.

### Telegram

```bash
python3 bot/bot.py
```

This command only prints the current placeholder message. It does **not** start a Telegram bot, polling loop, webhook, router, handler, middleware, or FSM. No Telegram library or bot token is currently used by the code.

## Configuration

The only environment variable read by the current source is `YS15_REPO`, used by the shell update scripts. Python does not load dotenv files. `.env.example` documents the variable without containing a secret.

## Environment Variables

| Variable | Required | Used by | Description | Safe example |
|---|---:|---|---|---|
| `YS15_REPO` | Optional | `scripts/update.sh`, update flow | HTTPS GitHub repository to use as the update source | `https://github.com/OWNER/REPOSITORY.git` |

There are currently no `BOT_TOKEN`, AI keys, database URLs, passwords, authentication secrets, or private keys used by the source code. Never add real credentials to `.env.example`, the README, registry JSON, or shell commands.

## Tools & Dependencies

### Runtime

- **Python 3** — executes the scanner, dispatcher, installer, registry reader, and verifier. Uses only the standard library (`json`, `pathlib`, `shutil`, `subprocess`, `os`, `sys`, and `importlib.util`).
- **Bash** — runs the Termux-oriented launchers and update scripts.

### Optional operational tools

- **Git** — required only for `scripts/update.sh` and update checks.
- **Termux `pkg`** — referenced by Termux registry installers such as `nmap`, `tor`, `tshark`, and `iodine`.
- **Go, Python packages, or external releases** — required only by the corresponding optional registry entry; they are not installed as core project dependencies.

The registry is metadata plus executable install commands, not a package manager lockfile. Installation requirements vary by tool and platform.

## Termux

Termux is an Android terminal environment that provides a Unix-like userspace without requiring root for the core project. Pirate's shell wrappers were written for Termux and use `$HOME/.ys-ultra15` as their base directory.

Install only what the project itself needs:

```bash
pkg update
pkg upgrade
pkg install -y git python
```

- `python`: runs the core CLI.
- `git`: supports the optional update workflow.
- `bash`: normally provided by Termux and runs the wrappers.

Additional packages should be installed only for the selected registry tool. Root access is not required merely to run Pirate; some third-party tools may have independent platform or privilege requirements.

## Linux Environments

A Linux distribution is a packaged operating system userspace with its own package manager and defaults. Pirate's standard-library CLI is portable across ordinary Unix-like systems.

- **Ubuntu:** convenient general-purpose development and broad documentation.
- **Debian:** conservative, stable base suitable for servers and minimal environments.
- **Kali Linux:** security-focused distribution with many assessment tools; not required for Pirate itself.
- **Arch Linux:** rolling-release distribution with current packages and more hands-on administration.
- **Fedora:** modern packages and strong general-purpose development tooling.
- **Alpine Linux:** small image base using musl; some third-party binaries and packages may need extra compatibility work.

For ordinary development, Ubuntu or Debian is sufficient. Choose another distribution only for a concrete operational requirement.

## Kali Linux

Kali Linux is a Linux distribution focused on cybersecurity, penetration testing, digital forensics, security research, and network analysis. Pirate can run there as a Python/Bash CLI, but installing Kali does not make the project a security service and is not required for the core.

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv

git clone https://github.com/DON-YS/Pirate.git
cd Pirate
python3 core/core.py status
python3 -m unittest discover -s tests -p 'test_*.py'
```

Use the registry's security tools only against authorized targets and isolated training labs.

## Termux + Linux Userspaces

Termux, a Linux userspace launched inside Termux, and Android root are different:

- **Termux:** Android application/userspace; no root required for Pirate.
- **Linux userspace in Termux:** an additional Ubuntu/Debian/Kali-like userspace, commonly provided by tools such as `proot-distro`; it is not the Android host kernel and does not automatically grant root.
- **Root:** elevated Android device privileges; not needed for this project and should not be added just to run it.

If a selected third-party tool needs a Linux package unavailable in Termux, use an appropriate userspace or distribution only for that tool. Pirate itself needs only Python and Bash, plus Git for updates.

## Railway Deployment

### Explicit deployment model

**CLI-only — not a Railway Web Service.**

Pirate has no HTTP server, web dashboard, health endpoint, persistent worker loop, or live Telegram bot. Its real commands are finite CLI commands such as `python3 core/core.py status`; they finish and exit. A normal Railway Service expects a continuously running process, so deploying the current CLI as a Railway service would not produce a functioning always-on application.

Do not add FastAPI, Flask, Express, an HTTP health endpoint, a web UI, Redis, Celery, Kafka, Kubernetes, or another service solely to satisfy Railway. That would change the project's architecture and behavior.

### If Railway is still used for a one-off CLI execution

Railway may be used only if the selected Railway product/workflow supports a finite job or manual command execution. The command must be one of the real commands documented above, for example:

```text
python3 core/core.py status
```

This is not an always-on web deployment and does not provide a health check. Confirm the Railway plan and job semantics in the dashboard before relying on it.

### GitHub → Railway workflow

No GitHub Action is needed for deployment. Railway's GitHub integration can watch `main` and deploy new commits automatically, while GitHub Actions (if added later) should remain a validation pipeline only. The minimal workflow is:

1. Create a Railway project/service only if a finite CLI job is appropriate for your use case.
2. Connect `DON-YS/Pirate` through Railway's GitHub integration.
3. Select branch `main`.
4. Configure the real command for the intended finite CLI execution.
5. Add only required variables in Railway Variables; currently that is optional `YS15_REPO`.
6. Push to `main`; Railway detects the commit and starts its configured deployment/job.
7. Read deployment logs and rerun/redeploy from the Railway dashboard when required.

There is no repository-level Railway config to maintain and no automatic deployment workflow committed here. If Railway requires a long-running worker for your selected deployment type, the current repository is not compatible without an explicit architectural decision to add one.

## Security

- Never commit `.env`, tokens, API keys, passwords, cookies, private keys, or database credentials.
- Store runtime values in Railway Variables or the local environment.
- Review `config/registry.json` before running an installer: its `install` values are shell commands by design.
- Keep security tools restricted to owned or explicitly authorized systems and isolated labs.
- The checked-in policy disables arbitrary remote shell, credential collection, real-world phishing, and destructive actions.
- Use least privilege; do not enable Android root merely to run Pirate.
- Keep Git and Python updated through the package manager appropriate to the host.

No hardcoded secret or live credential is currently documented or required by the inspected source.

## Troubleshooting

### `python` or `python3` is not found

Install Python with `pkg install python` on Termux or the host distribution's package manager. Then rerun the direct command.

### The interactive launcher cannot find files

The `bin/` wrappers assume `$HOME/.ys-ultra15`. Run `python3 core/core.py status` from a clone, or install/copy the project to the expected base path before using the wrappers.

### Registry/configuration file is missing

Run commands from the repository root for direct execution. The installed wrapper layout must contain `core/` and `config/` below `$HOME/.ys-ultra15`.

### An optional installer fails

The failing command belongs to the selected registry entry and may require Termux, Go, network access, or separate system permissions. Review the entry and install its prerequisites manually; do not run it against unauthorized targets.

### Update script fails

Set `YS15_REPO` to a valid HTTPS GitHub repository URL. The update workflow also relies on Git and may require the remote repository to contain the expected files, including `install.sh` for the interactive update path.

### Railway process exits immediately

That is expected for the current finite CLI commands. Pirate is **CLI-only — not a Railway Web Service**. Do not solve this by adding an HTTP server without an explicit architecture change.

### Telegram bot does not respond

No live Telegram bot is implemented. `bot/bot.py` is a placeholder and does not read a token or connect to Telegram.

## Project Structure

```text
.
├── .env.example                 Safe template for YS15_REPO
├── .gitignore                   Ignores local secrets and runtime files
├── LICENSE                      Project/third-party licensing notice
├── README.md                    This documentation
├── VERSION                      Current version: 15.0.0
├── bin/
│   ├── ys15                    Interactive launcher
│   ├── ys15-install            Install wrapper
│   ├── ys15-scan               Scan wrapper
│   └── ys15-update             Update wrapper
├── bot/
│   ├── README.md                Telegram control-layer notes
│   └── bot.py                   Non-operational placeholder
├── config/
│   ├── categories.json          Registry category labels
│   └── registry.json            Tool definitions and install metadata
├── core/
│   ├── core.py                 CLI dispatcher
│   ├── dependencies.py         Basic command availability report
│   ├── installer.py             Registry validation and execution
│   ├── registry.py              Registry loader
│   ├── scanner.py               Local capability scanner
│   ├── utils.py                 Small filesystem/banner helpers
│   └── verifier.py              Command verifier
├── scripts/
│   └── update.sh                Optional update workflow
├── security/
│   ├── lab-rules.md             Authorized-lab rules
│   └── policy.json              Safety policy
├── templates/
│   └── telegram-menu.json       Menu template; no live transport
├── tests/
│   └── test_repository.py       Repository smoke tests
└── update.sh                    Termux compatibility wrapper
```

## Testing and Verification

Run the repository's existing tests without adding dependencies:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m compileall -q core bot tests
python3 core/core.py status
```

The tests validate the version file, registry JSON, Python compilation, and defensive policy flags. They do not require Telegram, AI providers, a database, network access, or secrets.

## Roadmap and Limitations

- **Implemented:** registry-driven CLI scanning, installer dispatch, Termux-oriented wrappers, update scripts, security policy, and smoke tests.
- **Not currently implemented:** live Telegram transport, handlers, routers, middleware, FSM, AI/LLM integration, database, migrations, HTTP API, frontend, web dashboard, long-running worker, Docker deployment, Railway service configuration, and Kubernetes deployment.
- **Planned only if explicitly required:** a real Telegram worker or another long-running runtime. Such a change would require a separate architecture decision and must not be introduced solely to make the current CLI appear web-compatible.

## Contact

- **Telegram Channel:** https://t.me/mafia_4O4
- **Telegram Account:** `@II_4O4`
- **Telegram Bot:** https://t.me/MA_Boss_Bot (`@MA_Boss_Bot`)
- **Facebook:** [Yousef Z. A. Shaheen](https://www.facebook.com/share/19FsAxNz4o/)

## Legal Notice

Use every security-related tool only against systems you own or have explicit permission to test. Third-party projects listed in the registry remain subject to their own licenses and terms.
