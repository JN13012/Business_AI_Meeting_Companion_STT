# Business AI Meeting Companion - STT + Summary

Ce projet permet de :

1. Transcrire des fichiers audio en texte via Whisper.
2. Résumer automatiquement le contenu ou extraire les points clés via un LLM (IBM WatsonX).
3. Fournir une interface web simple avec Gradio pour tester l'outil facilement.

## Installation

```bash
git clone <ton-repo-url>
cd Business_AI_Meeting_Companion_STT
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt