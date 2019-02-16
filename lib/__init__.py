#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""
from lib import CircuitIconGIF
from lib import CircuitIconUnix
from lib import CircuitIconWin

class RESOURCES:
    def __init__(self):
        self.gif_icon = CircuitIconGIF.IMG().data
        self.unix_icon = CircuitIconUnix.IMG().data
        self.win_icon = CircuitIconWin.IMG().data