from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyAkf0LX8MDpgpfJSu05u2Z83v4GK_PdTWg")
model = genai.GenerativeModel("gemini-2.0-flash")

# Store chat history in a global list (reset if app restarts)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["text"]]} for m in chat_history
            ])
            response = chat.send_message(user_msg)
            reply = response.text.strip() if response.text else "(no response)"

            # Save to history
            chat_history.append({"role": "user", "text": user_msg})
            chat_history.append({"role": "model", "text": reply})

        return redirect(url_for("home"))

    return render_template("index.html", history=chat_history)

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    return redirect(url_for("home"))
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)
