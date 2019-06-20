# Summary

In this project a combination of sensors is used along with an Arduino UNO to keep track of the status of a room and control a couple of applicances to ensure the room temperature and lighting meet the user's preferences. This piece of code was originally created to work along the following projects:

[room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm)

[room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend)

[room-monitoring-frontend](https://github.com/heidinv12/room-monitoring-frontend)

The code ouputs a serie of strings that represent the data gathered from the sensors. The strings are printed to a serial port and can be picked up by [room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm) and stored in an Simple Storage Servive(S3) bucket for further processing and analysis. Nevertheless, this code can be used as a standalone project to control the temperature and lighting in a room.

**BEFORE CONTINUING BEWARE THIS PROJECT INVOLVES HIGH VOLTAGE. TURN OFF ALL POWER TO THE CIRCUIT BEFORE WORKING ON IT. DISCONECT ANY/ALL APPLICANCES TO BE USED FROM THE POWER SOURCE BEFORE MANIPULATING THEM. DISCONNECT THE RELAY(S) WHEN UPLOADING NEW CODE TO THE ARDUINO. BE CAREFULL AND BE SAFE.**


# How to install

- Clone the project to your local system (or copy the code from room-monitoring-sys.ino)
- Open room-monitoring-sys.ino in ArduinoIDE. If you dont have ArduinoIDE installed, go to the following website and follow the instructions to get started: https://www.arduino.cc/en/main/software
- Follow the circuit diagrams and list of components provided bellow to setup the circuit
- Connect the arduino board to your computer using the A-to-B USB
- In the Arduino IDE, compile the code to ensure it runs properly
- Download the code to the arduino board


# Components
- DHT11
- Reed switch
- MQ-2 gas sensor
- Mini PIR motion sensor
- 2 channel relay module
- Light cord
- Mini space heater
- UNO R3 Controller Board
- Breadboard
- Active Buzzer
- Jumper wires
- USB Cable A-to-B


# Circuit Diagrams

**Schematic**
![](/media/room_monioring_sys_schematic.PNG)

**Breadboard**
![](/media/room_monioring_sys_breadboard.PNG)


# Code Description
Because the data gathered by the sensors is so useful, most of it gets printed into a serial port where it can be collected by [room-monitoring-serial-communicator](https://github.com/heidinv12/room-monitoring-serial-comm). For every loop, the code outputs the data in the following format:

```motionSensor-gasSensor-doorMagnet-temperature-humidity```
 
 Here are the possible values for each type of data:
 
 **motionSensor**
 
 Code | Meaning
 ---- | ---
 MD  | Motion Detected
 NM  | No Motion      
 
 **gasSensor**
 
 Code | Meaning
 ---- | ---
 GA  | Gas Alert
 NG  | No Gas  
 
 **doorMagnet - reed switch**
 
 Code | Meaning
 ---- | ---
 A  | Alert
 H  | Open   
 L  | Closed

**temperature** is in celcius and can be any integer, **humidity** is a percentage and can only be a possitive integer that represents the relative amount of vapor in the air.

A real example for the output would be ```MD-NG-L-22-80```, which trasnlates to motion detected, no gas(smoke) detected in the room, the door is closed, the temeprature is 22 degrees celcius and 80% of the air is water vapor(very humid).

**Timers**

In this code I use timers to keep track of the door and ligth bulb status. The are two timers total, ```doorTimer``` and ```lightTimer```.

```doorTimer``` runs in 5 minutes intervals. This timer gets updated everytime the door sensor returns HIGH(door is open), after 5 minutes, it will trigger the following function: ```doorAlert()``` which will output ```A``` to the serial port and sets ```temp``` to ```A```(This flag comes in handy in ```checkDoorStatus()```).

```lightTimer``` runs in 1 hour intervals. This timer is updated everytime motion is detected in the room. After an hour is met, the timer will call the following function: ```turnOffLight()``` which, as the name implies, sets the relay connected to the light cord to HIGH, thus turning off the light. It also sets ``lightTemp`` to ```false```, which will be used later on in ```checkForMotion()```.


**Functions**: 

```checkForMotion()```

params: none

return: none

Reads digital input from motion sensor, if motion is detected(input is HIGH) the code prints ```MD``` to the serial port and sets the light cord relay to ```LOW```, turning on the light. Moreover, if motion is detected ```lightTimer``` is reset and ```lightTemp``` flag is set to ```true```. If motion is not detected then print ```NM``` to the serial port. Lastly, the function checks if ```lightTemp``` flag is set to ```true```, if so it updates ```lightTimer```. The reason for the way this part was impelemented is so the light is ON for as long as there is a person in the room. The project is currently installed in an office room where there is always someone for approximately 10 hours a day, the changes of that person moving in an hour is high. As long as a bit of motion is detected there will always be light and the lightbulb will only go off after a person is gone for a full hour. 


```checkDoorStatus()```

params: doorResult - digital input from contact reed switch attached to the door

return: none

If door is open, and ```temp``` is set to ```H``` update ```doorTimer```. This part checks whether the door has been open or just got open. If ```temp``` is ```A``` print ```H``` to serial port. If door is open and ```temp``` flag hasn't been set to alert, then keep outputting ```H``` to serial port and reset ```temp``` to ```H```. If the door is closed, reset ```doorTimer```, set flag ```temp``` to ```L``` and print it to a serial port. The code uses ```temp``` to check whether 5 minutes have passed with an open door, whenever the timer interval is met, the temp is set to ```A``` which stands for ```Alert```. Once an alert has been anounced the the code will keep printing the state of the door(```H``` in this case) to the serial port until it is closed.


```loop()```

params: none

return: none

Starts by checking fo rmotion in the room, then reads an analog input from the gas sensor. If the set threshold for gas is surpased, sound the buzzer and print ```GA``` to the serial port, otherwise turn off the buzzer and print ```NG``` instead. Next, the code checks for door status, then for temperature and humidity. The code prints the temeprature first then the humidity to the serial port, after it checks whether the temeprature value is lower than the predefined value, if so, turn on the space heater.

