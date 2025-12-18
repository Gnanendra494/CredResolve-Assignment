**Architecture**

-- **Voice I/O**: STT (Whisper/OpenAI) -> Agent -> TTS (gTTS) in Telugu (`te`).
- **Agent Loop**: Planner -> Executor -> Evaluator
  - Planner: decides required information and steps to apply
  - Executor: calls tools (retrieval, eligibility, mock API)
  - Evaluator: checks tool outputs, decides next actions or recovery
- **Tools**:
  - `retrieval`: local JSON DB of schemes
  - `eligibility`: rule-based engine to match user attributes
  - `mock_api`: simulate submission and return application id/status
- **Memory**: JSON-based persistent memory of user profiles & past interactions
- **Failure handling**:
  - STT fallback to typed input when audio unclear
  - Missing information prompts in Telugu
  - Tool errors trigger retries and human-readable failure messages

Sequence:
1. Receive audio from user
2. STT -> Telugu text
3. Planner generates plan (find schemes, ask clarifying ques.)
4. Executor calls retrieval & eligibility tools
5. Evaluator verifies and either proceeds to mock apply or asks for missing info
6. Memory updated
