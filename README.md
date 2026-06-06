# PenKit v1.0 — Arsenal Management Framework

A fancy Metasploit-style CLI tool to discover, manage, search, and launch all your pentesting tools from one place.

---

## ⚠️ Legal Disclaimer

This tool is intended **strictly for authorized security testing, CTF competitions, and educational purposes only.**
Use it only on systems you own or have **explicit written permission** to test.
Unauthorized use against systems you do not own is illegal and unethical. The author assumes no liability for misuse.

---

## 🖥️ OS Support

| OS | Status | Notes |
|---|---|---|
| **Kali Linux** | ✅ Fully supported | Primary target platform |
| **Ubuntu / Debian** | ✅ Fully supported | Works out of the box |
| **Arch / Parrot / BlackArch** | ✅ Supported | Community tested |
| **macOS** | ⚠️ Partial | Tool discovery works; install paths and some build steps may differ |
| **Windows** | ❌ Not supported | WSL2 may work but is untested |

> Python 3.7+ required. No third-party Python packages needed — stdlib only.

---

## Screenshots

<img width="923" height="385" alt="Screenshot 2026-06-06 224934" src="https://github.com/user-attachments/assets/cdac8706-33cf-45f3-82ae-36c276e47202" />


---

## Installation

```bash
chmod +x install.sh
./install.sh
```

Then just run:
```bash
penkit
```

---

## Features

| Feature | Details |
|---------|---------|
| **Curated Auto-discovery** | Scans the system against a curated list of ~120+ known pentest tools. Zero false positives. |
| **System-wide Install** | Installs tools to `/opt/` and symlinks to `/usr/local/bin/`. Survives uninstalls. |
| **Direct Execution** | Just type `nmap -sV 10.0.0.1`. No need for the `run` keyword. |
| **GitHub API Integration**| Auto-fetches READMEs to generate descriptions and categories. |
| **Language Build Support**| Auto-detects and builds Go, Rust, Python, and Make projects. |
| **Virtual Environments** | Prompts to install Python dependencies in a `venv` or `--break-system-packages`. |
| **Aliases** | Create custom command aliases (e.g. `alias qs "nmap -sS -T4 -p-"`). |
| **Health Checks** | `check <tool>` to verify if a tool is working properly. |
| **Updates** | Update single tools or all custom tools at once (`update --all`). |
| **Token Management** | Stores GitHub token securely with expiry warnings on launch. |
| **Non-interactive Mode**| Scriptable CLI args: `--install`, `--scan`, `--list`, `--update-all`. |

---

## Commands

```
<tool> [args...]        Run a tool directly
search <query>          Search tools by name, category, or keyword
list [category]         List all tools or filter by category
info <tool>             Show detailed info about a tool
scan                    Rescan your system for known pentest tools
install <url|path>      Install a tool from GitHub URL or zip/tar file
update <tool/--all>     Update GitHub-installed tool(s)
uninstall <tool>        Uninstall a custom tool (arsenal-only or system-wide)
check <tool>            Health check a tool (--version / --help)
add <name> <cmd>        Manually register a custom tool
remove <tool>           Remove tool from PenKit DB only
categories              Show all categories with counts
tag <tool> <category>   Change the category of a tool
alias <name> <cmd>      Create an alias
aliases                 List aliases
unalias <name>          Remove alias
config                  Manage settings and tokens
history                 Show command history
clear                   Clear the screen
help                    Show help menu
exit / quit             Exit PenKit
```

---

## Examples

```bash
pk > search brute          # find all brute force tools
pk > list recon            # list all recon tools
pk > info hydra            # show hydra details
pk > nmap -sV 10.0.0.1     # launch nmap with args directly
pk > install https://github.com/projectdiscovery/subfinder
pk > update subfinder      # git pull and rebuild subfinder
pk > alias ns "nmap -sV"   # create alias
pk > check sqlmap          # health check sqlmap
```

---

## Configuration

To set your GitHub API token (used for avoiding rate limits and reading READMEs for auto-categorization):

```bash
pk > config token set
```

To set your default preference for Python tool installation (`venv` vs `system`):

```bash
pk > config pip-mode
```

All data is stored in `~/.penkit/`.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
