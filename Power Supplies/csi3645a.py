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
        self.command = 0x00
        self.l_current = 0x00
        self.h_current = 0x00
        self.l2_voltage = 0x00
        self.h2_voltage = 0x00
        self.l1_voltage = 0x00
        self.h1_voltage = 0x00
        self.l_power = 0x00
        self.h_power = 0x00
        self.l2_char = 0x00
        self.h2_char = 0x00
        self.l1_char = 0x00
        self.h1_char = 0x00
        self.new_address = self.address
        self.system_resv = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.initialize()

    def constructFrame(self):
        self.frame = [self.frame_start, self.address, self.command, self.l_current, self.h_current, 
                      self.l2_voltage, self.h2_voltage, self.l1_voltage, self.h1_voltage, self.l_power, 
                      self.h_power, self.l2_char, self.h2_char, self.l1_char, self.h1_char, self.new_address]

        checksum = 0
        for i in self.frame:
            checksum += i

        self.frame.extend(self.system_resv)
        self.frame.extend([checksum % 256])

    def initialize(self):
        self.command = 0x82
        self.l_current = 0x02
        self.writeFunction()

    def writeFunction(self):
        self.constructFrame()
        self.com_device.write(bytearray(self.frame))
        time.sleep(.02)
        return self.com_device.read_all()

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

        byte_string = b""
        byte_string += b'\xAA'
        byte_string += self.address.encode()
        byte_string += b'\x80'
        self.key += '{:04}'.format(self.volts)
        self.key += '{:01}'.format(self.hectoVolts)
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
                self.milliamps = int(amperage.split('.')[1])
            except:
                self.milliamps = 0
        else:
            self.amps = int(amperage)
            self.milliamps = 0

        self.key = 'si'
        #self.key += '0' + '{:<04}'.format(self.milliAmps)
        self.key += "\n"
        self.writeFunction()

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
        self.command = b"\x82"
        self.l_current = b"\x03"
        self.writeFunction()

    def turnOFF(self):
        self.command = b"\x82"
        self.l_current = b"\x02"
        self.writeFunction()

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

    def reboot(self):
        self.key = "rb\n"
        self.writeFunction()

    def getAddress(self):
        self.key = "re\n"
        self.writeFunction()

    def presetCurrent(self):
        self.key = "ri\n"
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

    def quit(self):
        self.turnOFF()
        self.com_device.close()
