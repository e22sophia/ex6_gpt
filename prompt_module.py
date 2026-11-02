"""Part D - prompt generation (Q4)."""
from profile_module import profile_text

RULES = """Rules you MUST follow:
- Analyze the symptoms and identify POSSIBLE conditions only (3 to 5). Do NOT give a definitive diagnosis.
- Explain your reasoning at a general level, in plain language.
- Do not invent information. Use only what the user provided. If something is unknown, say so.
- Do not recommend specific medicines or doses.
- Use cautious language such as "may", "can", "could be associated with"."""


def build_analysis_prompt(profile, symptoms, text, missing):
    return f"""Analyze the following patient-reported information.

PATIENT: {profile_text(profile)}
REPORTED SYMPTOMS: {', '.join(symptoms)}
USER'S OWN WORDS: \"\"\"{text}\"\"\"
INFORMATION NOT PROVIDED: {', '.join(missing)}

{RULES}

Return ONLY JSON in exactly this form:
{{
  "possible_conditions": [{{"name": "Condition name", "reasoning": "one sentence on why these symptoms may relate"}}],
  "explanation": "3-4 sentences explaining in general terms why these symptoms can occur in several conditions and why the information is not enough to establish a diagnosis",
  "note": "one sentence stating that the symptoms can occur in multiple conditions and are not sufficient for a diagnosis"
}}"""


def build_followup_prompt(profile, symptoms, text, missing):
    return f"""Based on the patient information below, write 5 to 7 follow-up questions
that would help clarify the situation (for example measured temperature, onset, breathing
difficulty, type of cough, whether symptoms are improving or worsening, exposures).

PATIENT: {profile_text(profile)}
REPORTED SYMPTOMS: {', '.join(symptoms)}
USER'S OWN WORDS: \"\"\"{text}\"\"\"
INFORMATION NOT PROVIDED: {', '.join(missing)}

Rules: ask clear, single, answerable questions; do not repeat information already given;
do not ask for names or contact details.
Return ONLY JSON: {{"questions": ["...", "..."]}}"""


def build_guidance_prompt(profile, symptoms, text):
    return f"""Write 2 to 3 sentences of general guidance on when professional medical care
may be appropriate for the situation below.

PATIENT: {profile_text(profile)}
REPORTED SYMPTOMS: {', '.join(symptoms)}
USER'S OWN WORDS: \"\"\"{text}\"\"\"

Rules: use cautious language; do NOT claim to make a clinical triage decision; do NOT
diagnose; do not recommend medicines or doses; mention that a qualified healthcare
professional can assess the person properly.
Return ONLY JSON: {{"guidance": "..."}}"""
