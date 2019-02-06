#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""
import visa
import sys
import time
"""
To add electronic load, simply add the object class python script for the electronic load into the
Electronic Loads subdirectory following the same structure of other files, then add the import
and constructor to this file as seen below
"""


class ELECTRONICLOAD:
    def __init__(self):
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
                pass

        self.inst.timeout = 500
        try:
            self.name = str(self.idn).split(',')[0] + str(
                self.idn).split(',')[1]
            self.com_port = "COM" + str(self.inst.interface_number)
        except:
            raise ValueError('No Electronic loads found')

        if (self.name == "ARRAY3720A"):
            import array3720a
            self.electronicload = array3720a.ARRAY3720A(self.inst)
        elif (self.name == "ARRAY3721A"):
            import array3721a
            self.electronicload = array3721a.ARRAY3721A(self.inst)
        elif (self.name != None or self.name != ""):
            import generic_scpi
            print(self.name)
            self.electronicload = generic_scpi.GENERIC_SCPI(self.inst)
