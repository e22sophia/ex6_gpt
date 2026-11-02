"""
24CS2506 - Experiment 6: AI-Powered Medical Symptom Assistant (local Ollama version)
Run:  python main.py        (Ollama must be running; default model llama3.2)
Other model:  set OLLAMA_MODEL=mistral   (PowerShell: $env:OLLAMA_MODEL="mistral")
Informational tool only - NOT a medical diagnosis.
"""
import analysis_module as ana
import context_module as ctx
import input_module as inp
import profile_module as prof
import question_module as qst
import safety_module as saf
import save_module as sav
import symptom_module as sym
from utils import DISCLAIMER, MODEL, check_ollama

state = {"profile": None, "text": None, "symptoms": [], "missing": [],
         "analysis": None, "followups": None, "guidance": None}


def reset_results():
    state.update(symptoms=[], missing=[], analysis=None, followups=None, guidance=None)


def menu():
    print("\n" + "=" * 60)
    print(" AI-POWERED MEDICAL SYMPTOM ASSISTANT  (informational only)")
    print("=" * 60)
    for line in ("1. Enter Patient Information", "2. Enter Symptoms", "3. Analyze Symptoms",
                 "4. Generate Follow-up Questions", "5. Display Possible Conditions",
                 "6. Display Medical Attention Guidance", "7. Display Disclaimer",
                 "8. Save Report", "9. Exit"):
        print(" " + line)


def have_inputs():
    if not state["profile"]:
        print("Please enter patient information first (option 1).")
    elif not state["text"]:
        print("Please enter symptoms first (option 2).")
    else:
        return True
    return False


def ensure_symptoms():
    if not state["symptoms"]:
        check_ollama()
        print("Extracting symptoms ...")
        state["symptoms"] = sym.extract_symptoms(state["text"])
        print(sym.format_symptoms(state["symptoms"]))
        state["missing"] = ctx.find_missing_information(state["profile"], state["symptoms"], state["text"])


def ensure_analysis():
    ensure_symptoms()
    if not state["analysis"]:
        print(f"Analyzing with Ollama ({MODEL}) ...")
        state["analysis"] = ana.analyze(state["profile"], state["symptoms"], state["text"], state["missing"])


def ensure_followups():
    ensure_symptoms()
    if not state["followups"]:
        print("Generating follow-up questions ...")
        state["followups"] = qst.generate_followups(state["profile"], state["symptoms"],
                                                    state["text"], state["missing"])


def ensure_guidance():
    ensure_symptoms()
    if not state["guidance"]:
        state["guidance"] = saf.generate_guidance(state["profile"], state["symptoms"], state["text"])


def main():
    print("NOTE: This tool gives general information only. It is not a medical diagnosis.")
    while True:
        menu()
        choice = input("Enter choice (1-9): ").strip()
        try:
            if choice == "1":
                sample = None
                if input("Load a sample case from data/sample_cases.csv? (y/N): ").strip().lower() == "y":
                    sample = inp.load_sample_case()
                if sample:
                    state["profile"], state["text"] = prof.create_profile(sample[0]), sample[1]
                    print("\nSample case loaded (patient information and symptoms).")
                else:
                    state["profile"] = prof.create_profile(inp.collect_patient_info())
                reset_results()
                print("\n" + prof.format_profile(state["profile"]))

            elif choice == "2":
                state["text"] = inp.collect_symptoms()
                reset_results()
                print("Symptoms recorded. Choose option 3 to analyze.")

            elif choice == "3":
                if have_inputs():
                    alert = saf.emergency_alert(state["text"])
                    if alert:
                        print("\n" + alert + "\n")
                    ensure_analysis()
                    print("\n" + ana.format_analysis(state["symptoms"], state["analysis"]))
                    print("\n" + ctx_text())

            elif choice == "4":
                if have_inputs():
                    ensure_followups()
                    print("\n" + qst.format_followups(state["followups"]))

            elif choice == "5":
                if have_inputs():
                    ensure_analysis()
                    print("\n" + ana.format_conditions(state["analysis"]))

            elif choice == "6":
                if have_inputs():
                    ensure_guidance()
                    print("\n" + saf.format_guidance(state["guidance"]))

            elif choice == "7":
                print("\n" + DISCLAIMER)

            elif choice == "8":
                if have_inputs():
                    ensure_analysis()
                    ensure_followups()
                    ensure_guidance()
                    path = sav.save_report(state["profile"], state["symptoms"], state["analysis"],
                                           state["missing"], state["followups"], state["guidance"])
                    print(f"Report saved to: {path}")

            elif choice == "9":
                print("Take care. Remember: this tool is not a substitute for a healthcare professional.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 9.")
        except Exception as e:
            print(f"Error: {e}")


def ctx_text():
    return ctx.format_missing(state["missing"])


if __name__ == "__main__":
    main()
