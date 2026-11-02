"""Shared helpers: Ollama access, JSON parsing, text formatting, disclaimer."""
import json
import os
import re
import unicodedata

import ollama

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
NUM_CTX = 4096
NOT_PROVIDED = "Not provided"

DISCLAIMER = """DISCLAIMER
--------------------------------
This AI-generated response is intended for
educational and informational purposes only.
It is not a medical diagnosis and does not
replace advice from a qualified healthcare
professional.
For serious, worsening or urgent symptoms,
seek appropriate medical care."""

SYSTEM_PROMPT = (
    "You are a cautious medical information assistant used for education. "
    "You never give a definitive diagnosis, never prescribe medication or doses, "
    "and never invent information that the user did not provide. "
    "You do not make clinical triage decisions."
)


def check_ollama():
    """Verify the Ollama server is running and the model is downloaded."""
    try:
        listing = ollama.list()
    except Exception:
        raise RuntimeError("Cannot reach Ollama. Open the Ollama app (or run: ollama serve) and try again.")
    models = listing["models"] if isinstance(listing, dict) else listing.models
    names = [(m["model"] if isinstance(m, dict) else m.model) for m in models]
    if not any(n == MODEL or n.startswith(MODEL + ":") for n in names):
        raise RuntimeError(f"Model '{MODEL}' not found. Run: ollama pull {MODEL}\n"
                           f"Installed models: {', '.join(names) or 'none'}")


def ask_llm(prompt, as_json=False, max_tokens=900):
    kwargs = dict(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        options={"temperature": 0, "num_ctx": NUM_CTX, "num_predict": max_tokens},
    )
    if as_json:
        kwargs["format"] = "json"
    return ollama.chat(**kwargs)["message"]["content"].strip()


def parse_json(text):
    """Parse JSON from a model reply; tolerate extra text around it."""
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None


def ask_json(prompt, max_tokens=900):
    """Ask the model for JSON; return a dict (empty dict if parsing fails)."""
    data = parse_json(ask_llm(prompt, as_json=True, max_tokens=max_tokens))
    return data if isinstance(data, dict) else {}


def as_list(value):
    """Coerce a model value into a clean list of strings."""
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    out = []
    for v in value:
        v = str(v.get("name", v) if isinstance(v, dict) else v).strip(" -*\u2022")
        if v and v.lower() not in (x.lower() for x in out):
            out.append(v)
    return out


def clean_text(text):
    """Normalise whitespace / odd characters in free-text input."""
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"[^\x09\x0A\x20-\x7E]", " ", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def heading(title):
    return f"{title}\n{'-' * 32}"


def bullets(items):
    return "\n".join(f"\u2022 {i}" for i in items) if items else "\u2022 Not mentioned"


def numbered(items):
    return "\n".join(f"{n}. {i}" for n, i in enumerate(items, 1)) if items else "None generated"
