import os

from flask import Flask, request, jsonify
import requests

# create the Flask app
app = Flask(__name__)


@app.route('/checksum', methods=['POST'])
def get_message():
    content = request.json
    if "file" in content.keys() and content['file']:
        path = os.path.join(app.root_path, "/usr/src/" + content["file"])
        if os.path.exists(path):
            res = requests.post('http://app2:5001/', json={"data": content['file']})
            return res.json()
        else:
            return jsonify({"error": "File not found.", "file": content["file"]})
    else:
        return jsonify({"error": "Invalid JSON input.", "file": print("null")})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
