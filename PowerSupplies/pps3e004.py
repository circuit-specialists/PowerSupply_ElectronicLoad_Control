#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class PPS3E004:
    def __init__(self, com_device):
        self.com_device = com_device
        self.name = "PPS3E004"
        self.type = "powersupply"
        self.channels = 1
        self.setVoltage("0")
        self.setAmperage("0")
        self.setOutput(0)

    def setVoltage(self, voltage):
        self.voltage = voltage
        if("." in voltage):
            self.volts = voltage.split('.')[0]
            self.hectoVolts = voltage.split('.')[1]
        else:
            self.volts = voltage
            self.hectoVolts = 0

        self.key = 'su'
        self.key += '%04d' % int(self.volts)
        self.key += '%01d' % int(self.hectoVolts)
        self.key += "\n"
        self.writeFunction()

    def setAmperage(self, amperage):
        self.amperage = amperage
        if("." in amperage):
            self.amps = amperage.split('.')[0]
            self.milliAmps = amperage.split('.')[1]
        else:
            self.amps = amperage
            self.milliAmps = 0

        self.key = 'si'
        self.key += '%04d' % int(self.milliAmps)
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
        self.key = "so1\n"
        self.writeFunction()

    def turnOFF(self):
        self.key = "so0\n"
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

    def reboot(self):
        self.key = "rb\n"
        self.writeFunction()

    def getAddress(self):
        self.key = "re\n"
        self.writeFunction()

    def unknownRH(self):
        # gets result
        self.key = "rh\n"
        self.writeFunction()

    def presetCurrent(self):
        self.key = "ri\n"
        self.writeFunction()

    def unknownRJ(self):
        # gets result
        self.key = "rj\n"
        self.writeFunction()

    def unknownRK(self):
        # gets result
        self.key = "rk\n"
        self.writeFunction()

    def unknownRL(self):
        # gets result
        self.key = "rl\n"
        self.writeFunction()

    def unknownRM(self):
        # gets result
        self.key = "rm\n"
        self.writeFunction()

    def getDeviceSafeguard(self):
        self.key = "rp\n"
        self.writeFunction()

    def measureStatus(self):
        self.key = "rs\n"
        self.writeFunction()

    def presetVoltage(self):
        self.key = "ru\n"
        self.preset_voltage = self.writeFunction()

    def reboot_w(self):
        self.key = "rw\n"
        self.writeFunction()

    def unknownRX(self):
        # gets result
        self.key = "rx\n"
        self.writeFunction()

    def unknownRY(self):
        # gets same result rx
        self.key = "ry\n"
        self.writeFunction()

    def quit(self):
        self.turnOFF()
        self.com_device.close()
