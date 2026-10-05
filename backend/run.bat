@echo off
echo 🚀 Friday Backend Baslatiliyor...

echo 🔍 Ollama kontrol ediliyor...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama calismiyor!
    echo Lutfen Ollama'yi baslat:
    echo   ollama serve
    pause
    exit /b 1
)

echo ✅ Ollama baglantisi OK

if not exist ".venv" (
    echo 📦 Virtual environment olusturuluyor...
    python -m venv .venv
)

echo 🔧 Virtual environment etkinlestiriliyor...
call .venv\Scripts\activate

echo 📥 Bagimliliklar yukleniyor...
pip install -q -r requirements.txt

echo 🎯 Server baslatiliyor... http://0.0.0.0:8000
echo Android: http://192.168.1.100:8000 (kendi IP'nizi yazin)
echo Web: http://localhost:8000

uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
