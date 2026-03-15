from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from empathy_engine.service import AnalysisResult, EmpathyEngineService

app = FastAPI(title="Empathy Engine API", version="1.0.0")
service = EmpathyEngineService(output_dir="output")
web_dir = Path("web")

if (web_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(web_dir / "assets")), name="assets")


class SynthesisRequest(BaseModel):
    text: str = Field(min_length=1, description="Input text to convert into expressive speech")


class SynthesisResponse(BaseModel):
    audio_path: str
    emotion: str
    sentiment_score: float
    intensity: float
    voice_profile: dict
    ssml: str


class AnalysisResponse(BaseModel):
    emotion: str
    sentiment_score: float
    intensity: float
    voice_profile: dict
    ssml: str


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    index_path = web_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Web UI not found")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/synthesize", response_model=SynthesisResponse)
def synthesize(payload: SynthesisRequest) -> SynthesisResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text is empty")

    result = service.synthesize(text)
    return SynthesisResponse(**result.__dict__)


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: SynthesisRequest) -> AnalysisResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text is empty")

    result: AnalysisResult = service.analyze(text)
    return AnalysisResponse(**result.__dict__)


@app.post("/synthesize/audio")
def synthesize_audio(payload: SynthesisRequest) -> FileResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text is empty")

    result = service.synthesize(text)
    return FileResponse(result.audio_path, media_type="audio/mpeg", filename="empathy.mp3")


@app.post("/ssml")
def generate_ssml(payload: SynthesisRequest) -> dict:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text is empty")

    result: AnalysisResult = service.analyze(text)
    return {
        "emotion": result.emotion,
        "sentiment_score": result.sentiment_score,
        "intensity": result.intensity,
        "ssml": result.ssml,
    }
