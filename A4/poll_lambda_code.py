import json
import boto3

sqs = boto3.client('sqs')

connect_queue_url = 'https://sqs.us-east-1.amazonaws.com/319594468398/connect_queue'
subscribe_queue_url = 'https://sqs.us-east-1.amazonaws.com/319594468398/subscribe_queue'
publish_queue_url = 'https://sqs.us-east-1.amazonaws.com/319594468398/publish_queue'


def lambda_handler(event, context):
    sqs = boto3.client('sqs')

    msg_type = event['type']

    if msg_type == 'CONNECT':
        queue_url = connect_queue_url
    elif msg_type == 'SUBSCRIBE':
        queue_url = subscribe_queue_url
    elif msg_type == 'PUBLISH':
        queue_url = publish_queue_url
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid type'})
        }

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    if 'Messages' in response:
        receipt_handle = response['Messages'][0]['ReceiptHandle']

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        message_body = json.loads(response['Messages'][0]['Body'])
        print(message_body, ">>>>>>>>>>")
        if msg_type == 'CONNECT':
            return {
                'type': 'CONNACK',
                'returnCode': 0,
                'username': message_body['username'],
                'password': message_body['password']
            }
        elif msg_type == 'SUBSCRIBE':
            return {
                'type': 'SUBACK',
                'returnCode': 0
            }
        elif msg_type == 'PUBLISH':
            return {
                'type': 'PUBACK',
                'returnCode': 0,
                'payload': message_body['payload']
            }
    else:
        return {
            'error': 'No message found in queue'
        }
