"""Part J - save the report (Q10) in the 8-part structured format (Q8)."""
import os
from datetime import datetime

from analysis_module import format_conditions
from profile_module import format_profile
from question_module import format_followups
from safety_module import format_guidance
from symptom_module import format_symptoms
from context_module import format_missing
from utils import DISCLAIMER, MODEL, bullets, heading

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "medical_analysis.txt")


def build_report(profile, symptoms, analysis, missing, followups, guidance):
    parts = [
        "AI-POWERED MEDICAL SYMPTOM ASSISTANT - REPORT",
        "=" * 60,
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}    Model: {MODEL} (Ollama, local)",
        "=" * 60, "",
        "1. " + format_symptoms(symptoms), "",
        "2. " + format_profile(profile), "",
        "3. POSSIBLE CONDITIONS\n" + "-" * 32 + "\n"
        + bullets([c["name"] for c in analysis["possible_conditions"]]), "",
        "4. EXPLANATION\n" + "-" * 32 + "\n" + analysis["explanation"] + "\n\n" + analysis["note"], "",
        "5. " + format_missing(missing), "",
        "6. " + format_followups(followups), "",
        "7. MEDICAL ATTENTION GUIDANCE\n" + "-" * 32 + "\n" + "\n\n".join(guidance), "",
        "8. " + DISCLAIMER,
    ]
    return "\n".join(parts) + "\n"


def save_report(*args):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(build_report(*args))
    return OUTPUT_FILE
