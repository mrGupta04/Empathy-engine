from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from empathy_engine.emotion import EmotionDetector, EmotionResult
from empathy_engine.tts_engine import TTSEngine, VoiceProfile


@dataclass(frozen=True)
class SynthesisResult:
    audio_path: str
    emotion: str
    sentiment_score: float
    intensity: float
    voice_profile: dict
    ssml: str


@dataclass(frozen=True)
class AnalysisResult:
    emotion: str
    sentiment_score: float
    intensity: float
    voice_profile: dict
    ssml: str


class EmpathyEngineService:
    def __init__(self, output_dir: str = "output") -> None:
        self.detector = EmotionDetector()
        self.tts = TTSEngine(output_dir=output_dir)

    def analyze(self, text: str) -> AnalysisResult:
        emotion: EmotionResult = self.detector.detect(text)
        return self._build_analysis(text, emotion)

    def _build_analysis(self, text: str, emotion: EmotionResult) -> AnalysisResult:
        profile: VoiceProfile = self.tts.modulator.profile_for(emotion)
        ssml: str = self.tts.ssml_preview(text, emotion)

        return AnalysisResult(
            emotion=emotion.label,
            sentiment_score=round(emotion.sentiment_score, 3),
            intensity=round(emotion.intensity, 3),
            voice_profile=asdict(profile),
            ssml=ssml,
        )

    def synthesize(self, text: str) -> SynthesisResult:
        emotion: EmotionResult = self.detector.detect(text)
        analysis = self._build_analysis(text, emotion)
        audio_path: Path = self.tts.synthesize(text, emotion)

        return SynthesisResult(
            audio_path=str(audio_path),
            emotion=analysis.emotion,
            sentiment_score=analysis.sentiment_score,
            intensity=analysis.intensity,
            voice_profile=analysis.voice_profile,
            ssml=analysis.ssml,
        )
