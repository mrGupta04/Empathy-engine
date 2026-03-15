from __future__ import annotations

from xml.sax.saxutils import escape


def _inject_breaks(text: str) -> str:
    chunks = []
    for token in text.split():
        stripped = token.strip()
        escaped = escape(stripped)

        if stripped.endswith("!"):
            chunks.append(f"<emphasis level=\"strong\">{escaped}</emphasis>")
            chunks.append("<break time=\"180ms\"/>")
        elif stripped.endswith("?"):
            chunks.append(f"<emphasis level=\"moderate\">{escaped}</emphasis>")
            chunks.append("<break time=\"220ms\"/>")
        elif stripped.endswith((".", ",", ";", ":")):
            chunks.append(escaped)
            chunks.append("<break time=\"140ms\"/>")
        else:
            chunks.append(escaped)

    return " ".join(chunks).strip()


def build_ssml(
    text: str,
    voice: str,
    rate_percent: int,
    pitch_hz: int,
    volume_percent: int,
) -> str:
    prosody_rate = f"{rate_percent:+d}%"
    prosody_pitch = f"{pitch_hz:+d}Hz"
    prosody_volume = f"{volume_percent:+d}%"

    ssml_body = _inject_breaks(text)

    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        f'<voice name="{escape(voice)}">'
        f'<prosody rate="{prosody_rate}" pitch="{prosody_pitch}" volume="{prosody_volume}">'
        f"{ssml_body}"
        "</prosody>"
        "</voice>"
        "</speak>"
    )
