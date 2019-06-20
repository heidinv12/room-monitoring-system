import boto3
import json
import os
from operator import itemgetter
from datetime import datetime as dt
from datetime import date


def get_data(event, context):
    try:
        # get latest object from S3
        today = date.today()
        s3 = boto3.client('s3')
        s3_keys = s3.list_objects_v2(Bucket=os.getenv('S3_BUCKET'), Prefix=str(today), MaxKeys=500)

        s3_data = []
        motion_trigger_dates = []
        smoke_triggered_dates = []
        door_trigger_dates = []
        for key in s3_keys['Contents']:
            s3_obj = s3.get_object(
                Bucket=os.getenv('S3_BUCKET'),
                Key=key['Key']
            )
            item = json.loads(s3_obj['Body'].read().decode('utf-8'))
            if item['MotionDetectorState'] == 'Motion Detected':
                if is_one_min_apart(motion_trigger_dates, item['Date']):
                    motion_trigger_dates.append(item['Date'])
            elif item['SmokeSensorState'] == 'Alert':
                if is_one_min_apart(smoke_triggered_dates, item['Date']):
                    smoke_triggered_dates.append(item['Date'])
            elif item['Door'] == 'Alert':
                if is_one_min_apart(door_trigger_dates, item['Date']):
                    door_trigger_dates.append(item['Date'])

            s3_data.append(item)

        dynamodb = boto3.resource('dynamodb')
        config_table = dynamodb.Table(os.getenv('CONFIG_TABLE'))
        phones_table = dynamodb.Table(os.getenv('PHONES_TABLE'))

        # get latest configuration
        config_data = config_table.scan()['Items']
        newest_config = sorted(config_data, key=itemgetter('CreatedAt'), reverse=True)[0]
        phone_response = phones_table.scan()['Items']
        latest_room_status = sorted(s3_data, key=itemgetter('Date'), reverse=True)[0]

        data = {
            'Configurations': newest_config,
            'Phones': phone_response,
            'MotionSensor': motion_trigger_dates,
            'SmokeAlert': smoke_triggered_dates,
            'DoorSensor': door_trigger_dates,
            'RoomTemperature': latest_room_status['Temperature'],
            'RoomHumidity': latest_room_status['Humidity']
        }
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            "access-control-allow-origin": "*"
        }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(data)
        }
    except Exception as e:
        print('Couldnt fetch keys from S3 bucket: ' + str(e))
        return {
            "statusCode": 550,
            "message": "An error occurred while fetching the data"
        }


def is_one_min_apart(arr, d):
    d = dt.strptime(d, "%Y-%m-%d %H:%M:%S")
    for a in arr:
        a = dt.strptime(a, "%Y-%m-%d %H:%M:%S")
        diff = d - a
        if diff.total_seconds() <= 60:
            return False
    return True
