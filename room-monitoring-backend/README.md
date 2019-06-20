# room-monitoring-backend

This application was originally created to work along the following projects:

[room-monitoring-sys](https://github.com/heidinv12/room-monitoring-sys)

[room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm)

[room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend)

I decided to design it as a serverless component so I could focus all my time on coding without involving infrastructure. I used serverless framework to implement the project's configurations, as well as AWS Lambda for the endpoints.

# Technologies/Services used:

- Serverless Framework
- Twilio API
- AWS Lambda
- AWS DynamoDB
- AWS S3

# Code Description

The following is a diagram of how the endpoints in the backend interact with DynamoDB, S3 and Twilio as well as [room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend) and [room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm).

![](/media/backend_diagram.PNG)

**Endpoints**

```createConfigData``` used by [room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend), it expects the temperature and humidity configurations specified by a frontend user. This configuration values are then stored in a table in DynamoDB and will later be used by ```notificationWorker``` and ```getData```.

```createPhoneData``` also  used by [room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend), it expects a phone number and a name specified by a frontend user. This values are then stored in a table in DynamoDB and will later be used by ```notificationWorker``` and ```getData```.

```getData``` returns a dictionary in Json format containing the latest temperature and humidity configuration, a list of phones, the dates when the motion sensor was triggered, dates the gas sensor was triggered, dates the door sensor was triggered, and the actual room temperature and humidity values. This function is currently being used by [room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend).

```dataProcessing``` is used by [room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm), it expects five values as parameters: door sensor value, temperature, humidity, motion snesor and gas sensor value. The endpoint formats the data and stores it in an S3 bucket as Json files.

```notificationWorker``` is triggered by an S3 event, more specifically by the creation of a new object in the provided S3 bucket. This function gets a list of all phone numbers registered as well as the latest temperature and humidity configuration from DynamoDB. It then compares the latest configuration against the values newly stored in S3(which represent the room's real status). If conditions are met/unmet an alert message will be sent to each phone number on the list using TWILIO API.

Here is what the phone notifications look like:

![](/media/backend_notification.jpg)
