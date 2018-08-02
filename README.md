# Power Suply and Electronic Load Control

One script to rule them all, one script to find the device, and one script to bind them all together

* Tested operating systems: Windows
* Tested Power Supplies: CSI305DB, PPS2116A, PPS3E004
* Tested Electronic Loads: Array 3721A

## Features

* Autofinding on COM bus
* Run from command line (future:GUI)
* Manual Voltage and Amperage control
* Run predined csv with timing and power specs
* Control Vendor specific functions
* (future) Graph Voltage, Amperage, Power

## Documentation
*Install Instructions*
You first need to have python installed. If you don't, [download](https://www.python.org/downloads/) it here. You'll also need to install a few packages within python to communicate with the devices. These packages include, 'pyusb', 'pyvisa', and 'pyserial'. Each one of these can easily be install by using your command terminal, and the 'pip install' command. The last step is to download this [zipped](https://github.com/circuit-specialists/Power-Suply-and-Electronic-Load-Control/archive/master.zip) repo. Once you have the repo, unzip the repo to folder, open your command terminal, and navigate to the repo unzipped folder. To run the program, run main.py by executing 'python main.py' from the command terminal.

When program first runs, the option for either running a power supply or electronic load is given. Once the type of device is selected, the type of run usage needs to be selected. If you choose 'Auto-Mode', you'll need to have a .csv file titled 'auto_run_el.csv' for electronic loads, or 'auto_run_ps.csv' for power supplies. The format for each type is the first line in the provided example files.

If you chose manual mode, the program will prompt for the input values. Make sure to give full values, such as 0.123, 1, or 1.123. The program very likely will not be able to interpret truncated values such as .123.

More devices, and types of devices will be added on at later dates. To add a device yourself, place the device definitions and functions following the current structure as seen in "/Power Supplies/csi305db.py", or "Electronic Loads/array3721a.py" in the Power Supplies folder, and add the import/instantiation in the powersupply.py or electronicload.py script whichever type of device you are adding.