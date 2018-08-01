#!/usr/bin/python

import sys
sys.path.insert(0, './Power Supplies')

"""
To add powersupply, simply add the object class python script for the power supply into the
Power Supplies subdirectory following the same structure of other files, then add the import
and constructor to this file as seen below
"""


import csi305db
import pps2116a
import pps3e004


class POWERSUPPLY:
    def __init__(self):
        self.voltage = "0.0"
        self.amperage = "0.0"
        try:
            self.powersupply = csi305db.CSI305DB()
        except:
            pass
        try:
            self.powersupply = pps2116a.PPS2116A()
        except:
            pass
        try:
            self.powersupply = pps3e004.PPS3E004()
        except:
            pass
