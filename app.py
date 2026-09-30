import os, json, difflib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "faqs.json"), encoding="utf-8") as f:
    faqs = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    val = (data.get("message") or data.get("question") or "").strip().lower()
    if not val:
        return jsonify({"answer": "Please type a question."})

    questions = [f["question"].lower() for f in faqs]
    match = difflib.get_close_matches(val, questions, n=1, cutoff=0.6)
    if match:
        return jsonify({"answer": faqs[questions.index(match[0])]["answer"]})
    return jsonify({"answer": "Sorry, I don't have an answer for that yet."})

if __name__ == "__main__":
    app.run(debug=True)