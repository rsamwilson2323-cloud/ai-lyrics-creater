from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
import os
import traceback

# 🔑 PUT ONLY YOUR API KEY BETWEEN QUOTES
GROQ_API_KEY = "YOUR_API_KEY_HERE"

client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "ui.html")

@app.route("/lyrics", methods=["POST"])
def lyrics():
    try:
        data = request.get_json()
        mood = data.get("mood", "romantic")

        prompt = f"""
Write ORIGINAL song lyrics.

Structure:
Verse 1
Chorus
Verse 2
Chorus
Outro

Mood: {mood}
Make it emotional, creative, and unique.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=600
        )

        return jsonify({
            "lyrics": response.choices[0].message.content
        })

    except Exception:
        print("🔥 GROQ ERROR:")
        traceback.print_exc()
        return jsonify({"error": "AI generation failed"}), 500


if __name__ == "__main__":
    print("AI Lyrics Server Running...")
    app.run(host="127.0.0.1", port=5000)
