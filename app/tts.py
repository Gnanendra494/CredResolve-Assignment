import os
import tempfile
import shutil
from gtts import gTTS

def speak(text: str, lang: str = "mr") -> None:
    """Synthesize speech and play it.

    Uses macOS `afplay` when available for reliable playback. Falls back to printing text on failure.
    """
    try:
        print(f"[TTS] Using language='{lang}' for text: {text[:60]}...")
        tts = gTTS(text=text, lang=lang)
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        tts.save(path)

        # Prefer macOS afplay for playback (reliable and available on macOS) (I am Macbook M1 user)
        afplay = shutil.which("afplay")
        if afplay:
            os.system(f"{afplay} \"{path}\"")
        else:
            # Fallback to playsound if afplay not available
            try:
                from playsound import playsound
                playsound(path)
            except Exception:
                print("(TTS) Unable to play audio; printing text instead.")
                print(text)

        try:
            os.remove(path)
        except Exception:
            pass
    except Exception as e:
        print(f"TTS failed: {e}")
        print("Text output (Telugu):\n", text)
