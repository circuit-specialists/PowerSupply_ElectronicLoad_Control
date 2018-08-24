#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import msvcrt
import sys


class KEYBOARD:
    def __init__(self):
        self.input_buf = ''
        self.kill_signal = False

    def inputHandler(self):
        while True:
            if msvcrt.kbhit():
                self.input_buf = msvcrt.getch().decode('UTF-8')
                self.null = msvcrt.getch()
            if (self.kill_signal):
                return
    
    def getInput(self):
        temp = self.input_buf
        self.input_buf = ''
        return temp

    def quit(self):
        self.kill_signal = True