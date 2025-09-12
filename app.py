from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

CLIENT_URL = "http://127.0.0.1:5001"  # Local helper agent

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    try:
        action = request.form.get("action")
        mac_ip = request.form.get("mac_ip")
        mac_user = request.form.get("mac_user")
        fqdn = request.form.get("fqdn")
        ent_name = request.form.get("ent_name")
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        payload = {
            "action": action,
            "mac_ip": mac_ip,
            "mac_user": mac_user,
            "fqdn": fqdn,
            "ent_name": ent_name,
            "user_id": user_id,
            "password": password,
        }

        r = requests.post(f"{CLIENT_URL}/run", json=payload, timeout=60)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"success": False, "output": str(e)})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
