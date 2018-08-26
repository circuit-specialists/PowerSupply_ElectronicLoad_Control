#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import visa
import time


class GENERIC_SCPI:
    def __init__(self, visa_instance):
        # Connection to port
        self.inst = visa_instance
        self.name = self.inst.query("*IDN?")
        self.inst.write("SYST:REM")
        self.channels = 1

    def getCurrent(self):
        self.current = self.inst.query(":MEAS:CURR?")
        return self.current

    def getVoltage(self):
        self.voltage = self.inst.query(":MEAS:VOLT?")
        return self.voltage

    def getIdentifier(self):
        return self.name

    def getPower(self):
        self.power = self.inst.query(":MEAS:POW?")
        return self.power

    def unknown(self):
        self.unknown = self.inst.query("*cls")
        return self.unknown

    def setLock(self):
        self.lock = self.inst.write("SYST:LOC")

    def setMode(self, mode):
        mode = str(mode).upper()
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
        self.inst.write(self.key)

    def setResistance(self, ohms):
        self.key = "RES " + str(ohms)
        self.inst.write(self.key)

    def setVoltageTrig(self, voltage):
        self.key = "VOLT:TRIG " + str(voltage)
        self.inst.write(self.key)

    def setTrigExt(self):
        self.key = "TRIG:SOUR EXT"
        self.inst.write(self.key)

    def setCurrent(self, current):
        self.key = "CURR " + str(current)
        self.inst.write(self.key)

    def setOutput(self, state):
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def turnON(self):
        self.key = "INP ON"
        self.inst.write(self.key)

    def turnOFF(self):
        self.key = "INP OFF"
        self.inst.write(self.key)

    def quit(self):
        self.inst.close()
