# send_response.py
import requests
from send_response import send_to_phone


# Утсан дээр ажиллаж байгаа серверийн хаяг (Wi-Fi эсвэл Cloudflare tunnel ашиглаж болно)
PHONE_API_BASE = "http://10.6.133.47"  # ← үүнийг өөрийн IP эсвэл туннелээр солиорой

def send_to_phone(text):
    try:
        # Утсанд текст илгээх
        response = requests.post(
            f"{PHONE_API_BASE}/speak_text",  # эсвэл /show_text
            json={"text": text},
            timeout=5
        )

        if response.status_code == 200:
            print("✅ Хариу утсанд илгээгдлээ!")
        else:
            print(f"⚠️ Илгээхэд алдаа гарлаа: {response.status_code}, {response.text}")

    except Exception as e:
        print("❌ Утас руу хариу илгээхэд алдаа гарлаа:", e)
