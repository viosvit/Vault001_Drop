# whisper_utils.py
"""
Whisper Loop ™ Audio + Text Classifier Utilities
- classify_tone_intent(audio_path)  --> runs full tone pipeline from voice file
- classify(text)                    --> classifies tone + intent from transcript
- generate_reem(tone, intent)      --> deterministic REEM code generator
"""

import requests
import hashlib
import random
import os

# Optional audio tools
try:
    import whisper
    import librosa
except ImportError:
    whisper = None
    librosa = None

# -----------------------------------------------------------------------------
# CONFIG — Classifier API (for remote use)
# -----------------------------------------------------------------------------
CLASSIFIER_URL = "http://localhost:5050/analyze"  # Change if hosted elsewhere

# -----------------------------------------------------------------------------
# REMOTE + FALLBACK CLASSIFIER (TEXT)
# -----------------------------------------------------------------------------
def classify(text: str) -> tuple[str, str, str, str]:
    """
    Given raw text, return (tone, intent, REEM code, source)
    Falls back to local logic if API not available.
    """
    try:
        resp = requests.post(CLASSIFIER_URL, json={"text": text}, timeout=5)
        resp.raise_for_status()
        j = resp.json()
        return j["tone"], j["intent"], j["reem_code"], "remote"
    except Exception:
        lower = text.lower()
        tone = (
            "Grateful"    if any(w in lower for w in ("thank", "grateful")) else
            "Curious"     if "?" in lower else
            "Frustrated"  if any(w in lower for w in ("hate", "angry")) else
            "Reflective"
        )
        intent = (
            "Ask"         if "?" in lower else
            "Recommend"   if any(w in lower for w in ("recommend", "suggest")) else
            "Share"
        )
        reem_code = generate_reem(tone, intent)
        return tone, intent, reem_code, "fallback"

# -----------------------------------------------------------------------------
# AUDIO ENTRYPOINT: classify_tone_intent(audio_path)
# -----------------------------------------------------------------------------
def classify_tone_intent(audio_path: str) -> dict:
    """
    Transcribe voice file → Classify tone/intent → Return structured result
    Supports .wav, .m4a
    """
    # 1. Transcribe
    try:
        if not whisper:
            raise ImportError("whisper module not available")
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path, fp16=False)
        transcript = result["text"].strip()
    except Exception:
        if not librosa:
            raise RuntimeError("Librosa not installed for fallback mode")
        y, sr = librosa.load(audio_path, sr=16000)
        sec = len(y) / sr
        transcript = f"(fallback) ~{sec:.1f}s tone snippet"

    # 2. Classify
    tone, intent, reem_code, source = classify(transcript)

    return {
        "tone": tone,
        "intent": intent,
        "reem_code": reem_code,
        "confidence": 0.88 if source == "fallback" else 0.97,
        "source": source,
        "transcript": transcript
    }

# -----------------------------------------------------------------------------
# REEM CODE GENERATOR
# -----------------------------------------------------------------------------
def generate_reem(tone: str, intent: str) -> str:
    """
    Create a deterministic REEM code from tone + intent
    """
    h = hashlib.sha256(f"{tone}|{intent}".encode()).hexdigest()[:6]
    return f"{tone[:3].upper()}-{intent[:3].upper()}-{h[:3].upper()}"

# -----------------------------------------------------------------------------
# DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    path = "demo.wav"
    if os.path.exists(path):
        out = classify_tone_intent(path)
        print("\n--- CLASSIFIED ---")
        for k, v in out.items():
            print(f"{k:12}: {v}")
    else:
        print("No demo.wav found.")

