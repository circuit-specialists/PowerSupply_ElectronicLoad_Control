#!/usr/bin/python

"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import visa
import time


class CSI3005P:
    def __init__(self, visa_instance):
        # Connection to port
        self.inst = visa_instance
        self.name = "CSI3005P"
        self.type = "powersupply"
        self.inst.write("SYST:REM")
        self.channels = 1
        self.setVoltage("0")
        self.setAmperage("0")
        self.setOutput(0)

    def getID(self):
        return self.inst.query("*IDN?\n")[-1]

    def setVoltage(self, voltage):
        self.inst.query("VSET1:%s\n" % voltage)

    def setAmperage(self, amperage):
        self.inst.query("ISET1:%s\n" % amperage)

    def getVoltage(self):
        return self.inst.query("VSET1?\n")[-1]

    def getCurrent(self):
        return self.inst.query("ISET1?\n")[-1]

    def measureVoltage(self):
        return self.inst.query("VOUT1?\n")[-1]

    def measureCurrent(self):
        return self.inst.query("IOUT1?\n")[-1]

    def setOutput(self, state):
        if(state):
            self.turnON()
        else:
            self.turnOFF()

    def turnON(self):
        self.inst.query("OUTPUT1\n")

    def turnOFF(self):
        self.inst.query("OUTPUT0\n")

    def getStatus(self):
        return self.inst.query("STATUS?\n")[-1]

    def quit(self):
        self.turnOFF()
        self.inst.close()
