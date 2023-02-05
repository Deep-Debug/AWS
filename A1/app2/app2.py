from flask import Flask, request, jsonify
import hashlib

# create the Flask app
app = Flask(__name__)


@app.route('/', methods=['POST'])
def calculate_md5():
    my_response = {}
    content = request.json
    file_name = content['data']
    with open('/usr/src/' + file_name, 'rb') as my_file:
        line = my_file.read()
        my_response["file"] = file_name
        my_response["checksum"] = hashlib.md5(line).hexdigest()
        return jsonify(my_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
