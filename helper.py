from flask import Flask, request, jsonify
import subprocess
import platform
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/check_connection", methods=["POST"])
def check_connection():
    data = request.get_json()
    mac_ip = data.get("mac_ip")

    try:
        system = platform.system()
        if system == "Windows":
            cmd = ["ping", "-n", "1", "-w", "1000", mac_ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", mac_ip]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "output": result.stdout or result.stderr})
    except Exception as e:
        return jsonify({"success": False, "output": str(e)})


@app.route("/run_script", methods=["POST"])
def run_script():
    try:
        data = request.get_json()
        mac_user = data.get("mac_user")
        mac_ip = data.get("mac_ip")
        script = data.get("script")
        args = data.get("args", [])

        if not mac_user or not mac_ip or not script:
            return jsonify({"success": False, "output": "Missing inputs"}), 400

        if args:
            args_str = " ".join([f"'{a}'" for a in args])
            remote_cmd = f"osascript $HOME/Documents/automation/{script} {args_str}"
        else:
            remote_cmd = f"osascript $HOME/Documents/automation/{script}"

        ssh_cmd = ["ssh", f"{mac_user}@{mac_ip}", remote_cmd]

        system = platform.system()
        if system == "Windows":
            subprocess.Popen(
                ["cmd.exe", "/k"] + ssh_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif system == "Darwin":
            subprocess.Popen(
                [
                    "osascript",
                    "-e",
                    f'tell application "Terminal" to do script "{" ".join(ssh_cmd)}"',
                ]
            )
        else:
            subprocess.Popen(["gnome-terminal", "--"] + ssh_cmd)

        return jsonify({"success": True, "command": " ".join(ssh_cmd)})
    except Exception as e:
        return jsonify({"success": False, "output": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
