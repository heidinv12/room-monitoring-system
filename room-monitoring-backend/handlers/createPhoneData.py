import os
import json
import boto3
import datetime
from botocore.exceptions import ClientError


def create_phone(event, context):
    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    phones_table = dynamodb.Table(os.getenv('PHONES_TABLE'))

    date = str(datetime.datetime.now().replace(microsecond=0))
    try:
        if body['phone']:
            phones_table.put_item(
                Item={
                    'Phone': str(body['phone']),
                    'Name': body['user'],
                    'CreatedAt': date
                }
            )
    except ClientError as e:
        print(e)

    response = {
        "statusCode": 200
    }

    return response
