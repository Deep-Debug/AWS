import datetime
import io
import re
import time

import botocore
from PIL import Image

import requests
from flask import Flask, request, jsonify
import os
import json
import boto3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


aws_access_key_id = 'ASIAUU2KQSQXA47UFE2R'
aws_secret_access_key = 'UGecCDk3/4VhIERYk1GNrRfGqfxJ8JFlCYq8EN8U'
region_name = 'us-east-1'
table_name = 'studentdata'
aws_session_token = 'FwoGZXIvYXdzEOr//////////wEaDGf1k+gzqy74xKl8syLAAfl28QprRuVXxF9rUp2QJVbr8aWTe9hr7t8u1EktqlqNcFDLYnZASmTM5Xj4ZcivTO2jZ+uSfP6KozvF0xd8v1Pip+gmqlWCcTr5klvQzjccy+m4iRgEjTRsrb72c6OiduI+B+UP9GtAHxdF66SVzcbYulcWUfTrUy4a0meB0PG8CKduLIqYlNrcp9r0ADhq4D1DUXLJh1zOqVEdA+PEV8EdP2HU4gVYmOtBTTkiLg3X+ancs8uY4o1VGX/sSX0aHCjJwtuhBjItjo9/uMUNRJn0liXx55J9x4IOLvGxoUt6tktUA3dWTa8nDWZ1PiBEgK7DvxKM'


dynamodb = boto3.resource('dynamodb',
                          region_name=region_name,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)

dynamodb1 = boto3.client('dynamodb', region_name='us-east-1',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token
                        )

table = dynamodb.Table(table_name)

# Replace with your SNS topic ARN and email address
topic_arn = 'arn:aws:sns:us-east-1:319594468398:DalSafe'
email_address = 'deepdave08@gmail.com'

BUCKET_NAME = 'demo-images-cloud-project'

s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         aws_session_token=aws_session_token)

rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           aws_session_token=aws_session_token
                           )


@app.route('/upload', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload():
    data = request.json
    try:
        secret_name = "ApiGateWay"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        json_data = json.loads(get_secret_value_response["SecretString"])
        url = json_data["Deployment"]
        api_gateway_url = "https://" + url + ".execute-api.us-east-1.amazonaws.com/dev/imagepicker"
        response = requests.post(api_gateway_url)
        print(response)
        if response.status_code == 200:
            object_url = response.json()["body"]
            try:
                bucket_name, object_key = object_url.split('//')[1].split('/', 1)
                file_name = os.path.basename(object_key)
                bucket_name = bucket_name.split('.')[0]
                s3_client.head_object(Bucket=bucket_name, Key=object_key)
                s3_client.download_file(bucket_name, object_key, file_name)
                image = Image.open(os.path.abspath(file_name))
                stream = io.BytesIO()
                image.save(stream, format="JPEG")
                image_binary = stream.getvalue()
                response = rekognition.search_faces_by_image(
                    CollectionId='demo_1',
                    Image={'Bytes': image_binary}
                )
                isFound = False
                for res in response['FaceMatches']:
                    print(res['Face']['FaceId'], res['Face']['Confidence'])
                    face = dynamodb1.get_item(
                        TableName='facedata',
                        Key={'RekognitionId': {'S': res['Face']['FaceId']}}
                    )
                    if 'Item' in face:
                        isFound = True
                        return {"data" : data,"Found Person " : face['Item']['FullName']['S'],"image":object_url}

                if not isFound:
                    return {"data" : data,"Found Person " : 'No Criminal',"image":object_url}
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"The object {object_key} does not exist in bucket {bucket_name}")
                else:
                    print(f"Error downloading image from S3: {e}")
                return "Hii"
            return os.path.abspath(file_name)
        else:
            return {'error': f'API Gateway returned status code {response.status_code}'}
    except Exception as e:
        return {'error': f'Error in code: {e}'}
    print(data, "data>>>>>>>>>>>")
    return data


@app.route('/add_students', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_data_to_dynamodb():
    try:
        # Parse the request body as a JSON object
        data = request.json
        print(data,"data>>>>")
        # Extract the data fields
        item = {
            'id': data['id'],
            'name': data['name'],
            'number': data['number'],
            'email': data['email']
        }
        response = table.put_item(Item=item)
        print(response)
        return data

    except Exception as e:
        print(e)
        return data


@app.route('/add_criminal', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_criminal_image_inside_s3():
    try:
        file = request.files['image']
        # name = request.files['name']
        print(file, "file>>>>>>", request.form['name'])
        img_data = io.BytesIO(file.read())
        key = file.filename
        metadata = {
            'FullName': request.form['name']
        }
        try:
            s3_client.put_object(Bucket="videodemodeepfinalbucketfortheproject", Key=key, Body=img_data.getvalue(), Metadata=metadata)
            test_arr = [('test_img_1.jpg',"This is elon musk Img", 'Elon Musk'),
                      ('test_img_2.jpg',"This is Bill Gates Img", 'Bill Gates'),
                      ('test_img_3.jpg',"This is Sundar Pichai Img", 'Sundar Pichai')
                      ]
            for i in test_arr:
                with open(i[0], 'rb') as f:
                    s3_client.upload_fileobj(f, "videodemotestimagesforfinalproject", i[0], ExtraArgs={'Metadata': {'FullName':i[2]}})
            return {'message': f'{file.filename} uploaded to S3 bucket videodemotestimagesforfinalproject'}
        except Exception as e:
            return {'error': f'Error uploading {file.filename} to S3 bucket videodemotestimagesforfinalproject: {e}'}

        return "Image uploaded to S3!"
    except Exception as e:
        print(e)
        return "Image not uploaded to s3."


@app.route('/get_students', methods=['GET'])
def get_table_data():
    response = table.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    return {"data": [items]}


@app.route('/notify_students', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def notify_students():
    try:
        data = request.json
        print(data,"data>>>>>>")
        secret_name = "ApiGateWay"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        json_data = json.loads(get_secret_value_response["SecretString"])
        # Create an SNS client
        sns = boto3.client('sns',
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           aws_session_token=aws_session_token)

        # Subscribe the email address to the SNS topic
        sns.subscribe(
            TopicArn=json_data["SNS"],
            Protocol='email',
            Endpoint=data['email']
        )

        # Publish a message to the SNS topic
        sns.publish(
            TopicArn=json_data["SNS"],
            Subject='DalSafe Notification',
            Message='Warning ' + str(data['content']['Found Person ']) + ' has been seen in ' + str(data['content']['data']['hall']) + ' hall near '
                    + str(data['content']['data']['building']) + ' of ' + str(data['content']['data']['camera'])
                    + ' at ' + str(datetime.datetime.now())
        )
        return "Mail sent successfully"

    except Exception as e:
        print(e)
        return "Email not sent successfully."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
