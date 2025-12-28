# 🗣️ Voice-First Native Language Service Agent (Telugu)

**An end-to-end agentic assistant bridging the digital divide through native voice interactions.**

### 🚀 Overview
This project demonstrates a fully functional **Voice-First AI Agent** designed to help users discover and apply for government welfare schemes entirely in **Telugu**. Unlike simple chatbots, this system utilizes an **Agentic Workflow (Planner → Executor → Evaluator)** to reason, handle missing information, and execute tasks via mock APIs.

It is designed to handle the complexity of native language processing, including Speech-to-Text (STT) fallback, persistent memory, and context-aware reasoning.

---

### ✨ Key Features

* **🎙️ Voice-First Architecture:** Seamless Speech-to-Text (STT) and Text-to-Speech (TTS) pipeline optimized for Telugu.
* **🧠 Agentic Workflow:** Implements a robust `Planner` → `Executor` → `Evaluator` loop to break down complex user requests.
* **🇮🇳 Native Language Reasoning:** The agent reasons and prompts in Telugu, not just translating English outputs.
* **💾 Contextual Memory:** Maintains a persistent JSON memory of user profiles and conversation history to handle multi-turn dialogues.
* **🛠️ Robust Tooling:** Integrated with local scheme retrieval, rule-based eligibility engines, and mock application APIs.
* **🛡️ Failure Recovery:** Includes logic for STT errors, missing information prompts, and ambiguous input handling.

---

### 🏗️ Architecture

The system follows a modular design to ensure scalability and ease of debugging:

1.  **Input Layer:** Audio is captured and transcribed (STT).
2.  **Reasoning Core:**
    * **Planner:** Deconstructs the user intent (e.g., "I want to apply for Rythu Bandhu").
    * **Executor:** Calls specific tools (Search Scheme, Check Eligibility, Apply).
    * **Evaluator:** Verifies if the task was successful or if more info is needed.
3.  **Tool Layer:** Interfaces with local databases (`schemes_te.json`) and mock APIs.
4.  **Output Layer:** Generates a natural language response and converts it to audio (TTS).

---

### ⚡ Quick Start

#### Prerequisites
* macOS or Linux
* Python 3.9+
* `ffmpeg` (Required for audio processing)
    ```bash
    # macOS
    brew install ffmpeg
    ```

#### Installation

1.  **Clone and Enter Directory**
    ```bash
    git clone <https://github.com/Gnanendra494/CredResolve-Assignment.git>
    cd voice-agent-telugu
    ```

2.  **Set up Virtual Environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Generate Audio Samples** (Optional, for testing without a microphone)
    ```bash
    python scripts/generate_samples.py --lang te
    ```

---

### 🖥️ Usage

#### 1. Voice Mode (Simulated Input)
Run the agent using pre-generated audio files to simulate a user speaking.
```bash
python run_demo.py --audio samples/successful_1.mp3
```
### 2. Text/Fallback Mode
Interact with the agent via text if no audio input is available.
```bash
python run_demo.py --lang te
# Or bypass STT directly:
python run_demo.py --text "నాకు ప్రభుత్వం పథకాల గురించి సహాయం కావాలి" --lang te
```
### 3. Automated Scenario
Run a non-interactive scenario with a pre-filled user profile.
```bash
python run_demo_auto.py --lang te --age 35 --income 180000
```
### 📊 Evaluation & Memory
Evaluation: Refer to evaluation ```bash transcript.md ``` for a walkthrough of successful flows, missing info recovery, and edge cases.

Memory: Check  ```bash memory.json ``` after execution to see how user data and conversation history are stored persistently.
