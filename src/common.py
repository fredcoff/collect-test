import boto3
from botocore.exceptions import ClientError


def get_data_from_s3(bucket, key):
    try:
        s3_resource = boto3.resource('s3')
        s3_object = s3_resource.Object(bucket, key)

        return s3_object.get()['Body'].read().decode('utf-8')
    except ClientError as e:
        print (e)
        return None
