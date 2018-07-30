#!/usr/bin/python

import time
import threading
import keyboard
import powersupply
import sys

device = powersupply.POWERSUPPLY()
keys = keyboard.KEYBOARD()

print(device.powersupply.name)
print("Input Volts in Volts.hectoVolts")
device.voltage = str(input())
print("Input Amps in Amps.milliAmps")
device.amperage = str(input())
print('Voltage: ' + device.voltage)
print('Amps: ' + device.amperage)
print("Change Voltage with 'v'")
print("Change Amps with 'a'")
print("Terminate with 'q'")
device.powersupply.setParameters(device.voltage, device.amperage)

threads = []
t0 = threading.Thread(target=device.powersupply.control)
t1 = threading.Thread(target=keys.getInput)
threads.append(t0)
threads.append(t1)
t0.start()
t1.start()
while True:
    if(keys.input_buf > ""):
        if(keys.input_buf == "q"):
            print("exiting...")
            device.powersupply.quit()
            sys.exit()
        elif(keys.input_buf == "o"):
            device.powersupply.turnON()
        elif(keys.input_buf == "f"):
            device.powersupply.turnOFF()
        elif(keys.input_buf == "v"):
            print("Input Volts in Volts.hectoVolts")
            device.voltage = input()
        elif(keys.input_buf == "a"):
            print("Input Amps in Amps.milliAmps")
            device.amperage = input()
        keys.input_buf = ""
        device.powersupply.setParameters(device.voltage, device.amperage)
