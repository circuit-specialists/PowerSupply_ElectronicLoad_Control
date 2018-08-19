#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

# gui classes
try:  # windows
    import tkinter
    from tkinter import Menu, filedialog, Toplevel, Button, messagebox, Entry, Label
except:  # unix
    import Tkinter as tkinter
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    from Tkinter import Menu, Toplevel, Button, Entry, Label
    import os

# devices classes
import powersupply
import electronicload

# dependent classes
import sys
import webbrowser


class GUI:
    def __init__(self):
        self.timestamp = []
        self.voltage = []
        self.current = []
        self.output = []
        self.variable_count = 0
        self.programme_file = []
        self.help_url = "https://github.com/circuit-specialists/PowerSupply_ElectronicLoad_Control/wiki"
        self.floor = tkinter.Tk()
        try:  # windows
            self.floor.iconbitmap('CircuitSpecialists.ico')
        except:  # unix
            self.floor.iconbitmap('@CircuitSpecialists.xbm')
        self.floor.title('Circuit Specialists')
        self.setWindowSize()
        self.setMenuBar()

    def setWindowSize(self):
        # get screen size
        self.screen_width = self.floor.winfo_screenwidth()
        self.screen_height = self.floor.winfo_screenheight()

        # keep the window in ratio
        self.window_height = 500
        if (self.screen_height < 1080):
            self.height_aspect = self.window_height / 1080
            self.window_height *= self.height_aspect
        self.window_width = 700
        if (self.screen_width < 1920):
            self.width_aspect = self.window_width / 1920
            self.window_width *= self.width_aspect

        # set window to fit in ratio to screen size
        self.floor.geometry(
            str(self.window_width) + "x" + str(self.window_height))

    def setMenuBar(self):
        self.menubar = Menu(self.floor)
        self.setFileMenu()
        self.setEditMenu()
        self.setHelpMenu()
        self.floor.config(menu=self.menubar)

    def setFileMenu(self):
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open CSV File...", command=self.openCSVFile)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(
            label="Save as...", command=self.save_AS_CSVFile)
        self.filemenu.add_command(label="Close", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.floor.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def setEditMenu(self):
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Device", command=self.deviceSelection)
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label="Run Single Loop", command=self.runSingleLoop)
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label="Create CSV File", command=self.createCSVFile)
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label="Time Delay", command=lambda: self.getEntry("Time Delay"))
        self.editmenu.add_command(
            label="Voltage", command=lambda: self.getEntry("Voltage"))
        self.editmenu.add_command(
            label="Amperge", command=lambda: self.getEntry("Current"))
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Mode", command=self.donothing)
        self.editmenu.add_command(label="EL Setting", command=self.donothing)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Output", command=self.setOutput)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

    def setHelpMenu(self):
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(
            label="Help Index", command=lambda: self.gotoURL(self.help_url))
        self.helpmenu.add_command(label="About...", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def donothing(self):
        self.null = None

    def setOutput(self):
        self.device.setOutput(
            messagebox.askyesno(
                title="Output State", message="Turn On Output?"))

    def getEntry(self, parameter):
        self.top = Toplevel(self.floor)
        self.top.bind('<Return>', self.okay)
        if (parameter == "Time Delay"):
            Label(self.top, text="Input Time Delay").pack()
            self.entry_type = "TD"
        elif (parameter == "Voltage"):
            Label(self.top, text="Input Voltage Value").pack()
            self.entry_type = "V"
        elif (parameter == "Current"):
            Label(self.top, text="Input Current Value").pack()
            self.entry_type = "A"
        self.entry_dialog = Entry(self.top)
        self.entry_dialog.pack(padx=5)
        button_dialog = Button(self.top, text="OK", command=self.okay)
        button_dialog.pack(pady=5)

    def okay(self, event=None):
        self.entry = self.entry_dialog.get()
        self.top.destroy()
        if (self.entry_type == "TD"):
            print()
        elif (self.entry_type == "V"):
            self.device.setVoltage(self.entry)
        elif (self.entry_type == "A"):
            self.device.setAmperage(self.entry)

    def openCSVFile(self):
        self.programme_filename = filedialog.askopenfilename(
            initialdir="./",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        try:
            with open(self.programme_filename, "r") as f:
                self.programme_file = f.readlines()
        except:
            messagebox.showerror("Error", "Unable to open file")

    def save(self):
        try:
            self.log_file = open(self.save_filename + ".csv", "w")
        except:
            pass
        for i in range(0, self.variable_count):
            self.log_file.writelines("%d, %d, %d, %d" % self.timestamp[i],
                                     self.voltage[i], self.current[i],
                                     self.output[i])

    def save_AS_CSVFile(self):
        self.save_filename = filedialog.asksaveasfilename(
            initialdir="./",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        self.save()

    def createCSVFile(self):
        self.top = Toplevel(self.floor)
        Label(self.top, text="Create Run CSV").pack()
        self.entry_type = "CSVC"
        self.entry_dialog = Entry(self.top)
        self.entry_dialog.pack(padx=5)
        button_dialog = Button(self.top, text="OK", command=self.okay)
        button_dialog.pack(pady=5)

    def storeVariabels(self, Timestamp, Voltage, Current, Output):
        self.timestamp.append(Timestamp)
        self.voltage.append(Voltage)
        self.current.append(Current)
        self.output.append(Output)

    def runSingleLoop(self):
        self.null = None

    def deviceSelection(self):
        try:
            self.device = powersupply.POWERSUPPLY()
            self.device = self.device.powersupply
            messagebox.showinfo("Power Supply",
                                "Detected: " + self.device.name)
        except:
            try:
                self.device = electronicload.ELECTRONICLOAD()
                self.device = self.device.electronicload
                messagebox.showinfo("Electronic Load",
                                    "Detected: " + self.device.name)
            except:
                messagebox.showerror(
                    "Error", "Sorry, no devices currently supported are found")

    def gotoURL(self, url):
        webbrowser.open_new_tab(url)

    def about(self):
        messagebox.showinfo(
            "About", "Version 1.3 alpha\n"
            "Operating System: %s" % sys.platform)

    def startWindow(self):
        self.floor.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.startWindow()
