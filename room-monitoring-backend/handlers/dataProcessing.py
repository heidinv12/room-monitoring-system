import boto3
import json
import datetime
import uuid
import os

S3_CLIENT = boto3.client('s3')


def analyze_data(event, context):
    date = datetime.datetime.now().replace(microsecond=0)
    try:
        param = json.loads(event['body'])

        door = param['door']
        if door == 'A':
            door = 'Alert'
        elif door == 'H':
            door = 'Open'
        elif door == 'L':
            door = 'Closed'

        smoke_detector = param['smoke']
        if smoke_detector == 'GA':
            smoke_detector = 'Alert'
        elif smoke_detector == 'NG':
            smoke_detector = 'Passive'

        motion = param['movement']
        if motion == 'MD':
            motion = 'Motion Detected'
        elif motion == 'NM':
            motion = 'No Motion'

        body = {"SmokeSensorState": smoke_detector,
                "MotionDetectorState": motion,
                "Temperature": int(param['temperature']),
                "Humidity": int(param['humidity']),
                "Door":  door,
                "Date": str(date)}
    except KeyError as e:
        print("Event is missing specified key: %s" % e)

    key = str(datetime.date.today()) + '_' + str(uuid.uuid1())

    try:
        S3_CLIENT.put_object(Key=key,
                             Body=json.dumps(body),
                             Bucket=os.getenv('S3_BUCKET'),
                             ContentType='application/json')
    except Exception as e:
        print("Unexpected error: %s" % e)

    return {"status": 200, "message": "Process Completed"}
