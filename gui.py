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
import PowerSupplies as powersupply
import ElectronicLoads as electronicload


class GUI:
    def __init__(self):
        self.version = "beta"
        self.variable_init()
        self.help_url = "https://circuit-specialists.github.io/PowerSupply_ElectronicLoad_Control/"
        self.bottom = tkinter.Tk(className=' cs power control')
        self.bottom.tk.call(
            'wm', 'iconphoto', self.bottom._w,
            tkinter.Image("photo", file="CircuitSpecialists.gif"))
        self.bottom.title('Circuit Specialists Power Control')
        self.setWindowSize(self.bottom, 700, 500)
        self.setMenuBar()
        self.drawManualFrames()

    def drawManualFrames(self):
        self.manual_control_frame = Frame(self.bottom)
        self.manual_control_frame.pack(anchor="c")
        self.parameter_frame = Frame(self.manual_control_frame)
        self.parameter_frame.pack()
        self.current_frame = Frame(self.manual_control_frame)
        self.current_frame.pack()
        self.power_label = Label(self.manual_control_frame)
        self.power_label.pack()
        self.output_frame = Frame(self.manual_control_frame)
        self.output_frame.pack()

    def drawManualControls(self):
        # Top Bar Controls
        if(self.device_type == 'powersupply'):
            self.voltage_label = Label(self.parameter_frame, text="Voltage: ")
            voltage_bar = Spinbox(
                self.parameter_frame, from_=0, to=32, format="%.2f", increment=0.01)
            voltage_button = Button(
                self.parameter_frame,
                text="Set Volts",
                command=lambda: self.getEntry(voltage_bar, "V"))
            if(self.first_pack):
                self.voltage_label.pack(side=tkinter.LEFT, padx=5)
                voltage_bar.pack(side=tkinter.LEFT)
                voltage_button.pack(side=tkinter.LEFT, padx=5)
        elif(self.device_type == 'electronicload'):
            self.mode_label = Label(self.parameter_frame, text="Mode: CCH")
            self.device.setMode('cch')
            if(self.first_pack):
                self.mode_label.pack(side=tkinter.LEFT, padx=5)

        # Amperage Controls
        self.current_label = Label(self.current_frame, text="Amperage: ")
        current_bar = Spinbox(
            self.current_frame, from_=0, to=5.2, format="%.3f", increment=0.01)
        current_button = Button(
            self.current_frame,
            text="Set Amps",
            command=lambda: self.getEntry(current_bar, "A"))
        if(self.first_pack):
            self.current_label.pack(side=tkinter.LEFT)
            current_bar.pack(side=tkinter.LEFT)
            current_button.pack(side=tkinter.LEFT, padx=5)

        # Power Label
        self.updatePower(self.voltage, self.amperage)

        # Output Label
        self.output_label = Label(self.output_frame, text="Output: Off")
        output_on = Button(
            self.output_frame, text="On",
            command=lambda: self.updateOutput(1))
        output_off = Button(self.output_frame, text="Off",
                            command=lambda: self.updateOutput(0))
        if(self.first_pack):
            self.output_label.pack(side=tkinter.LEFT)
            output_on.pack(side=tkinter.LEFT)
            output_off = output_off.pack(side=tkinter.LEFT, padx=5)
        self.first_pack = False

    def updateVoltage(self, voltage):
        self.voltage_label.config(text="Voltage: %.2fV" % (voltage))

    def updateAmperage(self, amperage):
        self.current_label.config(text="Amperage: %.3fA" % (amperage))

    def updatePower(self, voltage, amperage):
        self.power_label.config(text="Power: %.3f Watts" %
                                (voltage * amperage))

    def updateOutput(self, state):
        if(self.device_type == 'electronicload'):
            self.updatePower(float(self.device.getVoltage()),
                             float(self.device.amperage))
        elif(self.device_type == 'powersupply'):
            self.updatePower(self.device.voltage, self.device.amperage)
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
            if(not th.is_alive()):
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
        filemenu.add_command(label="Save", command=self.save_CSVFile)
        filemenu.add_command(label="Save as...", command=self.save_AS_CSVFile)
        filemenu.add_command(
            label="Close", command=lambda: self.closeFile(self.save_file))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.bottom.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def setEditMenu(self):
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Find Device", command=self.deviceSelection)
        editmenu.add_command(label="Select Device", command=self.manualDeviceSelect)
        editmenu.add_separator()
        editmenu.add_command(
            label="Run Single Loop", command=self.promptSingleLoop)
        editmenu.add_command(
            label="Create CSV File", command=self.createCSVFile)
        editmenu.add_command(
            label="Reset Current Log", command=self.resetLog)
        editmenu.add_separator()
        editmenu.add_command(
            label="Mode",
            command=lambda: self.entryWindow("Electronic Load Mode"))
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
        entry_dialog.pack(padx=5)

        # Accept <enter> or okay button to get data
        self.window_levels[0].bind(
            '<Return>', lambda: self.getEntry(entry_dialog, entry_type))
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
                    if(self.device_type == 'powersupply'):
                        self.device.setVoltage(entry)
                    elif(self.device_type == 'electronicload'):
                        messagebox.showerror(
                            "User Error", "Voltage setting is not for Loads")
                    self.device.voltage = entry
                elif (type == "A"):
                    if(self.device_type == 'powersupply'):
                        self.device.setAmperage(entry)
                    elif(self.device_type == 'electronicload'):
                        self.device.setCurrent(entry)
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
                    self.runAutoWindow(type, parameters=[
                                       length, voltage, current])
            else:
                self.device.name
        except:
            messagebox.showerror("Error", "Device Not Connected")

        # if prompt window open, close it
        try:
            self.destroyWindowLevel(0)
        except:
            self.destroyWindowLevel(1)

    def convertFileToList(self, csv_file):
        self.total_time = 0
        for line in csv_file:
            self.total_time += float(line.split(',')[0])
            self.storeVariables(float(line.split(',')[0]),
                                line.split(',')[1],
                                line.split(',')[2],
                                line.split(',')[3])

    def openCSVFile(self):
        self.programme_filename = filedialog.askopenfilename(
            initialdir="./",
            title="Open file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        try:
            with open(self.programme_filename, "r") as f:
                self.programme_file = f.readlines()
        except:
            messagebox.showerror("Error", "Unable to open file")

        if(self.device_type == "None"):
            self.deviceSelection()
        self.runAutoWindow("CSVL", self.programme_file[1:])

    def saveFile(self, log_file):
        log_file.writelines("Timestamp, Voltage, Current, Output\n")
        for i in range(0, self.variable_count):
            log_file.writelines("%s, %s, %s, %s\n" % (
                self.timestamps[i], self.voltages[i], self.currents[i], self.outputs[i]))
        self.variable_count = 0
        self.closeFile(log_file)

    def save_AS_CSVFile(self):
        self.save_file = filedialog.asksaveasfile(
            initialdir="./", title="Save file", mode='w', defaultextension=".csv")
        if(self.save_file):
            self.saveFile(self.save_file)

    def save_CSVFile(self):
        try:
            self.saveFile(self.save_file)
        except:
            self.save_file = open("logfile.csv", "w")
            self.saveFile(self.save_file)

    def closeFile(self, log_file):
        try:
            log_file.close()
        except:
            messagebox.ERROR("Save Error",
                             "Error in saving %s" % (log_file))

    def createCSVFile(self):
        self.createTopWindow(400, 400, "Create Run CSV")
        entry_type = "ccsv"
        fields = self.createEntryBar(self.window_levels[0])

        Button(
            self.window_levels[0],
            text="OK",
            command=lambda: self.getEntry(fields, entry_type)).pack(pady=5)

    def storeVariables(self, Timestamp, Voltage, Current, Output):
        self.timestamps.append(Timestamp)
        self.voltages.append(Voltage)
        self.currents.append(Current)
        self.outputs.append(Output)
        self.variable_count += 1

    def resetLog(self):
        del self.timestamps[:]
        del self.voltages[:]
        del self.currents[:]
        del self.outputs[:]

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

    def updateReticules(self, start_point, max_x, max_y, parameter, time, color):
        line_width = 2
        x_scale = float(self.canvas_width / max_x)
        y_scale = float(self.canvas_height / max_y)
        end_point = [int(float(time) * x_scale),
                     int(float(parameter) * y_scale)]
        # x0, y0, x1, y1
        # draw measured value
        self.canvas.create_line(start_point[0], self.getRealY(start_point[1], line_width),
                                end_point[0], self.getRealY(end_point[1], line_width), fill=color, width=line_width)
        return end_point

    def getRealY(self, y_point, line_width):
        if(y_point < 2):
            return self.canvas_height - y_point
        else:
            return self.canvas_height - y_point + line_width

    def runAutoWindow(self, loop_type, parameters):
        # pop-up window
        self.createTopWindow(500, 400, "Running Mode")

        top_window = len(self.window_levels) - 1
        north_frame = Frame(self.window_levels[top_window])
        north_frame.pack(anchor="n", pady=30, padx=20)
        south_frame = Frame(self.window_levels[top_window])
        south_frame.pack(anchor="s", pady=30, padx=20)

        parameter_view_frame = Frame(north_frame)
        parameter_view_frame.pack(side=tkinter.LEFT, pady=30, padx=20)
        elapsed_label = Label(parameter_view_frame, text="Elapsed:   0(s)")
        elapsed_label.pack()
        length_label = Label(parameter_view_frame, text="Length:   0(s)")
        length_label.pack()
        voltage_label = Label(parameter_view_frame, text="Voltage:  0(V)")
        voltage_label.pack()
        amperage_label = Label(parameter_view_frame, text="Amperage: 0(A)")
        amperage_label.pack()

        reticule_frame = Frame(north_frame)
        reticule_frame.pack(side=tkinter.RIGHT, pady=30, padx=20)
        self.drawReticules(reticule_frame)

        control_frame = Frame(south_frame)
        control_frame.pack()
        start_button = Button(
            control_frame, text="Start", command=lambda: self.runThreadedLoop(loop_type, parameters, labels=[elapsed_label, length_label, voltage_label, amperage_label]))
        start_button.pack(side=tkinter.LEFT, padx=5)
        stop_button = Button(
            control_frame, text="Stop", command=self.stopLoop)
        stop_button.pack(side=tkinter.LEFT)
        save_button = Button(
            control_frame, text="Save", command=self.save_AS_CSVFile)
        save_button.pack(side=tkinter.LEFT, padx=5)

    def stopLoop(self):
        self.stop_loop = True

    def runThreadedLoop(self, loop_type, parameters, labels):
        self.addThread(lambda: self.runLoop(
            loop_type, parameters, labels))
        self.runThreads()
        self.stop_loop = False

    def runLoop(self, loop_type, parameters, labels):
        start_time = time.time()
        voltage_start_point = [0, 0]
        amperage_start_point = [0, 0]
        wait_time = 0.0
        max_voltage_y = 0.0
        max_amperage_y = 0.0

        if(loop_type == "RSL"):
            max_x = float(parameters[0])
            max_amperage_y = float(parameters[2])
            labels[3].config(text="Current:   %s(A)" % parameters[2])
            labels[1].config(text="Length:   %s(s)" % max_x)
            if(self.device_type == 'powersupply'):
                self.device.setVoltage(parameters[1])
                self.device.setAmperage(parameters[2])
                max_voltage_y = float(parameters[1])
                labels[2].config(text="Voltage:   %s(V)" % parameters[1])
            elif(self.device_type == 'electronicload'):
                max_voltage_y = float(self.device.getVoltage())
                self.device.setMode(parameters[1])
                labels[2].config(text="Mode:   %s" % parameters[1])
                self.device.setCurrent(parameters[2])
            self.device.setOutput(1)
        elif(loop_type == "CSVL"):
            last_read_time = start_time
            max_x = 0
            line_count = 0
            timestamps = []
            if(self.device_type == 'powersupply'):
                voltages = []
            elif(self.device_type == 'electronicload'):
                modes = []
            amperages = []
            outputs = []
            for line in self.programme_file[1:]:
                max_x += float(line.split(',')[0])
                timestamps.append(line.split(',')[0])
                amperages.append(line.split(',')[2])
                outputs.append(line.split(',')[3])
                if(self.device_type == 'powersupply'):
                    voltages.append(line.split(',')[1])
                    if(float(line.split(',')[1]) > max_voltage_y):
                        max_voltage_y = float(line.split(',')[1])
                elif(self.device_type == 'electronicload'):
                    modes.append(str(line.split(',')[1]))
                    max_voltage_y = float(self.device.getVoltage())
                    if(max_voltage_y < 1):
                        max_voltage_y = 1
                if(float(line.split(',')[2]) > max_amperage_y):
                    max_amperage_y = float(line.split(',')[2])
            labels[1].config(text="Length:   %s(s)" % max_x)
            if(self.device_type == 'electronicload'):
                self.device.setMode(modes[0])

        while (time.time() <= start_time + max_x):
            # update time ticker
            labels[0].config(text="Elapsed:   %d(s)" %
                             (time.time() - start_time))

            # get measured values
            if(self.device_type == "powersupply" and self.device.name != "CSI305DB"):
                type_parameter = self.device.measureVoltage()
                amperage = self.device.measureAmperage()
                voltage = type_parameter
            elif(self.device_type == "electronicload" and self.device.name != "CSI305DB"):
                type_parameter = self.device.mode
                amperage = self.device.getCurrent()
                voltage = self.device.getVoltage()

            if(loop_type == "CSVL" and time.time() >= last_read_time + wait_time):
                last_read_time = time.time()
                wait_time = float(timestamps[line_count])
                if (self.device_type == "powersupply"):
                    self.device.setVoltage(voltages[line_count])
                    self.device.setAmperage(amperages[line_count])
                    labels[2].config(text="Voltage:   %s(V)" %
                                     voltages[line_count])
                elif (self.device_type == "electronicload"):
                    self.device.setMode(modes[line_count])
                    self.device.setCurrent(amperages[line_count])
                    labels[2].config(text="Mode:   %s" %
                                     modes[line_count])

                self.device.setOutput(int(outputs[line_count]))
                labels[3].config(text="Current:   %s(A)" %
                                 amperages[line_count])
                line_count += 1

            if(self.device.name != "CSI305DB"):
                # graph measured values
                voltage_start_point = self.updateReticules(
                    voltage_start_point, max_x, max_voltage_y, voltage, time.time() - start_time, "#FF0000")
                amperage_start_point = self.updateReticules(
                    amperage_start_point, max_x, max_amperage_y, amperage, time.time() - start_time, "#FFFF00")

                # store values
                self.storeVariables(time.time() - start_time,
                                    type_parameter, amperage, self.device.output)

            if(self.stop_loop):
                break

        self.device.setOutput(0)
        self.threads.pop()

    def promptSingleLoop(self):
        if(self.device_type == "None"):
            self.deviceSelection()

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
        timelength_entry.focus_set()

        # Enter usage variable
        if (self.device_type == "powersupply"):
            usage_entry = self.createEntryBar(self.window_levels[0], "Voltage")
        elif (self.device_type == "electronicload"):
            usage_entry = self.createSpinBox(self.window_levels[0], "Mode")
        else:
            usage_entry = self.createEntryBar(self.window_levels[0], "Unknown")

        # Enter Current
        current_entry = self.createEntryBar(self.window_levels[0], "Current: ")

        # Submit values and run
        time_usage_current = [timelength_entry, usage_entry, current_entry]
        runLoopwindow = Button(
            self.window_levels[0],
            text="Run Loop",
            command=lambda: self.getEntry(time_usage_current, "RSL"))
        runLoopwindow.pack(pady=5)

    def createSpinBox(self, window_object, Label_Title):
        Label(window_object, text=Label_Title).pack()
        entry = Spinbox(window_object, values=("CCH", "CCL", "CV", "CRM"))
        entry.pack(pady=5)
        return entry

    def createEntryBar(self, window_object, Label_Title):
        Label(window_object, text=Label_Title).pack()
        entry = Entry(window_object)
        entry.pack(pady=5)
        return entry

    def deviceSelection(self):
        if(self.device_type != "None"):
            self.device.quit()

        try:
            self.device = electronicload.ELECTRONICLOAD()
            self.device = self.device.electronicload
            self.device_type = "electronicload"
            messagebox.showinfo("Electronic Load",
                                "Device Detected: %s" % self.device.name)
        except:
            try:
                self.device = powersupply.POWERSUPPLY()
                self.device = self.device.powersupply
                self.device_type = "powersupply"
                messagebox.showinfo("Power Supply",
                                    "Device Detected: %s" % self.device.name)
                if (self.device.name == "CSI305DB"):
                    self.addThread(self.device.control)

            except:
                messagebox.showerror(
                    "Error",
                    "Sorry, no devices were automatically found")

        self.runThreads()
        self.drawManualControls()

    def setDevice(self, device_name):
        self.device_type = "powersupply"
        self.device = powersupply.POWERSUPPLY(device_name.upper())
        self.destroyWindowLevel(0)

        self.runThreads()
        self.drawManualControls()

    def manualDeviceSelect(self):
        self.createTopWindow(250, 146, "Manual Device Select")
        top_window = len(self.window_levels) - 1
        north_frame = Frame(self.window_levels[top_window])
        north_frame.pack(anchor="n", pady=5, padx=10)
        south_frame = Frame(self.window_levels[top_window])
        south_frame.pack(anchor="s", pady=5, padx=10)


        label = Label(north_frame, text="Device Select")
        label.pack(pady=5)
        entry = Spinbox(north_frame, values=("CSI305DB", "CSI3645A"))
        entry.pack(pady=5)

        control_frame = Frame(south_frame)
        control_frame.pack()

        select = Button(
            control_frame,
            text="Select",
            command=lambda: self.setDevice(entry))
        select.pack(side=tkinter.LEFT, pady=5, padx=15)

        cancel = Button(
            control_frame,
            text="Cancel",
            command=lambda: self.destroyWindowLevel(top_window))
        cancel.pack(side=tkinter.LEFT, pady=5)

    def gotoURL(self, url):
        webbrowser.open_new_tab(url)

    def about(self):
        messagebox.showinfo(
            "About", "Version %s\n"
            "Operating System: %s" % (self.version, sys.platform))

    def startWindow(self):
        self.bottom.mainloop()
        try:
            self.device.run = False
        except:
            pass

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
        self.stop_loop = False
        self.first_pack = True


if __name__ == "__main__":
    gui = GUI()
    gui.startWindow()
