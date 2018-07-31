#!/usr/bin/python

import os
import visa
import sys
sys.path.insert(0, './Electronic Loads')

"""
To add electronic load, simply add the object class python script for the electronic load into the
Electronic Loads subdirectory following the same structure of other files, then add the import
and constructor to this file as seen below
"""


import generic_scpi
import array3721a


class ELECTRONICLOAD:
    def __init__(self):
        self.rm = visa.ResourceManager()
        for i in self.rm.list_resources():
            self.inst = self.rm.open_resource(i)
            try:
                self.idn = self.inst.query("*IDN?")
                for device in os.listdir():
                    if(device[:-3] in self.idn):
                        self.el = self.idn
            except:
                pass
        self.name = str(self.el).split(',')[0] + str(self.el).split(',')[1]
        self.com_port = "COM" + str(self.inst.interface_number)
        self.rm.close()

        if(self.name == "ARRAY3721A"):
            self.electronicload = array3721a.ARRAY3721A(self.com_port)
