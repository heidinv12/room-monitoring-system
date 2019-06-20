import os
import json
import boto3
import datetime
from botocore.exceptions import ClientError


def create(event, context):
    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    config_table = dynamodb.Table(os.getenv('CONFIG_TABLE'))

    try:
        date = str(datetime.datetime.now().replace(microsecond=0))
        config_table.put_item(
            Item={
                'MinTemperature': str(body['minTemperature']),
                'MaxTemperature': str(body['maxTemperature']),
                'MinHumidity': str(body['minHumidity']),
                'MaxHumidity': str(body['maxHumidity']),
                'CreatedAt': date
            }
        )
    except ClientError as e:
        print(e)

    response = {
        "statusCode": 200
    }

    return response
