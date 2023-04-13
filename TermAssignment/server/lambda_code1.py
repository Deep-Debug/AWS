from __future__ import print_function
import boto3
import json
import urllib

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


def get_faceId(bucket_name, key):
    print("inside index call>>>>>>>>>>>>>>>>: ", key, bucket_name)
    response = rekognition.index_faces(
        Image={"S3Object":
                   {"Bucket": bucket_name, "Name": key}},
        CollectionId="demo_1")
    return response


def add_data_dynamoDB(table_name, face_id, person_name):
    print("inside head call>>>>>>>>>>>>>>>>: ", table_name, face_id, person_name)
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            'RekognitionId': {'S': face_id},
            'FullName': {'S': person_name}
        }
    )


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("Records: ", event['Records'])
    key = event['Records'][0]['s3']['object']['key']
    print("KeyNew>>>>>>>>>>>>>>>>: ", key)
    try:
        print("befier index call>>>>>>>>>>>>>>>>: ", key, bucket)
        response = get_faceId(bucket, key)
        print("after index call>>>>>>>>>>>>>>>>: ", key, bucket, ">>>>>>>>", response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            face_id = response['FaceRecords'][0]['Face']['FaceId']
            print("before head call>>>>>>>>>>>>>>>>: ", key, bucket)
            ret = s3.head_object(Bucket=bucket, Key=key)
            print("after head call>>>>>>>>>>>>>>>>: ", key, bucket, ">>>>>>>>>>", ret)
            person_name = ret['Metadata']['fullname']
            print("before update call>>>>>>>>>>>>>>>>: ", key, bucket, ">>>>>>>>>>", person_name)
            add_data_dynamoDB('facedata', face_id, person_name)
            print("after update call>>>>>>>>>>>>>>>>: ", face_id, person_name)
        # Print response to console
        print(response)
        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e