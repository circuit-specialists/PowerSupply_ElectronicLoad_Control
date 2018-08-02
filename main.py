#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

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
device_selection = str(input())


if(device_selection == 'p'):
    try:
        device = powersupply.POWERSUPPLY()
    except:
        print("exiting...")
        keys.quit()
        sys.exit()
    print(device.powersupply.name)
    threads = []
    print("Open CSV file to run auto loop   press:'a'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    operation_selection = str(input())

    if(operation_selection == 'a'):
        print("Auto Mode")
        print()
        file = open("auto_run_ps.csv", "r")
        file_lines = file.readlines()
        file_lines = file_lines[1:]
        count = 0
        t0 = threading.Thread(target=device.powersupply.control)
        threads.append(t0)
        t0.start()
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()
        device.powersupply.setParameters(device.voltage, device.amperage)
        for i in file_lines:
            if(keys.input_buf == "q"):
                print("exiting...")
                device.powersupply.quit()
                keys.quit()
                t0.join()
                sys.exit()
            line = file_lines[count]
            device.voltage = line.split(',')[1]
            device.amperage = line.split(',')[2]
            device.powersupply.setParameters(device.voltage, device.amperage)
            device.powersupply.setOutput(int(line.split(',')[3]))
            time.sleep(float(line.split(',')[0]))
            count += 1

        print("Finished auto run mode")

    elif(operation_selection == 'm'):
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
                    t0.join()
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
    elif(operation_selection == 'q'):
        device = powersupply.POWERSUPPLY()
        print("exiting...")
        keys.quit()
        sys.exit()
elif(device_selection == 'l'):
    try:
        device = electronicload.ELECTRONICLOAD()
    except:
        print("exiting...")
        keys.quit()
        sys.exit()
    print(device.electronicload.name)
    threads = []
    print("Open CSV file to run auto loop   press:'a'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    operation_selection = str(input())

    if(operation_selection == 'a'):
        print("Auto Run Mode")
        print()
        # log file
        print("Input Log-Time interval. Default is 1s")
        interval_selection = str(input())
        if(interval_selection == ""):
            interval_selection = 1.0
        # log file
        log_file = open("auto_log_el.csv", "w")
        log_file.writelines(str("timestamp,voltage,current,power\n"))
        # script file
        par_file = open("auto_run_el.csv", "r")
        file_lines = par_file.readlines()
        file_lines = file_lines[1:]
        count = 0
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()
        device.electronicload.setCurrent(0)
        print("Running script")
        wait_read_time = 0.0
        last_read_time = time.time()
        wait_write_time = float(interval_selection)
        last_write_time = time.time()
        start_time = time.time()
        while True:
            if(keys.input_buf == "q"):
                print("exiting...")
                device.electronicload.quit()
                keys.quit()
                t0.join()
                sys.exit()
            if(last_read_time + wait_read_time < time.time()):
                last_read_time = time.time()
                line = file_lines[count]
                device.electronicload.setMode(line.split(',')[1])
                device.electronicload.setCurrent(line.split(',')[2])
                device.electronicload.setOutput(int(line.split(',')[3]))
                wait_read_time = float(line.split(',')[0])
                count += 1
                print("Line: " + str(count))
                try:
                    null = file_lines[count]
                except:
                    break
            if(last_write_time + wait_write_time < time.time()):
                log_file.writelines(str(time.time() - start_time) + "," +
                                    str(device.electronicload.getVoltage()[:-1]) + "," +
                                    str(device.electronicload.getCurrent()[:-1]) + "," +
                                    str(device.electronicload.getPower()[:-1]) + "\n")

        device.electronicload.turnOFF()
        print("Finished auto run mode")
        print("exiting...")
        keys.quit()
        device.electronicload.quit()
        sys.exit()

    elif(operation_selection == 'm'):
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
                    t0.join()
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

    elif(operation_selection == 'q'):
        print("exiting...")
        device.electronicload.quit()
        keys.quit()
        sys.exit()


elif(device_selection == 'q'):
    print("exiting...")
    try:
        device.powersupply.quit()
    except:
        device.electronicload.quit()
    keys.quit()
    sys.exit()

else:
    print("Invalid Option")
