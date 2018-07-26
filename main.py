#!/usr/bin/python

import time
import threading
import keyboard
import powersupply
import sys

device = powersupply.POWERSUPPLY()
keys = keyboard.KEYBOARD()

try:
    print("Input Volts in Volts.hectoVolts")
    device.voltage = input()
except:
    device.voltage = 0.0

try:
    print("Input Amps in Amps.milliAmps")
    device.amperage = input()
except:
    device.amperage = 0.0

print('Voltage: ' + device.voltage)
print('Amps: ' + device.amperage)
print("Change Voltage with 'v'")
print("Change Amps with 'a'")
print("Terminate with 'q'")
device.setParameters()

threads = []
t0 = threading.Thread(target=device.control)
t1 = threading.Thread(target=keys.getInput)
threads.append(t0)
threads.append(t1)
t0.start()
t1.start()
while True:
    if(not t1.is_alive()):
        print("exiting...")
        device.powersupply.quit()
        sys.exit()