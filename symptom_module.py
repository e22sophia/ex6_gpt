"""Part B - symptom extraction (Q2)."""
import re

from utils import ask_json, as_list, bullets, heading

# Fallback keyword table, used if the model reply cannot be parsed.
KEYWORDS = [
    (r"fever|temperature|febrile", "Fever"),
    (r"cough", "Cough"),
    (r"sore throat|throat (is |was )?(also )?(painful|sore|hurts?)|painful throat|throat pain", "Sore throat"),
    (r"headache|head (is )?(hurting|aching)", "Headache"),
    (r"nausea|nauseous", "Nausea"),
    (r"vomit", "Vomiting"),
    (r"diarrh", "Diarrhea"),
    (r"fatigue|tired|exhausted", "Fatigue"),
    (r"body ache|muscle (pain|ache)|body pain", "Body ache"),
    (r"runny nose|blocked nose|congestion", "Nasal congestion / runny nose"),
    (r"shortness of breath|breathless|difficulty breathing", "Shortness of breath"),
    (r"chest pain|chest tight", "Chest pain"),
    (r"stomach (pain|ache)|abdominal pain|belly pain", "Abdominal pain"),
    (r"rash|itching|itchy", "Skin rash / itching"),
    (r"dizz", "Dizziness"),
    (r"chills", "Chills"),
]


def extract_symptoms(text):
    """Q2: pull a clean symptom list out of natural-language input."""
    prompt = f"""Extract the medical symptoms mentioned in the text below.
Return ONLY JSON in this form: {{"symptoms": ["Symptom 1", "Symptom 2"]}}
Rules: use short standard symptom names (e.g. "Sore throat"); include only symptoms
actually stated; do not add symptoms the user did not mention; do not include
symptoms the user says they do NOT have.

TEXT: \"\"\"{text}\"\"\""""
    symptoms = as_list(ask_json(prompt, max_tokens=300).get("symptoms"))
    if not symptoms:  # fallback
        low = text.lower()
        symptoms = [label for pat, label in KEYWORDS if re.search(pat, low)]
    return symptoms


def format_symptoms(symptoms):
    return heading("REPORTED SYMPTOMS") + "\n" + bullets(symptoms)
