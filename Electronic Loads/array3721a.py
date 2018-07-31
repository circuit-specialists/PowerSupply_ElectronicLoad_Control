#!/usr/bin/python

import serial
import serial.tools.list_ports
import time


class ARRAY3721A:
    def __init__(self, com_port):
        # Connection to port
        self.com_device = serial.Serial(
            port=com_port, baudrate=9600, timeout=500, dsrdtr=1)
        self.name = "Array3721A"
        self.key = "SYST:REM"
        self.writeFunction()

    def writeFunction(self):
        self.com_device.write(str(self.key + "\r\n").encode())
        time.sleep(.01)

    def getCurrent(self):
        self.key = ":MEAS:CURR?"
        self.writeFunction()
        self.current = self.com_device.read_all()
        return self.current

    def getVoltage(self):
        self.key = ":MEAS:VOLT?"
        self.writeFunction()
        self.voltage = self.com_device.read_all()
        return self.voltage

    def getIdentifier(self):
        self.key = "*IDN?"
        self.writeFunction()
        self.indentifier = self.com_device.read_all()
        return self.indentifier

    def getPower(self):
        self.key = "MEAS:POW?"
        self.writeFunction()
        self.power = self.com_device.read_all()
        return self.power

    def unknown(self):
        self.key = "*cls"
        self.writeFunction()

    def unknown2(self):
        self.key = "SYST:LOC"
        self.writeFunction()

    def setMode(self, mode):
        mode = str(mode).upper()
        print(mode)
        if(mode == "CCH"):
            self.key = "MODE CCH"
        elif(mode == "CCL"):
            self.key = "MODE CCL"
        elif(mode == "CV"):
            self.key = "MODE CV"
        elif(mode == "CRM"):
            self.key = "MODE CRM"
        else:
            return
        self.writeFunction()

    def setResistance(self, ohms):
        self.key = "RES " + str(ohms)
        self.writeFunction()

    def setVoltageTrig(self, voltage):
        self.key = "VOLT:TRIG " + str(voltage)
        self.writeFunction()

    def setTrigExt(self):
        self.key = "TRIG:SOUR EXT"
        self.writeFunction()

    def setCurrent(self, current):
        self.key = "CURR " + str(current)
        self.writeFunction()

    def turnON(self):
        self.key = "INP ON"
        self.writeFunction()

    def turnOFF(self):
        self.key = "INP OFF"
        self.writeFunction()

    def quit(self):
        self.com_device.close()
        exit()
