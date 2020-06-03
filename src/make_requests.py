try:
    import unzip_requirements
except ImportError:
    pass

import boto3

import os
import datetime
import json
import csv
from .common import get_data_from_s3


def get_urls_from_s3(bucket, key):
    lines = get_data_from_s3(bucket, key).splitlines()
    urls = csv.DictReader(lines)

    return urls


def create_task(id, path):
    sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])

    queue.send_message(MessageBody=f'{id},{path}')


def handle(event, context):

    urls = get_urls_from_s3(os.environ['S3_BUCKET'], os.environ['S3_KEY_URLS'])
    print (urls)

    for url in urls:
        print (url)
        create_task(url['id'], url['path'])

    return {
        "statusCode": 200,
        "body": f'success'
    }


if __name__ == "__main__":
    handle(None, None)
