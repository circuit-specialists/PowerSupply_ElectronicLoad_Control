#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class CSI3645A:
    def __init__(self, address, com_device):
        self.com_device = com_device
        self.name = "CSI3645A"
        self.channels = 1
        self.frame_start = 0xAA
        self.address = address
        self.command = 0
        self.l_current = 0
        self.h_current = 0
        self.l2_max_voltage = 0xFF
        self.h2_max_voltage = 0xFF
        self.l1_max_voltage = 0xFF
        self.h1_max_voltage = 0xFF
        self.l_power = 0xFF
        self.h_power = 0xFF
        self.l2_voltage = 0
        self.h2_voltage = 0
        self.l1_voltage = 0
        self.h1_voltage = 0
        self.new_address = self.address
        self.system_resv = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.initialize()

    def initialize(self):
        self.command = 0x82
        self.l_current = 0x02
        self.writeFunction()
        self.command = 0x80
        self.l_current = 0
        self.writeFunction()

    def writeFunction(self):
        self.constructFrame()
        self.com_device.write(bytearray(self.frame))
        time.sleep(.02)
        return self.com_device.read_all()

    def constructFrame(self):
        self.frame = [self.frame_start, self.address, self.command, self.l_current, self.h_current, 
                      self.l2_max_voltage, self.h2_max_voltage, self.l1_max_voltage, self.h1_max_voltage, self.l_power, 
                      self.h_power, self.l2_voltage, self.h2_voltage, self.l1_voltage, self.h1_voltage, self.new_address]

        checksum = 0
        for i in self.frame:
            checksum += i

        self.frame.extend(self.system_resv)
        self.frame.extend([checksum % 256])
        print(self.frame)

    def setVoltage(self, voltage):
        self.voltage = voltage
        voltage = int(voltage.replace('.', ''))
        self.l2_voltage = int(voltage & 0xFF)
        voltage >>= 8
        self.h2_voltage = int(voltage & 0xFF)
        voltage >>= 8
        self.l1_voltage = int(voltage & 0xFF)
        voltage >>= 8
        self.h1_voltage = int(voltage & 0xFF)
        self.writeFunction()

    def setAmperage(self, amperage):
        self.amperage = amperage
        amperage = int(self.amperage.replace('.', ''))
        self.l_current = int(amperage & 0xFF)
        amperage >>= 8
        self.h_current = int(amperage & 0xFF)
        self.writeFunction()

    def setOutput(self, state):
        self.output = state
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def turnON(self):
        self.command = 0x82
        self.l_current = 3
        self.writeFunction()
        time.sleep(.4)

    def turnOFF(self):
        self.command = 0x82
        self.l_current = 2
        self.writeFunction()
        time.sleep(.4)

    def measureVoltage(self):
        self.key = "rv\n"
        self.voltage = self.writeFunction()
        self.voltage = float("%d%s%d" % (
            int(self.voltage[:2]), '.', int(self.voltage[2:-1])))
        return self.voltage

    def measureAmperage(self):
        self.key = "ra\n"
        self.amperage = self.writeFunction()
        self.amperage = float("%d%s%d" % (
            int(self.amperage[:2]), '.', int(self.amperage[2:-1])))
        return self.amperage

    def unsetPC(self):
        self.command = 0x82
        self.l_current = 0
        self.writeFunction()

    def quit(self):
        self.turnOFF()
        time.sleep(.2)
        self.unsetPC()
        self.com_device.close()
