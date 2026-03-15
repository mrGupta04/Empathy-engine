# The Empathy Engine

The Empathy Engine is a Python service that transforms plain text into emotionally expressive speech.
It detects emotion from text, maps that emotion to a vocal profile, and generates a playable MP3 file
with dynamic modulation of speech rate, pitch, and volume.

## Challenge Coverage

| Requirement | Status | Where It Is Implemented |
| --- | --- | --- |
| Text input (CLI/API) | Complete | `main.py`, `api.py` |
| Emotion detection (>=3) | Complete | `empathy_engine/emotion.py` |
| Vocal modulation (>=2 params) | Complete | `empathy_engine/tts_engine.py` |
| Emotion-to-voice mapping | Complete | `VoiceModulator` in `empathy_engine/tts_engine.py` |
| Playable audio output | Complete | MP3 output in `output/` |
| Granular emotions | Complete | `inquisitive`, `concerned`, `surprised` |
| Intensity scaling | Complete | `EmotionDetector._emphasis_boost` + profile scaling |
| Web interface | Complete | `web/index.html`, served from `/` |
| SSML integration | Complete | `empathy_engine/ssml.py`, `/ssml`, `--show-ssml` |

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start API + Web UI:

```bash
uvicorn api:app --reload
```

3. Open the demo UI:

```bash
http://127.0.0.1:8000/
```

Note: `edge-tts` requires internet access.

## Features

- Text input through CLI, REST API, and browser UI.
- Emotion detection with six classes:
  - positive
  - negative
  - neutral
  - inquisitive
  - concerned
  - surprised
- Intensity scaling based on sentiment magnitude and text emphasis signals.
- Emotion-to-voice mapping across three vocal parameters:
  - rate (speed)
  - pitch
  - volume
- SSML generation with prosody and break tags for preview and integration.
- Playable MP3 audio output.

## Architecture Overview

1. Input text arrives through CLI or API.
2. `EmotionDetector` (VADER + rules) outputs:
   - label
   - sentiment score
   - intensity
3. `VoiceModulator` maps emotion + intensity to a `VoiceProfile`.
4. `TTSEngine`:
   - synthesizes speech with `edge-tts`
   - applies pitch/speed/volume via engine controls
   - exports final `.mp3` into `output/`
5. `SSML Builder` creates an expressive SSML representation with prosody and pauses.

## Emotion-to-Voice Mapping Logic

The service maps emotion to the following patterns:

- positive:
  - slightly faster speed, higher pitch, louder output
- negative:
  - slower speed, lower pitch, quieter output
- neutral:
  - no strong modulation
- inquisitive:
  - slight speed and pitch lift
- concerned:
  - slower and softer for patient, calming delivery
- surprised:
  - noticeably faster, brighter, and louder

Intensity scaling:

- Intensity is computed from sentiment magnitude, boosted by punctuation/uppercase emphasis.
- Larger intensity values cause larger parameter shifts.

## Project Structure

- `empathy_engine/emotion.py` - sentiment and emotion classification
- `empathy_engine/tts_engine.py` - TTS generation and audio modulation
- `empathy_engine/ssml.py` - SSML generation utilities
- `empathy_engine/service.py` - orchestration service
- `main.py` - CLI entrypoint
- `api.py` - FastAPI entrypoint
- `web/index.html` - browser demo page
- `web/assets/styles.css` - UI styling
- `web/assets/app.js` - browser-side API client

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run: CLI

Interactive prompt:

```bash
python main.py
```

Direct text argument:

```bash
python main.py --text "We are thrilled to share your order has shipped today!"
```

Custom output folder:

```bash
python main.py --text "I understand this issue is frustrating, and I am here to help." --output-dir output
```

Print generated SSML as well:

```bash
python main.py --text "Could you share more details about the error?" --show-ssml
```

The command prints detected emotion and generated file path.

## Run: API

Start server:

```bash
uvicorn api:app --reload
```

Optional: run scripted API checks in PowerShell:

```powershell
./docs/api-quick-tests.ps1
```

Health check:

```bash
GET http://127.0.0.1:8000/health
```

Analyze emotion and SSML (no audio generation):

```bash
POST http://127.0.0.1:8000/analyze
Content-Type: application/json
{
  "text": "Could you tell me what happened so I can help?"
}
```

Synthesize with metadata + saved audio path:

```bash
POST http://127.0.0.1:8000/synthesize
Content-Type: application/json
{
  "text": "Great news, your request is approved!"
}
```

Synthesize and receive playable audio directly:

```bash
POST http://127.0.0.1:8000/synthesize/audio
Content-Type: application/json
{
  "text": "I am sorry this happened. Let us fix it together."
}
```

Generate SSML preview directly:

```bash
POST http://127.0.0.1:8000/ssml
Content-Type: application/json
{
  "text": "This is the best news ever!"
}
```

## Demo Flow (2-3 Minutes)

1. Run `python main.py --text "Could you share more details?" --show-ssml`.
2. Show the detected emotion, intensity, profile, and generated SSML in CLI.
3. Start API server and open `/` in browser.
4. Enter one positive and one concerned customer message.
5. Show emotion changes and audio playback differences.
6. Call `/ssml` and show generated prosody markup.

## Submission Checklist

Use this checklist before recording your demo or sharing the repository.

### 1) Environment

- [ ] Python virtual environment is active
- [ ] Dependencies installed from `requirements.txt`
- [ ] Internet connection available (required by edge-tts)

### 2) Core Requirement Proof

- [ ] CLI accepts text input
- [ ] API accepts text input
- [ ] At least 3 emotions shown in examples (positive/negative/neutral)
- [ ] Vocal parameter modulation shown (rate, pitch, volume)
- [ ] Emotion-to-voice mapping explained
- [ ] Playable audio output generated (`.mp3`)

### 3) Stretch Goal Proof

- [ ] Granular emotions demonstrated (`inquisitive`, `concerned`, `surprised`)
- [ ] Intensity scaling demonstrated with mild vs strong phrases
- [ ] Web UI demo completed (`/`)
- [ ] SSML output demonstrated (`/ssml` or `--show-ssml`)

### 4) Suggested Screenshot Set

- [ ] Home page with text entered
- [ ] Result panel with emotion, score, intensity, voice profile
- [ ] Audio player visible and loaded
- [ ] SSML preview visible
- [ ] CLI run showing output path
- [ ] `POST /analyze` JSON response

### 5) Final Submission

- [ ] README has setup, run, API, and design mapping sections
- [ ] Repository includes all source files and docs
- [ ] `output/` contains at least one generated sample audio file

## Web UI

Open this URL after starting the API server:

```bash
http://127.0.0.1:8000/
```

The UI includes:

- text area input
- one-click synthesis
- embedded audio player
- detected emotion, sentiment, intensity
- voice profile JSON
- generated SSML preview

## Design Choices

- `vaderSentiment` was selected for fast, lightweight sentiment scoring.
- Simple, transparent rule logic was added for nuanced classes (`inquisitive`, `concerned`, `surprised`) and better explainability.
- `edge-tts` was selected because it exposes explicit rate, pitch, and volume controls with expressive voices.
- SSML output is generated to demonstrate explicit prosody and pause control, and can be forwarded to SSML-capable engines.
- Parameter mapping is centralized in `VoiceModulator` so tuning behavior is straightforward.

## Notes

- Output format is MP3 for broad compatibility and easy streaming.
- Exact voice quality depends on network conditions and selected Edge voice.

## Submission Helper Docs

- Demo checklist: merged into this README under "Submission Checklist"
- API quick tests: `docs/api-quick-tests.ps1`
