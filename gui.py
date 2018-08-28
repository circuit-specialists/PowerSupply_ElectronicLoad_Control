#!/usr/bin/python
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

# dependent classes
import sys
import webbrowser
import threading
import time

# gui classess
if (sys.version_info.major >= 3):  # python 3
    import tkinter
    from tkinter import Menu, filedialog, Toplevel, Button, messagebox, Entry, Label, Canvas, Spinbox, Frame
else:  # python 2
    import Tkinter as tkinter
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    from Tkinter import Menu, Toplevel, Button, Entry, Label, Canvas, Spinbox, Frame

# Paths to devices and libraries
sys.path.insert(0, './Power Supplies')
sys.path.insert(0, './Electronic Loads')
import powersupply
import electronicload


class GUI:
    def __init__(self):
        # 1337
        # (0|]3
        self.version = "1.4 alpha"
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
        manual_control_frame = Frame(self.bottom)
        manual_control_frame.pack(anchor="c")

        # Voltage Controls
        voltage_frame = Frame(manual_control_frame)
        voltage_frame.pack()
        self.voltage_label = Label(voltage_frame, text="Voltage: ")
        self.voltage_label.pack(side=tkinter.LEFT, padx=5)
        voltage_bar = Spinbox(
            voltage_frame, from_=0, to=32, format="%.2f", increment=0.01)
        voltage_bar.pack(side=tkinter.LEFT)
        Button(
            voltage_frame,
            text="Set Volts",
            command=lambda: self.getEntry(voltage_bar, "V")).pack(
                side=tkinter.LEFT, padx=5)

        # Amperage Controls
        current_frame = Frame(manual_control_frame)
        current_frame.pack()
        self.current_label = Label(current_frame, text="Amperage: ")
        self.current_label.pack(side=tkinter.LEFT)
        current_bar = Spinbox(
            current_frame, from_=0, to=5.2, format="%.3f", increment=0.01)
        current_bar.pack(side=tkinter.LEFT)
        Button(
            current_frame,
            text="Set Amps",
            command=lambda: self.getEntry(current_bar, "A")).pack(
                side=tkinter.LEFT, padx=5)

        # Power Label
        self.power_label = Label(manual_control_frame)
        self.power_label.pack()
        self.updatePower(self.voltage, self.amperage)

        # Output Label
        output_frame = Frame(manual_control_frame)
        output_frame.pack()
        self.output_label = Label(output_frame, text="Output: Off")
        self.output_label.pack(side=tkinter.LEFT)
        Button(
            output_frame, text="On",
            command=lambda: self.updateOutput(1)).pack(side=tkinter.LEFT)
        Button(
            output_frame, text="Off",
            command=lambda: self.updateOutput(0)).pack(
                side=tkinter.LEFT, padx=5)

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

    def addThread(self, function):
        self.threads.append(threading.Thread(target=function))

    def runThreads(self):
        for th in self.threads:
            th.start()

    def quitThreads(self):
        for th in self.threads:
            try:
                th.join()
            except:
                pass

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
        filemenu.add_command(label="Save as...", command=self.save_AS_CSVFile)
        filemenu.add_command(label="Close", command=self.closeFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.bottom.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def setEditMenu(self):
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Find Device", command=self.deviceSelection)
        editmenu.add_separator()
        editmenu.add_command(
            label="Run Single Loop", command=self.promptSingleLoop)
        editmenu.add_separator()
        editmenu.add_command(
            label="Create CSV File", command=self.createCSVFile)
        editmenu.add_separator()
        editmenu.add_command(
            label="Run for (s)",
            command=lambda: self.entryWindow("Time Delay"))
        editmenu.add_command(
            label="Voltage", command=lambda: self.entryWindow("Voltage"))
        editmenu.add_command(
            label="Amperge", command=lambda: self.entryWindow("Current"))
        editmenu.add_separator()
        editmenu.add_command(
            label="Mode",
            command=lambda: self.entryWindow("Electronic Load Mode"))
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
        self.createTopWindow(250, 80, parameter)

        # window parameters
        if (parameter == "Time Delay"):
            Label(self.window_levels[0], text="Input Time Delay").pack()
            entry_type = "TD"
        elif (parameter == "Voltage"):
            Label(self.window_levels[0], text="Input Voltage Value").pack()
            entry_type = "V"
        elif (parameter == "Current"):
            Label(self.window_levels[0], text="Input Current Value").pack()
            entry_type = "A"
        elif (parameter == "Electronic Load Mode"):
            entry_type = "ELM"
        elif (parameter == "Resistance"):
            Label(self.window_levels[0], text="Input Resistance Value").pack()
            entry_type = "R"

        # window function
        if (entry_type != "ELM"):
            entry_dialog = Entry(self.window_levels[0])
        else:
            entry_dialog = Spinbox(
                self.window_levels[0], values=("CCH", "CCL", "CV", "CRM"))

        # Accept <enter> or okay button to get data
        self.window_levels[0].bind(
            '<Return>', lambda: self.getEntry(entry_dialog, entry_type))
        entry_dialog.pack(padx=5)
        Button(
            self.window_levels[0],
            text="OK",
            command=lambda: self.getEntry(entry_dialog, entry_type)).pack(
                pady=5)

    def getEntry(self, object, type, event=None):
        try:
            length = object[0].get()
            voltage = object[1].get()
            current = object[2].get()
            self.window_levels[0].destroy()
        except:
            entry = object.get()

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
            if (not entry_failed):
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
                elif (type == "RSL"):
                    self.runAutoWindow(parameters=[length, voltage, current])
            else:
                self.device.name
        except:
            messagebox.showerror("Error", "Device Not Connected")

        # if prompt window open, close it
        try:
            self.destroyWindowLevel(0)
        except:
            self.destroyWindowLevel(1)

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

        self.runAutoWindow(self.programme_file)

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
            messagebox.ERROR("Save Error",
                             "Error in saving %s" % (self.save_filename))

    def createCSVFile(self):
        self.createTopWindow(400, 400, "Create Run CSV")
        entry_type = "ccsv"
        #fields = self.createEntryBar(parameters_window)

        Button(
            self.window_levels[0],
            text="OK",
            command=lambda: self.getEntry(fields, entry_type)).pack(pady=5)

    def storeVariabels(self, Timestamp, Voltage, Current, Output):
        self.timestamps.append(Timestamp)
        self.voltages.append(Voltage)
        self.currents.append(Current)
        self.outputs.append(Output)

    def createTopWindow(self, width, height, title):
        top = Toplevel(self.bottom)
        self.setWindowSize(top, width, height)
        top.title(title)
        top.protocol("WM_DELETE_WINDOW", lambda: self.destroyWindow(top))
        top.tk.call('wm', 'iconphoto', top._w,
                    tkinter.Image("photo", file="CircuitSpecialists.gif"))
        self.window_levels.append(top)

    def destroyWindow(self, window):
        window.destroy()
        self.window_levels.remove(window)
        self.stop_loop = False

    def destroyWindowLevel(self, level_number):
        try:
            self.window_levels[level_number].destroy()
            self.window_levels.remove(self.window_levels[level_number])
        except:
            pass

    def drawReticules(self, window_object):
        self.canvas_width = int(self.window_width / 2)
        self.canvas_height = int(self.window_height / 2)
        self.canvas = Canvas(
            window_object, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # w.coords(i, new_xy) # change coordinates
        # w.itemconfig(i, fill="blue") # change color
        # (x1,y1,x2,y2)
        graph_x1 = 0
        graph_y1 = 0
        graph_x2 = int(self.canvas_width)
        graph_y2 = int(self.canvas_height)
        self.canvas.create_rectangle(
            graph_x1, graph_y1, graph_x2, graph_y2, fill="#1a1a1a")

        # grid lines (reticules)
        self.horizontal_line_distance = int(self.canvas_width / 10)
        self.vertical_line_distance = int(self.canvas_height / 10)
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
        self.createTopWindow(500, 400, "Running Mode")

        north_frame = Frame(self.window_levels[1])
        north_frame.pack(anchor="n", pady=30, padx=20)
        south_frame = Frame(self.window_levels[1])
        south_frame.pack(anchor="s", pady=30, padx=20)

        parameter_view_frame = Frame(north_frame)
        parameter_view_frame.pack(side=tkinter.LEFT, pady=30, padx=20)
        elapsed_label = Label(parameter_view_frame, text="Elapsed:   0(s)")
        elapsed_label.pack()
        Label(parameter_view_frame, text="Length:   %s(s)" %
              parameters[0]).pack()
        Label(parameter_view_frame, text="Voltage:  %s" % parameters[1]).pack()
        Label(parameter_view_frame, text="Amperage: %s" % parameters[2]).pack()

        reticule_frame = Frame(north_frame)
        reticule_frame.pack(side=tkinter.RIGHT, pady=30, padx=20)
        self.drawReticules(reticule_frame)

        control_frame = Frame(south_frame)
        control_frame.pack()
        start_button = Button(
            control_frame, text="Start", command=lambda: self.runThreadedLoop(parameters, "RSL", elapsed_label))
        start_button.pack(side=tkinter.LEFT, padx=5)
        stop_button = Button(
            control_frame, text="Stop", command=self.stopLoop)
        stop_button.pack(side=tkinter.LEFT)

    def stopLoop(self):
        self.stop_loop = True

    def runThreadedLoop(self, parameters, loop_type, elapsed_label):
        self.addThread(lambda: self.runLoop(parameters, loop_type, elapsed_label))
        self.runThreads()

    def runLoop(self, parameters, loop_type, elapsed_label):
        if(loop_type == "RSL"):
            start_time = time.time()
            self.device.setVoltage(parameters[2])
            self.device.setAmperage(parameters[1])
            self.device.setOutput(1)
            while (time.time() <= start_time + int(parameters[0])):
                elapsed_label.config(text="Elapsed:   %d(s)" %
                                     (time.time() - start_time))
                if(self.stop_loop):
                    break
            self.device.setOutput(0)
            self.threads.pop()
        else:
            # set time between file saves for logging
            if (self.device_type == "electronicload"):
                wait_read_time = 0.0
                last_read_time = time.time()
                wait_write_time = float(self.write_interval)
                last_write_time = time.time()
                start_time = time.time()

            count = 0
            for i in self.file_lines:
                line = self.file_lines[count]
                if (self.device.channels > 1):
                    self.device.setVoltage(line.split(',')[1], i)
                    self.device.setAmperage(line.split(',')[2], i)
                    self.device.setOutput(int(line.split(',')[3]), i)
                else:
                    if (self.device_type == "powersupply"):
                        self.device.setVoltage(line.split(',')[1])
                        self.device.setAmperage(line.split(',')[2])
                        self.device.setOutput(int(line.split(',')[3]))
                        time.sleep(float(line.split(',')[0]))
                        count += 1
                    elif (self.device_type == "electronicload"):
                        if (last_read_time + wait_read_time < time.time()):
                            last_read_time = time.time()
                            self.device.setMode(line.split(',')[1])
                            self.device.setCurrent(line.split(',')[2])
                            self.device.setOutput(int(line.split(',')[3]))
                            wait_read_time = float(line.split(',')[0])
                        if (last_write_time + wait_write_time < time.time()):
                            self.log_file.writelines(
                                str(time.time() - start_time) + "," +
                                str(self.device.getVoltage()[:-1]) + "," +
                                str(self.device.getCurrent()[:-1]) + "," +
                                str(self.device.getPower()[:-1]) + "\n")

    def promptSingleLoop(self):
        # pop-up window
        if (sys.version_info[0] < 3):
            self.createTopWindow(250, 260, "Single Loop Settings")
        else:
            self.createTopWindow(250, 225, "Single Loop Settings")

        # Display Type of Device
        device_type_label = Label(
            self.window_levels[0], text="Device Type: %s" % (self.device_type))
        device_type_label.pack(pady=5)

        # Enter Length of Time
        timelength_entry = self.createEntryBar(self.window_levels[0],
                                               "Length in (s): ")

        # Enter usage variable
        if (self.device_type == "powersupply"):
            usage = "Voltage"
        elif (self.device_type == "electronicload"):
            usage = "Mode"
        else:
            usage = "Unknown"
        usage_entry = self.createEntryBar(self.window_levels[0], usage)

        # Enter Current
        current_entry = self.createEntryBar(self.window_levels[0], "Current: ")

        # Submit values and run
        time_usage_current = [timelength_entry, usage_entry, current_entry]
        runLoopwindow = Button(
            self.window_levels[0],
            text="Run Loop",
            command=lambda: self.getEntry(time_usage_current, "RSL"))
        runLoopwindow.pack(pady=5)

    def createEntryBar(self, window_object, Label_Title):
        Label(window_object, text=Label_Title).pack()
        entry = Entry(window_object)
        entry.pack(pady=5)
        return entry

    def deviceSelection(self):
        if (self.device_type == "None"):
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
                        "Error",
                        "Sorry, no devices currently supported are found")
        else:
            messagebox.showinfo("Power Supply",
                                "Device Detected: " + self.device.name)

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
        self.threads = []
        self.window_levels = []
        self.stop_loop = False


if __name__ == "__main__":
    gui = GUI()
    gui.startWindow()
