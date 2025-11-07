#!/bin/bash

echo "🚀 Iniciando Bot de Doblaje de Videos..."

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python bot.py
