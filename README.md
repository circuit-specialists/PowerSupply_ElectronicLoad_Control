# Power Suply and Electronic Load Control

One script to rule them all, one script to find the device, and one script to bind them all together

* Tested operating systems: Windows, Linux
* Tested Power Supplies: CSI305DB, PPS2116A, PPS2320A, PPS3E004
* Tested Electronic Loads: Array 3721A

## Features

* Autofinding Devices on COM bus
* Run from GUI or command line (GUI currently in alpha)
* Manual Voltage and Amperage control
* Run predined csv with timing and power specs
* Control Vendor specific functions
* (future) GUI graph for Voltage, Amperage, Power

## Documentation
**_Install Instructions_**

You first need to have python installed. If you don't, [download](https://www.python.org/downloads/) it here. Next, download this [zipped](https://github.com/circuit-specialists/Power-Suply-and-Electronic-Load-Control/archive/master.zip) repo. Once you have the repo, unzip the repo to a folder run `pip install -r requirements.txt` to install the dependencies. Once finish you can run the main.py. (FYI, log file is about 1KB per second)

**_Program Usage_**

* There are two modes. 
    * The GUI version is current as of v1.3 alpha.
        * To run the GUI version, run `python gui.py`.
    * The command line version is current as of v1.3.
        * To run the command line version, run `python cmd.py`.

###### GUI Help
To access the GUI help, run the GUI and select the help menu item.

###### Command Line Help
When the program first runs, the option for either running auto mode running from a csv file, or manual mode is given.

If you choose `Auto Mode`, you'll need to have the .csv file copied into the Example CSV folder. Then select from the list, the file number you want to load. The format for each device type csv file is diplayed in the first line of the provided example files.

If you chose `Manual Mode`, the program will prompt for the input values. Make sure to give full values, such as 0.123, 1, or 1.123. The program very likely will not be able to interpret truncated values such as .123.

**_Device Additions_**

More devices, and types of devices will be added on at later dates. To add a device yourself, place the device definitions and functions following the current structure as seen in "/Power Supplies/*.py", or "Electronic Loads/*.py" in the Power Supplies folder, then add the import/instantiation into powersupply.py or electronicload.py, whichever type of device you are adding along with the specs neccesary to interact with device.