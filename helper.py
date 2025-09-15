from flask import Flask, request, jsonify
import subprocess
import platform
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/run_script", methods=["POST"])
def run_script():
    try:
        data = request.get_json()
        mac_user = data.get("mac_user")
        mac_ip = data.get("mac_ip")
        script = data.get("script")  # e.g., sometest.scpt

        if not mac_user or not mac_ip or not script:
            return jsonify({"success": False, "output": "Missing inputs"}), 400

        ssh_cmd = f"ssh {mac_user}@{mac_ip} 'osascript \"$HOME/Documents/automation/{script}\"'"

        system = platform.system()

        if system == "Windows":
            ssh_cmd = f"ssh {mac_user}@{mac_ip} osascript '/Users/versamacmini/Documents/automation/{script}'"
            subprocess.Popen(
                ["cmd.exe", "/k", ssh_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE
            )

        elif system == "Darwin":  # macOS
            subprocess.Popen(
                [
                    "osascript",
                    "-e",
                    f'tell application "Terminal" to do script "{ssh_cmd}"',
                ]
            )
        else:  # Linux
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", ssh_cmd])

        return jsonify(
            {"success": True, "output": "SSH script started in new terminal"}
        )

    except Exception as e:
        return jsonify({"success": False, "output": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
