#!/usr/bin/env python3
import argparse
import os

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio", help="Path to user audio (wav/mp3). If omitted, will ask for typed input.")
    p.add_argument("--text", help="Direct text input (bypass STT)")
    p.add_argument("--lang", help="Language code (mr or te)", default="te")
    args = p.parse_args()

    # set APP_LANG before importing the agent package
    os.environ["APP_LANG"] = args.lang

    from app.agent import run_agent_on_audio, run_agent_on_text

    if args.text:
        run_agent_on_text(args.text)
    elif args.audio:
        run_agent_on_audio(args.audio)
    else:
        prompt = "User (Telugu): " if args.lang == "te" else "User (Marathi): "
        print(f"No audio or text provided. Please type the user's utterance ({args.lang}) to simulate STT:")
        text = input(prompt)
        run_agent_on_text(text)

if __name__ == "__main__":
    main()
