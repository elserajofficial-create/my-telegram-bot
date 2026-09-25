import os
import time
import requests
from google import genai

# جلب البيانات من بيئة الاستضافة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IDIpUO6SE4C-ZR10erljYLNZ9iDWwcXKk8CRJRPUWbrg")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8924152978:AAG--Ix-9e6rLVnt8n4m0BYVkbK8gHHppzk")
CHAT_ID = os.environ.get("CHAT_ID", "7737468137")

ai_client = genai.Client(api_key=GEMINI_API_KEY)

# مسح أي Webhook قديم لتحديث الاتصال
requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def ask_gemini(prompt_text):
    try:
        system_instruction = "أنت مساعد ذكي شخصي للمستخدم سراج (Siraj). أجب بذكاء ووضوح وبلاغة."
        # استخدام النموذج المطلوب gemini-2.5-flash
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config={"system_instruction": system_instruction}
        )
        return response.text
    except Exception as e:
        return f"⚠️ حدث خطأ في معالجة الذكاء الاصطناعي: {e}"

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 10, "offset": offset}
    try:
        res = requests.get(url, params=params, timeout=15).json()
        return res.get("result", [])
    except Exception:
        return []

print("🚀 البوت يعمل الآن على الاستضافة السحابية 24/7...")
send_telegram_message("🤖 مرحباً سراج! البوت يعمل الآن بشكل دائم على السحابة دون الحاجة لـ Colab.")

updates = get_updates()
last_update_id = updates[-1]["update_id"] + 1 if updates else None

while True:
    try:
        updates = get_updates(last_update_id)
        for update in updates:
            last_update_id = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                user_msg = update["message"]["text"]
                ai_reply = ask_gemini(user_msg)
                send_telegram_message(ai_reply)
    except Exception as e:
        print(f"Error in loop: {e}")
    time.sleep(1)
