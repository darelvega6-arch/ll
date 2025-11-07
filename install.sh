#!/bin/bash

echo "🎬 Instalando Bot de Doblaje de Videos con IA..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg no está instalado. Instalando..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "❌ Por favor instala FFmpeg manualmente desde https://ffmpeg.org/download.html"
        exit 1
    fi
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios
mkdir -p temp output

echo "✅ Instalación completada!"
echo ""
echo "Para iniciar el bot:"
echo "  source venv/bin/activate"
echo "  python bot.py"
