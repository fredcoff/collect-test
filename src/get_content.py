try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import os
import datetime
import json
import csv
import requests


def get_data_from_event(event):
    if 'Records' in event and len(event['Records']) > 0 and 'body' in event['Records'][0]:
        message = event['Records'][0]['body']
        pos = message.find(',')
        if pos != -1:
            return message[:pos], message[pos+1:]

    return ''


def save_content(id, content):
    dt = datetime.date.today()

    try:
        s3 = boto3.resource('s3')
        s3.Bucket(os.environ['S3_BUCKET']).put_object(Key=f'{dt.year}/{dt.month}/{id}', Body=content)
    except:
        print ("error while saving content")


def handle(event, context):

    id, path = get_data_from_event(event)

    if path == '':
        return False

    try:
        payload = {'api_key': os.environ['API_KEY'], 'url': path}
        resp = requests.get(os.environ['SCRAPER_API'], params=payload)
        result = resp.text
    except:
        result = '404'

    save_content(id, result)

    return True


if __name__ == "__main__":
    handle({
        "Records": [
            {
                "body": "1,https://www.hklaw.com/en/professionals/d/driscoll-allison-k"
            }
        ]
    }, None)
