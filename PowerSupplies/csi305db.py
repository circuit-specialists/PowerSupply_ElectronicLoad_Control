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
        self.type = "powersupply"
        self.channels = 1
        self.output_key = 'NY'
        self.setVoltage("0")
        self.setAmperage("0")
        self.setOutput(0)

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
                self.milliAmps = int(amperage.split('.')[1])
            except:
                self.milliAmps = 0
        else:
            self.amps = int(amperage)
            self.milliAmps = 0

    def control(self):
        self.run = True
        while self.run:
            self.key = 'HPPSU'
            self.key += '{:02}'.format(self.volts)
            self.key += '{:<02}'.format(self.hectoVolts)
            self.key += 'H'
            self.key += '{:01}'.format(self.amps)
            self.key += '{:<03}'.format(self.milliAmps)
            self.key += self.output_key
            self.com_device.write(self.key.encode())
            self.com_device.write(self.key.encode())
            self.com_device.read_all()

    def breakControl(self):
        self.run = False

    def turnON(self):
        self.output_key = 'OY'

    def turnOFF(self):
        self.output_key = 'NY'

    def setOutput(self, state):
        self.output = state
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def quit(self):
        self.breakControl()
        time.sleep(0.2)
        self.com_device.flushInput()
        self.com_device.flushOutput()
        self.turnOFF()
        self.com_device.close()
