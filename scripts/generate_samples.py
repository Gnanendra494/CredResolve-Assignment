"""Generate sample Telugu audio files for demo recording.

Creates three mp3 files in `samples/`:
- successful_1_te.mp3 (complete info)
- missing_info_1_te.mp3 (missing info)
- edge_noisy_1_te.mp3 (short query)

Requires gTTS and ffmpeg (for playback if you play them).
"""
import os
from pathlib import Path
from gtts import gTTS

def default_samples_for_lang(lang: str):
    if lang == "te":
        return [
            ("successful_1_te.mp3", "నాకు ప్రభుత్వం పథకాల గురించి సహాయం కావాలి. నా వయసు 35 మరియు నా వార్షిక ఆదాయం 180000."),
            ("missing_info_1_te.mp3", "నేను రైతు ని. నాకు పంట కోసం బియ్యం సహాయం కావాలి."),
            ("edge_noisy_1_te.mp3", "నాకు ఆరోగ్య బీమా పథకమా ఉందా? ఎలా దరఖాస్తు చేయాలి చెప్పండి.")
        ]
    # default to Telugu samples
    return [
        ("successful_1_te.mp3", "నాకు శాసన పథకాల గురించి సహాయం కావాలి. నా వయసు 35 మరియు వార్షిక ఆదాయం 180000."),
        ("missing_info_1_te.mp3", "నేను రైతును. నాకు పంట కోసం సహాయం కావాలి."),
        ("edge_noisy_1_te.mp3", "నాకు ఆరోగ్య బీమా ఉన్నదా? దరఖాస్తు ఎలా చేయాలో చెప్పండి.")
    ]


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--lang", default="te", help="Language code (mr or te)")
    args = p.parse_args()

    out_dir = Path.cwd() / "samples"
    out_dir.mkdir(exist_ok=True)
    samples = default_samples_for_lang(args.lang)
    for fname, text in samples:
        path = out_dir / fname
        print(f"Generating {path} ...")
        tts = gTTS(text=text, lang=("te" if args.lang == "te" else "mr"))
        tts.save(str(path))
    print("Done. Generated sample files in ./samples/")


if __name__ == "__main__":
    main()
