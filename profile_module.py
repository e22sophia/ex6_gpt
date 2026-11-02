"""Patient profile handling."""
from utils import heading


def create_profile(info):
    return dict(info)


def profile_text(profile):
    """Compact text used inside prompts."""
    return (f"Age: {profile['age']}; Sex: {profile['sex']}; Duration: {profile['duration']}; "
            f"Severity: {profile['severity']}; History: {profile['history']}; "
            f"Medications: {profile['medications']}; Allergies: {profile['allergies']}")


def format_profile(profile):
    rows = [("Age", profile["age"]), ("Sex", profile["sex"]), ("Duration", profile["duration"]),
            ("Severity", profile["severity"]), ("History", profile["history"]),
            ("Medications", profile["medications"]), ("Allergies", profile["allergies"])]
    return heading("PATIENT INFORMATION") + "\n" + "\n".join(f"{k:<12}: {v}" for k, v in rows)
