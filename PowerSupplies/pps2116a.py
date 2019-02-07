#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class PPS2116A:
    def __init__(self, com_device):
        self.com_device = com_device
        self.name = "PPS2116A"
        self.channels = 1

    def getChannels(self):
        return self.channels

    def setVoltage(self, voltage):
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

        self.key = 'su'
        self.key += '{:02}'.format(self.volts)
        self.key += '{:<02}'.format(self.hectoVolts)
        self.key += "\n"
        self.writeFunction()

    def setAmperage(self, amperage):
        self.amperage = amperage
        if("." in amperage):
            try:
                self.amps = int(amperage.split('.')[0])
            except:
                self.amps = 0
            try:
                self.milliAmps = int(amperage.split('.')[1])
            except:
                self.milliAmps = 0
        else:
            self.amps = int(amperage)
            self.milliAmps = 0

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
        self.output = state
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

    def measureVoltage(self):
        self.key = "rv\n"
        self.voltage = self.writeFunction()
        self.voltage = float("%d%s%d" % (int(self.voltage[:2]), '.', int(self.voltage[2:-1])))
        return self.voltage

    def measureAmperage(self):
        self.key = "ra\n"
        self.amperage = self.writeFunction()
        self.amperage = float("%d%s%d" % (int(self.amperage[:2]), '.', int(self.amperage[2:-1])))
        return self.amperage

    def presetVoltage(self):
        self.key = "ru\n"
        self.writeFunction()

    def presetCurrent(self):
        self.key = "ri\n"
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
