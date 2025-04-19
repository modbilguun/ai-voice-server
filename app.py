# app.py – Render дээр ажиллах
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Локал receiver-г tunnel URL-р дамжуулна
LOCAL_RECEIVER = "https://mainly-projector-passenger-equipped.trycloudflare.com "

@app.route("/", methods=["GET"])
def root():
    return "🌐 Render API Working!"

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    files = {"audio": (audio_file.filename, audio_file.stream, audio_file.content_type)}

    try:
        print("📤 Локал руу дамжуулж байна...")
        response = requests.post(LOCAL_RECEIVER, files=files)

        if response.ok:
            return response.json(), 200
        else:
            print("❌ Локал серверээс error ирлээ:", response.status_code)
            return jsonify({"error": "Local server returned error"}), 500
    except Exception as e:
        print("❌ Холболт амжилтгүй:", e)
        return jsonify({"error": "Failed to contact local server"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
