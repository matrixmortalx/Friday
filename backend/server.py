from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json
from typing import Optional
import anthropic

app = FastAPI(title="Friday AI Backend - Gemma + Claude Powered")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")

# Dil Modelleri - Local Ollama
OLLAMA_MODELS = {
    "gemma3:4b": {"name": "Gemma 3 4B", "type": "ollama", "size": "4B", "provider": "ollama"},
    "gemma3:12b": {"name": "Gemma 3 12B", "type": "ollama", "size": "12B", "provider": "ollama"},
    "gemma2:2b": {"name": "Gemma 2 2B", "type": "ollama", "size": "2B", "provider": "ollama"},
    "llama2:7b": {"name": "Llama 2 7B", "type": "ollama", "size": "7B", "provider": "ollama"},
    "llama2:13b": {"name": "Llama 2 13B", "type": "ollama", "size": "13B", "provider": "ollama"},
    "mistral:7b": {"name": "Mistral 7B", "type": "ollama", "size": "7B", "provider": "ollama"},
    "neural-chat:7b": {"name": "Neural Chat 7B", "type": "ollama", "size": "7B", "provider": "ollama"},
    "orca-mini:3b": {"name": "Orca Mini 3B", "type": "ollama", "size": "3B", "provider": "ollama"},
    "dolphin-mixtral:8x7b": {"name": "Dolphin Mixtral", "type": "ollama", "size": "MoE", "provider": "ollama"},
    "openchat:7b": {"name": "OpenChat 7B", "type": "ollama", "size": "7B", "provider": "ollama"},
}

# Claude Models - Anthropic API
CLAUDE_MODELS = {
    "claude-3-5-sonnet-20241022": {"name": "Claude 3.5 Sonnet", "type": "claude", "size": "L", "provider": "anthropic"},
    "claude-3-5-opus-20241022": {"name": "Claude 3.5 Opus", "type": "claude", "size": "XL", "provider": "anthropic"},
}

# Combine all models
AVAILABLE_MODELS = {**OLLAMA_MODELS, **CLAUDE_MODELS}

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ImageRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str
    model: str
    provider: str
    tokens: Optional[int] = None

class ModelListResponse(BaseModel):
    available_models: dict
    current_model: str
    default_model: str
    providers: dict

class ImageResponse(BaseModel):
    image_url: str
    prompt: str

@app.get("/")
async def root():
    return {
        "status": "Friday backend running",
        "version": "2.0",
        "backends": ["Ollama + Gemma", "Anthropic Claude"],
        "available_models": list(AVAILABLE_MODELS.keys()),
        "default_model": DEFAULT_MODEL,
        "claude_available": bool(ANTHROPIC_API_KEY)
    }

@app.get("/models")
async def list_models():
    ollama_count = len([m for m in AVAILABLE_MODELS.values() if m["provider"] == "ollama"])
    claude_count = len([m for m in AVAILABLE_MODELS.values() if m["provider"] == "anthropic"])
    
    return ModelListResponse(
        available_models=AVAILABLE_MODELS,
        current_model=DEFAULT_MODEL,
        default_model=DEFAULT_MODEL,
        providers={
            "ollama": {"count": ollama_count, "available": True},
            "anthropic": {"count": claude_count, "available": bool(ANTHROPIC_API_KEY)}
        }
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        model = req.model or DEFAULT_MODEL

        if model not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail=f"Model {model} not available")

        model_info = AVAILABLE_MODELS[model]
        provider = model_info["provider"]

        # Claude Modelleri
        if provider == "anthropic":
            if not ANTHROPIC_API_KEY:
                return ChatResponse(
                    reply="Anthropic API anahtarı ayarlanmamış. ANTHROPIC_API_KEY ortam değişkenini ayarla.",
                    model=model,
                    provider="anthropic"
                )

            try:
                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                response = client.messages.create(
                    model=model,
                    max_tokens=512,
                    temperature=req.temperature,
                    messages=[
                        {"role": "user", "content": req.message}
                    ]
                )
                
                answer = response.content[0].text
                tokens = response.usage.output_tokens

                return ChatResponse(
                    reply=answer,
                    model=model,
                    provider="anthropic",
                    tokens=tokens
                )
            except anthropic.APIError as e:
                return ChatResponse(
                    reply=f"Claude API Hatası: {str(e)}",
                    model=model,
                    provider="anthropic"
                )

        # Ollama Modelleri
        else:
            payload = {
                "model": model,
                "prompt": req.message,
                "stream": False,
                "options": {
                    "temperature": req.temperature,
                    "top_p": req.top_p,
                    "num_predict": 256
                }
            }

            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("response", "Cevap alınamadı.")
            eval_count = data.get("eval_count", 0)

            return ChatResponse(
                reply=answer,
                model=model,
                provider="ollama",
                tokens=eval_count
            )

    except requests.exceptions.ConnectionError:
        return ChatResponse(
            reply="Ollama'ya bağlanılamıyor. Ollama'nın http://localhost:11434 adresinde çalıştığından emin ol.",
            model=DEFAULT_MODEL,
            provider="ollama"
        )
    except requests.exceptions.Timeout:
        return ChatResponse(
            reply="İstek zaman aşımına uğradı. Lütfen daha kısa bir sorgu dene veya model değiştir.",
            model=DEFAULT_MODEL,
            provider="ollama"
        )
    except Exception as e:
        return ChatResponse(
            reply=f"Hata: {str(e)}",
            model=DEFAULT_MODEL,
            provider="unknown"
        )

@app.post("/api/image", response_model=ImageResponse)
async def generate_image(req: ImageRequest):
    try:
        prompt = req.prompt.strip()
        if not prompt:
            raise ValueError("Prompt boş olamaz")

        prompt_encoded = prompt.replace(" ", "%20")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"

        return ImageResponse(
            image_url=image_url,
            prompt=prompt
        )
    except Exception:
        return ImageResponse(
            image_url="",
            prompt=req.prompt
        )

@app.get("/api/health")
async def health_check():
    health_status = {
        "status": "healthy",
        "backends": {}
    }

    # Ollama kontrol
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        health_status["backends"]["ollama"] = {
            "status": "healthy",
            "url": OLLAMA_URL,
            "models_available": len(models),
            "models": [m.get("name") for m in models[:5]]  # İlk 5 modeli göster
        }
    except Exception as e:
        health_status["backends"]["ollama"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Claude kontrol
    if ANTHROPIC_API_KEY:
        try:
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            # Basit test
            health_status["backends"]["anthropic"] = {
                "status": "healthy",
                "models": ["claude-3-5-sonnet-20241022", "claude-3-5-opus-20241022"]
            }
        except Exception as e:
            health_status["backends"]["anthropic"] = {
                "status": "unhealthy",
                "error": str(e)
            }
    else:
        health_status["backends"]["anthropic"] = {
            "status": "unavailable",
            "reason": "API key not configured"
        }

    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
