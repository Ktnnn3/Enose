# Write your code here :-)
#!/usr/bin/python

# Write your code here :-)
#!/usr/bin/python
import spidev
import RPi.GPIO as GPIO
from scipy.integrate import simps
import math
import pandas_datareader as pdr
import pandas as pd
import psutil
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import os
import time
class AdventureDone(Exception): pass


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
plt.rcParams['animation.html'] = 'jshtml'
fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()

relay1_pump = 17
relay2_sol = 27
relay3_sol = 22

#define

gas_channel = [0,1,2,3,4,5,6]
graphsensor0 = []
graphsensor1 = []
graphsensor2 = []
graphsensor3 = []
graphsensor4 = []
graphsensor5 = []
graphsensor6 = []
flow = []

win =[[]for i in range(7)]
cutvar=0



y =[[]for i in range(7)]
initValue=0
maxSlope=[0.0,0.0,0.0,0.0,0.0,0.0,0.0]
check=[0.0,0.0,0.0,0.0,0.0,0.0,0.0]
cutoff=[2.7,1.4,4.50,2.40,2.30,3.30,0.31]
lastcheck=[0.0,0.0,0.0,0.0,0.0,0.0,0.0]

timeout_start = time.time()



GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set LED pin as output
GPIO.setup(relay1_pump, GPIO.OUT)
GPIO.setup(relay2_sol, GPIO.OUT)
GPIO.setup(relay3_sol, GPIO.OUT)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7


def ReadChannel(channel):
    adc = spi.xfer2([4 | 2 | (channel >> 2), (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data


def ConvertVolts(data, places):
    volts = (data * 5.0) / float(4096)
    volts = round(volts, places)
    return volts


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    if type(n) == float:
        return math.floor(n * multiplier) / multiplier


def round_four(num):
    xnum = num*10.0
    xnum = int(xnum)
    if xnum % 10 > 4:
        return (xnum+1)/10.0
    else:
        return xnum/10.0


def calSensor(a, b, Max):
    print(a[len(a)-1])
    if a[len(a)-1] > (maxSlope[Max]) and a[len(a)-1] > cutoff[Max]:
        check[Max] = -1
        print('in condition')
        b.append(a[len(a)-1])
        maxSlope[Max] = a[len(a)-1]
    elif (a[len(a)-1]+0.05) < (maxSlope[Max]):
        print('maxslope', maxSlope[Max])
        print('+0.05 =', a[len(a)-1]+0.05)
        print('else')
        checkNegativeSlope()


def checkNegativeSlope():
    print('sumcheck = ', sum(check))
    # print(y[6])
    if sum(lastcheck) != 7:
        for i in range(len(check)):
            if sum(check) <= -1:
                if check[i] == 0:
                    if len(y[i]) == 0:
                        y[i].append(win[i][2])
                        lastcheck[i] = 1
                    else:
                        y[i][0] = win[i][2]
                else:
                    if win[i][len(win[i])-1] < maxSlope[i]:
                        lastcheck[i] = 1
    else:
        raise AdventureDone


def area(a):
    if len(a) != 1:
        return simps(a)/10.0
    else:
        return a[0]


def prediction(a):
    g0 = a[0]*(1.29086995124816)
    g1 = a[1]*(-0.475657880306244)
    g2 = a[2]*(-0.100802682340145)
    g3 = a[3]*(-0.173830837011337)
    g4 = a[4]*(0.33036082983017)
    g5 = a[5]*(0.58828580379486)
    g6 = a[6]*(0.303013116121292)
    ans = g0+g1+g2+g3+g4+g5+g6
    return ans

def gas_level():
    gas0_level = ReadChannel(gas_channel[0])
    gas0_volts = ConvertVolts(gas0_level, 2)

    gas1_level = ReadChannel(gas_channel[1])
    gas1_volts = ConvertVolts(gas1_level, 2)

    gas2_level = ReadChannel(gas_channel[2])
    gas2_volts = ConvertVolts(gas2_level, 2)

    gas3_level = ReadChannel(gas_channel[3])
    gas3_volts = ConvertVolts(gas3_level, 2)

    gas4_level = ReadChannel(gas_channel[4])
    gas4_volts = ConvertVolts(gas4_level, 2)

    gas5_level = ReadChannel(gas_channel[5])
    gas5_volts = ConvertVolts(gas5_level, 2)

    gas6_level = ReadChannel(gas_channel[6])
    gas6_volts = ConvertVolts(gas6_level, 2)

    graphsensor0.append(gas0_volts)
    graphsensor1.append(gas1_volts)
    graphsensor2.append(gas2_volts)
    graphsensor3.append(gas3_volts)
    graphsensor4.append(gas4_volts)
    graphsensor5.append(gas5_volts)
    graphsensor6.append(gas6_volts)
    #print('gaslevel done')

def cutoff_func():

    for i in range(len(cutoff)):

        cutoff[i] = win[i][0]
        cutoff[i] = cutoff[i]+0.1
    cutvar = 1
    for i in range(len(cutoff)):
        print('cutoff{} : {}'.format(i, cutoff[i]))
    return cutvar

    


def testing_time():
    x=1
    timeout = 1
    #1*60=60 sec
    #5*60=300 sec
    t_end = time.time()+timeout*60
    GPIO.output(relay1_pump, GPIO.HIGH)
    GPIO.output(relay2_sol, GPIO.LOW)
    GPIO.output(relay3_sol, GPIO.LOW)

    try:
        while True :
        #while time.time() < t_end and x <= timeout*100:

            gas_level()
            if(x % 100 == 0):
                #print('Im in if-con')
                graphsensor0_s = pd.Series(graphsensor0)
                graphsensor1_s = pd.Series(graphsensor1)
                graphsensor2_s = pd.Series(graphsensor2)
                graphsensor3_s = pd.Series(graphsensor3)
                graphsensor4_s = pd.Series(graphsensor4)
                graphsensor5_s = pd.Series(graphsensor5)
                graphsensor6_s = pd.Series(graphsensor6)
                #no here
                #print(windows0 = ,windows0)

                windows0 = graphsensor0_s.rolling(100).mean().tolist()
                windows1 = graphsensor1_s.rolling(100).mean().tolist()
                windows2 = graphsensor2_s.rolling(100).mean().tolist()
                windows3 = graphsensor3_s.rolling(100).mean().tolist()
                windows4 = graphsensor4_s.rolling(100).mean().tolist()
                windows5 = graphsensor5_s.rolling(100).mean().tolist()
                windows6 = graphsensor6_s.rolling(100).mean().tolist()

                ax.plot(windows0, color='b')
                ax.plot(windows1, color='r')
                ax.plot(windows2, color='g')
                ax.plot(windows3, color='c')
                ax.plot(windows4, color='m')
                ax.plot(windows5, color='y')
                ax.plot(windows6, color='k')
                fig.canvas.draw()

                win[0].append(windows0[x-1])
                win[1].append(windows1[x-1])
                win[2].append(windows2[x-1])
                win[3].append(windows3[x-1])
                win[4].append(windows4[x-1])
                win[5].append(windows5[x-1])
                win[6].append(windows6[x-1])

                if(cutvar == 0):
                    for i in range(len(cutoff)):
                        cutoff_func()
            


                print("delta V win0 : {}V".format(win[0]))
                print("delta V win1 : {}V".format(win[1]))
                print("delta V win2 : {}V".format(win[2]))
                print("delta V win3 : {}V".format(win[3]))
                print("delta V win4 : {}V".format(win[4]))
                print("delta V win5 : {}V".format(win[5]))
                print("delta V win6 : {}V".format(win[6]))
                print('------------------------------------')
                for i in range(7):
                    calSensor(win[i],y[i],i)

                # time.sleep(0.005)
            x += 1
    except AdventureDone:
            pass

def setting_time():
    timeout = 0.5
    t_end = time.time()+timeout*60
    GPIO.output(relay1_pump, GPIO.HIGH) # Turn LED on
        #time.sleep(1)
    GPIO.output(relay2_sol, GPIO.HIGH)
    GPIO.output(relay3_sol, GPIO.LOW)
    dosth=0
    while time.time() < t_end:
       dosth = dosth+1
    print(dosth)
     
        

def reco_time():
    timeout = 0.5
    t_end = time.time()+timeout*60
    GPIO.output(relay1_pump, GPIO.HIGH) # Turn LED on
    GPIO.output(relay2_sol, GPIO.LOW)
    GPIO.output(relay3_sol, GPIO.HIGH)
    dosth=0
    while time.time() < t_end:
       dosth = dosth+1
    print(dosth)



# Define delay between readings
# while time.time() < timeout_start + timeout and x < timeout*100:
while True:
    print('setting time...')
    setting_time()
    print('testing time...')
    testing_time()
    print('recovery time...')
    reco_time()
    break
    
print('len graphsensor0 = ',len(graphsensor0))
#print('graphsensor0 = ',graphsensor0)
print('win0 = ',win[0])
for i in range(len(y)):
    print("y{} : {}".format(i,y[i]))
print('check =',check)
finalarea= [0,1,2,3,4,5,6]
for i in range(len(y)):
    print(area(y[i]))
finalarea[0] = area(y[0])
finalarea[1] = area(y[1])
finalarea[2] = area(y[2])
finalarea[3] = area(y[3])
finalarea[4] = area(y[4])
finalarea[5] = area(y[5])
finalarea[6] = area(y[6])
print(finalarea)
print(prediction(finalarea))





