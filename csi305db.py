#!/usr/bin/python

import serial
import serial.tools.list_ports
import time
import msvcrt

class CSI305DB:
    def __init__(self):
        pid="0403"
        hid="6001"
        self.com_ports = list(serial.tools.list_ports.comports())
        for p in self.com_ports:
            if pid and hid in p.hwid:
                print(p)
                # Connection to port
                self.com_device = serial.Serial(port=p.device, baudrate=9600, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)

        if self.com_device is None:
            raise ValueError('Device not found')

    def set(self, Volts, hectoVolts, Amps, milliAmps):
        self.key = 'HPPSU'
        self.key += '{:02}'.format(Volts)
        self.key += '{:02}'.format(hectoVolts)
        self.key += 'H'
        self.key += '{:01}'.format(Amps)
        self.key += '{:03}'.format(milliAmps)
        self.key += 'NY'
        self.com_device.write(self.key.encode())
        self.com_device.write(self.key.encode())
        #self.buf_read = self.com_device.read(100)
        #print(self.buf_read)

    def quit(self):
        self.com_device.close()
        exit()
        