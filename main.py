from flask import Flask,request,make_response, jsonify
from vertexai.preview.language_models import ChatModel,ChatSession,ChatMessage
import dotenv
from flask_cors import CORS
import json,os
from pydub import AudioSegment
dotenv.load_dotenv()
import subprocess
from google.cloud import translate

if os.environ.get("PROJECT_ID"):
    #PARENT = f"projects/{os.environ.get('PROJECT_ID')}"
    PARENT = "projects/new-project-412511" 
if not os.path.exists("./secret.json"):
    if os.environ.get("CREDENTIALS"):
        with open("secret.json","w") as f:
            f.write(os.environ.get("CREDENTIALS"))


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True if os.environ.get("PRODUCTION","False")=="True" else True

support_context="Imagine you are a friendly, thoughtful personal healthcare advisor with the name Gaia including mental health support. A user has just reached out to you seeking guidance and support. Write a response that empathetically addresses their concerns, provides accurate healthcare information, and offers practical advice to improve their overall well-being. Keep in mind the importance of being understanding, non-judgmental, and respectful throughout the conversation."

bison_model=ChatModel.from_pretrained("chat-bison@001")

def palm(message:str,context:str,history:list):
    valid_history=[]
    for i,h in enumerate(history):
        if "content" in h and "author" in h:
            valid_history.append(ChatMessage(h["content"],h['author']))
    chat=ChatSession(model=bison_model,context=context,message_history=valid_history,temperature=0.94)
    response=chat.send_message(message)
    return response

@app.post("/query")
def query():
    try:
        req_data=request.json #message,context,history:list of chat messages
        message=req_data.get("message")
        context=req_data.get("context","")
        history=req_data.get("history",[])
        response=palm(message,context,history)
        return f"{response}"
    except Exception as e:
        return make_response("Server error",500)

@app.post("/support")
def support():
    try:
        req_data=request.json #message,context,history:list of chat messages
        message=req_data.get("message")
        context=req_data.get("context","")
        history=req_data.get("history",[])
        response=palm(message,support_context+context,history)
        return f"{response}"
    except Exception as e:
        return make_response("Server error",500)

@app.post("/convertToSpeech")
def convertToSpeech():
    try:
        audio_file = request.files['audio']
        audio_file.save("./audio.mpeg")
        sound = AudioSegment.from_file("./audio.mpeg", format="mpeg")
        sound.export("./output.ogg", format="ogg")
        result = subprocess.run(["./rhubarb","-f","json","./output.ogg"] , capture_output=True)
        return f"{result.stdout.decode('utf-8')}"
    except Exception as e:
        print(e)
        return make_response(f"{e}",500)

@app.post("/translate")
def translate1():
    try:
        client = translate.TranslationServiceClient()
        req_data=request.json
        message=req_data.get("message")
        language=req_data.get("language","en-IN")

        response = client.translate_text(
            parent="projects/new-project-412511",
            contents=[message],
            target_language_code=language,
        )
        return f"{response.translations[0].translated_text}"
    
    except Exception as e:
        print(e)
        return make_response(f"{e}",500)
    
if __name__=='__main__':
   app.run(debug=False, host="0.0.0.0", port=8080)
