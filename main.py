#!/usr/bin/python

import time
import threading
import keyboard
import powersupply
import electronicload
import sys

keys = keyboard.KEYBOARD()

print("Select Device Type")
print("Power Supply                     press:'p'")
print("Electronic Load                  press:'l'")
selection = str(input())
if(selection == 'p'):
    device = powersupply.POWERSUPPLY()
    print(device.powersupply.name)
    print("Open CSV file to run auto loop   press:'o'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    threads = []
    selection = str(input())

    if(selection == 'o'):
        print("Auto Mode")
        print()
        file = open("auto_run_ps.txt", "r")
        file_lines = file.readlines()
        file_lines = file_lines[1:]
        count = 0
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()
        device.powersupply.setParameters(device.voltage, device.amperage)
        device.powersupply.control()
        try:
            device.powersupply.turnON()
        except:
            pass
        for i in file_lines:
            if(keys.input_buf > ""):
                if(keys.input_buf == "q"):
                    print("Quitting Early...")
                    device.powersupply.quit()
                    keys.quit()
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
                    keys.quit()
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
                device.powersupply.setParameters(
                    device.voltage, device.amperage)
elif(selection == 'l'):
    device = electronicload.ELECTRONICLOAD()
    print(device.electronicload.name)
    print("Open CSV file to run auto loop   press:'o'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    threads = []
    selection = str(input())

    if(selection == 'o'):
        print("Auto Mode")
        print()
        file = open("auto_run_el.txt", "r")
        file_lines = file.readlines()
        file_lines = file_lines[1:]
        count = 0
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()
        device.electronicload.setCurrent(0)
        try:
            device.electronicload.turnON()
        except:
            pass
        for i in file_lines:
            if(keys.input_buf > ""):
                if(keys.input_buf == "q"):
                    print("Quitting Early...")
                    device.electronicload.quit()
                    keys.quit()
                    sys.exit()
            line = file_lines[count]
            print(line.split(',')[1])
            device.electronicload.setMode(line.split(',')[1])
            device.electronicload.setCurrent(line.split(',')[2])
            time.sleep(float(line.split(',')[0]))
            count += 1

        print("Finished auto run mode")
        print("exiting...")
        device.electronicload.quit()
        keys.quit()
        sys.exit()

    elif(selection == 'm'):
        print("Manual Mode")
        print()
        print("Set Current Limit")
        device.electronicload.setCurrent = str(input())
        print("Change Current with 'c'")
        threads.append(t0)
        t0.start()
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()

        while True:
            if(keys.input_buf > ""):
                if(keys.input_buf == "q"):
                    print("exiting...")
                    device.electronicload.quit()
                    keys.quit()
                    sys.exit()
                elif(keys.input_buf == "o"):
                    device.electronicload.turnON()
                elif(keys.input_buf == "f"):
                    device.electronicload.turnOFF()
                elif(keys.input_buf == "v"):
                    print("Set Current Limit")
                    device.electronicload.setCurrent = str(input())
                keys.input_buf = ""
            print(device.electronicload.getCurrent())


elif(selection == 'q'):
    print("exiting...")
    try:
        device.powersupply.quit()
        keys.quit()
    except:
        pass
    try:
        device.electronicload.quit()
        keys.quit()
    except:
        pass
    sys.exit()

else:
    print("Invalid Option")
