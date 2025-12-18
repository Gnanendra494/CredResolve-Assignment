from typing import Dict, Any, List
import os
from .stt import transcribe_from_file
from .tts import speak
from .tools import retrieval, eligibility, mock_api
from .memory import Memory
from . import llm

LANG = os.getenv("APP_LANG", "mr")

mem = Memory()

def planner(user_text: str) -> Dict[str, Any]:
    """Planner: prefer the LLM planner when available, otherwise use a simple heuristic.

    The LLM planner will attempt to return a JSON plan in Telugu (or Marathi depending on `APP_LANG`).
    """
    try:
        plan = llm.plan_with_llm(user_text, lang=LANG)
        print(f"[Planner] LLM plan: {plan}")
        if isinstance(plan, dict) and plan.get("action"):
            return plan
    except Exception as e:
        print(f"[Planner] LLM planner failed: {e}")

    # Heuristic fallback: extract keywords and ask retrieval
    keywords = []
    words = user_text.split()
    # heuristics: pick nouns/words longer than 3 chars
    for w in words:
        if len(w) > 3:
            keywords.append(w)
    plan = {"action": "search_schemes", "keywords": keywords}
    print(f"[Planner] Fallback plan: {plan}")
    return plan


# Language-specific messages
MESSAGES = {
    "mr": {
        "no_scheme": "माफ करा, मी कोणतीही योजना सापडली नाही. कृपया थोडे अधिक माहिती द्या.",
        "ask_field": "कृपया तुमचे {field} सांगा.",
        "apply_start": "तुम्ही {scheme} साठी पात्र आहात. मी आता अर्ज करणार आहे.",
        "apply_success": "{message}. अर्ज क्रमांक: {id}",
        "not_eligible": "तुम्ही सध्याच्या माहितीनुसार पात्र दाखवत नाही. मी पर्यायी योजना शोधत आहे.",
        "recommend": "शिफारस: {name} - {desc}",
        "enter_field_input": "Enter {field} (Marathi / numeric): "
    },
    "te": {
        "no_scheme": "క్షమించండి, నేను ఏ పథకమును కనుగొనలేకపోయాను. దయచేసి మరింత సమాచారం ఇవ్వండి.",
        "ask_field": "దయచేసి మీ {field} చెప్పండి.",
        "apply_start": "మీరు {scheme} కోసం అర్హులై ఉంటారు. నేను ఇప్పుడు దరఖాస్తు చేస్తున్నాను.",
        "apply_success": "{message}. దరఖాస్తు నంబర్: {id}",
        "not_eligible": "పరిస్థితి ప్రకారం మీరు అర్హులు కాకపోవచ్చు. నేను ప్రత్యామ్నాయ పథకాలను వెతుకుతాను.",
        "recommend": "సిఫారసు: {name} - {desc}",
        "enter_field_input": "Enter {field} (Telugu / numeric): "
    }
}

MSG = MESSAGES.get(LANG, MESSAGES["mr"])

def executor(plan: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
    act = plan.get("action")
    if act == "search_schemes":
        kws = plan.get("keywords", [])
        print(f"[Executor] Searching schemes with keywords: {kws}")
        schemes = retrieval.find_schemes_by_keywords(kws)
        scored = []
        for s in schemes:
            res = eligibility.check_eligibility(user_info, s)
            scored.append({"scheme": s, "eligibility": res})
        print(f"[Executor] Retrieved {len(scored)} schemes")
        return {"results": scored}
    return {"results": []}

def evaluator(executor_out: Dict[str, Any]) -> Dict[str, Any]:
    # choose best match (eligible true) otherwise return top suggestions
    results = executor_out.get("results", [])
    eligible = [r for r in results if r["eligibility"]["eligible"]]
    if eligible:
        print(f"[Evaluator] Found eligible schemes: {len(eligible)}")
        return {"selected": eligible[0]}
    else:
        print(f"[Evaluator] No eligible schemes found; returning top suggestion")
        return {"selected": results[0] if results else None}

def run_agent_on_audio(audio_path: str, user_id: str = "user_1") -> None:
    # Step 1: STT
    user_text = transcribe_from_file(audio_path, lang=LANG)
    mem.add_conversation({"user_id": user_id, "text": user_text})

    # Step 2: Planner
    plan = planner(user_text)

    # Load user info from memory (if any)
    user_info = mem.get_user(user_id)

    # Step 3: Executor
    exec_out = executor(plan, user_info)

    # Step 4: Evaluator
    eval_out = evaluator(exec_out)

    selected = eval_out.get("selected")
    if not selected:
        speak(MSG["no_scheme"], lang=LANG)
        return

    scheme = selected["scheme"]
    elig = selected["eligibility"]

    if not elig["eligible"] and elig["missing"]:
        # ask for missing information
        for field in elig["missing"]:
            msg = MSG["ask_field"].format(field=field)
            speak(msg, lang=LANG)
            # fallback to typed reply for now
            reply = input(MSG["enter_field_input"].format(field=field))
            if field == "age":
                user_info["age"] = int(reply)
            elif field == "annual_income":
                user_info["annual_income"] = int(reply)
            elif field == "land_size":
                user_info["land_size"] = float(reply)
        mem.save_user(user_id, user_info)
        # re-run eligibility for selected scheme
        elig = eligibility.check_eligibility(user_info, scheme)

    if elig["eligible"]:
        speak(MSG["apply_start"].format(scheme=scheme.get("name")), lang=LANG)
        resp = mock_api.apply_to_scheme(user_info, scheme)
        mem.add_conversation({"action": "applied", "result": resp})
        speak(MSG["apply_success"].format(message=resp.get("message"), id=resp.get("application_id")), lang=LANG)
    else:
        speak(MSG["not_eligible"], lang=LANG)
        # present alternatives
        alt = exec_out.get("results", [])[:3]
        for a in alt:
            speak(MSG["recommend"].format(name=a['scheme']['name'], desc=a['scheme']['description']), lang=LANG)


def run_agent_on_text(user_text: str, user_id: str = "user_1") -> None:
    """Run the agent pipeline directly on text (useful for demos when STT is not used)."""
    print(f"[Run] Running agent on text: {user_text}")
    mem.add_conversation({"user_id": user_id, "text": user_text})
    plan = planner(user_text)
    user_info = mem.get_user(user_id)
    exec_out = executor(plan, user_info)
    eval_out = evaluator(exec_out)

    selected = eval_out.get("selected")
    if not selected:
        speak(MSG["no_scheme"], lang=LANG)
        return

    scheme = selected["scheme"]
    elig = selected["eligibility"]

    if not elig["eligible"] and elig["missing"]:
        for field in elig["missing"]:
            msg = MSG["ask_field"].format(field=field)
            speak(msg, lang=LANG)
            reply = input(MSG["enter_field_input"].format(field=field))
            if field == "age":
                user_info["age"] = int(reply)
            elif field == "annual_income":
                user_info["annual_income"] = int(reply)
            elif field == "land_size":
                user_info["land_size"] = float(reply)
        mem.save_user(user_id, user_info)
        elig = eligibility.check_eligibility(user_info, scheme)

    if elig["eligible"]:
        speak(MSG["apply_start"].format(scheme=scheme.get("name")), lang=LANG)
        resp = mock_api.apply_to_scheme(user_info, scheme)
        mem.add_conversation({"action": "applied", "result": resp})
        speak(MSG["apply_success"].format(message=resp.get("message"), id=resp.get("application_id")), lang=LANG)
    else:
        speak(MSG["not_eligible"], lang=LANG)
        alt = exec_out.get("results", [])[:3]
        for a in alt:
            speak(MSG["recommend"].format(name=a['scheme']['name'], desc=a['scheme']['description']), lang=LANG)
