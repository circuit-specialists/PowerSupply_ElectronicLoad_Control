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
            if(voltage > "1."):
                self.volts = int(voltage.split('.')[0])
            else:
                self.volts = 0
            if(voltage < "."):
                self.hectoVolts = int(voltage.split('.')[1])
            else:
                self.hectoVolts = 0
        else:
            self.volts = 0
            self.hectoVolts = 0

        if(amperage != "."):
            if(amperage > "1."):
                self.amps = int(amperage.split('.')[0])
            else:
                self.amps = 0
            if(amperage < "."):
                self.milliAmps = int(amperage.split('.')[1])
            else:
                self.milliAmps = 0
        else:
            self.amps = 0
            self.milliAmps = 0

        self.control()

    def setCPUADDR(self, ADDR):
        self.key = 'sa'
        self.key += '{:04}'.format(ADDR)
        self.key += "\n"
        return self.key.encode()

    def setCPUData(self, Data):
        self.key += 'si'
        self.key += '{:04}'.format(Data)
        self.key += "\n"
        return self.key.encode()

    def turnON(self):
        self.key = "o1\n"
        return self.key.encode()

    def turnOFF(self):
        self.key = "o0\n"
        return self.key.encode()

    def measureVoltage(self):
        self.key = "rv\n"
        return self.key.encode()

    def measureAmperage(self):
        self.key = "ra\n"
        return self.key.encode()

    def presetVoltage(self):
        self.key = "ru\n"
        return self.key.encode()

    def presetCurrent(self):
        self.key = "ri\n"
        return self.key.encode()

    def getAddress(self):
        self.key = "re\n"

    def getDeviceSafeguard(self):
        self.key = "rp\n"
        return self.key.encode()

    def measureStatus(self):
        self.key = "rs\n"
        return self.key.encode()

    def quit(self):
        self.turnOFF()
        self.com_device.close()
        exit()
