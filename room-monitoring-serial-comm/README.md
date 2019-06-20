# room-monitoring-serial-comm

This code uses python library PySerial to extract data from a serial port. It was originally created to get data from a series of sensors connected to an Arduino board and send that data as a formatted payload to an API for storage. Below are the links to the Arduino project and Backend web application this script connects to:

[room-monitoring-sys](https://github.com/heidinv12/room-monitoring-sys)

[room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend)

[room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend)

Following is a diagram of how all components work together:

![](/media/diagram_of_components.PNG)

The code expects five values from the serial port and sends the data to [room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend) by doing a POST request on 'DataProcessing' endpoint.
