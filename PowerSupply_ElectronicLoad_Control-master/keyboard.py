#!/usr/bin/python

import msvcrt
import sys

class KEYBOARD:
    def __init__(self):
        self.input_buf = ""
        self.kill_signal = False

    def getInput(self):
        while True:
            if msvcrt.kbhit():
                self.input_buf = msvcrt.getch().decode('UTF-8')
                self.null = msvcrt.getch()
            if(self.kill_signal):
                return

    def quit(self):
        self.kill_signal = True