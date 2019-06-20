import boto3
import json
import os
import twilio
import twilio.rest
from twilio.rest import Client
from operator import itemgetter

TWILIO_CLIENT = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))


def notify(event, context):
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    config_table = dynamodb.Table(os.getenv('CONFIG_TABLE'))  # update this
    phones_table = dynamodb.Table(os.getenv('PHONES_TABLE'))  # update this

    try:
        # get latest object from S3
        s3_obj = s3.get_object(
            Bucket=os.getenv('S3_BUCKET'),
            Key=event['Records'][0]['s3']['object']['key']
        )
        s3_obj = json.loads(s3_obj['Body'].read().decode('utf-8'))
        current_temp = s3_obj['Temperature']
        current_hum = s3_obj['Humidity']
        door = s3_obj['Door']
        smoke_alert = s3_obj['SmokeSensorState']

        # get latest configuration
        config_response = config_table.scan()
        config_data = config_response['Items']
        newest_config = sorted(config_data, key=itemgetter('CreatedAt'), reverse=True)[0]
        min_temp = int(newest_config['MinTemperature'])
        max_temp = int(newest_config['MaxTemperature'])
        min_hum = int(newest_config['MinHumidity'])
        max_hum = int(newest_config['MaxHumidity'])

        # get all registered phones
        phone_response = phones_table.scan()['Items']
    except Exception as e:
        print('Couldnt fetch keys from S3 bucket or DynamoDB tables')
        return {
            "statusCode": 550,
            "message": "An error occurred while fetching the data"
        }

    if smoke_alert == 'Alert':
        message = "SMOKE DETECTED IN THE ROOM!!"
        send_alert(message, phone_response)

    if door == 'Alert':
        message = "DOOR has been open for longer than 5 minutes"
        send_alert(message, phone_response)

    # checking temperature
    if current_temp < min_temp:
        message = "It's too cold! Temperature Is lower than " + str(min_temp) + "C"
        send_alert(message, phone_response)
    elif current_temp > max_temp:
        message = "It's too hot! Temperature Is greater than " + str(max_temp) + "C"
        send_alert(message, phone_response)

    # checking humidity
    if current_hum < min_hum:
        message = "It's not humid enough! humidity Is lower than " + str(min_hum) + "%"
        send_alert(message, phone_response)
    elif current_hum > max_hum:
        message = "It's too humid! humidity Is greater than " + str(max_hum) + "%"
        send_alert(message, phone_response)


def send_alert(msg, phone_response):
    for item in phone_response:
        return TWILIO_CLIENT.api.account.messages.create(
            body=msg,
            to='+1' + str(int(item['Phone'])),
            from_='+1' + os.getenv('TWILIO_FROM_PHONE')
        )
