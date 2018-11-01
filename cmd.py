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
        self.getDevice()
        self.device_output = 0
        self.run_type = self.getRunType(prompt=True)
        self.keys = keyboard.KEYBOARD()
        self.addThread(self.keys.inputHandler)
        if (self.run_type == 'a'):
            if (self.device_type == 'electronicload'):
                self.setLogFile('electronicload_log')
            self.loadCSVFile()
            self.run_log = True
            self.addThread(self.logfileThread)
            self.addThread(self.outputThread)
            self.addThread(self.runCSV)
        elif (self.run_type == 'm'):
            self.getParameters(prompt=True)
            self.addThread(self.runManual)
        else:
            self.quit()

        if (self.device.name == "CSI305DB"):
            self.addThread(self.device.control)

        self.runThreads()

    def getRunType(self, prompt):
        if (prompt):
            print("Open CSV file to run auto loop   press:'a'")
            print("For Manual Control               press:'m'")
            print("Quit                             press:'q'")
        return self.getInput()

    def getInput(self):
        if (sys.version_info.major >= 3):
            return str(input())  # python 3
        else:
            return str(raw_input())  # python 2

    def getDevice(self):
        try:
            self.device = electronicload.ELECTRONICLOAD()
            self.device = self.device.electronicload
            self.device_type = "electronicload"
        except:
            try:
                self.device = powersupply.POWERSUPPLY()
                self.device = self.device.powersupply
                self.device_type = "powersupply"
            except:
                print("No Supported Devices connected to computer bus")
                sys.exit()

        print(self.device.name)

    def loadCSVFile(self):
        files = os.listdir('./Example CSV')
        count = 1
        for filenames in files:
            print("%d: %s" % (count, filenames))
            count += 1
        file_selection = int(self.getInput())
        print('Running...    ./Example CSV/%s' % (files[file_selection - 1]))
        file = open('./Example CSV/%s' % (files[file_selection - 1]), "r")
        self.file_lines = file.readlines()
        self.file_lines = self.file_lines[1:]

    def setLogFile(self, filename):
        print(filename)
        if (filename != "" or filename != None):
            self.log_file = open("%s.csv" % filename, "w")
        else:
            self.log_file = open("auto_log_el.csv", "w")
        self.log_file.writelines(str("timestamp,voltage,current,power\n"))
        print("Input Log-Time interval. Default is 1s")
        self.write_interval = self.getInput()
        if (self.write_interval == None or self.write_interval == ""):
            self.write_interval = 1.0
        else:
            self.write_interval = float(self.write_interval)

    def runCSV(self):
        while(self.run_log):
            # input handler
            input_temp = self.keys.getInput()
            if (input_temp == 'q'):
                self.quit()
        print("Finished auto run mode")
        self.quit()

    def outputThread(self):
        for line in self.file_lines:
            try:
                # csv file loop
                if (self.device.channels > 1):
                    self.device.setVoltage(line.split(',')[1], line)
                    self.device.setAmperage(line.split(',')[2], line)
                    self.device.setOutput(int(line.split(',')[3]), line)
                else:
                    if (self.device_type == "powersupply"):
                        self.device.setVoltage(line.split(',')[1])
                        self.device.setAmperage(line.split(',')[2])
                        self.device.setOutput(int(line.split(',')[3]))
                        time.sleep(float(line.split(',')[0]))
                    elif (self.device_type == "electronicload"):
                        self.device.setMode(line.split(',')[1])
                        self.device.setCurrent(line.split(',')[2])
                        self.device.setOutput(int(line.split(',')[3]))
                        time.sleep(float(line.split(',')[0]))
            except:
                pass
        self.run_log = False

    def logfileThread(self):
        start_time = time.time()
        while (self.run_log):
            try:
                try:
                    currentVolts = self.device.getVoltage()[:-1]
                except:
                    currentVolts = "N/A"
                try:
                    currentAmps = self.device.getCurrent()[:-1]
                except:
                    currentAmps = "N/A"
                try:
                    currentPower = self.device.getPower()[:-1]
                except:
                    currentPower = "N/A"
                self.log_file.writelines(
                    str(time.time() - start_time) + "," +
                    str(currentVolts) + "," +
                    str(currentAmps) + "," +
                    str(currentPower) + "\n")
            except:
                pass
            time.sleep(self.write_interval)

    def runThreads(self):
        for th in self.threads:
            if(not th.is_alive()):
                th.start()

    def quitThreads(self):
        for th in self.threads:
            try:
                print(len(self.threads))
                th.join()
            except:
                self.threads.pop()

    def addThread(self, function):
        self.threads.append(threading.Thread(target=function))

    def quit(self):
        print("exiting...")
        self.keys.quit()
        try:
            self.device.quit()
        except:
            pass
        # self.quitThreads()
        exit()

    def getParameters(self, prompt):
        if (self.device.channels > 1):
            for i in range(1, self.device.channels):
                print("Setting Channel: %s" % str(i))

        self.run_time = self.getLength(prompt)

        if (self.device_type == "powersupply"):
            self.getVoltage(prompt)
            print('Voltage: %s' % self.device.voltage)

        self.getCurrent(prompt)
        print('Amps: %s' % self.device.amperage)

    def getLength(self, prompt):
        if (prompt):
            print("Input Time to run in (s)")
        return float(self.getInput())

    def getVoltage(self, prompt):
        if (prompt):
            print("Input Volts in Volts.hectoVolts")
        self.device.setVoltage(self.getInput())

    def getCurrent(self, prompt):
        if (prompt):
            print("Input Amps in Amps.milliAmps")
        if (self.device_type == "powersupply"):
            self.device.setAmperage(self.getInput())
        elif (self.device_type == "electronicload"):
            self.device.setCurrent = self.getInput()

    def flipOutput(self):
        if (self.device.output):
            self.device.setOutput(0)
        else:
            self.device.setOutput(1)

    def runManual(self):
        start_time = time.time()
        self.device.setOutput(1)
        while time.time() <= start_time + self.run_time:
            # input handler
            input_temp = self.keys.getInput()
            if (input_temp == 'q'):
                break
            elif (input_temp == 'v'):
                self.getVoltage(prompt=False)
            elif (input_temp == 'a'):
                self.getCurrent(prompt=False)
            elif (input_temp == 'o'):
                self.flipOutput()

        self.quit()


if __name__ == "__main__":
    cmd = CMD()
