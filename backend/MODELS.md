# Friday - Dil Modelleri (Ollama + Anthropic Claude)

## Ollama Modelleri (Local)

### Hafif Modeller
- **Gemma 2 2B** - `gemma2:2b`
- **Orca Mini 3B** - `orca-mini:3b`
- **Gemma 3 4B** - `gemma3:4b` ⭐ Varsayılan

### Orta Modeller
- **Mistral 7B** - `mistral:7b`
- **Neural Chat 7B** - `neural-chat:7b`
- **OpenChat 7B** - `openchat:7b`
- **Llama 2 7B** - `llama2:7b`

### Büyük Modeller
- **Gemma 3 12B** - `gemma3:12b`
- **Llama 2 13B** - `llama2:13b`
- **Dolphin Mixtral** - `dolphin-mixtral:8x7b`

## Claude Modelleri (Anthropic API)

### Kullanılabilir
- **Claude 3.5 Sonnet** - `claude-3-5-sonnet-20241022` ⭐ Dengeli
- **Claude 3.5 Opus** - `claude-3-5-opus-20241022` 🚀 En güçlü

## Kurulum

### Ollama Modelleri
```bash
ollama pull gemma3:4b
ollama pull mistral:7b
ollama pull gemma3:12b
ollama serve
```

### Claude API
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## Backend Başlatma

```bash
cd Friday/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## API Örnekleri

### Ollama Modeli (Local)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Merhaba",
    "model": "gemma3:4b",
    "temperature": 0.7
  }'
```

### Claude Sonnet (Hızlı & Dengeli)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Merhaba",
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.7
  }'
```

### Claude Opus (En Güçlü)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Merhaba",
    "model": "claude-3-5-opus-20241022",
    "temperature": 0.7
  }'
```

### Görsel Üretme
```bash
curl -X POST http://localhost:8000/api/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "futuristic city at sunset"
  }'
```

### Mevcut Modelleri Listele
```bash
curl http://localhost:8000/models
```

### Sistem Sağlığı
```bash
curl http://localhost:8000/api/health
```

## Performans Karşılaştırması

| Model | Boyut | Hız | Kalite | Maliyet | Tavsiye |
|-------|-------|-----|--------|---------|----------|
| gemma2:2b | 2B | ⚡⚡⚡ | ⭐⭐ | Ücretsiz | Çok hafif |
| gemma3:4b | 4B | ⚡⚡ | ⭐⭐⭐⭐ | Ücretsiz | **Default** |
| mistral:7b | 7B | ⚡ | ⭐⭐⭐⭐ | Ücretsiz | Orta |
| claude-3-5-sonnet | L | ⚡ | ⭐⭐⭐⭐⭐ | Ucuz | Dengeli |
| claude-3-5-opus | XL | ⚠️ | ⭐⭐⭐⭐⭐ | Orta | En güçlü |
| gemma3:12b | 12B | ⚠️ | ⭐⭐⭐⭐⭐ | Ücretsiz | Güçlü Local |

## İleri Ayarlar

### Temperature (Yaratıcılık)
- 0.0 - 0.3: Tutarlı, deterministik
- 0.7 (default): Dengeli
- 0.9 - 1.0: Yaratıcı, çeşitli

### Top P (Çeşitlilik)
- 0.9 (default): Dengeli
- 0.5: Daha tutarlı
- 1.0: Tam çeşitlilik

## Sorun Giderme

### "Model not found"
```bash
ollama pull model_name
```

### Anthropic hatası
```bash
export ANTHROPIC_API_KEY="your-key"
```

### Ollama bağlantı hatası
```bash
ollama serve
```

### Yavaş cevap
- Daha hafif model seç (gemma3:4b)
- Temperature azalt (0.3)
- Prompt'u kısalt
