import boto3
import json
import os
from botocore.exceptions import ClientError


def delete_phone(event, context):
    dynamodb = boto3.resource('dynamodb')
    phones_table = dynamodb.Table(os.getenv('PHONES_TABLE'))

    body = json.loads(event['body'])
    try:
        phones_table.delete_item(
            Key={
                'Phone': str(body['phone'])
            }
        )
    except ClientError as e:
        print(e)

    response = {
        "statusCode": 200
    }

    return response
