from __future__ import annotations

import argparse

from empathy_engine.service import EmpathyEngineService


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Empathy Engine CLI")
    parser.add_argument("--text", type=str, help="Text to synthesize")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory for output audio files")
    parser.add_argument("--show-ssml", action="store_true", help="Print generated SSML to stdout")
    args = parser.parse_args()

    service = EmpathyEngineService(output_dir=args.output_dir)

    if args.text:
        text = args.text
    else:
        text = input("Enter text to synthesize: ").strip()

    if not text:
        raise SystemExit("No text was provided.")

    result = service.synthesize(text)

    print("\nSynthesis complete")
    print(f"Emotion: {result.emotion}")
    print(f"Sentiment score: {result.sentiment_score}")
    print(f"Intensity: {result.intensity}")
    print(f"Voice profile: {result.voice_profile}")
    print(f"Audio file: {result.audio_path}")
    if args.show_ssml:
        print("SSML:")
        print(result.ssml)


if __name__ == "__main__":
    run_cli()
