#!/usr/bin/python

import serial
import serial.tools.list_ports
import time


class PPS2116A:
    def __init__(self):
        self.pid = "EA60"
        self.vid = "10C4"
        self.com_ports = list(serial.tools.list_ports.comports())
        for p in self.com_ports:
            if self.pid and self.vid in p.hwid:
                print(p)
                # Connection to port
                self.com_device = serial.Serial(
                    port=p.device, baudrate=9600, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)
                self.key = "a\n"
                self.com_device.write(self.key.encode())
                time.sleep(.02)
                self.com_device.read_all()
                self.key = "o0\n"
                self.com_device.write(self.key.encode())
                time.sleep(.02)
                self.com_device.read_all()
                self.name = "PPS2116A"
                print("Press 'o' for output and 'f' to turn off")

        if self.com_device is None:
            raise ValueError('Device not found')

    def setVoltage(self):
        self.key = 'su'
        self.key += '{:02}'.format(self.volts)
        self.key += '{:<02}'.format(self.hectoVolts)
        self.key += "\n"
        return self.key.encode()

    def setAmperage(self):
        self.key = 'si'
        self.key += '{:01}'.format(self.amps)
        self.key += '{:<03}'.format(self.milliAmps)
        self.key += "\n"
        return self.key.encode()

    def control(self):
        self.com_device.write(self.setVoltage())
        time.sleep(.02)
        self.com_device.read_all()
        self.com_device.write(self.setAmperage())
        time.sleep(.02)
        self.com_device.read_all()

    def setParameters(self, voltage, amperage):
        if(voltage != "."):
            try:
                self.volts = int(voltage.split('.')[0])
                try:
                    self.hectoVolts = int(voltage.split('.')[1])
                except:
                    self.hectoVolts = 0
            except:
                self.volts = 0

        if(amperage != "."):
            try:
                self.amps = int(amperage.split('.')[0])
                try:
                    self.milliAmps = int(amperage.split('.')[1])
                except:
                    self.milliAmps = 0
            except:
                self.volts = 0

        self.control()

    def writeFunction(self):
        self.com_device.write(self.key.encode())
        time.sleep(.01)
        self.com_device.read_all()

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

    def turnON(self):
        self.key = "o1\n"
        self.writeFunction()

    def turnOFF(self):
        self.key = "o0\n"
        self.writeFunction()

    def measureVoltage(self):
        self.key = "rv\n"
        self.writeFunction()

    def measureAmperage(self):
        self.key = "ra\n"
        self.writeFunction()

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
        exit()
