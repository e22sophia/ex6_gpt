"""Part C - missing-information detection (Q3)."""
from profile_module import profile_text
from utils import NOT_PROVIDED, ask_json, as_list, bullets, heading


def rule_based_missing(profile, symptoms, text):
    low = text.lower()
    sym = " ".join(symptoms).lower()
    missing = []
    if "fever" in sym and not any(ch.isdigit() for ch in text):
        missing.append("Exact temperature")
    if any(k in sym for k in ("cough", "throat", "chest", "breath", "fever")) and "breath" not in low:
        missing.append("Breathing difficulty")
    if not any(w in low for w in ("worse", "worsen", "better", "improv", "same", "increasing")):
        missing.append("Severity progression (improving or worsening)")
    missing.append("Additional symptoms")
    if profile["history"] == NOT_PROVIDED:
        missing.append("Relevant medical history")
    if profile["medications"] == NOT_PROVIDED:
        missing.append("Current medications")
    if profile["allergies"] == NOT_PROVIDED:
        missing.append("Allergies")
    return missing


def find_missing_information(profile, symptoms, text):
    """Q3: combine fixed checks with model-suggested gaps."""
    missing = rule_based_missing(profile, symptoms, text)
    prompt = f"""A user reported these details for a symptom check.
{profile_text(profile)}
Symptoms: {', '.join(symptoms)}
Original description: \"\"\"{text}\"\"\"

List up to 4 pieces of information that are NOT given but would help a clinician
understand these symptoms (e.g. exact temperature, exposure to sick contacts, recent travel).
Return ONLY JSON: {{"missing_information": ["..."]}}"""
    for item in as_list(ask_json(prompt, max_tokens=300).get("missing_information")):
        if item.lower() not in (m.lower() for m in missing):
            missing.append(item)
    return missing[:9]


def format_missing(missing):
    return heading("MISSING INFORMATION") + "\n" + bullets(missing)
