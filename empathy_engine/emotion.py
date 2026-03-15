from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@dataclass(frozen=True)
class EmotionResult:
    label: str
    sentiment_score: float
    intensity: float


class EmotionDetector:
    """Rule-assisted sentiment detector with intensity estimation."""

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def detect(self, text: str) -> EmotionResult:
        cleaned = text.strip()
        if not cleaned:
            return EmotionResult(label="neutral", sentiment_score=0.0, intensity=0.0)

        scores: Dict[str, float] = self._analyzer.polarity_scores(cleaned)
        compound = scores["compound"]

        label = self._label_from_score(cleaned, compound)
        intensity = min(1.0, abs(compound) + self._emphasis_boost(cleaned))

        return EmotionResult(label=label, sentiment_score=compound, intensity=intensity)

    def _label_from_score(self, text: str, compound: float) -> str:
        lowered = text.lower()

        concern_tokens = (
            "sorry",
            "concern",
            "worried",
            "unfortunately",
            "issue",
            "wrong",
            "frustrat",
            "problem",
            "error",
            "failed",
            "failure",
        )

        question_tokens = ("how", "what", "why", "could", "can", "would", "when", "where")

        if any(token in lowered for token in ("surprised", "wow", "unbelievable", "shocked", "amazing")):
            return "surprised"

        # Prefer a calming tone for support/problem statements and "what went wrong" style questions.
        if any(token in lowered for token in concern_tokens):
            if compound <= 0.2:
                return "concerned"

        if "?" in text and "wrong" in lowered:
            return "concerned"

        if "?" in text and compound > -0.45 and any(token in lowered for token in question_tokens):
            return "inquisitive"

        if compound >= 0.25:
            return "positive"
        if compound <= -0.25:
            return "negative"
        return "neutral"

    def _emphasis_boost(self, text: str) -> float:
        exclamations = text.count("!")
        uppercase_tokens = [t for t in text.split() if len(t) > 2 and t.isupper()]
        elongated_tokens = [t for t in text.split() if len(t) > 3 and t[-1] == t[-2]]

        boost = min(0.25, exclamations * 0.04)
        boost += min(0.2, len(uppercase_tokens) * 0.05)
        boost += min(0.15, len(elongated_tokens) * 0.05)

        return boost
