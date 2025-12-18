import time
import uuid

def apply_to_scheme(user_info: dict, scheme: dict) -> dict:
    """Simulate applying to a government scheme. Returns fake application id and status."""
    time.sleep(0.5)
    app_id = str(uuid.uuid4())
    return {
        "application_id": app_id,
        "status": "submitted",
        "scheme_id": scheme.get("id"),
        "message": "దరఖాస్తు విజయవంతంగా సమర్పించబడింది"
    }
