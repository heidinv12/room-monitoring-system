import serial
import time
import datetime
import requests
import json

conn = serial.Serial('com3', 9600)
time.sleep(2)


def call_data_processing_api(temp, hum, door, smoke, movement):
    print('CALLING API')
    # call API with params every 30 minutes
    headers = {
        'accept': 'application/json'
    }
    url = 'DATA_PROCESSING_ENDPOINT_URL'
    data = {"temperature": temp, "humidity": hum, "door": door, "smoke": smoke, "movement": movement}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print('response ' + str(response))
    except requests.exceptions.ConnectionError:
        print('Connection error')
        time.sleep(2)


if __name__ == "__main__":
    start = time.time()
    while True:
        clean_input = conn.readline().strip().decode("utf-8")
        print(clean_input + '-' + str(datetime.datetime.now().replace(microsecond=0)))

        try:
            movement, smoke, door, temp, hum = clean_input.split('-')
            if door == 'A' or smoke == 'GA' or movement == 'MD':
                print('ALERT!')
                call_data_processing_api(temp, hum, door, smoke, movement)

            end = time.time()
            diff = int(end - start)
            if diff == 1800:
                start = time.time()
                call_data_processing_api(temp, hum, door, smoke, movement)

        except ValueError as e:
            print("Code failed: " + str(e))
