import serial
import serial.tools.list_ports
import time
import visa


class GENERIC_SCPI:
    def __init__(self):
        rm = visa.ResourceManager()
        rm.list_resources()
        ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
        inst = rm.open_resource('GPIB0::12::INSTR')
        print(inst.query("*IDN?"))