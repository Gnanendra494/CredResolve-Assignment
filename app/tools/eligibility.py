from typing import Dict, Any

def check_eligibility(user_info: Dict[str, Any], scheme: Dict) -> Dict:
    """Simple rule-based eligibility check. Returns dict with result and missing fields."""
    rules = scheme.get("eligibility", {})
    missing = []
    eligible = True

    # Age check
    age = user_info.get("age")
    if rules.get("min_age") or rules.get("max_age"):
        if age is None:
            missing.append("age")
            eligible = False
        else:
            if rules.get("min_age") and age < rules["min_age"]:
                eligible = False
            if rules.get("max_age") and age > rules["max_age"]:
                eligible = False

    # Income
    inc = user_info.get("annual_income")
    if rules.get("income_below"):
        if inc is None:
            missing.append("annual_income")
            eligible = False
        else:
            if inc > rules["income_below"]:
                eligible = False

    # Farmer flag
    if rules.get("farmer"):
        if not user_info.get("farmer"):
            eligible = False

    # Land size
    if rules.get("land_size_max") is not None:
        ls = user_info.get("land_size")
        if ls is None:
            missing.append("land_size")
            eligible = False
        else:
            if ls > rules["land_size_max"]:
                eligible = False

    return {"eligible": eligible, "missing": missing}
