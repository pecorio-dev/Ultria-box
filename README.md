# Ultria — Pentest Multi-Tool Framework

> **For authorized penetration testing, CTF competitions, and security education only.**
> Unauthorized use against systems you do not own or have explicit written permission to test is illegal and unethical. The author assumes no responsibility for misuse.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tools](#tools)
  - [1 · Windows Virus Builder](#1--windows-virus-builder)
  - [2 · Android Builder](#2--android-builder)
  - [3 · Discord C2 Controller](#3--discord-c2-controller)
  - [4 · Remote Screen View](#4--remote-screen-view)
  - [5 · Virus Remover](#5--virus-remover)
  - [6 · Discord ZIP Lister](#6--discord-zip-lister)
  - [7 · Auto-Connect](#7--auto-connect)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Build](#build)
- [Known Limitations & Non-Functional Features](#known-limitations--non-functional-features)
- [Disclaimer](#disclaimer)

---

## Overview

**Ultria** is a Python-based penetration testing toolkit designed for security researchers, CTF players, and authorized pentesters. It bundles several offensive security tools under a single unified terminal launcher (`Ultria.py`), each accessible through a numbered menu.

The project covers a wide attack surface: Windows payload generation, Android APK building, C2 communication over Discord, live remote screen viewing, credential-based auto-login via browser automation, and more.

> This project is a work in progress. Some modules may be incomplete, platform-dependent, or require additional setup to function correctly. See the [Known Limitations](#known-limitations--non-functional-features) section for details.

---

## Project Structure

```
Ultria/
├── Ultria.py                    # Main launcher — unified entry point
├── 1.py                         # Windows Virus Builder (CTK GUI)
├── 2.py                         # Android Builder (CTK GUI)
├── 3.py                         # Discord C2 Controller
├── 4.py                         # Remote Screen View (CTK GUI)
├── 5.py                         # Virus Remover
├── Auto-Connect.py              # Auto-Connect (CTK GUI)
├── Discord-ZIP-Lister.py        # Discord ZIP Lister
├── Build.bat                    # Compile Ultria to a standalone .exe
│
├── Config/
│   ├── Config.py                # Project metadata (name, version, author)
│   └── Util.py                  # Shared utilities, colors, banner functions
│
├── FileDetectedByAntivirus/
│   └── VirusBuilderOptions.py   # Payload code templates (flagged by AV — expected)
│
├── UPX/
│   └── upx.exe                  # UPX packer binary (optional, for compression)
│
└── build/
    ├── VirusBuilder/            # Generated Windows payloads (.exe)
    ├── AndroidBuilder/          # Generated Android projects (.apk)
    ├── RemoteView/              # Saved frames from remote screen sessions
    ├── Build/                   # Compiled Ultria-box launcher
    ├── c2_victims.json          # Active C2 victim registry
    └── c2_registry.json         # C2 message ID registry
```

---

## Tools

### 1 · Windows Virus Builder

**File:** `1.py`

A graphical payload builder for Windows targets. Features a multi-section CTK GUI with three categories of modules: **Stealer**, **Malware**, and **Evasion**.

**Stealer modules:**
| Module | Description |
|---|---|
| System Info | OS, hardware, public IP, username |
| Passwords | Saved browser passwords (Chrome, Edge, Firefox) |
| Cookies | Browser session cookies |
| Discord Accounts | Token harvester |
| Discord Injection | Persistent token logger injected into Discord |
| Wallets Session | Hot-wallet credential files |
| Game Launchers | Steam, Epic, Origin session files |
| Telegram Session | Telegram `tdata` folder |
| Roblox Accounts | Roblox `.ROBLOSECURITY` cookie |
| Browsing History | Chrome, Edge, Firefox history |
| Download History | Recent browser downloads |
| Cards | Saved payment card data |
| Browser Extensions | Extension data export |
| Interesting Files | Documents, SSH keys, config files |
| Webcam Snapshot | Capture from webcam |
| Screenshot | Full multi-monitor capture |
| WiFi Passwords | Saved wireless credentials |
| Clipboard | Current clipboard contents |
| SSH Keys | `.ssh` directory |
| FileZilla Credentials | Saved FTP credentials |
| Environment Variables | System env + `.env` files |
| Minecraft Session | Account tokens |
| Keylogger | Background keystroke logger |
| Crypto Wallets | Desktop wallet app data |
| Microphone Recording | Short audio clip |
| Firefox Data | Firefox profiles and logins |
| Steam Session | Steam session files |

**Malware modules:**
| Module | Description |
|---|---|
| Block Keyboard | Disable keyboard input |
| Block Mouse | Disable mouse input |
| Block Task Manager | Prevent process killing |
| Block AV Sites | Block antivirus vendor websites via hosts |
| Clipboard Hijacker | Replace crypto addresses in clipboard |
| Spam Programs | Open many windows rapidly |
| Spam Files | Flood disk with junk files |
| Shutdown | Force shutdown the target |
| Fake Error | Show a deceptive error dialog on launch |
| Melt (Self-Delete) | Wipe the executable after running |
| Anti VM & Debug | Exit in sandboxed / debugged environments |
| Launch at Startup | Persist via registry `Run` key |
| Restart Every 5m | Re-run the payload periodically |
| Disable Defender | Attempt to kill Windows Defender |
| USB Spreader | Copy payload to attached USB drives |
| Scheduled Task | Persist via Windows Task Scheduler |
| C2 Heartbeat | Live shell + command execution via Discord |
| Process Disguise | Impersonate a legitimate system process name |
| Polymorphic Repack | Repack the executable every 24h |
| LAN Spreader | Spread across devices on the local network |

**Evasion modules:**
| Module | Description |
|---|---|
| Timing Evasion | Sleep 30s before payload activates |
| String Encryption | XOR-obfuscate embedded strings |
| UPX Compression | Pack with UPX to reduce size and entropy |
| Fake Metadata | Spoof product/company/version metadata |

The builder also supports **icon spoofing**, **file binder**, **profile save/load**, and a **preset mode** (`--preset <webhook>`) for headless builds.

Output: `build/VirusBuilder/<name>.exe`

---

### 2 · Android Builder

**File:** `2.py`

Generates an Android Studio–compatible project with embedded spyware capabilities. The output is a full Gradle project that can be compiled into an APK via Android Studio or the command line.

Output: `build/AndroidBuilder/<AppName>/`

---

### 3 · Discord C2 Controller

**File:** `3.py`

A command-and-control interface that uses Discord webhooks and message patching as the communication channel. Victims running the C2 heartbeat module poll a Discord message for commands and respond via the same webhook.

Features: victim management, command dispatch, response reading, victim registry stored in `build/c2_victims.json`.

---

### 4 · Remote Screen View

**File:** `4.py`

A real-time screen streaming viewer. Victims send JPEG frames to an HTTP receiver running on the attacker's machine. The GUI displays the live stream, FPS, and frame count.

**Modes:**
- **Local Test** — captures the attacker's own screen (no victim needed, useful for testing)
- **HTTP Direct** — victim sends frames directly to attacker IP:port
- **Discord Relay** — frames are sent as Discord attachments and polled by the viewer

**Controls:** stream start/stop, JPEG quality slider, target FPS slider, auto-parameter detection (WiFi signal), optional localhost.run SSH tunnel (no port forwarding needed), save frame to disk.

Output frames: `build/RemoteView/`

---

### 5 · Virus Remover

**File:** `5.py`

Scans and removes common RAT artifacts: registry run keys, scheduled tasks, suspicious processes, and known malware file paths. Useful for cleaning test machines after authorized engagements.

---

### 6 · Discord ZIP Lister

**File:** `Discord-ZIP-Lister.py`

Lists and downloads ZIP archives (including multi-part split ZIPs) sent to a Discord C2 channel. Automatically reassembles split archives into the complete file.

Registry file: `build/c2_registry.json`

---

### 7 · Auto-Connect

**File:** `Auto-Connect.py`

Automates account login using stolen session cookies and credentials. Supports hundreds of domains. Uses Selenium with Chrome DevTools Protocol (CDP) to inject `HttpOnly` cookies directly, bypassing the restriction that JavaScript cannot set them.

Features: ZIP auto-discovery from `build/`, domain filtering and search, pagination (40 domains/page), cookie injection via CDP, password-based form autofill.

---

## Requirements

### Python version
Python **3.10 or newer** (tested on 3.12 and 3.14).

### Packages
Install all dependencies:
```bash
pip install customtkinter pillow selenium requests cryptography colorama
```

| Package | Used by |
|---|---|
| `customtkinter` | 1.py, 2.py, 4.py, Auto-Connect.py |
| `pillow` | 4.py (screen capture, image display) |
| `selenium` | Auto-Connect.py |
| `requests` | Util.py, 3.py, 4.py, Discord-ZIP-Lister.py |
| `cryptography` | 1.py (payload AES encryption) |
| `colorama` | Util.py (terminal colors) |

### System dependencies
- **Google Chrome** + matching **ChromeDriver** — required for Auto-Connect.py
- **UPX** — optional, included at `UPX/upx.exe` — used by the Virus Builder UPX module
- **OpenSSH** — optional — used by Remote Screen View for the localhost.run tunnel feature
- **Android Studio / Gradle** — required to compile APKs generated by 2.py

---

## Installation

```bash
git clone https://github.com/pecorio-dev/Ultria.git
cd Ultria
pip install customtkinter pillow selenium requests cryptography colorama
python Ultria.py
```

No `setup.py` or `requirements.txt` is provided at this time. Install the packages listed above manually.

---

## Usage

Launch the unified menu:
```bash
python Ultria.py
```

The terminal menu shows all available tools:
```
╔══ Tools ══════════════════════════════════════════════════════╗
║  [1]  Windows Virus Builder         · Build obfuscated .exe
║  [2]  Android Virus Builder         · Generate APK
║  [3]  Discord C2 Controller         · Manage victims & commands
║  [4]  Remote Screen View            · Real-time screen stream
║  [5]  Virus Remover                 · Detect & remove RATs
║  [6]  Discord ZIP Lister            · List & download ZIP archives
║  [7]  Auto-Connect                  · Auto-login with cookies
╠══ Build ══════════════════════════════════════════════════════╣
║  [B]  Preset Build  ·  full stealer + C2
╠══ Exit ═══════════════════════════════════════════════════════╣
║  [0]  Exit
╚═══════════════════════════════════════════════════════════════╝
```

Type the number of the tool you want to launch and press Enter.

**Preset build** (`B`): prompts for a Discord webhook URL and builds a pre-configured full stealer + C2 payload non-interactively. Equivalent to `python 1.py --preset <webhook>`.

---

## Build

To compile the Ultria launcher itself into a standalone Windows executable:

```bat
Build.bat
```

This runs PyInstaller using the spec at `build/Build/Ultria-box.spec` and outputs the binary to `build/Build/Ultria-box/Ultria-box.exe`.

Alternatively, run manually:
```bash
python -m PyInstaller build/Build/Ultria-box.spec
```

---

## Known Limitations & Non-Functional Features

This project is a personal toolkit under active development. Several features are incomplete, environment-dependent, or not yet fully tested. The list below documents known issues and things that may not work out of the box.

### General

- **No `requirements.txt`** — dependencies must be installed manually. If a tool fails to import on launch, it prints the missing module name and exits gracefully.
- **Windows-only** — the entire project targets Windows 10/11. Running on Linux will break most tools (`ctypes.windll`, `winreg`, UPX path, `ImageGrab`, etc.). Partial Linux support exists in `Config/Util.py` (`os_name` detection) but is not maintained.
- **Python version compatibility** — some generated payload code uses workarounds for Python 3.12+ (e.g., generator expressions inside `exec()` are broken in 3.12 — the builder uses explicit `bytearray` loops instead). Behavior on Python 3.9 or below is untested.
- **Antivirus detection** — most built payloads will be detected by Windows Defender and other AV products immediately. The evasion modules (obfuscation, UPX, fake metadata, timing) reduce detection rates but do not guarantee evasion against all AV vendors or EDR solutions.

### 1 · Windows Virus Builder

- **UPX compression** — requires `UPX/upx.exe` to exist. If the file is missing or UPX fails, the build completes without compression and prints an error.
- **File binder** — the binder feature (attach a decoy file) is partially implemented. Edge cases with non-PE binder files may not work correctly.
- **Fake metadata** — requires the `pywin32` or `PyInstaller`-compatible resource editor. If metadata injection fails, the build still completes without fake metadata.
- **LAN Spreader** — network discovery depends on ARP and ICMP, which are often blocked by firewalls and require elevated privileges. Results may vary significantly.
- **Polymorphic Repack** — regenerates the payload hash periodically but does not guarantee AV evasion on each repack cycle.
- **C2 Heartbeat + `msg_id`** — the C2 heartbeat relies on a Discord message ID (`msg_id`) that must be stored in `build/c2_victims.json`. If the registry is corrupted or the message was deleted from Discord, the C2 will not work.
- **Discord Injection** — targets the Discord desktop client. Discord updates frequently; the injection path or mechanism may break after a client update.
- **Icon spoofing** — only `.ico` files are supported. PNG/SVG icons must be converted first.

### 2 · Android Builder

- **APK compilation is not done by this tool** — `2.py` generates an Android Studio project. You must open it in Android Studio (or run `./gradlew assembleDebug`) to produce an actual APK. A working JDK and Android SDK are required.
- **The generated project targets a recent API level** — older Android devices (API < 26) may not install the APK without adjustments to `build.gradle`.
- **Permissions** — some dangerous permissions (`READ_CONTACTS`, `RECORD_AUDIO`, `ACCESS_FINE_LOCATION`) require explicit user approval on Android 6+. The payload does not include social engineering to obtain them.

### 3 · Discord C2 Controller

- **Rate limits** — Discord enforces strict API rate limits. Sending commands too quickly or having many active victims may result in 429 errors and delayed command delivery.
- **Message deletion** — if the victim's C2 message is deleted from Discord (e.g., the webhook channel is purged), the victim becomes unreachable. The registry must be updated manually.
- **`c2_victims.json` schema** — if the file is missing or malformed, the C2 controller will show an empty victim list without a visible error.

### 4 · Remote Screen View

- **Local Test mode** — uses `PIL.ImageGrab.grab()` to capture the attacker's screen. On some systems, this may require elevated privileges or fail silently if screen capture is blocked by security software.
- **HTTP Direct mode** — requires the attacker's machine to be reachable by the victim (open port, no NAT blocking). If behind a router without port forwarding, use the built-in **Tunnel** feature (requires OpenSSH to be installed).
- **Tunnel feature** — uses `localhost.run` via SSH. Requires `ssh` in PATH (comes with Windows 10 1809+ via OpenSSH). If the SSH tunnel fails to connect, the viewer falls back to showing a "Tunnel failed" message.
- **Discord Relay mode** — frame rate is capped at ~2 FPS due to Discord webhook rate limits. This mode is very slow and intended as a fallback only.
- **No audio** — screen streaming is video-only (JPEG frames). No audio channel is implemented.
- **Thread safety** — CTK widget updates from background threads were fixed (v1.0 had silent failures on some systems where the Start Stream button appeared to do nothing).

### 5 · Virus Remover

- **Heuristic only** — detection is based on known artifact patterns (registry key names, file paths, process names). It will not detect custom or modified RATs that use non-default names.
- **Requires admin privileges** — removing registry entries from `HKLM` and killing protected processes requires running as Administrator.

### 6 · Discord ZIP Lister

- **Token required** — requires a valid Discord user or bot token with access to the C2 channel. Bots must have `MESSAGE_CONTENT` intent enabled in the Discord developer portal.
- **Large files** — Discord limits attachments to 25 MB per message (500 MB for Nitro boosted servers). Very large payloads must be split manually before sending.

### 7 · Auto-Connect

- **ChromeDriver version** — must match the installed version of Google Chrome. If Chrome updates automatically, ChromeDriver may become incompatible. Update ChromeDriver manually or use `webdriver-manager`.
- **HttpOnly cookies** — injected via Selenium CDP (`Network.setCookie`). Some sites perform additional server-side session validation (IP binding, device fingerprinting) that will cause the injected session to be rejected even if the cookie is valid.
- **2FA / MFA** — accounts protected by two-factor authentication cannot be accessed through cookie injection alone. The tool does not handle TOTP, SMS codes, or passkeys.
- **Domain support** — the tool supports generic cookie/password injection for any domain. However, site-specific login flows (React SPAs, OAuth redirects) may require manual interaction after injection.
- **ZIP auto-scan** — scans `build/` and the system Downloads folder for `browser_data.zip`. If the ZIP was saved elsewhere, use the manual browse button.

---

## Disclaimer

This software is provided **for educational and authorized security testing purposes only**.

- You must have **explicit written permission** from the owner of any system before using these tools against it.
- The author (**pecorio-dev**) is not responsible for any damage, data loss, legal consequences, or other harm resulting from the use or misuse of this software.
- Use in CTF competitions, on your own hardware, or in professional pentest engagements with signed authorization is the only legitimate use case.
- Some features generate binaries that **will trigger antivirus software** — this is expected and by design. Do not run built payloads on machines you are not authorized to test.

**By using this software, you agree to these terms.**

---

*Ultria v1.0 · Python 3 · Windows 10/11 · pecorio-dev*
