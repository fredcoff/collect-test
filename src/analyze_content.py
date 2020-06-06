try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import os
import datetime
import json
import csv
import re
import uuid
from .common import get_data_from_s3, ResultModel


def get_organized_urls_from_s3(bucket, key):
    lines = get_data_from_s3(bucket, key).splitlines()
    urls = csv.DictReader(lines)

    url_dic = {}
    try:
        for url in urls:
            url_dic[url['id']] = url['path']
    except:
        print ("error while processing urls")

    return url_dic


def get_content_from_s3(bucket, key):
    return get_data_from_s3(bucket, key)


def get_keywords_from_s3(bucket, key):
    try:
        lines = get_data_from_s3(bucket, key).splitlines()
        keywords = csv.DictReader(lines)

        return keywords
    except:
        print ("error while getting keywords")
        return []


def process_content(content, keywords, url, key):
    result = ResultModel(id=str(uuid.uuid4()), url=url, content=key, 
        lastUpdate=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    
    if content == '404':
        result.status = 404
        result.tags = ''
    else:
        tags = []
        for keyword in keywords:
            pat = keyword['Keyword/Phrase']
            res = re.search(f'\\b{pat}\\b', content, flags=re.IGNORECASE)
            if res:
                tags.append(res.group())
        result.tags = ','.join(tags)
        result.status = 200
    
    print (result.tags)
    result.save()


def get_id_from_key(key):
    pos = key.rfind('/')
    if pos != -1:
        return key[pos+1:]
    return key


def handle(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    content = get_content_from_s3(bucket, key)

    if content == '':
        return False

    keywords = get_keywords_from_s3(os.environ['S3_BUCKET'], os.environ['S3_KEY_KEYWORDS'])

    url_dic = get_organized_urls_from_s3(os.environ['S3_BUCKET'], os.environ['S3_KEY_URLS'])
    
    url_id = get_id_from_key(key)
    if url_id in url_dic:
        process_content(content, keywords, url_dic[url_id], key)
        return True
    
    return False


if __name__ == "__main__":
    handle({
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": os.environ['S3_BUCKET']
                    },
                    "object": {
                        "key": "2020/6/1"
                    }
                }
            }
        ]
    }, None)
