#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

# gui classes
try:  # windows
    import tkinter
    from tkinter import Menu, filedialog, Toplevel, Button, messagebox, Entry, Label, Canvas, Spinbox
except:  # unix
    import Tkinter as tkinter
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    from Tkinter import Menu, Toplevel, Button, Entry, Label, Canvas, Spinbox

# devices classes
import powersupply
import electronicload

# dependent classes
import sys
import webbrowser
import threading


class GUI:
    def __init__(self):
        self.threads = []
        self.variable_init()
        self.help_url = "https://circuit-specialists.github.io/PowerSupply_ElectronicLoad_Control/"
        self.bottom = tkinter.Tk(className=' cs power control')
        self.bottom.tk.call(
            'wm', 'iconphoto', self.bottom._w,
            tkinter.Image("photo", file="CircuitSpecialists.gif"))
        self.bottom.title('Circuit Specialists Power Control')
        self.setWindowSize(self.bottom, 700, 500)
        self.setMenuBar()
        self.drawManualControls()

    def drawManualControls(self):
        # Voltage Controls
        Label(self.bottom, text="Voltage: ").pack()
        self.voltage_bar = Spinbox(
            self.bottom, from_=0, to=32, format="%.2f", increment=0.01)
        self.voltage_bar.pack()
        self.setVoltsButton = Button(
            self.bottom, text="Set Volts", command=lambda: self.okay(self.voltage_bar, "V"))
        self.setVoltsButton.pack()

        # Amperage Controls
        Label(self.bottom, text="Amperage: ").pack()
        self.current_bar = Spinbox(
            self.bottom, from_=0, to=5.2, format="%.2f", increment=0.01)
        self.current_bar.pack()
        self.setAmpsButton = Button(
            self.bottom, text="Set Amps", command=lambda: self.okay(self.current_bar, "A"))
        self.setAmpsButton.pack()

        # Power Label
        self.power_label = Label(self.bottom)
        self.power_label.pack()
        self.updatePower(self.voltage, self.amperage)

        # Output Label
        self.output_label = Label(self.bottom, text="Output Off")
        self.output_label.pack()
        self.output_On_Button = Button(
            self.bottom, text="On", command=lambda: self.updateOutput(1))
        self.output_On_Button.pack()
        self.output_Off_Button = Button(
            self.bottom, text="Off", command=lambda: self.updateOutput(0))
        self.output_Off_Button.pack()

    def updatePower(self, voltage, amperage):
        self.power_label.config(text="Power: %.3f Watts" %
                                (voltage * amperage))

    def updateOutput(self, state):
        try:
            self.device.setOutput(state)
        except:
            pass
        self.output_label.config(text="Output: %s" %
                                 ("On" if state else "Off"))

    def drawCanvas(self):
        self.canvas_width = int(self.window_width / 2)
        self.canvas_height = int(self.window_height / 2)
        self.canvas = Canvas(
            self.bottom, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # w.coords(i, new_xy) # change coordinates
        # w.itemconfig(i, fill="blue") # change color
        # (x1,y1,x2,y2)
        self.graph_x1 = 0
        self.graph_y1 = 0
        self.graph_x2 = int(self.canvas_width)
        self.graph_y2 = int(self.canvas_height)
        self.canvas.create_rectangle(
            self.graph_x1, self.graph_y1, self.graph_x2, self.graph_y2, fill="#1a1a1a")

        # grid lines (reticules)
        self.horizontal_line_distance = int(self.canvas_width / 7)
        self.vertical_line_distance = int(self.canvas_height / 7)
        for x in range(self.horizontal_line_distance, self.canvas_width, self.horizontal_line_distance):
            self.canvas.create_line(x, 0, x, self.canvas_height,
                                    fill="#ffffff", dash=(4, 4))
        for y in range(self.vertical_line_distance, self.canvas_height, self.vertical_line_distance):
            self.canvas.create_line(0, y, self.canvas_width, y,
                                    fill="#ffffff", dash=(4, 4))

    def setWindowSize(self, object, width, height):
        # get screen size
        self.screen_width = object.winfo_screenwidth()
        self.screen_height = object.winfo_screenheight()

        # keep the window in ratio
        self.window_width = width
        if (self.screen_width < 1920):
            self.width_aspect = self.window_width / 1920
            self.window_width *= self.width_aspect
        self.window_height = height
        if (self.screen_height < 1080):
            self.height_aspect = self.window_height / 1080
            self.window_height *= self.height_aspect

        # set window to fit in ratio to screen size
        self.window_x = int(self.screen_width / 2 - self.window_width / 2)
        self.window_y = int(self.screen_height / 2 - self.window_height / 2)
        object.geometry('%dx%d+%d+%d' %
                        (self.window_width, self.window_height, self.window_x, self.window_y))

    def setMenuBar(self):
        self.menubar = Menu(self.bottom)
        self.setFileMenu()
        self.setEditMenu()
        self.setHelpMenu()
        self.bottom.config(menu=self.menubar)

    def setFileMenu(self):
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open CSV File...", command=self.openCSVFile)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_command(
            label="Save as...", command=self.save_AS_CSVFile)
        self.filemenu.add_command(label="Close", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.bottom.quit)
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
        # pop-up window
        self.top = Toplevel(self.bottom)
        self.setWindowSize(self.top, 250, 80)
        self.top.title(parameter)
        self.top.tk.call(
            'wm', 'iconphoto', self.top._w,
            tkinter.Image("photo", file="CircuitSpecialists.gif"))
        self.entry_dialog = Entry(self.top)
        self.top.bind('<Return>',
                      lambda: self.okay(self.entry_dialog, entry_type))

        # window parameters
        if (parameter == "Time Delay"):
            Label(self.top, text="Input Time Delay").pack()
            entry_type = "TD"
        elif (parameter == "Voltage"):
            Label(self.top, text="Input Voltage Value").pack()
            entry_type = "V"
        elif (parameter == "Current"):
            Label(self.top, text="Input Current Value").pack()
            entry_type = "A"

        # window function
        self.entry_dialog.pack(padx=5)
        button_dialog = Button(self.top, text="OK",
                               command=lambda: self.okay(self.entry_dialog, entry_type))
        button_dialog.pack(pady=5)

    def okay(self, object, type, event=None):
        entry = object.get()
        try:
            self.top.destroy()
            try:
                if (type == "TD"):
                    print()
                elif (type == "V"):
                    self.device.setVoltage(entry)
                    self.device.voltage = entry
                elif (type == "A"):
                    self.device.setAmperage(entry)
                    self.device.amperage = entry
                elif(type == "O"):
                    self.device.setOutput(entry)
                    self.device.output = entry
                elif(type == 'ccsv'):
                    print()
            except:
                messagebox.showerror("Error", "Device Not Connected")
        except:
            if(type == "V"):
                self.voltage = float(entry)
            elif(type == "A"):
                self.amperage = float(entry)

        self.updatePower(self.voltage, self.amperage)
        self.updateOutput(entry)

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
        self.top = Toplevel(self.bottom)
        Label(self.top, text="Create Run CSV").pack()
        entry_type = "ccsv"
        self.entry_dialog = Entry(self.top)
        self.entry_dialog.pack(padx=5)
        button_dialog = Button(self.top, text="OK",
                               command=lambda: self.okay(self.entry_dialog, entry_type))
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

    def variable_init(self):
        self.timestamps = []
        self.voltages = []
        self.currents = []
        self.outputs = []
        self.variable_count = 0
        self.programme_file = []
        self.voltage = 0
        self.amperage = 0
        self.output = 0

    def gotoURL(self, url):
        webbrowser.open_new_tab(url)

    def about(self):
        messagebox.showinfo(
            "About", "Version 1.3 alpha\n"
            "Operating System: %s" % sys.platform)

    def startWindow(self):
        self.bottom.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.startWindow()
