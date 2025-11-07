import os
import subprocess
from deep_translator import GoogleTranslator
import whisper
from TTS.api import TTS
import torch
from pydub import AudioSegment
from audio_separator import AudioSeparator
from emotion_detector import EmotionDetector

class VideoProcessor:
    def __init__(self):
        print("🚀 Cargando modelos de IA avanzados...")
        self.whisper_model = whisper.load_model("medium")  # Mejor modelo
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"💻 Usando dispositivo: {self.device}")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.audio_separator = AudioSeparator()
        self.emotion_detector = EmotionDetector()
        print("✅ Modelos cargados - Calidad PREMIUM")
        
    def extract_audio(self, video_path, audio_path):
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path, '-y'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        audio = AudioSegment.from_wav(audio_path)
        return len(audio) / 1000.0
    
    def transcribe_audio(self, audio_path):
        result = self.whisper_model.transcribe(audio_path, fp16=False)
        text = result['text'].strip()
        language = result['language']
        
        if not text:
            raise Exception("No se detectó voz en el audio")
        
        return text, language
    
    def translate_text(self, text, target_lang):
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    
    def synthesize_speech(self, text, target_lang, output_path, reference_audio, emotion_params=None):
        # XTTS v2 clona la voz con parámetros emocionales
        temp_output = "temp_synthesis.wav"
        
        # Mejorar calidad de síntesis
        self.tts.tts_to_file(
            text=text,
            speaker_wav=reference_audio,
            language=target_lang,
            file_path=temp_output,
            speed=emotion_params.get('speed', 1.0) if emotion_params else 1.0,
            split_sentences=True  # Mejor prosodia
        )
        
        # Aplicar ajustes emocionales
        if emotion_params:
            self.emotion_detector.apply_emotion_to_audio(temp_output, output_path, emotion_params)
            if os.path.exists(temp_output):
                os.remove(temp_output)
        else:
            os.rename(temp_output, output_path)
    
    def process_video(self, video_path, target_lang, output_path, keep_background=True, progress_callback=None):
        temp_audio = "temp_audio.wav"
        vocals_audio = "vocals.wav"
        background_audio = "background.wav"
        dubbed_vocals = "dubbed_vocals.wav"
        final_audio = "final_audio.wav"
        
        try:
            print("🎬 Extrayendo audio del video...")
            self.extract_audio(video_path, temp_audio)
            
            # Detectar número de hablantes
            num_speakers = self.audio_separator.detect_speakers(temp_audio)
            print(f"👥 Detectados {num_speakers} hablante(s) en el video")
            
            # Separar voces del fondo
            print("🎵 Separando voces del audio de fondo...")
            vocals_audio, background_audio = self.audio_separator.separate_vocals_background(
                temp_audio, "./temp"
            )
            
            # Detectar emoción en la voz original
            print("🎭 Analizando emociones en la voz...")
            emotion, emotion_params = self.emotion_detector.analyze_emotion(vocals_audio)
            
            print("🎤 Transcribiendo con Whisper AI...")
            text, source_lang = self.transcribe_audio(vocals_audio)
            
            if not text or len(text.strip()) == 0:
                raise Exception("No se detectó voz en el audio")
            
            print(f"📝 Detectado ({source_lang}): '{text[:60]}...'")
            print(f"🌍 Traduciendo a {target_lang}...")
            translated_text = self.translate_text(text, target_lang)
            
            if not translated_text:
                raise Exception("Error en la traducción")
            
            print(f"✨ CLONANDO VOZ con emoción {emotion.upper()}...")
            self.synthesize_speech(translated_text, target_lang, dubbed_vocals, vocals_audio, emotion_params)
            
            # Mezclar con fondo si se solicita
            if keep_background and os.path.exists(background_audio):
                print("🎚️ Mezclando voces dobladas con audio de fondo (50% volumen)...")
                self.audio_separator.mix_audio(dubbed_vocals, background_audio, final_audio, 0.5)
            else:
                print("🔇 Generando sin audio de fondo...")
                final_audio = dubbed_vocals
            
            print("🎬 Generando video final...")
            self.merge_audio_video(video_path, final_audio, output_path)
            
            self.cleanup([temp_audio, vocals_audio, background_audio, dubbed_vocals, final_audio])
            
            return output_path, num_speakers, emotion
        except Exception as e:
            self.cleanup([temp_audio, vocals_audio, background_audio, dubbed_vocals, final_audio])
            raise e
    
    def merge_audio_video(self, video_path, audio_path, output_path):
        subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_path, '-y'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def cleanup(self, files):
        for file in files:
            if os.path.exists(file):
                os.remove(file)
