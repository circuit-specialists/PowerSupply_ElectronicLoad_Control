#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class CSI305DB:
    def __init__(self, com_device):
        self.com_device = com_device
        self.name = "CSI305DB"
        self.channels = 1
        self.run = True

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

    def setAmperage(self, amperage):
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

    def control(self):
        while self.run:
            self.key = 'HPPSU'
            self.key += '{:02}'.format(self.volts)
            self.key += '{:<02}'.format(self.hectoVolts)
            self.key += 'H'
            self.key += '{:01}'.format(self.amps)
            self.key += '{:<03}'.format(self.milliAmps)
            self.key += 'NY'
            self.com_device.write(self.key.encode())
            self.com_device.write(self.key.encode())
            time.sleep(.02)
            self.com_device.read_all()

    def turnON(self):
        print()

    def turnOFF(self):
        print()

    def setOutput(self, state):
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def quit(self):
        self.turnOFF()
        self.com_device.close()
        self.run = False
