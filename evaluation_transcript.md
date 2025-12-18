**Evaluation Transcript (Template)**

Language: Telugu

1) Successful interaction
- User (audio): "నాకు ప్రభుత్వం పథకాల గురించి సమాచారం కావాలి. నా వయసు 35 మరియు నా వార్షిక ఆదాయం 1,80,000 ఉంది."
- Agent (STT -> Telugu): transcribed text
- Planner: search keywords -> ["పథకం","అరువు"]
- Executor: retrieved `మాతృశక్తి సహాయ పథకం` -> eligibility true
- Agent: applies via `mock_api` -> returns application id

2) Missing info / recovery
- User (audio): "నేను రైతు ని; నాకు సహాయం కావాలి" (no age provided)
- Agent asks for age in Telugu via TTS
- User provides age (via typed fallback or re-record)
- Agent proceeds, updates memory, applies

3) Edge-case: STT failure
- User mumbles or audio noisy
- STT fallback triggers: agent asks for typed input in Telugu
- Agent continues with typed content
