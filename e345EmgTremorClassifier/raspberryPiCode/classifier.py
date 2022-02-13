# E345 Wearables
# This code reads in serial input from tne arduino as a string and parses it into an array
# The array reaches a set window size then takes a periodogram
# We average the power spectral density values
# Once this number reaches a set threshold several times we trigger the alarm
# This process separates muscle tremors from general muscle use

# This script is autostarted on pi boot

import serial
import numpy as np
from scipy import signal

# sounds alarm with speaker.alarm()
import speaker # speaker.py

# This is string data from arduino in pi usb port
serialPort = serial.Serial('/dev/ttyACM0', 9600)

sampleRate=100 #Hz
windowSize=400 #Data values
split=10 #periodogram split
sensitivity=1.0e-5 # The expected value of the power spectral density average (acquired from testing)
triggerThreshold=3 # How many consecutive times you must break the threshold

data = np.array([])

# function returns 1 if tremor detected
def classify(data):
    print(data)
    data = data/625
    f, Pxx_den = signal.periodogram(data, sampleRate) #Pxx_den is power spectral density values
    freqVal = np.average(Pxx_den) # This value usually sits around 1e-7 and goes above 1e-5 durind tremors
    print(freqVal)
    if (freqVal > sensitivity):
        return 1
    return 0
#    for i in range(split):
#        f, Pxx_den = signal.periodogram(data[int(i*(len(data)/split)):int((i+1)*len(sig)/split)], sampleRate)
#        freqVal = Pxx_den.avg()
#        print(freqVal)
#        if (freqVal > sensitivity):
#            test = 1
#    return test

i=0 # window size iter
triggers=0

print("Starting up, testing speaker")
speaker.alarm(0.5)
while True:
    i+=1
    
    # Read int from serial port into data[]
    strData = serialPort.readline()
    if strData:
        strData = str(strData)
        strData=strData.replace('\\',' ')
        for s in strData.split(' '):
            if s.isdigit():
                data = np.append(data, float(s))

# classify when len(data) is windowSize
    if i>=windowSize:
        i=0

        if classify(data):
            triggers+=1
        else:
            triggers=0

        if triggers >= triggerThreshold:
            speaker.alarm(5)
            triggers=0
        data=np.array([])


