from flask import Flask, render_template, request, jsonify
import requests, os

app = Flask(__name__)

API_URL = os.environ.get("LIKE_API_URL", "https://two0likeapifreebyzexxyh4x.onrender.com/like")
API_KEY = os.environ.get("LIKE_API_KEY", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/like")
def send_like():
    data = request.get_json(silent=True) or {}
    uid = str(data.get("uid", "")).strip()
    region = str(data.get("region", "ID")).strip().upper()

    if not uid.isdigit():
        return jsonify({"ok": False, "message": "UID harus berupa angka."}), 400
    if not API_KEY:
        return jsonify({"ok": False, "message": "API key belum dipasang di server."}), 500

    try:
        r = requests.get(API_URL, params={
            "key": API_KEY, "uid": uid, "region": region
        }, timeout=30)
        return jsonify({"ok": True, "data": r.json()}), r.status_code
    except requests.RequestException as e:
        return jsonify({"ok": False, "message": f"API tidak dapat dihubungi: {e}"}), 502
    except ValueError:
        return jsonify({"ok": False, "message": "API mengirim respons bukan JSON."}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
