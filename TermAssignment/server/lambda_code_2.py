import boto3
import random

s3 = boto3.resource('s3')
BUCKET_NAME = 'videodemotestimagesforfinalproject'


def lambda_handler(event, context):
    bucket_name = 'videodemotestimagesforfinalproject'
    bucket = s3.Bucket(bucket_name)
    objects = list(bucket.objects.all())
    random_object = random.choice(objects)
    # Generate the object URL
    object_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{random_object.key}'
    # Return the object URL in the response
    return {
        'statusCode': 200,
        'body': object_url
    }