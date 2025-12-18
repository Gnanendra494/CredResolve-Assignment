# Voice-First Native Language Service Agent (Telugu)

Overview
--------
This repository is a runnable demo that showcases a voice-first, agentic assistant operating end-to-end in Telugu. The agent helps users discover and (mock) apply for government/public welfare schemes. It demonstrates:

- Voice I/O: STT -> (Agent reasoning in Telugu) -> TTS
- Agent loop: Planner → Executor → Evaluator
- Tooling: retrieval (local schemes), eligibility engine (rule-based), mock API for application submission
- Memory: persistent JSON memory of user profiles and conversation history
-- Failure handling: STT fallback, missing-information prompts in Telugu, retry logic

Goals for this assignment
------------------------
-- Meet the hard requirements: voice-first, native-language pipeline (Telugu), agentic workflow, multiple tools, memory, and failure handling.
- Provide a reproducible demo and supporting materials (architecture doc, evaluation transcript, sample audio for recording).

Prerequisites
-------------
- macOS or Linux
- Python 3.9+
- `ffmpeg` (for audio playback/processing). Install on macOS:
```bash
brew install ffmpeg
```

Quick install
-------------
```bash
cd "/Users/gnanendra/Desktop/CredResolve Assignment"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment variables
---------------------
- If you plan to integrate an LLM (OpenAI), create a `.env` file with:
```
OPENAI_API_KEY=sk-...
```
An example `.env.example` is included in the repo.

Run the demo (voice-first)
-------------------------

1) Generate sample Telugu audio files (optional but recommended for demo recording):
```bash
python scripts/generate_samples.py --lang te
```
This will create `samples/` with three mp3s covering: a successful application, a missing-info interaction, and a short noisy/edge utterance.

2) Run the agent with a sample file:
```bash
python run_demo.py --audio samples/successful_1.mp3
```

3) Or run interactive fallback (if STT is not configured):
```bash
python run_demo.py
```
The program will then ask you to type Telugu input, which simulates STT.

LLM integration (optional)
-------------------------
The code includes `app/llm.py`, a thin wrapper that will call OpenAI (if `OPENAI_API_KEY` is present) to produce structured plans in Telugu. The agent falls back to the local heuristic planner if no key is provided. To enable:

1. Add `OPENAI_API_KEY` to `.env`.
2. Install dependencies and run the demo. When the LLM is available the Planner will ask the model to return a JSON plan (action + keywords) in Telugu.

Files and structure
-------------------
- `run_demo.py` — CLI runner for demo scenarios (audio or text fallback)
- `app/` — core application
	- `app/stt.py` — STT wrapper (Whisper/OpenAI fallback; typed fallback)
	- `app/tts.py` — TTS wrapper (gTTS playback in Telugu)
	- `app/agent.py` — Planner/Executor/Evaluator orchestration (entrypoint)
	- `app/llm.py` — LLM wrapper that requests JSON plans (optional)
	- `app/memory.py` — JSON memory store
	- `app/tools/` — retrieval, eligibility, mock_api tools
- `schemes_te.json` — sample scheme data in Telugu
- `samples/` — (generated) mp3 files for recording
- `scripts/generate_samples.py` — script to produce sample mp3s via gTTS
- `architecture.md` — architecture overview and diagrams
- `evaluation_transcript.md` — template transcript to use for evaluation and recording

Recording your 5–7 minute demo
------------------------------
Recommended flow and timestamps to hit all evaluation criteria:

-- 00:00–00:30 — Short intro and goal of the demo (Telugu caption/voiceover is fine)
- 00:30–01:30 — Voice-first successful use-case: user asks for schemes, STT->Agent selects scheme, applies (show console prints), memory updated
-- 01:30–02:30 — Missing information flow: user omits age -> agent asks clarifying question in Telugu -> user responds -> agent proceeds
- 02:30–03:00 — Failure handling: show STT fallback (noisy audio or typed fallback) and recovery
- 03:00–04:00 — Show tool usage: retrieval, eligibility, and mock API calls (print outputs), show memory file `memory.json`
- 04:00–05:00 — Show Planner–Executor–Evaluator reasoning (print plan + decisions), optionally show LLM plan output (if enabled)
- 05:00–05:30 — Show evaluation transcript file and explain how scenarios map to grading criteria
- 05:30–06:00 — Wrap up and next steps (extending data, production TTS/STT, secure LLM)

Evaluation checklist
--------------------
- Voice-first interaction: audio in/out demonstrated.
- Native language throughout: Telugu prompts, TTS, planner prompts (if using LLM, ensure Telugu system prompt).
- Agentic workflow: Planner–Executor–Evaluator sequence is executed and visible.
- Tools: retrieval + eligibility + mock API are used and visible.
- Memory: conversation and user profile saved to `memory.json`.
- Failure handling: STT fallback and missing-info prompts present.

Extending the demo
------------------
-- Replace `app/stt.py` with a cloud STT (OpenAI / Whisper API) for production-quality transcription in Telugu.
-- Replace `app/tts.py` with a cloud TTS (Google Cloud / AWS Polly / Azure TTS) for higher fidelity voices.
-- Expand `schemes_te.json` and improve `eligibility.py` to match official forms and required documents.

Need help?
-----------
If you want, I can:

- Add fully working OpenAI-based planning integration and show a sample run (you will need to provide `OPENAI_API_KEY`).

