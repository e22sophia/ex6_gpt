"""Part G - risk / escalation messaging (Q7).
Uses cautious language. It does NOT make a clinical triage decision."""
import re

from prompt_module import build_guidance_prompt
from utils import ask_json, heading

BASE_MESSAGE = ("If symptoms are severe, rapidly worsening,\n"
                "or concerning, seek appropriate professional\nmedical care.")

# (regex, readable label)
RED_FLAGS = [
    (r"chest (pain|pressure|tightness)", "chest pain or pressure"),
    (r"(difficulty|trouble) breathing|short(ness)? of breath|can'?t breathe|struggling to breathe", "difficulty breathing"),
    (r"faint|passed out|unconscious|lost consciousness", "fainting or loss of consciousness"),
    (r"confus|disorient", "confusion"),
    (r"seizure|convulsion", "a seizure"),
    (r"slurred speech|face droop|weakness (on|in) one side|numbness (on|in) one side", "possible stroke-like signs"),
    (r"severe bleeding|bleeding (heavily|a lot)|vomiting blood|blood in (stool|vomit)|coughing (up )?blood", "significant bleeding"),
    (r"swelling of (the )?(face|lips|tongue|throat)|throat (is )?closing", "swelling of the face or throat"),
    (r"stiff neck", "a stiff neck together with fever"),
    (r"suicid|kill myself|end my life|self[- ]harm", "thoughts of self-harm"),
    (r"severe (abdominal|stomach|belly) pain", "severe abdominal pain"),
]
NEGATIONS = ("no ", "not ", "without ", "denies ", "never ", "n't ")


def _negated(text, start):
    before = text[max(0, start - 25):start]
    return any(n in before for n in NEGATIONS)


def detect_red_flags(text):
    low = text.lower()
    found = []
    for pattern, label in RED_FLAGS:
        for m in re.finditer(pattern, low):
            if not _negated(low, m.start()):
                if label not in found:
                    found.append(label)
                break
    return found


def special_notes(profile, severity_text):
    notes = []
    if profile["age"] < 3:
        notes.append("Because the person is a very young child, it is generally advisable to contact a "
                     "healthcare professional early when a child is unwell.")
    elif profile["age"] >= 65:
        notes.append("Because the person is an older adult, it is generally advisable to contact a "
                     "healthcare professional early when symptoms appear.")
    if severity_text.lower() == "severe":
        notes.append("The symptoms were described as severe; consider seeking professional medical care promptly.")
    return notes


def emergency_alert(text):
    """Short immediate warning shown before analysis if red-flag wording is present."""
    flags = detect_red_flags(text)
    if not flags:
        return None
    return ("IMPORTANT: You mentioned " + ", ".join(flags) + ".\n"
            "Symptoms like these can sometimes be serious. Please consider contacting a healthcare\n"
            "professional or local emergency services promptly rather than waiting for this tool.")


def generate_guidance(profile, symptoms, text):
    """Returns the guidance as a list of paragraphs (strings)."""
    paragraphs = [BASE_MESSAGE]
    alert = emergency_alert(text)
    if alert:
        paragraphs.append(alert)
    paragraphs += special_notes(profile, profile["severity"])
    try:
        extra = str(ask_json(build_guidance_prompt(profile, symptoms, text), max_tokens=300)
                    .get("guidance", "")).strip()
    except Exception:
        extra = ""
    if extra:
        paragraphs.append(extra)
    paragraphs.append("This tool does not perform medical triage. A qualified healthcare "
                      "professional can assess your situation properly.")
    return paragraphs


def format_guidance(paragraphs):
    return heading("MEDICAL ATTENTION") + "\n" + "\n\n".join(paragraphs)
