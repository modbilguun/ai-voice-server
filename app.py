from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Локал receiver.py ажиллаж буй tunnel URL
LOCAL_RECEIVER = "https://memories-aids-telling-journey.trycloudflare.com "

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
            result = response.json()
            print("✅ Хариу амжилттай ирлээ:", result)
            return jsonify(result), 200
        else:
            print("❌ Локал серверээс алдаа:", response.status_code)
            return jsonify({"error": "Local server returned error"}), 500
    except Exception as e:
        print(f"❌ Алдаа гарлаа: {e}")
        return jsonify({"error": "Failed to contact local server"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
