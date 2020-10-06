try:
    import unzip_requirements
except ImportError:
    pass

import csv
import boto3
import json
import os
from datetime import datetime

TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
OUTPUT_BUCKET = os.environ['S3_BUCKET']
HEADERS = os.environ['HEADERS'].split(',')
TEMP_FILENAME = '/tmp/result.csv'
OUTPUT_KEY_PREFIX = 'exports/'
OUTPUT_KEY_SUFFIX =  datetime.now().strftime("%Y-%m-%d")

s3_resource = boto3.resource('s3')
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(TABLE_NAME)


def get_values(item, headers):
    return [item.get(header, "") for header in headers]


def handle(event, context):

    with open(TEMP_FILENAME, 'w') as output_file:
        writer = csv.writer(output_file)
        header = True
        first_page = True

        # Paginate results
        while True:

            # Scan DynamoDB table
            if first_page:
                response = table.scan()
                first_page = False
            else:
                response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])

            for item in response['Items']:

                # Write header row?
                if header:
                    writer.writerow(HEADERS)
                    header = False

                writer.writerow(get_values(item, HEADERS))

            # Last page?
            if 'LastEvaluatedKey' not in response:
                break

    # Upload temp file to S3
    s3_resource.Bucket(OUTPUT_BUCKET).upload_file(TEMP_FILENAME, f'{OUTPUT_KEY_PREFIX}{OUTPUT_KEY_SUFFIX}.csv')


if __name__ == "__main__":
    handle(None, None)
