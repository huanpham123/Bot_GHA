import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# Lấy API key từ biến môi trường GEMINI_API_KEY
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/')
def index():
    return render_template("ghiam.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "API error", "details": response.text}), 500
        
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            # Giả sử cấu trúc phản hồi: { "content": { "parts": [ { "text": ... } ] } }
            reply = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "Không có nội dung phản hồi.")
        else:
            reply = "Không nhận được phản hồi từ API."
        return jsonify({"final_answer": reply})
    except Exception as e:
        return jsonify({"error": "API error", "details": str(e)}), 500

if __name__ == '__main__':
    # Vercel sẽ quản lý quá trình khởi chạy, sử dụng PORT từ biến môi trường
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
