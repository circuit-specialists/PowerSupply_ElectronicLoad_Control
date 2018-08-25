#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import sys
if (sys.platform == "win32"):
    import msvcrt
else:
    import termios, sys, os


class KEYBOARD:
    def __init__(self):
        self.input_buf = ''
        self.kill_signal = False

    def inputHandler(self):
        while True:
            if (sys.platform == "win32"):
                if msvcrt.kbhit():
                    self.input_buf = msvcrt.getch().decode('UTF-8')
                    self.null = msvcrt.getch()
            else:
                self.input_buf = sys.stdin.read(1)
                self.null = sys.stdin.read(1)
                print(self.input_buf)
            if (self.kill_signal):
                return

    def getInput(self):
        temp = self.input_buf
        self.input_buf = ''
        return temp

    def quit(self):
        self.kill_signal = True