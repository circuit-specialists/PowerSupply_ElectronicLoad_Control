#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class PPS2320A:
    def __init__(self, com_device):
        self.com_device = com_device
        self.name = "PPS2320A"
        self.channels = 2
        self.com_device.write('o2\n'.encode())
        time.sleep(.02)
        self.com_device.read_all()

    def setVoltage(self, voltage, channel):
        self.voltage = voltage
        if("." in voltage):
            try:
                self.volts = int(voltage.split('.')[0])
            except:
                self.volts = 0
            try:
                self.hectoVolts = int(voltage.split('.')[1])
            except:
                self.hectoVolts = 0
        else:
            self.volts = int(voltage)
            self.hectoVolts = 0

        if(channel == 2):
            self.key = 'sa'
        else:
            self.key = 'su'
        self.key += '{:02}'.format(self.volts)
        self.key += '{:<02}'.format(self.hectoVolts)
        self.key += "\n"
        self.writeFunction()

    def setAmperage(self, amperage, channel):
        self.amperage = amperage
        if("." in amperage):
            try:
                self.amps = int(amperage.split('.')[0])
            except:
                self.amps = 0
            try:
                self.milliamps = int(amperage.split('.')[1])
            except:
                self.milliamps = 0
        else:
            self.amps = int(amperage)
            self.milliamps = 0

        if(channel == 2):
            self.key = 'sd'
        else:
            self.key = 'si'
        self.key += '{:01}'.format(self.amps)
        self.key += '{:<03}'.format(self.milliAmps)
        self.key += "\n"
        self.writeFunction()

    def writeFunction(self):
        self.com_device.write(self.key.encode())
        time.sleep(.02)
        return self.com_device.read_all()

    def setCPUADDR(self, ADDR):
        self.key = 'sa'
        self.key += '{:04}'.format(ADDR)
        self.key += "\n"
        self.writeFunction()

    def setCPUData(self, Data):
        self.key += 'si'
        self.key += '{:04}'.format(Data)
        self.key += "\n"
        self.writeFunction()

    def setOutput(self, state):
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def turnON(self):
        self.key = "o1\n"
        self.writeFunction()

    def turnOFF(self):
        self.key = "o0\n"
        self.writeFunction()

    def setMode(self, mode):
        mode = str(mode).upper
        if('PARALLEL' in mode):
            self.key = 'o3\n'
        elif('SERIAL' in mode):
            self.key = 'o4\n'
        elif('TRACK' in mode):
            self.key = 'o5\n'
        elif('NORMAL' in mode):
            self.key = 'o2\n'
        self.writeFunction()

    def setFixedCH(self, option):
        self.fixedChannels = ["2.5V", "3.3V", "5V"]
        if(option == 1):
            self.key = 'oa\n'
        elif(option == 2):
            self.key = 'o8\n'
        elif(option == 3):
            self.key = 'o9\n'
        print(self.fixedChannels[option - 1])
        self.writeFunction()

    def measureVoltage(self, channel):
        if(channel):
            self.key = "rv\n"
        elif(channel == 2):
            self.key = "rh\n"
        self.voltage = self.writeFunction()
        self.voltage = float("%d%s%d" % (int(self.voltage[:2]), '.', int(self.voltage[2:-1])))
        return self.voltage

    def measureAmperage(self, channel):
        if(channel):
            self.key = "ra\n"
        elif(channel == 2):
            self.key = "rj\n"
        self.amperage = self.writeFunction()
        self.amperage = float("%d%s%d" % (int(self.amperage[:2]), '.', int(self.amperage[2:-1])))
        return self.amperage

    def presetVoltage(self, channel):
        if(channel):
            self.key = "ri\n"
        elif(channel == 2):
            self.key = "ru\n"
        self.writeFunction()

    def presetCurrent(self, channel):
        if(channel):
            self.key = "rq\n"
        elif(channel == 2):
            self.key = "rk\n"
        self.writeFunction()

    def getAddress(self):
        self.key = "re\n"
        self.writeFunction()

    def getDeviceSafeguard(self):
        self.key = "rp\n"
        self.writeFunction()

    def measureStatus(self):
        self.key = "rs\n"
        self.writeFunction()

    def quit(self):
        self.turnOFF()
        self.com_device.close()
