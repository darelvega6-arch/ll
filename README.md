# 🎬 Bot de Doblaje de Videos con IA - VERSIÓN ÉPICA

Bot de Telegram profesional que dobla videos a diferentes idiomas usando inteligencia artificial avanzada para clonar voces con emociones.

## 🌟 Características ÉPICAS

### 🎭 Clonación de Voz con Emociones
- ✅ **XTTS v2** - Clonación de voz ultra realista
- ✅ **Detección de emociones** - Analiza y replica: felicidad, tristeza, enojo, emoción
- ✅ **Ajuste automático** de tono, velocidad y energía según la emoción
- ✅ **Voces naturales** que suenan como la persona original

### 👥 Detección Inteligente de Hablantes
- ✅ Detecta automáticamente cuántas personas hablan
- ✅ Identifica cambios de hablante en tiempo real
- ✅ Procesa múltiples voces en el mismo video

### 🎵 Separación Profesional de Audio
- ✅ **Demucs** (Meta AI) - Separa voces del fondo
- ✅ Mantiene música y efectos de sonido originales
- ✅ Opción de mantener o quitar audio de fondo
- ✅ Mezcla profesional con balance ajustable

### 📊 Animaciones de Progreso en Tiempo Real
- ✅ Barras de progreso animadas
- ✅ Iconos dinámicos que cambian
- ✅ Información detallada de cada etapa
- ✅ Experiencia visual interactiva

### 🌍 Transcripción y Traducción Avanzada
- ✅ **Whisper AI** - Transcripción de alta precisión
- ✅ Detección automática de idioma
- ✅ Traducción con Google Translator
- ✅ 10+ idiomas soportados

## 🚀 Instalación

### Requisitos previos

1. Python 3.8+
2. FFmpeg
3. 4GB RAM mínimo (8GB recomendado)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Instalación rápida

```bash
# Clonar repositorio
git clone <repo>
cd ll

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar bot
python bot.py
```

## 🎯 Uso

### Comandos del Bot

- `/start` - Iniciar el bot
- `/help` - Ver ayuda
- `/languages` - Ver idiomas disponibles

### Proceso de Doblaje

1. **Envía un video** (máx. 50MB)
2. **Selecciona idioma** de destino
3. **Elige audio de fondo**:
   - 🎵 Con música/efectos originales
   - 🔇 Solo voces dobladas
4. **Espera el proceso** (con animaciones en tiempo real)
5. **Recibe tu video** con:
   - Voz clonada con emociones
   - Número de hablantes detectados
   - Audio de fondo (si elegiste)

## 🛠️ Modelos de IA Utilizados

### 1. **Whisper** (OpenAI)
- Transcripción de audio profesional
- Detección automática de idioma
- 99+ idiomas soportados

### 2. **Coqui XTTS v2**
- Clonación de voz multilingüe
- Solo necesita 6 segundos de audio
- 17+ idiomas con voces naturales
- Soporte para emociones

### 3. **Demucs** (Meta AI)
- Separación de audio estado del arte
- Separa voces, música, bajo y batería
- Calidad profesional

### 4. **Librosa**
- Análisis de emociones en audio
- Detección de tempo, tono y energía
- Procesamiento de señales avanzado

### 5. **Google Translator**
- Traducción automática gratuita
- 100+ idiomas
- Sin API key necesaria

## 📊 Arquitectura del Sistema

```
Video → Extracción Audio → Separación (Demucs)
                              ↓
                    Voces ← → Fondo
                      ↓
              Detección Hablantes
                      ↓
              Análisis Emociones
                      ↓
              Transcripción (Whisper)
                      ↓
              Traducción (Google)
                      ↓
        Síntesis con Emociones (XTTS v2)
                      ↓
              Mezcla con Fondo
                      ↓
              Video Final Doblado
```

## 🌍 Idiomas Soportados

- 🇪🇸 Español (es)
- 🇬🇧 English (en)
- 🇫🇷 Français (fr)
- 🇩🇪 Deutsch (de)
- 🇮🇹 Italiano (it)
- 🇵🇹 Português (pt)
- 🇷🇺 Русский (ru)
- 🇯🇵 日本語 (ja)
- 🇨🇳 中文 (zh)
- 🇸🇦 العربية (ar)

## ⚙️ Características Técnicas

### Detección de Emociones
- **Happy** 😄: Velocidad +10%, Tono +2, Energía +20%
- **Sad** 😢: Velocidad -10%, Tono -2, Energía -20%
- **Angry** 😡: Velocidad +15%, Tono +1, Energía +30%
- **Excited** 🤩: Velocidad +20%, Tono +3, Energía +40%
- **Neutral** 😐: Sin ajustes

### Separación de Audio
- Voces: Extraídas con alta fidelidad
- Fondo: Música, efectos, ambiente
- Mezcla: 30% fondo, 100% voces (ajustable)

### Optimizaciones
- Procesamiento por segmentos
- GPU automática si disponible
- Limpieza automática de archivos
- Manejo robusto de errores

## 📦 Estructura del Proyecto

```
ll/
├── bot.py                    # Bot principal con animaciones
├── video_processor.py        # Motor de procesamiento
├── audio_separator.py        # Separación de audio
├── emotion_detector.py       # Detección de emociones
├── progress_animator.py      # Animaciones de progreso
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
├── download_models.py        # Descarga de modelos
├── README.md                 # Documentación
├── temp/                     # Archivos temporales
└── output/                   # Videos procesados
```

## 🔧 Configuración Avanzada

### Ajustar volumen de fondo

En `audio_separator.py`:
```python
self.mix_audio(vocals, background, output, background_volume=0.3)  # 30%
```

### Cambiar modelo de Whisper

En `video_processor.py`:
```python
self.whisper_model = whisper.load_model("medium")  # base, small, medium, large
```

### Forzar CPU/GPU

En `video_processor.py`:
```python
self.device = "cpu"  # o "cuda"
```

## 🚀 Mejoras Futuras

- [ ] Soporte para videos largos (>10 min)
- [ ] Múltiples voces simultáneas
- [ ] Subtítulos automáticos
- [ ] Interfaz web
- [ ] API REST
- [ ] Procesamiento en lote

## 📄 Licencias

- Whisper: MIT License
- Coqui TTS: MPL 2.0 License (uso no comercial)
- Demucs: MIT License
- python-telegram-bot: LGPLv3

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/amazing`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing`)
5. Abre un Pull Request

## 📧 Soporte

Para problemas o preguntas, abre un issue en GitHub.

## 🎉 Créditos

Desarrollado con ❤️ usando:
- OpenAI Whisper
- Coqui TTS
- Meta Demucs
- Librosa
- Python Telegram Bot

---

**¡Disfruta doblando videos con IA de nivel profesional!** 🎬✨
