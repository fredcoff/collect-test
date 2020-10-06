try:
    import unzip_requirements
except ImportError:
    pass

import csv
import boto3
import json
import os
from datetime import datetime
from .common import get_data_from_s3, ResultModel

OUTPUT_BUCKET = os.environ['S3_BUCKET']
TEMP_FILENAME = '/tmp/result.csv'
OUTPUT_KEY_PREFIX = 'exports/'
OUTPUT_KEY_SUFFIX =  datetime.now().strftime("%Y-%m-%d")

s3_resource = boto3.resource('s3')

def handle(event, context):
    ResultModel.dump(TEMP_FILENAME)

    # Upload temp file to S3
    s3_resource.Bucket(OUTPUT_BUCKET).upload_file(TEMP_FILENAME, f'{OUTPUT_KEY_PREFIX}{OUTPUT_KEY_SUFFIX}.json')


if __name__ == "__main__":
    handle(None, None)
