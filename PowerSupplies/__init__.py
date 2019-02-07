#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""
import serial
import serial.tools.list_ports
import time
import sys
import visa
"""
To add powersupply, simply add the object class python script for the power supply into the
Power Supplies subdirectory following the same structure of other files, then add the import
and constructor to this file as seen below
"""


class POWERSUPPLY:
    def __init__(self, device_name=None):
        com_ports = list(serial.tools.list_ports.comports())
        for p in com_ports:
            if "6001" and "0403" in p.hwid:
                # Generic UART bridge, must be more specific
                if(device_name is None):
                    raise ValueError('Found Generic UART Device')
                else:
                    self.setDevice(device_name, p.device)
            elif "10C4" and "EA60" in p.hwid:
                # Connection to port
                com_device = serial.Serial(
                    port=p.device,
                    baudrate=9600,
                    timeout=500,
                    parity=serial.PARITY_EVEN,
                    rtscts=0)
                response = self.write(com_device, "a\n").decode()
                if ("DPS3205U" in response):
                    import pps2116a
                    self.powersupply = pps2116a.PPS2116A(com_device)
                    break
                elif ("3203" in response):
                    import pps2320a
                    self.powersupply = pps2320a.PPS2320A(com_device)
                    break
                else:
                    com_device.baudrate = 38400
                    response = self.write(com_device, "a\n").decode()
                    if ("300V/0400mA" in response):
                        import pps3e004
                        self.powersupply = pps3e004.PPS3E004(com_device)
                        break

        if (self.powersupply is None):
            raise ValueError()

    def setDevice(self, device_name, device):
        if(device_name.upper() == 'CSI305DB'):
            import csi305db
            try:
                com_device = serial.Serial(
                    port=device,
                    baudrate=9600,
                    timeout=500,
                    parity=serial.PARITY_EVEN,
                    rtscts=0)
                self.powersupply = csi305db.CSI305DB(com_device)
            except:
                print(p)
        elif(device_name.upper() == 'CSI3645A'):
            import csi3645a
            address = 1
            try:
                com_device = serial.Serial(
                    port=device,
                    baudrate=38400,
                    timeout=500,
                    parity=serial.PARITY_EVEN,
                    rtscts=0)
                self.powersupply = csi3645a.CSI3645A(address, com_device)
            except:
                print(p)

    def write(self, com_device, bytes):
        print(bytes.encode())
        com_device.write(bytes.encode())
        time.sleep(.02)
        return com_device.read_all()
