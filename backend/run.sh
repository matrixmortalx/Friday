#!/bin/bash

# Friday Backend Starter Script

echo "🚀 Friday Backend Başlatılıyor..."

# Kontrol: Ollama çalışıyor mu?
echo "🔍 Ollama kontrol ediliyor..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama çalışmıyor!"
    echo "Lütfen Ollama'yı başlat:"
    echo "  ollama serve"
    exit 1
fi

echo "✅ Ollama bağlantısı OK"

# Virtual environment oluştur (varsa atla)
if [ ! -d ".venv" ]; then
    echo "📦 Virtual environment oluşturuluyor..."
    python -m venv .venv
fi

# Virtual environment'ı etkinleştir
echo "🔧 Virtual environment etkinleştiriliyor..."
source .venv/bin/activate 2>/dev/null || .venv\Scripts\activate 2>/dev/null

# Bağımlılıkları yükle
echo "📥 Bağımlılıklar yükleniyor..."
pip install -q -r requirements.txt

# Server başlat
echo "🎯 Server başlatılıyor... http://0.0.0.0:8000"
echo "Android: http://192.168.1.100:8000 (kendi IP'nizi yazın)"
echo "Web: http://localhost:8000"

uvicorn server:app --host 0.0.0.0 --port 8000 --reload
