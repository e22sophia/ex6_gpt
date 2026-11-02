"""Part F - follow-up questions (Q6)."""
from prompt_module import build_followup_prompt
from utils import ask_json, as_list, heading, numbered

FALLBACK = [
    "What is your measured temperature?",
    "When exactly did the symptoms begin?",
    "Are you experiencing difficulty breathing?",
    "Are the symptoms improving or worsening?",
    "Do you have any other symptoms not mentioned yet?",
]


def generate_followups(profile, symptoms, text, missing):
    questions = as_list(ask_json(build_followup_prompt(profile, symptoms, text, missing), max_tokens=500)
                        .get("questions"))
    questions = [q if q.endswith("?") else q + "?" for q in questions][:7]
    return questions or FALLBACK


def format_followups(questions):
    return heading("FOLLOW-UP QUESTIONS") + "\n" + numbered(questions)
