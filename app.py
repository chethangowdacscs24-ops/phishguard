"""Web demo:  python app.py  ->  http://127.0.0.1:5000"""
from flask import Flask, render_template, request, jsonify
from predict import check_url

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def api_check():
    url = (request.get_json(silent=True) or {}).get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    return jsonify(check_url(url))


if __name__ == "__main__":
    app.run(debug=True)
