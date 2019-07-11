#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""
import visa
import sys
import time
import serial
import serial.tools.list_ports
"""
To add electronic load, simply add the object class python script for the electronic load into the
Electronic Loads subdirectory following the same structure of other files, then add the import
and constructor to this file as seen below
"""
from ElectronicLoads import array3720a
from ElectronicLoads import array3721a
from ElectronicLoads import array371x
from ElectronicLoads import generic_scpi


class BUS_INIT:
    def __init__(self, device_name=None):
        self.rm = visa.ResourceManager()
        self.threads = []
        # find all scpi devices
        self.device_count = 0
        for i in self.rm.list_resources():
            self.inst = self.rm.open_resource(i)
            self.inst.timeout = 100
            try:
                self.idn = self.inst.query("*IDN?")
                break
            except:
                self.inst.close()

        if(device_name != None):
            print('true')
            self.setDevice(device_name, self.inst)

        self.inst.timeout = 500
        try:
            self.name = str(self.idn).split(',')[0] + str(
                self.idn).split(',')[1]
            self.com_port = "COM" + str(self.inst.interface_number)
        except:
            self.inst.close()
            raise ValueError('No Electronic loads found')

        if (self.name == "ARRAY3720A"):
            self.device = array3720a.ARRAY3720A(self.inst)
        elif (self.name == "ARRAY3721A"):
            self.device = array3721a.ARRAY3721A(self.inst)
        elif (self.name != None or self.name != ""):
            print(self.name)
            self.device = generic_scpi.GENERIC_SCPI(self.inst)

    def setDevice(self, device_name, device):
        if(device_name.upper() == 'ARRAY3720A'):
            try:
                self.device = array3720a.ARRAY3720A(self.inst)
            except:
                print("Failed %s:%s" % [device_name, device])
        elif(device_name.upper() == 'ARRAY3721A'):
            try:
                self.device = array3721a.ARRAY3721A(self.inst)
            except:
                print("Failed %s:%s" % [device_name, device])
        elif(device_name.upper() == 'ARRAY371X'):
            com_device = serial.Serial(
            port=device,
            baudrate=9600,
            timeout=500,
            parity=serial.PARITY_EVEN,
            rtscts=0)
            try:
                self.device = array371x.ARRAY371X(com_device)
            except:
                print("Failed %s:%s" % device_name, device)
        else:
            try:
                self.device = generic_scpi.GENERIC_SCPI(self.inst)
            except:
                print("Failed %s:%s" % [device_name, device])
