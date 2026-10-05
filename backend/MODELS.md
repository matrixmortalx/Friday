# Friday - Kullanılabilir Dil Modelleri

## Yerleşik Modeller (Ollama)

Her model Ollama tarafından yönetilir. İndirmek için:

```bash
ollama pull model_name
```

### Hafif Modeller (Hızlı, Az Bellek)

- **Gemma 2 2B** - `gemma2:2b` ⭐ Çok hafif, hızlı
- **Orca Mini 3B** - `orca-mini:3b` - Küçük, etkili
- **Gemma 3 4B** - `gemma3:4b` ⭐ Tavsiye edilir (varsayılan)

### Orta Modeller (Dengeli)

- **Mistral 7B** - `mistral:7b` - Hızlı, iyi kalite
- **Neural Chat 7B** - `neural-chat:7b` - Konuşmaya uygun
- **OpenChat 7B** - `openchat:7b` - Açık kaynak, iyi
- **Llama 2 7B** - `llama2:7b` - Meta tarafından

### Büyük Modeller (Güçlü, Yavaş)

- **Gemma 3 12B** - `gemma3:12b` - Daha güçlü
- **Llama 2 13B** - `llama2:13b` - Daha yapay zeka
- **Dolphin Mixtral** - `dolphin-mixtral:8x7b` - Mixture of Experts

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

### Çok Hafif (Eski Cihazlar)
```bash
ollama pull gemma2:2b
ollama pull orca-mini:3b
```

## Modelleri İndirme

```bash
# Tümünü indir
for model in gemma3:4b gemma3:12b mistral:7b llama2:7b neural-chat:7b; do
  ollama pull $model
done

# Veya tek tek
ollama pull gemma3:4b
ollama pull mistral:7b
```

## Model Değiştirme

### Android Uygulaması

Ayarlar menüsünde model seçebilir.

### Web Arayüzü

`www/index.html` dosyasında:
```js
const MODEL = 'gemma3:4b';
```

### Backend API

Chat isteğinde model belirtebilir:
```json
{
  "message": "Merhaba",
  "model": "mistral:7b",
  "temperature": 0.7
}
```

## Performans Karşılaştırması

| Model | Boyut | Hız | Kalite | Bellek | Tavsiye |
|-------|-------|-----|--------|--------|----------|
| gemma2:2b | 2B | ⚡⚡⚡ | ⭐⭐ | 2GB | Çok hafif |
| orca-mini:3b | 3B | ⚡⚡⚡ | ⭐⭐⭐ | 3GB | Hafif |
| gemma3:4b | 4B | ⚡⚡ | ⭐⭐⭐⭐ | 4GB | **Tavsiye** |
| mistral:7b | 7B | ⚡ | ⭐⭐⭐⭐ | 7GB | Orta |
| gemma3:12b | 12B | ⚠️ | ⭐⭐⭐⭐⭐ | 12GB | Güçlü |
| llama2:13b | 13B | ⚠️ | ⭐⭐⭐⭐⭐ | 13GB | Çok güçlü |

## Sorun Giderme

### "Model not found" hatası
```bash
ollama pull model_name
```

### Çok yavaş cevap
- Daha hafif model seç (gemma2:2b)
- Bilgisayarı kontrol et
- Diğer programları kapat

### Hatalı cevaplar
- Temperature değerini azalt (0.3-0.5)
- Prompt'u daha spesifik yap
- Daha büyük model dene

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

# Model indir
POST /api/models/download?model_name=mistral:7b
```
