#!/usr/bin/python

import psdevices
import math


class POWERSUPPLY:
    def __init__(self):
        self.voltage = "0.0"
        self.amperage = "0.0"
        self.powersupply = psdevices.PSDEVICES()

    def setParameters(self):
        try:
            self.volts = int(self.voltage.split('.')[0])
            self.hectoVolts = int(self.voltage.split('.')[1])
        except:
            self.volts = int(self.voltage)
            self.hectoVolts = 0
        try:
            self.amps = int(self.amperage.split('.')[0])
            self.milliAmps = int(self.amperage.split('.')[1])
        except:
            self.amps = int(self.amperage)
            self.milliAmps = 0

    def control(self):
        if(self.powersupply.device == "CSI305DB"):
            while True:
                    self.powersupply.set(self.volts, self.hectoVolts,
                                    self.amps, self.milliAmps)
        elif(self.powersupply.device == "PPS2116A"):
            self.powersupply.set(self.volts, self.hectoVolts,
                                    self.amps, self.milliAmps)
            self.powersupply.turnON()
