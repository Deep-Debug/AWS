import requests
from flask import Flask, request
import os
import json
import boto3

app = Flask(__name__)


@app.route('/start')
def start():
    my_data = {"banner": "B00931783", "ip": "34.203.77.194"}
    response = requests.post(' http://52.91.127.198:8080/start/', json={"data": my_data})
    return response


# source code used :- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
# The AWS SDK for Python provides a pair of methods to upload a file to an S3 bucket.
# Modification :- changed parameters, added file creation and create s3Uri code for assignment requirement
@app.route('/storedata', methods=['POST'])
def store_data():
    try:
        my_data = request.get_json()
        data = my_data['data']
        file_name = "deep.txt"
        with open(file_name, "w") as fp:
            fp.write(data)
        object_name = os.path.basename(file_name)
        s3_client = boto3.client('s3')
        bucket = "csci5409-23-02-23"
        s3_client.upload_file(file_name, bucket, object_name)
        url = "https://csci5409-23-02-23.s3.amazonaws.com/deep.txt"
        response = json.loads('{"s3uri":"' + url + '"}')
        return response
    except Exception as e:
        print(e)
        return json.loads('{"error": "Error in storedata"}')


# source code used:- https://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket
# Modification:- changed bucket name, object name and aws credential
@app.route('/deletefile', methods=['POST'])
def delete_file():
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-1",
        aws_access_key_id="ASIAUU2KQSQXAPME4ZAW",
        aws_secret_access_key="xnqb5uC59PlauBEeirNdLqOycWAgEY46GFPwfjmf",
        aws_session_token="FwoGZXIvYXdzEJ7//////////wEaDKQGuBN5ns7Q5Ta9aCLAATD2zz7mv9MwPwZySvFjVPudZWMpVBXOHO3EPl/Nuecsz2gKNgQXXTwyNcxcwF4Ihtn0v4Efgz6P4lrBOiNEkCf7MbQOTpNt7oZsO4R3+9gB1TfyIrBb7BJLHwnspjlgxF+k+lWmlUt6VtnKaJrQqVujqR8ubRYTLVlhXPXbDvBdVNu5DoOWmRfRrT2j2EnSNkrQm99X7bQqB4IceJa4K+HozcQMPi3CihhWdIE0IX62YjQyrSE6RXBnrnMFY4w3uCiF4emfBjItPCXZ1f4FXIeXnmbvrfrpo8gnnh0j+ApIE4BylwNU8A8wDFphk4ULPcJEQ4mu"
    )
    s3.Object('csci5409-23-02-23', 'deep.txt').delete()
    return "deleted successfully"


# source code used :- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
# The AWS SDK for Python provides a pair of methods to upload a file to an S3 bucket.
# Modification :- changed parameters, added file creation and create s3Uri code for assignment requirement
@app.route('/appenddata', methods=['POST'])
def append_data():
    try:
        my_data = request.get_json()
        data = my_data['data']
        file_name = "deep.txt"
        with open(file_name, "a") as fp:
            fp.write(data)
        object_name = os.path.basename(file_name)
        s3_client = boto3.client('s3')
        bucket = "csci5409-23-02-23"
        s3_client.upload_file(file_name, bucket, object_name)
        url = "https://csci5409-23-02-23.s3.amazonaws.com/deep.txt"
        response = json.loads('{"s3uri":"' + url + '"}')
        return response
    except Exception as e:
        print(e)
        return json.loads('{"error": "Error in appenddata"}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
