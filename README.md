# Experiment 6 - AI-Powered Medical Symptom Assistant (Ollama / local LLM)
24CS2506 - Building Applications using GPT-4

Informational tool only. It is NOT a medical diagnosis.

## Setup
1. Ollama must be installed and running (https://ollama.com)
2. ollama pull llama3.2        (or set OLLAMA_MODEL to another installed model)
3. pip install -r requirements.txt

## Run
    python main.py

Other model:  $env:OLLAMA_MODEL="mistral"    (PowerShell)   |   set OLLAMA_MODEL=mistral   (cmd)

## Suggested order
1 (patient info, or load a sample case) -> 2 (symptoms) -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 (save) -> 9
Report is saved to outputs/medical_analysis.txt
