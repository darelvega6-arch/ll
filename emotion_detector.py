import librosa
import numpy as np
import soundfile as sf

class EmotionDetector:
    def __init__(self):
        self.emotions = {
            'neutral': {'speed': 1.0, 'pitch': 0, 'energy': 1.0},
            'happy': {'speed': 1.1, 'pitch': 2, 'energy': 1.2},
            'sad': {'speed': 0.9, 'pitch': -2, 'energy': 0.8},
            'angry': {'speed': 1.15, 'pitch': 1, 'energy': 1.3},
            'excited': {'speed': 1.2, 'pitch': 3, 'energy': 1.4}
        }
    
    def analyze_emotion(self, audio_path):
        """Analiza la emoción del audio"""
        y, sr = librosa.load(audio_path, sr=22050)
        
        # Extraer características
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        rms = np.mean(librosa.feature.rms(y=y))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # Clasificar emoción basada en características
        emotion = 'neutral'
        
        if tempo > 140 and rms > 0.05:
            emotion = 'excited'
        elif tempo > 120 and spectral_centroid > 2000:
            emotion = 'happy'
        elif tempo < 80 and rms < 0.03:
            emotion = 'sad'
        elif rms > 0.06 and zcr > 0.1:
            emotion = 'angry'
        
        params = self.emotions[emotion]
        
        print(f"🎭 Emoción detectada: {emotion.upper()}")
        print(f"   Tempo: {float(tempo):.1f} BPM")
        print(f"   Energía: {float(rms):.3f}")
        print(f"   Tono promedio: {float(spectral_centroid):.1f} Hz")
        
        return emotion, params
    
    def apply_emotion_to_audio(self, audio_path, output_path, emotion_params):
        """Aplica parámetros emocionales al audio"""
        y, sr = librosa.load(audio_path, sr=44100)  # Mayor calidad
        
        # Ajustar velocidad suavemente
        if emotion_params['speed'] != 1.0:
            speed_factor = 1.0 + (emotion_params['speed'] - 1.0) * 0.5  # Suavizar
            y = librosa.effects.time_stretch(y, rate=speed_factor)
        
        # Ajustar tono suavemente
        if emotion_params['pitch'] != 0:
            pitch_steps = emotion_params['pitch'] * 0.5  # Suavizar
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_steps)
        
        # Ajustar energía suavemente
        energy_factor = 1.0 + (emotion_params['energy'] - 1.0) * 0.3  # Suavizar
        y = y * energy_factor
        
        # Normalizar con compresión dinámica
        max_val = np.max(np.abs(y))
        if max_val > 0:
            y = y / max_val * 0.98
        
        sf.write(output_path, y, sr)
        return output_path
