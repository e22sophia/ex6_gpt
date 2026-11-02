"""Part E - symptom analysis (Q5)."""
from prompt_module import build_analysis_prompt
from utils import ask_json, as_list, bullets, heading

DEFAULT_NOTE = ("These symptoms can occur in multiple conditions.\n"
                "The information provided is not sufficient to\nestablish a diagnosis.")


def analyze(profile, symptoms, text, missing):
    data = ask_json(build_analysis_prompt(profile, symptoms, text, missing), max_tokens=900)
    conditions = []
    for c in data.get("possible_conditions", []) if isinstance(data.get("possible_conditions"), list) else []:
        if isinstance(c, dict) and c.get("name"):
            conditions.append({"name": str(c["name"]).strip(), "reasoning": str(c.get("reasoning", "")).strip()})
        elif isinstance(c, str):
            conditions.append({"name": c.strip(), "reasoning": ""})
    return {
        "possible_conditions": conditions[:5],
        "explanation": str(data.get("explanation", "")).strip() or "Not mentioned.",
        "note": str(data.get("note", "")).strip() or DEFAULT_NOTE,
    }


def format_analysis(symptoms, result):
    """Matches the SYMPTOM ANALYSIS sample layout."""
    names = [c["name"] for c in result["possible_conditions"]]
    return (heading("SYMPTOM ANALYSIS") + "\nReported Symptoms:\n" + bullets(symptoms) +
            "\n\nPossible Conditions:\n" + bullets(names) +
            "\n\nNote:\n" + result["note"])


def format_conditions(result):
    """Possible conditions with reasoning, plus the general explanation."""
    lines = [heading("POSSIBLE CONDITIONS")]
    for c in result["possible_conditions"]:
        lines.append(f"\u2022 {c['name']}" + (f" - {c['reasoning']}" if c["reasoning"] else ""))
    if not result["possible_conditions"]:
        lines.append("\u2022 Not enough information")
    lines += ["", "Explanation:", result["explanation"]]
    return "\n".join(lines)
