#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

import sys
if ("win" in sys.platform):
    import msvcrt
else:
    import termios
    import tty


class KEYBOARD:
    def __init__(self):
        self.input_buf = ''
        self.kill_signal = False

    def inputHandler(self):
        while True:
            if ("win" in sys.platform):
                if msvcrt.kbhit():
                    self.input_buf = msvcrt.getch().decode('UTF-8')
                    self.null = msvcrt.getch()
            else:
                #self.input_buf = sys.stdin.read(1)
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                self.input_buf = ch

            if (self.kill_signal):
                return

    def getInput(self):
        if(self.input_buf != ''):
            temp = self.input_buf
            self.input_buf = ''
            return temp

    def quit(self):
        self.kill_signal = True
