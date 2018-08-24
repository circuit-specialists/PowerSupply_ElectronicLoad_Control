#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import time
import threading
import keyboard
import sys
import os

# Path to CSV Files
sys.path.insert(0, './Example CSV')

# Path to devices
sys.path.insert(0, './Power Supplies')
sys.path.insert(0, './Electronic Loads')
import powersupply
import electronicload


class CMD:
    def __init__(self):
        # last update v1.3
        self.threads = []
        self.keys = keyboard.KEYBOARD()
        self.getDevice()
        self.device_output = 0
        self.run_type = self.getRunType(prompt=True)
        if(self.run_type == 'a'):
            if(self.device_type == 'electronicload'):
                self.setLogFile('')
            self.loadCSVFile()
            self.runCSV()
        elif(self.run_type == 'm'):
            self.getParameters(prompt=True)
            self.addThread(self.keys.inputHandler)
            self.addThread(self.runManual)
            self.runThreads()

    def getRunType(self, prompt):
        if(prompt):
            print("Open CSV file to run auto loop   press:'a'")
            print("For Manual Control               press:'m'")
            print("Quit                             press:'q'")
        return str(input())

    def getDevice(self):
        try:
            self.device = powersupply.POWERSUPPLY()
            self.device = self.device.powersupply
            self.device_type = "powersupply"
        except:
            try:
                self.device = electronicload.ELECTRONICLOAD()
                self.device = self.device.electronicload
                self.device_type = "electronicload"
            except:
                print("No Supported Devices connected to computer bus")
                self.quit()

        print(self.device.name)

    def loadCSVFile(self):
        files = os.listdir('./Example CSV')
        count = 1
        for filenames in files:
            print("%d: %s" % (count, filenames))
            count += 1
        file_selection = int(input())
        print('Running...    ./Example CSV/%s' % (files[file_selection - 1]))
        file = open('./Example CSV/%s' % (files[file_selection - 1]), "r")
        self.file_lines = file.readlines()
        self.file_lines = self.file_lines[1:]

    def setLogFile(self, filename):
        if(filename != "" or filename != None):
            self.log_file = open("%s.csv" % filename, "w")
        else:
            self.log_file = open("auto_log_el.csv", "w")
        self.log_file.writelines(str("timestamp,voltage,current,power\n"))
        print("Input Log-Time interval. Default is 1s")
        self.write_interval = str(input())
        if (self.write_interval == ""):
            self.write_interval = 1.0

    def runCSV(self):
        # set time between file saves for logging
        if(self.device_type == "electronicload"):
            wait_read_time = 0.0
            last_read_time = time.time()
            wait_write_time = float(self.write_interval)
            last_write_time = time.time()
            start_time = time.time()

        count = 0
        for i in self.file_lines:
            line = self.file_lines[count]
            if(self.device.channels > 1):
                self.device.setVoltage(line.split(',')[1], i)
                self.device.setAmperage(line.split(',')[2], i)
                self.device.setOutput(int(line.split(',')[3]), i)
            else:
                if(self.device_type == "powersupply"):
                    self.device.setVoltage(line.split(',')[1])
                    self.device.setAmperage(line.split(',')[2])
                    self.device.setOutput(int(line.split(',')[3]))
                    time.sleep(float(line.split(',')[0]))
                    count += 1
                elif(self.device_type == "electronicload"):
                    if (last_read_time + wait_read_time < time.time()):
                        last_read_time = time.time()
                        self.device.setMode(line.split(',')[1])
                        self.device.setCurrent(
                            line.split(',')[2])
                        self.device.setOutput(
                            int(line.split(',')[3]))
                        wait_read_time = float(line.split(',')[0])
                    if (last_write_time + wait_write_time < time.time()):
                        self.log_file.writelines(
                            str(time.time() - start_time) + "," +
                            str(self.device.getVoltage()[:-1]) + "," +
                            str(self.device.getCurrent()[:-1]) + "," +
                            str(self.device.getPower()[:-1]) + "\n")

        print("Finished auto run mode")
        self.quit()

    def runThreads(self):
        for th in self.threads:
            th.start()

    def quitThreads(self):
        for th in self.threads:
            try:
                th.join()
            except:
                pass

    def addThread(self, function):
        self.threads.append(threading.Thread(target=function))

    def quit(self):
        print("exiting...")
        self.keys.quit()
        try:
            self.device.quit()
        except:
            pass
        self.quitThreads()
        sys.exit()

    def getParameters(self, prompt):
        if(self.device.channels > 1):
            for i in range(1, self.device.channels):
                print("Setting Channel: %s" % str(i))

        if(self.device_type == "powersupply"):
            self.getVoltage(prompt)
            print('Voltage: %s' % self.device.voltage)

        self.getCurrent(prompt)
        print('Amps: %s' % self.device.amperage)

    def getVoltage(self, prompt):
        if(prompt):
            print("Input Volts in Volts.hectoVolts")
        self.device.setVoltage(str(input()))

    def getCurrent(self, prompt):
        if(prompt):
            print("Input Amps in Amps.milliAmps")
        if(self.device_type == "powersupply"):
            self.device.setAmperage(str(input()))
        elif(self.device_type == "electronicload"):
            self.device.setCurrent = str(input())

    def flipOutput(self):
        if(self.device_output):
            self.device.setOutput(0)
            self.device_output = 0
        else:
            self.device.setOutput(1)
            self.device_output = 1

    def runManual(self):
        while True:
            if(self.device.name == "CSI305DB"):
                self.device.control()

            # input handler
            input_temp = self.keys.getInput()
            if(input_temp == 'q'):
                self.quit()
            elif(input_temp == 'v'):
                self.getVoltage(prompt=False)
            elif(input_temp == 'a'):
                self.getCurrent(prompt=False)
            elif(input_temp == 'o'):
                self.flipOutput()


if __name__ == "__main__":
    cmd = CMD()
