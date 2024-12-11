from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)


@app.route("/display-message", methods=["POST"])
def display_message():
    data = request.get_json()
    if "line1" not in data or "line2" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Call the external Python script with the JSON data
    script_path = "./display_test.py"
    result = subprocess.run(
        ["python3", script_path, json.dumps(data)], capture_output=True, text=True
    )

    if result.returncode != 0:
        return (
            jsonify({"error": "Script execution failed", "details": result.stderr}),
            500,
        )

    return jsonify({"message": "Script executed successfully", "output": result.stdout})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
