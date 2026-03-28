import os
import torch
import gradio as gr
from dotenv import load_dotenv
from transformers import pipeline
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# .env
load_dotenv()

def get_watsonx_llm():
    # chargement des variables .env
    api_key = os.getenv("IBM_WATSONX_APIKEY")
    url = os.getenv("IBM_WATSONX_URL")
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")


    # Configuration de l'IA : 'greedy' force le choix du mot le plus probable pour garantir une analyse factuelle et pas inventif / Similaire à Temperature
    # 800 limite de longueur de la réponse
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 800,
    }
     # Creation de l'objet WatsonxLLM pour connecter le code à Granite d'IBM
    return WatsonxLLM(
        model_id="ibm/granite-3-8b-instruct",
        url=url,
        apikey=api_key,
        project_id=project_id,
        params=parameters,
    )

llm = get_watsonx_llm()

# Prompt d'instruction
def analyze_with_watsonx(transcript_text):
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template=(
            "Instructions: You are a professional assistant. Analyze the transcript below.\n"
            "Provide a summary, action items, and tone.\n\n"
            "Transcript:\n{transcript}\n\n"
            "Analysis:"
        )
    )

    # LCEL = LangChain Expression Language : pipeline (prompt => llm)
    chain = prompt | llm
    # Execution de la chain avec .invoke
    response = chain.invoke({"transcript": transcript_text})
    return response

# Fonction principale
def process_audio(audio_path):
    if audio_path is None:
        return "Erreur : Veuillez fournir un fichier audio."

    try:
        # Charge le modèle de reconnaissance vocale en local (utilisation GPU avec cuda) / decoupage de l'audio en tranche de 30s.
        print("--- Transcription audio en cours... ---")
        stt_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny.en",
            chunk_length_s=30,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        # Transcription par lots de 8 morceaux de 30s
        result = stt_pipe(audio_path, batch_size=8)
        transcription = result["text"]
        
        print("--- Analyse intelligente en cours... ---")

        # Envoie le texte transcrit à la fonction Watsonx pour obtenir l'analyse IA.
        analysis = analyze_with_watsonx(transcription)

        # Assemble et formate le texte final pour l'affichage dans l'interface.
        return f"--- TRANSCRIPTION ---\n{transcription}\n\n--- ANALYSE ---\n{analysis}"

    except Exception as e:
        return f"Une erreur est survenue : {str(e)}"

# WEB Interface Gradio
demo = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(sources="upload", type="filepath", label="Fichier Audio"),
    outputs=gr.Textbox(label="Résultat final", lines=20),
    title="🎙️ Business AI Meeting Companion",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)