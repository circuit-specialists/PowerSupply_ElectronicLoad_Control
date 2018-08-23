#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import time
import threading
import keyboard
import sys

# Path to CSV Files
sys.path.insert(0, './Example CSV')

# Path to devices
sys.path.insert(0, './Power Supplies')
sys.path.insert(0, './Electronic Loads')
import powersupply
import electronicload

keys = keyboard.KEYBOARD()

# last update v1.2
print("Select Device Type")
print("Power Supply                     press:'p'")
print("Electronic Load                  press:'l'")
device_selection = str(input())
if (device_selection == 'p'):
    try:
        device = powersupply.POWERSUPPLY()
    except:
        print("No Supported Power Supplies connected to computer bus")
        print("exiting...")
        keys.quit()
        sys.exit()
    print(device.powersupply.name)
    threads = []
    print("Open CSV file to run auto loop   press:'a'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    operation_selection = str(input())

    if (operation_selection == 'a'):
        print("Auto Mode")
        print()
        file = open("auto_run_ps.csv", "r")
        file_lines = file.readlines()
        file_lines = file_lines[1:]
        count = 0
        try:
            t0 = threading.Thread(target=device.powersupply.control)
            threads.append(t0)
            t0.start()
        except:
            pass
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()
        for i in file_lines:
            if (keys.input_buf == "q"):
                print("exiting...")
                keys.quit()
                device.powersupply.quit()
                t0.join()
                t1.join()
                sys.exit()
            line = file_lines[count]
            device.powersupply.setVoltage(line.split(',')[1], i)
            device.powersupply.setAmperage(line.split(',')[2], i)
            device.powersupply.setOutput(int(line.split(',')[3]), i)
            time.sleep(float(line.split(',')[0]))
            count += 1
        print("Finished auto run mode")
        print("exiting...")
        device.powersupply.turnOFF()
        keys.quit()
        device.powersupply.quit()
        t0.join()
        t1.join()
        sys.exit()

    elif (operation_selection == 'm'):
        print("Manual Mode")
        print()
        for i in range(1, device.powersupply.channels):
            print("Setting Channel:" + str(i))
            print("Input Volts in Volts.hectoVolts")
            device.powersupply.setVoltage(str(input()), i)
            print("Input Amps in Amps.milliAmps")
            device.powersupply.setAmperage(str(input()), i)
            print('Voltage: ' + device.powersupply.voltage)
            print('Amps: ' + device.powersupply.amperage)
        print("Change Voltage with 'v'")
        print("Change Amps with 'a'")
        try:
            t0 = threading.Thread(target=device.powersupply.control)
            threads.append(t0)
            t0.start()
        except:
            pass
        t1 = threading.Thread(target=keys.getInput)
        threads.append(t1)
        t1.start()

        while True:
            if (keys.input_buf > ""):
                if (keys.input_buf == "q"):
                    print("exiting...")
                    keys.quit()
                    device.powersupply.quit()
                    t0.join()
                    sys.exit()
                elif (keys.input_buf == "o"):
                    device.powersupply.turnON()
                elif (keys.input_buf == "f"):
                    device.powersupply.turnOFF()
                elif (keys.input_buf == "v"):
                    if (device.powersupply.channels > 1):
                        print("Which Channel?")
                        channel = str(input())
                        print("Input Volts in Volts.hectoVolts")
                        device.powersupply.setVoltage(str(input()), channel)
                    else:
                        print("Input Volts in Volts.hectoVolts")
                        device.powersupply.setVoltage(str(input()), 1)
                elif (keys.input_buf == "a"):
                    if (device.powersupply.channels > 1):
                        print("Which Channel?")
                        channel = str(input())
                        print("Input Amps in Amps.milliAmps")
                        device.powersupply.setVoltage(str(input()), channel)
                    else:
                        print("Input Amps in Amps.milliAmps")
                        device.powersupply.setAmperage(str(input()), 1)
                keys.input_buf = ""
    elif (operation_selection == 'q'):
        print("exiting...")
        keys.quit()
        device.powersupply.quit()
        sys.exit()

elif (device_selection == 'l'):
    try:
        device = electronicload.ELECTRONICLOAD()
    except:
        print("No Supported Electronic Loads connected to computer bus")
        print("exiting...")
        keys.quit()
        sys.exit()
    print(device.electronicload.name)
    threads = []
    print("Open CSV file to run auto loop   press:'a'")
    print("For Manual Control               press:'m'")
    print("Quit                             press:'q'")
    operation_selection = str(input())

    if (operation_selection == 'a'):
        print("Auto Run Mode")
        print()
        # log file
        print("Input Log-Time interval. Default is 1s")
        interval_selection = str(input())
        if (interval_selection == ""):
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
            if (keys.input_buf == "q"):
                print("exiting...")
                keys.quit()
                device.electronicload.quit()
                t0.join()
                t1.join()
                sys.exit()
            if (last_read_time + wait_read_time < time.time()):
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
            if (last_write_time + wait_write_time < time.time()):
                log_file.writelines(
                    str(time.time() - start_time) + "," +
                    str(device.electronicload.getVoltage()[:-1]) + "," +
                    str(device.electronicload.getCurrent()[:-1]) + "," +
                    str(device.electronicload.getPower()[:-1]) + "\n")

        device.electronicload.turnOFF()
        print("Finished auto run mode")
        print("exiting...")
        keys.quit()
        device.electronicload.quit()
        t0.join()
        t1.join()
        sys.exit()

    elif (operation_selection == 'm'):
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
            if (keys.input_buf > ""):
                if (keys.input_buf == "q"):
                    print("exiting...")
                    keys.quit()
                    device.electronicload.quit()
                    t0.join()
                    t1.join()
                    sys.exit()
                elif (keys.input_buf == "o"):
                    device.electronicload.turnON()
                elif (keys.input_buf == "f"):
                    device.electronicload.turnOFF()
                elif (keys.input_buf == "v"):
                    print("Set Current Limit")
                    device.electronicload.setCurrent = str(input())
                keys.input_buf = ""
            print(device.electronicload.getCurrent())

    elif (operation_selection == 'q'):
        print("exiting...")
        keys.quit()
        device.electronicload.quit()
        sys.exit()

elif (device_selection == 'q'):
    print("exiting...")
    keys.quit()
    sys.exit()

else:
    print("Invalid Option")
