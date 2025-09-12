from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    action = data.get("action")
    mac_ip = data.get("mac_ip")
    mac_user = data.get("mac_user")
    fqdn = data.get("fqdn")
    ent_name = data.get("ent_name")
    user_id = data.get("user_id")
    password = data.get("password")

    try:
        if action in ["register", "connect"]:
            cmd = f'ssh {mac_user}@{mac_ip} "osascript ~/automation/{action}.scpt \'{fqdn}\' \'{ent_name}\' \'{user_id}\' \'{password}\'"'
        elif action in ["disconnect", "fetch", "uninstall"]:
            cmd = f'ssh {mac_user}@{mac_ip} "osascript ~/automation/{action}.scpt"'
        elif action == "ssh":
            cmd = f'start cmd /k ssh {mac_user}@{mac_ip}'
        else:
            return jsonify({"success": False, "output": "Invalid action"})

        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            return jsonify({"success": True, "output": process.stdout})
        else:
            return jsonify({"success": False, "output": process.stderr})

    except Exception as e:
        return jsonify({"success": False, "output": str(e)})

if __name__ == "__main__":
    app.run(port=5001)
