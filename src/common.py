import boto3
from botocore.exceptions import ClientError
import os
from pynamodb.attributes import UnicodeAttribute, UnicodeAttribute, NumberAttribute, MapAttribute, ListAttribute, BooleanAttribute
from pynamodb.models import Model


class EmailMap(MapAttribute):
    email = UnicodeAttribute(null=False)
    primary = BooleanAttribute(default=False)
    email_type = UnicodeAttribute(null=True)


class ResultModel(Model):
    class Meta:
        table_name = os.environ['DYNAMODB_TABLE_NAME']
        region = os.environ['AWS_REGION']
    id = UnicodeAttribute(hash_key=True)
    url = UnicodeAttribute(null=False)
    status = NumberAttribute(default=404)
    content = UnicodeAttribute(null=True)
    tags = UnicodeAttribute(null=True)
    lastUpdate = UnicodeAttribute(null=True)
    emails = ListAttribute(of=EmailMap)


def get_data_from_s3(bucket, key):
    try:
        s3_resource = boto3.resource('s3')
        s3_object = s3_resource.Object(bucket, key)

        return s3_object.get()['Body'].read().decode('utf-8')
    except ClientError as e:
        print (e)
        return None
