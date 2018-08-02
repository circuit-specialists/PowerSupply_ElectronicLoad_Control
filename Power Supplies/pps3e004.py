#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import serial
import serial.tools.list_ports
import time


class PPS3E004:
    def __init__(self):
        self.pid = "EA60"
        self.vid = "10C4"
        self.com_ports = list(serial.tools.list_ports.comports())
        for p in self.com_ports:
            if self.pid and self.vid in p.hwid:                
                # Connection to port
                self.com_device = serial.Serial(
                    port=p.device, baudrate=38400, timeout=500, parity=serial.PARITY_EVEN, rtscts=0)
                self.key = "a\n"
                for i in range(0, 3):
                    self.com_device.write(self.key.encode())
                    time.sleep(.02)
                    self.spec = self.com_device.read_all()
                if("300V/0400mA\r\n".encode() in self.spec):
                    print(str(self.spec)[2:-5])
                else:
                    self.com_device.close()
                    raise ValueError("Not right device")
                time.sleep(.02)
                self.com_device.read_all()
                self.name = "PPS3E004"
                print("Press 'o' for output and 'f' to turn off")

        if self.com_device is None:
            raise ValueError('Device not found')

    def setVoltage(self):
        self.key = 'su'
        self.key += '{:04}'.format(self.volts)
        self.key += '{:01}'.format(self.hectoVolts)
        self.key += "\n"
        return self.key.encode()

    def setAmperage(self):
        self.key = 'si'
        self.key += '{:04}'.format(self.milliAmps)
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
            except:
                self.volts = 0
            try:
                self.hectoVolts = int(voltage.split('.')[1])
            except:
                self.hectoVolts = 0

        if(amperage != "."):
            try:
                self.amps = int(amperage.split('.')[0])
            except:
                self.amps = 0
            try:
                self.milliAmps = int(amperage.split('.')[1])
            except:
                self.milliAmps = 0

        self.control()

    def writeFunction(self):
        self.com_device.write(self.key.encode())
        time.sleep(.01)
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

    def turnON(self):
        self.key = "so1\n"
        self.writeFunction()

    def turnOFF(self):
        self.key = "so0\n"
        self.writeFunction()

    def setOutput(self, state):
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def measureAmperage(self):
        self.key = "ra\n"
        self.amperage = self.writeFunction()

    def reboot(self):
        self.key = "rb\n"
        self.writeFunction()

    def unknownRC(self):
        self.key = "rc\n"
        self.writeFunction()

    def unknownRD(self):
        self.key = "rd\n"
        self.writeFunction()

    def getAddress(self):
        self.key = "re\n"
        self.writeFunction()

    def unknownRF(self):
        self.key = "rf\n"
        self.writeFunction()

    def unknownRG(self):
        self.key = "rg\n"
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

    def unknownRN(self):
        self.key = "rn\n"
        self.writeFunction()

    def unknownRO(self):
        self.key = "ro\n"
        self.writeFunction()

    def getDeviceSafeguard(self):
        self.key = "rp\n"
        self.writeFunction()

    def unknownRQ(self):
        self.key = "rq\n"
        self.writeFunction()

    def unknownRR(self):
        self.key = "rr\n"
        self.writeFunction()

    def measureStatus(self):
        self.key = "rs\n"
        self.writeFunction()

    def unknownRT(self):
        self.key = "rt\n"
        self.writeFunction()

    def presetVoltage(self):
        self.key = "ru\n"
        self.preset_voltage = self.writeFunction()

    def measureVoltage(self):
        self.key = "rv\n"
        self.voltage = self.writeFunction()

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

    def unknownRZ(self):
        self.key = "rz\n"
        self.writeFunction()

    def quit(self):
        self.turnOFF()
        self.com_device.close()
        exit()
