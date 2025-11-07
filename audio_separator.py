import subprocess
import os
import noisereduce as nr
import soundfile as sf
import numpy as np

class AudioSeparator:
    def __init__(self):
        self.demucs_available = True
    
    def separate_vocals_background(self, audio_path, output_dir):
        """Separa voces del fondo usando Demucs"""
        print("🎵 Separando voces del audio de fondo...")
        
        # Usar Demucs para separación profesional
        cmd = [
            'demucs',
            '--two-stems=vocals',
            '-n', 'htdemucs',
            '--out', output_dir,
            audio_path
        ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            # Encontrar archivos generados
            audio_name = os.path.splitext(os.path.basename(audio_path))[0]
            vocals_path = os.path.join(output_dir, 'htdemucs', audio_name, 'vocals.wav')
            background_path = os.path.join(output_dir, 'htdemucs', audio_name, 'no_vocals.wav')
            
            if os.path.exists(vocals_path) and os.path.exists(background_path):
                return vocals_path, background_path
        except:
            pass
        
        # Fallback: reducción de ruido simple
        return self.simple_vocal_extraction(audio_path, output_dir)
    
    def simple_vocal_extraction(self, audio_path, output_dir):
        """Extracción simple de voces usando reducción de ruido"""
        print("🎵 Usando extracción simple de voces...")
        
        data, rate = sf.read(audio_path)
        
        # Reducir ruido de fondo
        reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.8)
        
        vocals_path = os.path.join(output_dir, 'vocals_simple.wav')
        sf.write(vocals_path, reduced_noise, rate)
        
        # Crear audio de fondo (original - voces)
        background = data - reduced_noise
        background_path = os.path.join(output_dir, 'background_simple.wav')
        sf.write(background_path, background, rate)
        
        return vocals_path, background_path
    
    def detect_speakers(self, audio_path):
        """Detecta número de hablantes en el audio"""
        print("👥 Detectando número de hablantes...")
        
        # Análisis simple basado en energía y pausas
        data, rate = sf.read(audio_path)
        
        # Convertir a mono si es estéreo
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        # Calcular energía en ventanas
        window_size = int(rate * 0.5)  # 500ms
        energy = []
        
        for i in range(0, len(data) - window_size, window_size // 2):
            window = data[i:i + window_size]
            energy.append(np.sqrt(np.mean(window ** 2)))
        
        # Detectar cambios significativos (posibles cambios de hablante)
        energy = np.array(energy)
        threshold = np.mean(energy) * 0.3
        
        active_segments = energy > threshold
        changes = np.diff(active_segments.astype(int))
        num_changes = np.sum(np.abs(changes))
        
        # Estimar número de hablantes
        if num_changes < 5:
            return 1
        elif num_changes < 15:
            return 2
        else:
            return 3  # 3 o más
    
    def mix_audio(self, vocals_path, background_path, output_path, background_volume=0.5):
        """Mezcla voces dobladas con audio de fondo"""
        print(f"🎚️ Mezclando audio (fondo al {int(background_volume*100)}%)...")
        
        vocals, rate = sf.read(vocals_path)
        background, _ = sf.read(background_path)
        
        # Convertir a mono si es necesario
        if len(vocals.shape) > 1:
            vocals = np.mean(vocals, axis=1)
        if len(background.shape) > 1:
            background = np.mean(background, axis=1)
        
        # Ajustar longitudes
        min_len = min(len(vocals), len(background))
        vocals = vocals[:min_len]
        background = background[:min_len]
        
        # Mezclar con volumen ajustado
        mixed = vocals + (background * background_volume)
        
        # Normalizar
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.95
        
        sf.write(output_path, mixed, rate)
        return output_path
