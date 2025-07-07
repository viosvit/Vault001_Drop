from __future__ import annotations

#!/usr/bin/env python3
"""
Vault 001 – Mixed-Mode Unlock
• REAL decryption   • Cinematic terminal ritual
"""

import argparse, sys, time, os, json, hashlib, getpass, base64
from tqdm import tqdm
from cryptography.fernet import Fernet
import simpleaudio as sa
from pathlib import Path

# ---------- CONFIG ----------
VAULT_FILE    = "Vault001.vault"
OUTPUT_FILE   = "Vault001_decrypted.json"
HEARTBEAT_WAV = "heartbeat.wav"
ECHO_WAV      = "echo_raw.wav"
REEM_CODE     = "REF-SHA-B3E"
CIA_HASH      = "b3e5...8c2"
# -----------------------------

def play_wav(fname, block=False):
    if not os.path.exists(fname): return
    try:
        wave_obj = sa.WaveObject.from_wave_file(fname)
        play = wave_obj.play()
        if block: play.wait_done()
    except Exception: pass

def slow_print(line, delay=0.03):
    for ch in line:
        sys.stdout.write(ch); sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n"); sys.stdout.flush()

def decrypt_vault(path: Path, password: str) -> dict:
    key = hashlib.sha256(password.encode()).digest()
    key = hashlib.sha256(key).digest()[:32]
    fkey = Fernet(base64.urlsafe_b64encode(key))
    with open(path, "rb") as f:
        encrypted = f.read()
    decrypted = fkey.decrypt(encrypted)
    data = json.loads(decrypted)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--voice", action="store_true")
    args = parser.parse_args()

    vault_path = Path(f"Vault{args.id.zfill(3)}.vault")
    if not vault_path.exists():
        print("❌ Vault file not found.")
        sys.exit(1)

    slow_print(f"\nunlock_vault --id {args.id} {'--voice' if args.voice else ''} 🔐", 0.02)
    play_wav(HEARTBEAT_WAV)
    time.sleep(1.5)

    if args.voice:
        slow_print("🔍 Voiceprint detected…")
        play_wav(ECHO_WAV)
        time.sleep(2)

    slow_print("> Signature verified ✅")
    slow_print(f"> Tone: {REEM_CODE}")
    slow_print(f"> CIA Hash: {CIA_HASH}")

    pwd = getpass.getpass("> Enter vault passphrase: ")

    slow_print("> Decrypting Vault 001…")
    for _ in tqdm(range(60), bar_format="{l_bar}{bar}"):
        time.sleep(0.015)

    try:
        vault_data = decrypt_vault(vault_path, pwd)
    except Exception as e:
        slow_print(f"❌ Decryption failed: {e}")
        sys.exit(1)

    # ── Output ─────────────────────────────────────────
    slow_print("> ✅ Vault decrypted.")
    print(json.dumps(vault_data, indent=2))

if __name__ == "__main__":
    main()

