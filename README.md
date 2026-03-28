🎙️ Business AI Meeting Companion

Ce projet est un assistant intelligent qui automatise la transcription et l'analyse de vos réunions audio en combinant Whisper (STT) et IBM WatsonX (LLM).

✨ Fonctionnalités
Transcription précise : Conversion de l'audio en texte via le modèle Whisper d'OpenAI.

Analyse Intelligente : Résumé automatique, extraction des points clés et ton de la conversation via IBM WatsonX.

Interface Web : UI simple et intuitive développée avec Gradio.

🛠️ Installation
Bash
# 1. Cloner le projet
git clone https://github.com/JN13012/Business_AI_Meeting_Companion_STT
cd Business_AI_Meeting_Companion_STT

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

🚀 Utilisation
Configurez vos clés API WatsonX dans le fichier main.py (ou via un fichier .env).

Lancez l'application :

Bash
python main.py
Ouvrez votre navigateur sur http://localhost:7860 pour tester l'outil.