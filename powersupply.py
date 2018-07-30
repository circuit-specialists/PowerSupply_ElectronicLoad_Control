#!/usr/bin/python

import sys
sys.path.insert(0, './Power Supplies')


import csi305db
import pps2116a


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
