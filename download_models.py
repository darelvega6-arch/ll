#!/usr/bin/env python3
import whisper
from TTS.api import TTS
import torch

print("=" * 50)
print("Descargando modelos de IA...")
print("=" * 50)

print("\n1. Whisper (transcripción)...")
whisper.load_model("base")
print("✓ Whisper listo")

print("\n2. XTTS v2 (clonación de voz)...")
print("   Esto puede tomar 5-10 minutos...")
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print("✓ XTTS v2 listo")

print("\n" + "=" * 50)
print("¡Todos los modelos descargados!")
print("=" * 50)
