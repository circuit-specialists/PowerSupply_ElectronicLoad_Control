#!/usr/bin/python

import serial
import serial.tools.list_ports
import time
import msvcrt


class PSDEVICES:
    def __init__(self):
        pid = "0403"
        hid = "6001"
        self.com_ports = list(serial.tools.list_ports.comports())
        for p in self.com_ports:
            if "0403" and "6001" in p.hwid:
                print(p)
                # Connection to port
                self.com_device = serial.Serial(
                    port=p.device, baudrate=9600, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)
                self.device = "CSI305DB"
            elif "EA60" and "10C4" in p.hwid:
                print(p)
                # Connection to port
                self.com_device = serial.Serial(
                    port=p.device, baudrate=9600, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)
                self.device = "PPS2116A"
                self.key = "a\n"
                self.com_device.write(self.key.encode())
                time.sleep(.02)
                self.com_device.read_all()
                self.key = "o0\n"
                self.com_device.write(self.key.encode())
                time.sleep(.01)
                self.com_device.read_all()


        if self.com_device is None:
            raise ValueError('Device not found')

    def set(self, Volts, hectoVolts, Amps, milliAmps):
        if(self.device == "CSI305DB"):
            self.key = 'HPPSU'
            self.key += '{:02}'.format(Volts)
            self.key += '{:<02}'.format(hectoVolts)
            self.key += 'H'
            self.key += '{:01}'.format(Amps)
            self.key += '{:<03}'.format(milliAmps)
            self.key += 'NY'
            self.com_device.write(self.key.encode())
            self.com_device.write(self.key.encode())
        elif(self.device == "PPS2116A"):
            self.key = 'su'
            self.key += '{:02}'.format(Volts)
            self.key += '{:<02}'.format(hectoVolts)
            self.key += "\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.com_device.read_all()
            self.key = 'si'
            self.key += '{:01}'.format(Amps)
            self.key += '{:<03}'.format(milliAmps)
            self.key += "\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.com_device.read_all()

    def turnON(self):
        if(self.device == "PPS2116A"):
            self.key = "o1\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.measured_voltage = self.com_device.read_all()

    def turnOFF(self):
        if(self.device == "PPS2116A"):
            self.key = "o0\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.measured_voltage = self.com_device.read_all()

    def measureOutput(self):
        if(self.device == "PPS2116A"):
            measureVoltage()
            measureAmperage()
            measureS()

    def measureVoltage(self):
        if(self.device == "PPS2116A"):
            self.key = "rv\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.measured_voltage = self.com_device.read_all()

    def measureAmperage(self):
        if(self.device == "PPS2116A"):
            self.key = "ra\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.measured_amperage = self.com_device.read_all()

    def measureS(self):
        if(self.device == "PPS2116A"):
            self.key = "rs\n"
            self.com_device.write(self.key.encode())
            time.sleep(.01)
            self.measured_s = self.com_device.read_all()


        #self.buf_read = self.com_device.read(100)
        # print(self.buf_read)

    def quit(self):
        self.turnOFF()
        self.com_device.close()
        exit()
