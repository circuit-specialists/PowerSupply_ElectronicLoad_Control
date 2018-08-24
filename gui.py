#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

# gui classes
try:  # windows
    import tkinter
    from tkinter import Menu, filedialog, Toplevel, Button, messagebox, Entry, Label, Canvas, Spinbox, Frame
except:  # unix
    import Tkinter as tkinter
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    from Tkinter import Menu, Toplevel, Button, Entry, Label, Canvas, Spinbox, Frame

# dependent classes
import sys
import webbrowser
import threading

# Paths to devices and libraries
sys.path.insert(0, './Power Supplies')
sys.path.insert(0, './Electronic Loads')
import powersupply
import electronicload


class GUI:
    def __init__(self):
        # 1337
        # (0|]3
        self.version = "1.3 alpha"
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
        voltage_frame = Frame(self.bottom)
        self.voltage_label = Label(voltage_frame, text="Voltage: ")
        self.voltage_label.pack(side=tkinter.LEFT, padx=5)
        voltage_bar = Spinbox(
            voltage_frame, from_=0, to=32, format="%.2f", increment=0.01)
        voltage_bar.pack(side=tkinter.LEFT)
        setVoltsButton = Button(
            voltage_frame,
            text="Set Volts",
            command=lambda: self.getEntry(voltage_bar, "V"))
        setVoltsButton.pack(side=tkinter.LEFT, padx=5)
        voltage_frame.pack()

        # Amperage Controls
        current_frame = Frame(self.bottom)
        self.current_label = Label(current_frame, text="Amperage: ")
        self.current_label.pack(side=tkinter.LEFT)
        current_bar = Spinbox(
            current_frame, from_=0, to=5.2, format="%.3f", increment=0.01)
        current_bar.pack(side=tkinter.LEFT)
        setAmpsButton = Button(
            current_frame,
            text="Set Amps",
            command=lambda: self.getEntry(current_bar, "A"))
        setAmpsButton.pack(side=tkinter.LEFT, padx=5)
        current_frame.pack()

        # Power Label
        self.power_label = Label(self.bottom)
        self.power_label.pack()
        self.updatePower(self.voltage, self.amperage)

        # Output Label
        output_frame = Frame(self.bottom)
        self.output_label = Label(output_frame, text="Output: Off")
        self.output_label.pack(side=tkinter.LEFT)
        output_On_Button = Button(
            output_frame, text="On", command=lambda: self.updateOutput(1))
        output_On_Button.pack(side=tkinter.LEFT)
        output_Off_Button = Button(
            output_frame, text="Off", command=lambda: self.updateOutput(0))
        output_Off_Button.pack(side=tkinter.LEFT, padx=5)
        output_frame.pack()

    def updateVoltage(self, voltage):
        self.voltage_label.config(text="Voltage: %.2fV" % (voltage))

    def updateAmperage(self, amperage):
        self.current_label.config(text="Amperage: %.3fA" % (amperage))

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

    def runThread(self, object):
        threads = []
        t1 = threading.Thread(target=self.donothing)
        threads.append(t1)
        t1.start()

    def drawCanvas(self):
        self.canvas_width = int(self.window_width / 2)
        self.canvas_height = int(self.window_height / 2)
        self.canvas = Canvas(
            self.bottom, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # w.coords(i, new_xy) # change coordinates
        # w.itemconfig(i, fill="blue") # change color
        # (x1,y1,x2,y2)
        graph_x1 = 0
        graph_y1 = 0
        graph_x2 = int(self.canvas_width)
        graph_y2 = int(self.canvas_height)
        self.canvas.create_rectangle(
            graph_x1,
            graph_y1,
            graph_x2,
            graph_y2,
            fill="#1a1a1a")

        # grid lines (reticules)
        self.horizontal_line_distance = int(self.canvas_width / 7)
        self.vertical_line_distance = int(self.canvas_height / 7)
        for x in range(self.horizontal_line_distance, self.canvas_width,
                       self.horizontal_line_distance):
            self.canvas.create_line(
                x, 0, x, self.canvas_height, fill="#ffffff", dash=(4, 4))
        for y in range(self.vertical_line_distance, self.canvas_height,
                       self.vertical_line_distance):
            self.canvas.create_line(
                0, y, self.canvas_width, y, fill="#ffffff", dash=(4, 4))

    def runAutoWindow(self, parameters):
        # pop-up window
        self.creatTopWindow(400, 400, "Running Mode")
        
        start_button = Button(
            self.top,
            text="Start",
            command=lambda: self.donothing)
        start_button.pack(pady=5)
        stop_button = Button(
            self.top,
            text="Stop",
            command=lambda: self.donothing)
        stop_button.pack(pady=5)

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
        object.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height,
                                         self.window_x, self.window_y))

    def setMenuBar(self):
        self.menubar = Menu(self.bottom)
        self.setFileMenu()
        self.setEditMenu()
        self.setHelpMenu()
        self.bottom.config(menu=self.menubar)

    def setFileMenu(self):
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(
            label="Open CSV File...", command=self.openCSVFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(
            label="Save as...", command=self.save_AS_CSVFile)
        filemenu.add_command(label="Close", command=self.closeFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.bottom.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def setEditMenu(self):
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(
            label="Find Device", command=self.deviceSelection)
        editmenu.add_separator()
        editmenu.add_command(
            label="Run Single Loop", command=self.runSingleLoop)
        editmenu.add_separator()
        editmenu.add_command(
            label="Create CSV File", command=self.createCSVFile)
        editmenu.add_separator()
        editmenu.add_command(
            label="Run for (s)", command=lambda: self.entryWindow("Time Delay"))
        editmenu.add_command(
            label="Voltage", command=lambda: self.entryWindow("Voltage"))
        editmenu.add_command(
            label="Amperge", command=lambda: self.entryWindow("Current"))
        editmenu.add_separator()
        editmenu.add_command(
            label="Mode", command=lambda: self.entryWindow("Electronic Load Mode"))
        editmenu.add_command(
            label="Resistance", command=lambda: self.entryWindow("Resistance"))
        editmenu.add_separator()
        editmenu.add_command(label="Output", command=self.setOutput)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

    def setHelpMenu(self):
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(
            label="Help Index", command=lambda: self.gotoURL(self.help_url))
        helpmenu.add_command(label="About...", command=self.about)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

    def donothing(self):
        self.null = None

    def setOutput(self):
        self.device.setOutput(
            messagebox.askyesno(
                title="Output State", message="Turn On Output?"))

    def entryWindow(self, parameter):
        # pop-up window
        self.creatTopWindow(250, 80, parameter)
        

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
        elif (parameter == "Electronic Load Mode"):
            entry_type = "ELM"
        elif (parameter == "Resistance"):
            Label(self.top, text="Input Resistance Value").pack()
            entry_type = "R"

        # window function
        if(entry_type != "ELM"):
            entry_dialog = Entry(self.top)
        else:
            entry_dialog = Spinbox(
                self.top, values=("CCH", "CCL", "CV", "CRM"))

        #
        self.top.bind('<Return>',
                      lambda: self.getEntry(entry_dialog, entry_type))
        entry_dialog.pack(padx=5)
        button_dialog = Button(
            self.top,
            text="OK",
            command=lambda: self.getEntry(entry_dialog, entry_type))
        button_dialog.pack(pady=5)

    def getEntry(self, object, type, event=None):
        entry = object.get()
        print(entry)
        print(type)

        # set entry to variables
        try:
            if (type == "V"):
                self.voltage = float(entry)
                self.updateVoltage(float(entry))
            elif (type == "A"):
                self.amperage = float(entry)
                self.updateAmperage(float(entry))
            elif (type == "O"):
                self.updateOutput(entry)
            elif (type == "R"):
                self.resistance = float(entry)
            self.updatePower(self.voltage, self.amperage)
            entry_failed = False
        except:
            messagebox.showerror("Error", "Not a valid input")
            entry_failed = True

        # set device settings to entry variables
        try:
            if(not entry_failed):
                if (type == "TD"):
                    print()
                elif (type == "V"):
                    self.device.setVoltage(entry)
                    self.device.voltage = entry
                elif (type == "A"):
                    self.device.setAmperage(entry)
                    self.device.amperage = entry
                elif (type == "O"):
                    self.device.setOutput(entry)
                    self.device.output = entry
                elif (type == 'ccsv'):
                    print()
                elif (type == "ELM"):
                    self.device.setMode(entry)
                elif (type == "R"):
                    self.device.setResistance(entry)
            else:
                self.device.name
        except:
            messagebox.showerror("Error", "Device Not Connected")

        # if prompt window open, close it
        try:
            self.top.destroy()
        except:
            pass

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

    def saveFile(self):
        try:
            self.log_file = open(self.save_filename + ".csv", "w")
        except:
            pass
        for i in range(0, self.variable_count):
            self.log_file.writelines("%d, %d, %d, %d" % self.timestamps[i],
                                     self.voltages[i], self.currents[i],
                                     self.outputs[i])

    def save_AS_CSVFile(self):
        self.save_filename = filedialog.asksaveasfilename(
            initialdir="./",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        self.saveFile()

    def closeFile(self):
        try:
            self.save_filename.close()
        except:
            messagebox.ERROR("Save Error", "Error in saving %s" %
                             (self.save_filename))

    def createCSVFile(self):
        self.top = Toplevel(self.bottom)
        Label(self.top, text="Create Run CSV").pack()
        entry_type = "ccsv"
        entry_dialog = Entry(self.top)
        entry_dialog.pack(padx=5)
        button_dialog = Button(
            self.top,
            text="OK",
            command=lambda: self.getEntry(entry_dialog, entry_type))
        button_dialog.pack(pady=5)

    def storeVariabels(self, Timestamp, Voltage, Current, Output):
        self.timestamps.append(Timestamp)
        self.voltages.append(Voltage)
        self.currents.append(Current)
        self.outputs.append(Output)

    def creatTopWindow(self, width, height, title):
        self.top = Toplevel(self.bottom)
        self.setWindowSize(self.top, width, height)
        self.top.title(title)
        self.top.tk.call('wm', 'iconphoto', self.top._w,
                         tkinter.Image("photo", file="CircuitSpecialists.gif"))

    def runSingleLoop(self):
        # pop-up window
        self.creatTopWindow(250, 225, "Single Loop Settings")

        # Display Type of Device
        device_type_label = Label(
            self.top, text="Device Type: %s" % (self.device_type))
        device_type_label.pack(pady=5)

        # Enter Length of Time
        timelength_entry = self.createEntryBar(self.top, "Length in (s): ")

        # Enter usage variable
        if(self.device_type == "powersupply"):
            usage = "Voltage"
        elif(self.device_type == "electronicload"):
            usage = "Mode"
        else:
            usage = "Unknown"
        usage_entry = self.createEntryBar(self.top, usage)

        # Enter Current
        current_entry = self.createEntryBar(self.top, "Current: ")

        # Submit values and run
        time_usage_current = [timelength_entry, usage_entry, current_entry]
        runLoop = Button(
            self.top, text="Run Loop", command=lambda: self.getEntry(time_usage_current, "LR"))
        runLoop.pack(pady=5)

    def createEntryBar(self, window_object, Label_Title):
        Label(window_object, text=Label_Title).pack()
        entry = Entry(window_object)
        entry.pack(pady=5)
        return entry

    def deviceSelection(self):
        try:
            self.device = powersupply.POWERSUPPLY()
            self.device = self.device.powersupply
            self.device_type = "powersupply"
            messagebox.showinfo("Power Supply",
                                "Device Detected: " + self.device.name)
        except:
            try:
                self.device = electronicload.ELECTRONICLOAD()
                self.device = self.device.electronicload
                self.device_type = "electronicload"
                messagebox.showinfo("Electronic Load",
                                    "Device Detected: " + self.device.name)
            except:
                messagebox.showerror(
                    "Error", "Sorry, no devices currently supported are found")

    def gotoURL(self, url):
        webbrowser.open_new_tab(url)

    def about(self):
        messagebox.showinfo(
            "About", "Version %s\n"
            "Operating System: %s" % (self.version, sys.platform))

    def startWindow(self):
        self.bottom.mainloop()

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
        self.device_type = "None"


if __name__ == "__main__":
    gui = GUI()
    gui.startWindow()
