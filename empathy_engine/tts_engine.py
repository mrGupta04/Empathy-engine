from __future__ import annotations

import asyncio
import pathlib
from dataclasses import dataclass
from datetime import datetime

import edge_tts

from empathy_engine.emotion import EmotionResult
from empathy_engine.ssml import build_ssml


@dataclass(frozen=True)
class VoiceProfile:
    rate_percent: int
    pitch_hz: int
    volume_percent: int


class VoiceModulator:
    """Maps emotion labels to TTS control parameters."""

    def profile_for(self, emotion: EmotionResult) -> VoiceProfile:
        i = emotion.intensity

        if emotion.label == "positive":
            return VoiceProfile(
                rate_percent=round(6 + (18 * i)),
                pitch_hz=round(8 + (22 * i)),
                volume_percent=round(4 + (14 * i)),
            )

        if emotion.label == "negative":
            return VoiceProfile(
                rate_percent=round(-4 - (14 * i)),
                pitch_hz=round(-8 - (20 * i)),
                volume_percent=round(-4 - (14 * i)),
            )

        if emotion.label == "concerned":
            return VoiceProfile(
                rate_percent=round(-2 - (10 * i)),
                pitch_hz=round(-2 - (8 * i)),
                volume_percent=round(-2 - (8 * i)),
            )

        if emotion.label == "surprised":
            return VoiceProfile(
                rate_percent=round(10 + (16 * i)),
                pitch_hz=round(16 + (26 * i)),
                volume_percent=round(8 + (14 * i)),
            )

        if emotion.label == "inquisitive":
            return VoiceProfile(
                rate_percent=round(2 + (8 * i)),
                pitch_hz=round(6 + (14 * i)),
                volume_percent=round(0 + (8 * i)),
            )

        return VoiceProfile(
            rate_percent=0,
            pitch_hz=0,
            volume_percent=0,
        )


class TTSEngine:
    """Generate expressive speech with edge-tts using dynamic controls."""

    def __init__(self, output_dir: str = "output", voice: str = "en-US-AriaNeural") -> None:
        self.output_dir = pathlib.Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice = voice
        self.modulator = VoiceModulator()

    def synthesize(self, text: str, emotion: EmotionResult) -> pathlib.Path:
        profile = self.modulator.profile_for(emotion)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        out_path = self.output_dir / f"empathy_{emotion.label}_{ts}.mp3"

        asyncio.run(self._synthesize_to_file(text, profile, out_path))

        return out_path

    def ssml_preview(self, text: str, emotion: EmotionResult) -> str:
        profile = self.modulator.profile_for(emotion)
        return build_ssml(
            text=text,
            voice=self.voice,
            rate_percent=profile.rate_percent,
            pitch_hz=profile.pitch_hz,
            volume_percent=profile.volume_percent,
        )

    async def _synthesize_to_file(self, text: str, profile: VoiceProfile, out_path: pathlib.Path) -> None:
        communicator = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self._signed_percent(profile.rate_percent),
            pitch=self._signed_hz(profile.pitch_hz),
            volume=self._signed_percent(profile.volume_percent),
        )
        await communicator.save(str(out_path))

    def _signed_percent(self, value: int) -> str:
        return f"{value:+d}%"

    def _signed_hz(self, value: int) -> str:
        return f"{value:+d}Hz"
