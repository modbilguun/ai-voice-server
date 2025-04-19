from flask import Flask, request, jsonify
import os
from whisper_transcribe import transcribe_audio
from ask_gpt import ask_gpt
from scipy.io import wavfile
import numpy as np

app = Flask(__name__)  # 🟢 ЭНЭ ШУУД ЭХЭНДЭЭ БАЙХ ЁСТОЙ

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return "🤖 AI Voice Receiver Working!"

@app.route("/process_all", methods=["POST"])
def process_all():
    print("📥 POST /process_all дуудагдлаа")

    if "audio" not in request.files:
        print("❌ Аудио файл байхгүй байна")
        return jsonify({"error": "Аудио олдсонгүй"}), 400

    audio_file = request.files["audio"]
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)
    print(f"✅ Аудио хүлээн авлаа: {file_path}")

    try:
        sample_rate, audio_data = wavfile.read(file_path)
        audio_data = audio_data.astype(np.float32) / 32768.0
    except Exception as e:
        print("❌ Файл уншихад алдаа:", e)
        return jsonify({"error": f"Файл уншихад алдаа: {str(e)}"}), 500

    try:
        text = transcribe_audio(audio_data)
        print("🗣️ Танигдсан текст:", text)
    except Exception as e:
        print("❌ Whisper хөрвүүлэлтэд алдаа:", e)
        return jsonify({"error": f"Whisper алдаа: {str(e)}"}), 500

    try:
        reply = ask_gpt(text)
        print("🤖 GPT хариу:", reply)
    except Exception as e:
        print("❌ GPT хариу авахад алдаа:", e)
        return jsonify({"error": f"GPT алдаа: {str(e)}"}), 500

    return jsonify({
        "recognized_text": text,
        "gpt_reply": reply
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
