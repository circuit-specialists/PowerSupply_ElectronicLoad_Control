#!/usr/bin/python

import serial
import serial.tools.list_ports
import time


class CSI305DB:
    def __init__(self):
        self.pid = "0403"
        self.vid = "6001"
        self.com_ports = list(serial.tools.list_ports.comports())
        for p in self.com_ports:
            if self.pid and self.vid in p.hwid:
                print(p)
                # Connection to port
                self.com_device = serial.Serial(
                    port=p.device, baudrate=9600, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)
                self.name = "CSI305DB"

            if self.com_device is None:
                raise ValueError('Device not found')

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

    def control(self):
        while True:
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

    def quit(self):
        self.com_device.close()
        exit()
