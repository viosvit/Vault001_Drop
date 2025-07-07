# vault_crypto.py

import json
import base64
import os
from pathlib import Path
from datetime import datetime
from getpass import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import hashlib

# ─────────────────────────────────────────────────────────────
VAULT_PATH = Path("Vault001.vault")

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def encrypt_vault(data: dict, password: str) -> dict:
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    iv = secrets.token_bytes(12)
    json_bytes = json.dumps(data).encode()
    encrypted = aesgcm.encrypt(iv, json_bytes, None)
    tag = encrypted[-16:]
    ciphertext = encrypted[:-16]
    return {
        "metadata": {
            "salt": base64.b64encode(salt).decode(),
            "iv": base64.b64encode(iv).decode(),
            "tag": base64.b64encode(tag).decode()
        },
        "data": base64.b64encode(ciphertext).decode()
    }

def hash_signature(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# ─────────────────────────────────────────────────────────────
def main():
    print("🧬 Creating Vault001")
    entry = {
        "title": input("Title: "),
        "location": input("Location: "),
        "memo": input("Memo: "),
        "reflection": input("Reflection: "),
        "notes": input("Notes: "),
        "tone": input("Tone: "),
        "intent": input("Intent: "),
        "reem_code": input("REEM Code: "),
        "source": input("Source: "),
        "timestamp": datetime.utcnow().isoformat()
    }

    entry["cia_signature"] = hash_signature(entry)

    password = getpass("🔐 Enter password to encrypt: ")
    blob = encrypt_vault(entry, password)

    with open(VAULT_PATH, "w") as f:
        json.dump(blob, f, indent=2)
        print(f"✅ Saved Vault001 → {VAULT_PATH}")

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()

