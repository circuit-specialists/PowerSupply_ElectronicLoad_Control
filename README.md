# Power Suply and Electronic Load Control

One script to rule them all, one script to find the device, and one script to bind them all together

* Tested operating systems: Windows
* Tested devices: CSI305DB, PPS2116A

## Features

* Autofinding on COM bus
* Run from command line (future:GUI)
* Manual Voltage and Amperage control
* Run predined csv with timing and power specs
* Control Vendor specific functions
* (future) Graph Voltage, Amperage, Power

## Documentation
You first need to have python installed. If you don't, [download](https://www.python.org/downloads/) it here. Download this [zipped](https://github.com/circuit-specialists/Power-Suply-and-Electronic-Load-Control/archive/master.zip) repo, unzip the repo to folder, open your command terminal, and navigate to that unzipped folder. Once arrived, simple type 'python main.py' to run program.

Current control structures are printed for each device assuming there are required extra steps, or extra functions. Each device is coded to expose a function for each possible control structure, but not each function is accesible. A menu system may be added, or wait until GUI is operational.