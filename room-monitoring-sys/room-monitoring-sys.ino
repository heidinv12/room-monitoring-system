#include <dht11.h>
#include "Timer.h"

// timer variables
Timer doorTimer;
Timer lightTime;

// reed switch variables
int magnetResult = 0;
const int magnetPin = 4;

// Temperature and humidity
// sensor variables
dht11 DHT;
const int dhtData = 3;
int temperature = 0;
int humidity = 0;
char temp='H';

// motion an gas sensor
// variables
int motionSensorPin = 8;
int gasSensor = A0;
int gasSensorTresh = 400;
int buzzer = 7;

// realay pin variables
int relayHeater = 12;
int relayLight = 13;

// light timer flag
bool lightTemp = false;


// Triggers after door timer is met
void doorAlert(){
  Serial.print('A');
  Serial.print('-');
  temp='A';
}

// Triggers after light timer is met
void turnOffLight(){
  lightTemp = false;
  digitalWrite(relayLight, HIGH);
}

// 5 mins interval setup to track when the door is left open
int afterEvent = doorTimer.after(300000, doorAlert, 0);

// 1 hr interval for turning on/off lightbulb
int afterLight = lightTime.after(3600000, turnOffLight, 0);

void setup() {
  Serial.begin(9600);

  // setup reed switch
  pinMode(magnetPin,INPUT); 
  digitalWrite(magnetPin,HIGH);

  // setup motion sensor
  pinMode(motionSensorPin,INPUT);
  digitalWrite(motionSensorPin,LOW);

  // setup gas sensor and buzzer
  pinMode(gasSensor,INPUT);
  pinMode(buzzer, OUTPUT);
  
  // setup relay
  pinMode(relayHeater, OUTPUT);
  digitalWrite(relayHeater, HIGH);
  pinMode(relayLight, OUTPUT);
  digitalWrite(relayLight, HIGH);
}

// check wehther door is open or closed
// if open for more than 5mins, throw an
// alert
void checkDoorStatus(int doorResult){
  if(doorResult==HIGH){
    if(temp=='H'){
      doorTimer.update();
    }else if(temp=='A'){
      Serial.print('H');
      Serial.print('-');
    }
    
    if(temp!='A'){
      Serial.print('H');
      Serial.print('-');
      temp = 'H';
    }
  }else if(doorResult==LOW){
    doorTimer.stop(afterEvent);
    temp = 'L';
    Serial.print('L');
    Serial.print('-');
    // 5 mins interval
    afterEvent = doorTimer.after(300000, doorAlert, 0);
  }
}

// If motion is detected turn on the lightbulb
// for an 1hr, reset timer every time motion is
// detected
void checkForMotion(){
  if(digitalRead(motionSensorPin)==HIGH){
    // Motion Detected
    Serial.print("MD");
    Serial.print("-");
    digitalWrite(relayLight, LOW);
    lightTime.stop(afterLight);
    afterLight = lightTime.after(180000, turnOffLight, 0);
    lightTemp = true;
  } else if (lightTemp==false || digitalRead(motionSensorPin)==LOW){
    // No Motion detected
    Serial.print("NM");
    Serial.print("-");
  }

  if (lightTemp==true){
    lightTime.update();
  }
}
 
void loop() {
  // read motion sensor
  checkForMotion();
  
  // read smoke sensor
  int gasSensorInput = analogRead(gasSensor);
  if(gasSensorInput >= gasSensorTresh){
    //trigger the buzzer!
    digitalWrite(buzzer, HIGH);
    Serial.print("GA");
    Serial.print('-');
  } else{
    //turn off buzzer
    digitalWrite(buzzer, LOW);
    Serial.print("NG");
    Serial.print('-');
  }
  
  //read reed switch attached to the door
  magnetResult = digitalRead(magnetPin);
  checkDoorStatus(magnetResult);
  
  // read dht11 sensor
  DHT.read(dhtData);
  temperature = DHT.temperature;
  humidity = DHT.humidity;
  
  // print format is temperature-humidity
  Serial.print(temperature); 
  Serial.print('-');
  Serial.println(humidity);

  if (temperature <= 20){
    digitalWrite(relayHeater, LOW);
  } else if(temperature == 25) {
    // Dont stop heating until temperature reaches 25 C.
    // This way the heater wont have to be turn on/off as
    // many times.
    digitalWrite(relayHeater, HIGH);
  }
  
  delay(500);
}
