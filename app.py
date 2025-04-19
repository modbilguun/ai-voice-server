# app.py – Render дээр ажиллах зориулалттай
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Локал PC дээр ажиллаж буй receiver.py-н хаяг (IP-ээ тааруулна уу)
LOCAL_RECEIVER = "https://te-authorized-naples-gmt.trycloudflare.com"  # ← энд өөрийн локал IP-г тавь

@app.route("/", methods=["GET"])
def root():
    return "🌐 Render Upload API Working!"

@app.route("/upload", methods=["POST"])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    files = {
        'audio': (
            audio_file.filename,
            audio_file.stream,
            audio_file.content_type
        )
    }

    try:
        print("🔁 Локал receiver рүү илгээж байна...")
        response = requests.post(LOCAL_RECEIVER, files=files)

        if response.ok:
            return response.json(), response.status_code
        else:
            return jsonify({"error": "Local server returned error"}), 500
    except Exception as e:
        print(f"❌ Алдаа гарлаа: {e}")
        return jsonify({"error": "Failed to contact local server"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
