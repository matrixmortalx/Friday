from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json
from typing import Optional

app = FastAPI(title="Friday AI Backend - Gemma Powered")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")

AVAILABLE_MODELS = {
    "gemma3:4b": {"name": "Gemma 3 4B", "type": "ollama", "size": "4B"},
    "gemma3:12b": {"name": "Gemma 3 12B", "type": "ollama", "size": "12B"},
    "gemma2:2b": {"name": "Gemma 2 2B", "type": "ollama", "size": "2B"},
    "llama2:7b": {"name": "Llama 2 7B", "type": "ollama", "size": "7B"},
    "llama2:13b": {"name": "Llama 2 13B", "type": "ollama", "size": "13B"},
    "mistral:7b": {"name": "Mistral 7B", "type": "ollama", "size": "7B"},
    "neural-chat:7b": {"name": "Neural Chat 7B", "type": "ollama", "size": "7B"},
    "orca-mini:3b": {"name": "Orca Mini 3B", "type": "ollama", "size": "3B"},
    "dolphin-mixtral:8x7b": {"name": "Dolphin Mixtral", "type": "ollama", "size": "MoE"},
    "openchat:7b": {"name": "OpenChat 7B", "type": "ollama", "size": "7B"},
}

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
    tokens: Optional[int] = None

class ModelListResponse(BaseModel):
    available_models: dict
    current_model: str
    default_model: str

class ImageResponse(BaseModel):
    image_url: str
    prompt: str

@app.get("/")
async def root():
    return {
        "status": "Friday backend running",
        "version": "1.0",
        "backend": "Ollama + Gemma",
        "available_models": list(AVAILABLE_MODELS.keys()),
        "default_model": DEFAULT_MODEL
    }

@app.get("/models")
async def list_models():
    return ModelListResponse(
        available_models=AVAILABLE_MODELS,
        current_model=DEFAULT_MODEL,
        default_model=DEFAULT_MODEL
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        model = req.model or DEFAULT_MODEL

        if model not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail=f"Model {model} not available")

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
            tokens=eval_count
        )
    except requests.exceptions.ConnectionError:
        return ChatResponse(
            reply="Ollama'ya bağlanılamıyor. Ollama'nın http://localhost:11434 adresinde çalıştığından emin ol.",
            model=DEFAULT_MODEL
        )
    except requests.exceptions.Timeout:
        return ChatResponse(
            reply="İstek zaman aşımına uğradı. Lütfen daha kısa bir sorgu dene veya model değiştir.",
            model=DEFAULT_MODEL
        )
    except Exception as e:
        return ChatResponse(
            reply=f"Hata: {str(e)}",
            model=DEFAULT_MODEL
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
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        return {
            "status": "healthy",
            "ollama_url": OLLAMA_URL,
            "models_available": len(models),
            "models": [m.get("name") for m in models]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "ollama_url": OLLAMA_URL
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


