#!/usr/bin/env python3
"""Run the agent non-interactively by pre-filling user profile.

This avoids interactive prompts by saving a user profile to memory before running.
"""
from app.memory import Memory
from app.agent import run_agent_on_text
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", help="User utterance to run", default="मला శासकीय योजनांबद्दल माहिती हवी आहे. माझे वय 35 आहे आणि माझे वार्षिक उत्पन्न 180000 आहे.")
    p.add_argument("--age", type=int, default=35)
    p.add_argument("--income", type=int, default=180000)
    p.add_argument("--farmer", action="store_true")
    p.add_argument("--lang", help="Language code (mr or te)", default="mr")
    args = p.parse_args()
    args = p.parse_args()

    # set language for this run
    import os
    os.environ["APP_LANG"] = args.lang

    mem = Memory()
    # Pre-fill user profile so agent won't ask for missing fields
    mem.save_user("user_1", {"age": args.age, "annual_income": args.income, "farmer": args.farmer})

    run_agent_on_text(args.text, user_id="user_1")

if __name__ == "__main__":
    main()
