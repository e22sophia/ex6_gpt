"""Part A - collect user input (Q1)."""
import csv
import os

from utils import clean_text, NOT_PROVIDED

SAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample_cases.csv")


def ask_text(prompt, required=False):
    while True:
        value = clean_text(input(prompt))
        if value:
            return value
        if not required:
            return NOT_PROVIDED
        print("  This field is required.")


def ask_age():
    while True:
        raw = input("Age (years): ").strip()
        if raw.isdigit() and 0 <= int(raw) <= 120:
            return int(raw)
        print("  Please enter a valid age between 0 and 120.")


def ask_choice(prompt, options):
    labels = " / ".join(f"{i}={o}" for i, o in enumerate(options, 1))
    while True:
        raw = input(f"{prompt} ({labels}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        for o in options:
            if raw.lower() == o.lower():
                return o
        print("  Invalid choice.")


def collect_patient_info():
    """Q1: age, sex, duration, severity, history, medications, allergies."""
    print("\n--- Patient Information ---")
    return {
        "age": ask_age(),
        "sex": ask_choice("Sex", ["Female", "Male", "Other", "Prefer not to say"]),
        "duration": ask_text("How long have you had the symptoms? (e.g. 2 days): ", required=True),
        "severity": ask_choice("Severity", ["Mild", "Moderate", "Severe"]),
        "history": ask_text("Relevant medical history (Enter to skip): "),
        "medications": ask_text("Current medications (Enter to skip): "),
        "allergies": ask_text("Allergies (Enter to skip): "),
    }


def collect_symptoms():
    """Natural-language symptom description (used by Q2)."""
    print("\nDescribe your symptoms in your own words.")
    print("Example: I have been having fever and cough for two days. My throat is also painful.")
    print("Press Enter on an empty line when finished.")
    lines = []
    while True:
        line = input("> ")
        if not line.strip():
            if lines:
                break
            print("  Please describe at least one symptom.")
            continue
        lines.append(line)
    return clean_text(" ".join(lines))


def load_sample_case():
    """Load a case from data/sample_cases.csv. Returns (info, symptom_text) or None."""
    if not os.path.isfile(SAMPLE_FILE):
        print("Sample file not found.")
        return None
    with open(SAMPLE_FILE, newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))
    print("\nSample cases:")
    for i, c in enumerate(cases, 1):
        print(f"  {i}. {c['age']}y {c['sex']} - {c['symptoms'][:60]}")
    raw = input("Choose a case number (Enter to cancel): ").strip()
    if not (raw.isdigit() and 1 <= int(raw) <= len(cases)):
        return None
    c = cases[int(raw) - 1]
    info = {
        "age": int(c["age"]), "sex": c["sex"], "duration": c["duration"],
        "severity": c["severity"], "history": c["history"] or NOT_PROVIDED,
        "medications": c["medications"] or NOT_PROVIDED, "allergies": c["allergies"] or NOT_PROVIDED,
    }
    return info, c["symptoms"]
