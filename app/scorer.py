def calculate_score(issues: list) -> dict:
    score = 100

    penalties = {
        "Critical": 25,
        "High": 15,
        "Medium": 8,
        "Low": 3
    }

    for issue in issues:
        score -= penalties.get(issue["severity"], 5)

    score = max(score, 0)

    return {
        "score": score,
        "status": get_status(score)
    }


def get_status(score: int) -> str:
    if score >= 85:
        return "Production Ready"
    if score >= 65:
        return "Needs Minor Improvements"
    if score >= 40:
        return "Needs Refactoring"
    return "High Risk"