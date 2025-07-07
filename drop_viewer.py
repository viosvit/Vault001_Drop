import streamlit as st
from pathlib import Path
import base64
import json
import qrcode
from io import BytesIO
import streamlit.components.v1 as components

# ───────────────────────────────────────────────
# Config
# ───────────────────────────────────────────────
VAULT_FILE = Path("Vault001.vault")
VIDEO_FILE = Path("Vault001_Unlock.mov")
BURDEN_FILE = Path("BURDEN.mp3")
QR_IMAGE = Path("vault001_qr.png")
NFT_URL = "https://xrp.cafe/nft/000827103C2C3DC1B554A4373008A8F5C7C3F42B13E5A56EC4E1FF6003E820C5"

# ───────────────────────────────────────────────
# Load Files
# ───────────────────────────────────────────────
def get_file_download_link(file_path, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path.name}">{label}</a>'
    return href

def load_qr_code_image():
    if QR_IMAGE.exists():
        return QR_IMAGE
    else:
        qr = qrcode.make(NFT_URL)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        with open(QR_IMAGE, "wb") as f:
            f.write(buf.getvalue())
        return QR_IMAGE

# ───────────────────────────────────────────────
# UI
# ───────────────────────────────────────────────
st.set_page_config(page_title="Vault001 Drop", layout="centered")
st.markdown("""
<style>
    .center {text-align: center;}
    .highlight {font-weight: bold; font-size: 1.5em; color: #e63946;}
    .subtitle {color: #555; font-size: 1.1em;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="center">
    <h1>🔓 The Vault Has Opened</h1>
    <div class="subtitle">“Own your imprint.”</div>
    <p class="highlight">The first emotionally verified Vault — tone-signed, time-stamped, and sovereign.</p>
</div>
""", unsafe_allow_html=True)

# 1. Unlock Ritual
st.subheader("1. Unlock Ritual")
if VIDEO_FILE.exists():
    st.video(str(VIDEO_FILE))
else:
    st.warning("⚠️ Unlock video not found.")

# 2. The Echo (Encrypted Tone)
st.subheader("2. The Echo (Encrypted Tone)")
st.markdown("**REEM Code:** REF-SHA-B3E")

# 3. Download the Vault Artifact
st.subheader("3. Download the Vault Artifact")
st.markdown("**🔐 CIA Signature:** b3e5...8c2")
if VAULT_FILE.exists():
    st.markdown(get_file_download_link(VAULT_FILE, "⬇️ Download Vault001.vault"), unsafe_allow_html=True)
else:
    st.warning("Vault file not found.")

# 4. Vault001 on XRP Ledger
st.subheader("4. Vault001 on XRP Ledger")
st.image(load_qr_code_image(), caption="Scan or click to view the minted NFT on-chain:", use_container_width=True)
st.markdown(f"[🔗 Vault001 NFT]({NFT_URL})")
st.markdown(f"[🔗 View on XRP Cafe]({NFT_URL})")

# 5. Optional Music Player
st.subheader("🌀 Atmosphere")
if BURDEN_FILE.exists():
    with open(BURDEN_FILE, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3")
    st.markdown("*(‘No Burdens’ playback optional)*")
else:
    st.info("‘BURDEN.mp3’ not found.")

st.markdown("""
<div class="center">
    <hr/>
    <p class="subtitle">🧬 Powered by <strong>Whisper Loop™</strong> + <strong>VIOS Protocol</strong></p>
</div>
""", unsafe_allow_html=True)

