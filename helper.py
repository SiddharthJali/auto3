from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import platform

app = Flask(__name__)
CORS(app)

def open_terminal_and_run(command):
    system = platform.system()

    if system == "Windows":
        subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    elif system == "Darwin":
        osa = f'tell app "Terminal" to do script "{command}"'
        subprocess.Popen(["osascript", "-e", osa])
    elif system == "Linux":
        subprocess.Popen(["x-terminal-emulator", "-e", command])
    else:
        raise Exception(f"Unsupported system: {system}")

@app.route("/run_script", methods=["POST"])
def run_script():
    data = request.json
    mac_user = data.get("mac_user")
    mac_ip = data.get("mac_ip")
    script = data.get("script")
    args = data.get("args", [])

    cmd = f"ssh {mac_user}@{mac_ip} 'osascript ~/Documents/automation/{script} {' '.join([repr(a) for a in args])}'"

    try:
        open_terminal_and_run(cmd)
        return jsonify({"status": "success", "command": cmd})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
