# This sounds the alarm for a specified time in seconds

import RPi.GPIO as GPIO
from RPi.GPIO import PWM
import time
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
p = GPIO.PWM(25,50)


def alarm(alarmTime):
    for i in range(int(alarmTime*5)):
        p.start(90)
        for x in range(200,2200):
            p.ChangeFrequency(x)
            time.sleep(0.0001)
        p.stop()
GPIO.cleanup
