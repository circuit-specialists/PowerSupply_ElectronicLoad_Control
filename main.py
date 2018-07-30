#!/usr/bin/python

import time
import threading
import keyboard
import powersupply
import sys

device = powersupply.POWERSUPPLY()
keys = keyboard.KEYBOARD()
print(device.powersupply.name)
print("Open CSV file to run auto loop   press:'o'")
print("For Manual Control               press:'m'")
print("Quit                             press:'q'")
threads = []
selection = str(input())

if(selection == 'o'):
    print("Auto Mode")
    print()
    file = open("auto_run_test.txt", "r")
    file_lines = file.readlines()
    file_lines = file_lines[1:]
    count = 0
    t1 = threading.Thread(target=keys.getInput)
    threads.append(t1)
    t1.start()
    device.powersupply.setParameters(device.voltage, device.amperage)
    device.powersupply.control()
    device.powersupply.turnON()
    for i in file_lines:
        if(keys.input_buf > ""):
            if(keys.input_buf == "q"):
                print("Quitting Early...")
                device.powersupply.quit()
                sys.exit()
        line = file_lines[count]
        device.voltage = line.split(',')[1]
        device.amperage = line.split(',')[2]
        device.powersupply.setParameters(device.voltage, device.amperage)
        device.powersupply.control()
        time.sleep(float(line.split(',')[0]))
        count += 1

    print("Finished auto run mode")

elif(selection == 'm'):
    print("Manual Mode")
    print()
    print("Input Volts in Volts.hectoVolts")
    device.voltage = str(input())
    print("Input Amps in Amps.milliAmps")
    device.amperage = str(input())
    print('Voltage: ' + device.voltage)
    print('Amps: ' + device.amperage)
    print("Change Voltage with 'v'")
    print("Change Amps with 'a'")
    device.powersupply.setParameters(device.voltage, device.amperage)
    t0 = threading.Thread(target=device.powersupply.control)
    threads.append(t0)
    t0.start()
    t1 = threading.Thread(target=keys.getInput)
    threads.append(t1)
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

elif(selection == 'q'):
    print("exiting...")
    device.powersupply.quit()
    sys.exit()

else:
    print("Invalid Option")
