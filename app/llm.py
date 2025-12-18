import os
import json
from typing import Dict, Any

def plan_with_llm(user_text: str, lang: str = "mr") -> Dict[str, Any]:
    """Request a structured plan from an LLM (OpenAI) in Telugu (or Marathi based on `lang`).

    Returns a dict with at least: {"action": str, "keywords": [str]}
    Falls back to a heuristic planner when no API key is found or on error.
    """
    # Heuristic fallback
    def fallback(text: str) -> Dict[str, Any]:
        keywords = [w for w in text.split() if len(w) > 3][:6]
        return {"action": "search_schemes", "keywords": keywords}

    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback(user_text)
        openai.api_key = api_key

        # Choose system prompt based on language
        lang = (lang or "mr").lower()
        if lang == "te":
            system = (
                "మీరు ఒక ప్లాన్-ఆధారిత ఏజెంట్‌గా వ్యవహరించాలి. వినియోగదారు తెలుగు భాషలో మాట్లాడారు. "
                "దయచేసి అవుట్‌పుట్ కేవలం JSON గా ఇవ్వండి, నిర్మాణం: {\"action\":..., \"keywords\":[...]}"
            )
            prompt = (
                f"వినియోగదారుని వాక్యం: {user_text}\n\n"
                "దయచేసి వెంటనే JSON ప్లాన్ ఇవ్వండి: action (search_schemes/apply/ask_info), keywords (తెలుగు పదాల జాబితా)."
            )
        else:
            system = (
                "आपण एक योजना-निर्मित सहाय्यक आहात. वापरकर्त्याने मराठीत बोलले आहे. "
                "आउटपुट फक्त JSON मध्ये पाठवा, संरचना द्या: {\"action\":..., \"keywords\":[...]}"
            )
            prompt = (
                f"वापरकर्त्याचे वाक्य: {user_text}\n\n"
                "कृपया लगेच JSON प्लॅन द्या: action (search_schemes/apply/ask_info), keywords (मराठी शब्द सूची)."
            )

        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=200,
        )
        content = resp["choices"][0]["message"]["content"].strip()
        # attempt to parse JSON from model output
        try:
            plan = json.loads(content)
            return plan
        except Exception:
            # If model responds with text, try extracting a JSON substring
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1:
                try:
                    plan = json.loads(content[start:end+1])
                    return plan
                except Exception:
                    return fallback(user_text)
        return fallback(user_text)
    except Exception:
        return fallback(user_text)
