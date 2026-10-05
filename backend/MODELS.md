# Friday - Kullanılabilir Dil Modelleri

## Yerleşik Modeller (Ollama)

Her model Ollama tarafından yönetilir. İndirmek için:

```bash
ollama pull model_name
```

### Hafif Modeller (Hızlı, Az Bellek)

- **Gemma 2 2B** - `gemma2:2b`
- **Orca Mini 3B** - `orca-mini:3b`
- **Gemma 3 4B** - `gemma3:4b` ⭐ Varsayılan

### Orta Modeller (Dengeli)

- **Mistral 7B** - `mistral:7b`
- **Neural Chat 7B** - `neural-chat:7b`
- **OpenChat 7B** - `openchat:7b`
- **Llama 2 7B** - `llama2:7b`

### Büyük Modeller (Güçlü, Yavaş)

- **Gemma 3 12B** - `gemma3:12b`
- **Llama 2 13B** - `llama2:13b`
- **Dolphin Mixtral** - `dolphin-mixtral:8x7b`

## Öneriler

### Telefon/Emülatör için
```bash
ollama pull gemma3:4b
```

### Daha iyi cevaplar için
```bash
ollama pull gemma3:12b
ollama pull mistral:7b
```

## Model Değiştirme

### Backend API

```json
{
  "message": "Merhaba",
  "model": "mistral:7b",
  "temperature": 0.7
}
```

## API Endpoints

```bash
# Mevcut modelleri listele
GET /models

# Sağlık kontrolü
GET /api/health

# Sohbet
POST /api/chat
{"message": "Merhaba", "model": "gemma3:4b"}

# Görsel üret
POST /api/image
{"prompt": "Güzel bir gün batımı"}
```
