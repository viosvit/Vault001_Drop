import streamlit as st
import tempfile
from whisper_utils import classify_tone_intent

st.set_page_config(page_title="Whisper Loop™ Viewer", layout="centered")
st.title("🌀 Whisper Loop™ — Tone Classifier Demo")

uploaded_file = st.file_uploader("🎙️ Upload a voice file (.wav or .m4a)", type=["wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.info("Running Whisper Loop™ classifier...")
    result = classify_tone_intent(temp_path)

    st.subheader("📊 Classification Results")
    st.write(f"**Tone:** {result['tone']}")
    st.write(f"**Intent:** {result['intent']}")
    st.write(f"**REEM Code:** {result['reem_code']}")
    st.write(f"**Confidence:** {result['confidence']*100:.1f}%")

