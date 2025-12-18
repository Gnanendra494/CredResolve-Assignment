import os
from typing import Optional

def transcribe_from_file(audio_path: str, lang: str = "mr") -> str:
    """Transcribe audio using Whisper if available, otherwise fallback to asking user to type input.

    Returns transcribed text in the target native language (Telugu) when possible.
    """
    # Try to use whisper package if installed
    try:
        import whisper
        print(f"[STT] Loading whisper model 'small' and transcribing {audio_path} (lang={lang})")
        model = whisper.load_model("small")
        result = model.transcribe(audio_path, language=lang)
        text = result.get("text", "").strip()
        print(f"[STT] Whisper output: {text}")
        if text:
            return text
    except Exception as e:
        print(f"[STT] Whisper transcription failed: {e}")

    # Try OpenAI if configured (optional)
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("OPENAI_API_KEY"):
            print("[STT] Attempting OpenAI transcription as fallback")
            audio_file = open(audio_path, "rb")
            resp = openai.Audio.transcribe("gpt-4o-mini-transcribe", audio_file, language=lang)
            text = resp.get("text", "").strip()
            print(f"[STT] OpenAI transcription output: {text}")
            if text:
                return text
    except Exception as e:
        print(f"[STT] OpenAI transcription failed: {e}")

    # here Fallback: ask user to type the transcription (useful for testing)
    print("STT fallback: Please type the user's words in Telugu:")
    return input("Typed user input (Telugu): ")
