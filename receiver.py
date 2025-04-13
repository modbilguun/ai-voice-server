from flask import Flask, request, jsonify
import os
from whisper_transcribe import transcribe_audio
from ask_gpt import ask_gpt_response


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "🤖 AI Voice Receiver Working!"

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "Файл олдсонгүй"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "Файлын нэр хоосон байна"}), 400

    # Хадгалах
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    print(f"✅ Хүлээн авлаа: {file_path}")

    # 1. Whisper хөрвүүлэлт
    text = transcribe_audio(file_path)
    print("🗣️ Танигдсан текст:", text)

    # 2. ChatGPT хариу авах (дараа бичигдэнэ)
    reply = ask_gpt_response(text)
    print("🤖 GPT хариу:", reply)

    return jsonify({
        "input": text,
        "response": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
