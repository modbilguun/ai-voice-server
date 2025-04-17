from flask import Flask, request, jsonify
from whisper_transcribe import transcribe_audio_from_file  # Whisper хөрвүүлэлт
from ask_gpt import ask_chatgpt                            # ChatGPT API
from send_response import send_to_phone                    # Хариуг утас руу илгээх
import os
import traceback

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/process_all", methods=["POST"])
def process_all():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        # 1. Аудио хадгалах
        audio_file = request.files['audio']
        audio_path = os.path.join(UPLOAD_FOLDER, "latest.wav")
        audio_file.save(audio_path)

        print("➡️ Whisper хөрвүүлэлт эхэлж байна...")
        transcript = transcribe_audio_from_file(audio_path)
        print(f"🎙 Танигдсан текст: {transcript}")

        print("🤖 ChatGPT рүү илгээж байна...")
        reply = ask_chatgpt(transcript)
        print(f"📩 GPT хариу: {reply}")

        print("📲 Утас руу хариу илгээж байна...")
        send_to_phone(reply)

        return jsonify({
            "status": "success",
            "recognized_text": transcript,
            "gpt_reply": reply
        })

    except Exception as e:
        print("❌ Алдаа гарлаа:")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Локал болон Render дээр ажиллуулж болно
    app.run(host="0.0.0.0", port=5000)
