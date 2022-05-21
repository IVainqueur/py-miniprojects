'''
    This program has Timer that checks every 100 milliseconds if the /media/pi folder is populated.
    IF YES: that means there is an external device connected to the Raspberry Pi so turn the connectedLED on
    ELSE: just turn off the connectedLED and turn on the errorPin

'''



import requests
from threading import Timer
import time
import os
import RPi.GPIO as GPIO
import atexit

# Setting up the board and GPIO Related Stuff
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Renaming some variables for convinience
HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
digitalWrite = GPIO.output


# The Global Variables
prevConnection = False
connectedPin = 3
errorPin = 5


# Setting the LEDs
GPIO.setup(connectedPin, OUTPUT, initial=LOW)
GPIO.setup(errorPin, OUTPUT, initial=HIGH)

# Function to switch off the LEDS at exit
def turnOffLeds():
    print("======== BYE ===========")
    digitalWrite(connectedPin, LOW)
    digitalWrite(errorPin, LOW)
    
atexit.register(turnOffLeds)

def checkUSB():
    global prevConnection
    # print("Checking")
    if len(os.listdir("/media/pi")) > 0:
        if not prevConnection:
            prevConnection = True
            digitalWrite(connectedPin, HIGH)
            digitalWrite(errorPin, LOW)
    else:
        if prevConnection:
            prevConnection = False
            digitalWrite(connectedPin, LOW)
            digitalWrite(errorPin, HIGH)

    Timer(0.1, checkUSB).start()

checkUSB()


