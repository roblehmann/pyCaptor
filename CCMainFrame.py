# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sat Oct 12 14:20:36 2013
#

from CCDataFrame import CCDataFrame
from collections import deque
from datetime import datetime
from DynLightPlotFrame import DynLightPlotFrame
import os
import serial
from serial.tools import list_ports
import sys
import threading
import wx
# begin wxGlade: dependencies
from captorControlNotebook import captorControlNotebook
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

#----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more elegant.

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

#----------------------------------------------------------------------
ID_SETTINGS     = wx.NewId()
ID_EXIT         = wx.NewId()

msgSep = ","
msgTerm = "#"

DEBUG = True
# names of values obtained from the reactor
VARIABLE_NAMES = ["OD850nm_s1","OD740nm_s1","ODred_s1","ODgreen_s1","ODblue_s1",
    "OD850nm_s2","OD740nm_s2","ODred_s2","ODgreen_s2","ODblue_s2",
    "Brightness","Temperature"]
# max. number of samples to show in plot
BUFFER_SIZE = 1000

class CCMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.serial     = serial.Serial()
        self.serial.timeout = 0.5   #make sure that the alive event can be checked from time to time
        self.thread     = None
        self.alive      = threading.Event()
        self.dataFrame = CCDataFrame(None, wx.ID_ANY, "")
        self.dataFrame.mainFrame = self
        self.dataFrame.Show()
        # reactor data
        self.referenceVals1 = [5,5,5,5,5]  # reference values from detector 1
        self.referenceVals2 = [5,5,5,5,5]  # reference values from detector 2 
        self.odVals1    = [0,0,0,0,0] # od values from detector 1
        self.odVals2    = [0,0,0,0,0] # od values from detector 2
        self.bgVals     = [0,0] # background values for both detectors
        self.temp       = 0 # sample temperature
        self.lightBrightness = 0
        self.reactorMode    = 1
        self.minLight       = 0
        self.maxLight       = 255
        self.sampleRate     = 10
        self.sampleTime     = 0
        # dynamic light program definition
        self.dynLight = None
        # frame showing a plot of the profile
        self.dynLightPlotFrame = None
        # frame showing real time plot of OD curve
        self.odCurveFrame = None
        self.dataStore    = DataStore(BUFFER_SIZE,VARIABLE_NAMES)
        
        # begin wxGlade: CCMainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_main = wx.Notebook(self, wx.ID_ANY, style=0)
        self.notebook_1_pane_1 = captorControlNotebook(self.notebook_main, wx.ID_ANY)
        self.notebook_reactor_connection = wx.Panel(self.notebook_main, wx.ID_ANY)
        self.label_1_copy = wx.StaticText(self.notebook_reactor_connection, wx.ID_ANY, _("Captor Control"))
        self.label_9 = wx.StaticText(self.notebook_reactor_connection, wx.ID_ANY, _("Reactor Connection Configuration"))
        self.label_10 = wx.StaticText(self.notebook_reactor_connection, wx.ID_ANY, _("Select Connection"))
        self.serial_connection_combo_box = wx.ComboBox(self.notebook_reactor_connection, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.button_connect_serial = wx.Button(self.notebook_reactor_connection, wx.ID_ANY, _("Connect"))
        self.button_refresh_serial_copy = wx.Button(self.notebook_reactor_connection, wx.ID_ANY, _("Refresh"))
        self.notebook_logging = wx.Panel(self.notebook_main, wx.ID_ANY)
        self.label_1_copy_copy = wx.StaticText(self.notebook_logging, wx.ID_ANY, _("Captor Control"))
        self.label_11 = wx.StaticText(self.notebook_logging, wx.ID_ANY, _("Data Logging Configuration"))
        self.button_select_logfile = wx.Button(self.notebook_logging, wx.ID_ANY, _("Select Logfile"))
        self.label_active_log_file = wx.StaticText(self.notebook_logging, wx.ID_ANY, _("./log.txt"))
        self.notebook_reference_values = wx.Panel(self.notebook_main, wx.ID_ANY)
        self.label_1_copy_copy_copy = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("Captor Control"))
        self.label_12 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("Reference Value Measurement"))
        self.button_measure_refs = wx.Button(self.notebook_reference_values, wx.ID_ANY, _("Measure Reference Vals"))
        self.label_13 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD 850nm (1)"))
        self.label_od850_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_4 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD 850nm (2)"))
        self.label_od850_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD 740nm (1)"))
        self.label_od740_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_5 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD 740nm (2)"))
        self.label_od740_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Red (1)"))
        self.label_odRed_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_6 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Red (2)"))
        self.label_odRed_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Green (1)"))
        self.label_odGreen_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_7 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Green (2)"))
        self.label_odGreen_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_3 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Blue (1)"))
        self.label_odBlue_1 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.label_13_copy_8 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("OD Blue (2)"))
        self.label_odBlue_2 = wx.StaticText(self.notebook_reference_values, wx.ID_ANY, _("-"))
        self.notebook_dyn_light = wx.Panel(self.notebook_main, wx.ID_ANY)
        self.label_dynLightTitle = wx.StaticText(self.notebook_dyn_light, wx.ID_ANY, _("Captor Control"))
        self.label_14 = wx.StaticText(self.notebook_dyn_light, wx.ID_ANY, _("Dynamic Light Program"))
        self.label_5 = wx.StaticText(self.notebook_dyn_light, wx.ID_ANY, _("File Loaded:"))
        self.dyn_light_filepath_label = wx.StaticText(self.notebook_dyn_light, wx.ID_ANY, _("-"))
        self.button_ld_dynlght_copy_copy = wx.Button(self.notebook_dyn_light, wx.ID_ANY, _("Load File"))
        self.button_plotDynLight_copy_copy = wx.Button(self.notebook_dyn_light, wx.ID_ANY, _("Show Profile"))
        self.button_uld_dynlght_copy_copy = wx.Button(self.notebook_dyn_light, wx.ID_ANY, _("Upload to Reactor"))
        self.button_dld_dynlght_copy_copy = wx.Button(self.notebook_dyn_light, wx.ID_ANY, _("Download From Reactor"))
        self.notebook_remote_control = wx.Panel(self.notebook_main, wx.ID_ANY)
        self.label_1_copy_copy_copy_copy_2 = wx.StaticText(self.notebook_remote_control, wx.ID_ANY, _("Captor Control"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOpenConnectReactorButton, self.button_connect_serial)
        self.Bind(wx.EVT_BUTTON, self.OnOpenRefreshReactorListButton, self.button_refresh_serial_copy)
        self.Bind(wx.EVT_BUTTON, self.OnOpenLogfileDialogButton, self.button_select_logfile)
        self.Bind(wx.EVT_BUTTON, self.OnOpenMeasureRefValsButton, self.button_measure_refs)
        self.Bind(wx.EVT_BUTTON, self.OnOpenDynLightFileDialogButton, self.button_ld_dynlght_copy_copy)
        self.Bind(wx.EVT_BUTTON, self.OnShowDynLightClicked, self.button_plotDynLight_copy_copy)
        self.Bind(wx.EVT_BUTTON, self.OnOpenUploadDynLightButton, self.button_uld_dynlght_copy_copy)
        self.Bind(wx.EVT_BUTTON, self.OnOpenDownloadDynLightButton, self.button_dld_dynlght_copy_copy)
        # end wxGlade
        self.__attach_events()          # register events
        self.list_connections()         # fill list with all serial connections
        self.serial_connection_combo_box.SetSelection(self.serial_connection_combo_box.GetCount()-1)# select last connection by default
        

    def __set_properties(self):
        # begin wxGlade: CCMainFrame.__set_properties
        self.SetTitle(_("Captor Control"))
        self.SetSize((730, 500))
        self.label_1_copy.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.label_9.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.serial_connection_combo_box.SetMinSize((250, -1))
        self.button_connect_serial.SetMinSize((94, 20))
        self.label_1_copy_copy.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.label_11.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.label_1_copy_copy_copy.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.button_measure_refs.SetMinSize((200, 20))
        self.label_dynLightTitle.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.label_14.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.dyn_light_filepath_label.SetMinSize((250, -1))
        self.label_1_copy_copy_copy_copy_2.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CCMainFrame.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_rc_main = wx.BoxSizer(wx.VERTICAL)
        sizer_dyn_light_main = wx.BoxSizer(wx.VERTICAL)
        sizer_22 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_4_copy = wx.GridSizer(2, 2, 0, 0)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_refVals_main = wx.BoxSizer(wx.VERTICAL)
        sizer_21 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.GridSizer(5, 4, 0, 0)
        sizer_logging_main = wx.BoxSizer(wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_connection_main = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_connection_main.Add(self.label_1_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_15.Add(self.label_9, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_17.Add(self.label_10, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_17.Add(self.serial_connection_combo_box, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_16.Add(sizer_17, 1, 0, 0)
        sizer_18.Add(self.button_connect_serial, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_18.Add(self.button_refresh_serial_copy, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_16.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_15.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_connection_main.Add(sizer_15, 1, wx.EXPAND, 0)
        self.notebook_reactor_connection.SetSizer(sizer_connection_main)
        sizer_logging_main.Add(self.label_1_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_19.Add(self.label_11, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_20.Add(self.button_select_logfile, 0, wx.ALL, 10)
        sizer_20.Add(self.label_active_log_file, 0, wx.ALL, 10)
        sizer_19.Add(sizer_20, 1, wx.EXPAND, 0)
        sizer_logging_main.Add(sizer_19, 1, wx.EXPAND, 0)
        self.notebook_logging.SetSizer(sizer_logging_main)
        sizer_refVals_main.Add(self.label_1_copy_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_21.Add(self.label_12, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_21.Add(self.button_measure_refs, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        grid_sizer_2.Add(self.label_13, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_od850_1, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_4, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_od850_2, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_od740_1, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_5, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_od740_2, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_1, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odRed_1, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_6, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odRed_2, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_2, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odGreen_1, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_7, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odGreen_2, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_3, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odBlue_1, 0, 0, 0)
        grid_sizer_2.Add(self.label_13_copy_8, 0, wx.ALL, 10)
        grid_sizer_2.Add(self.label_odBlue_2, 0, 0, 0)
        sizer_21.Add(grid_sizer_2, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_refVals_main.Add(sizer_21, 1, wx.EXPAND, 0)
        self.notebook_reference_values.SetSizer(sizer_refVals_main)
        sizer_dyn_light_main.Add(self.label_dynLightTitle, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_22.Add(self.label_14, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_5.Add(self.label_5, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer_5.Add(self.dyn_light_filepath_label, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer_22.Add(sizer_5, 1, 0, 0)
        grid_sizer_4_copy.Add(self.button_ld_dynlght_copy_copy, 0, wx.ALL, 10)
        grid_sizer_4_copy.Add(self.button_plotDynLight_copy_copy, 0, wx.ALL, 10)
        grid_sizer_4_copy.Add(self.button_uld_dynlght_copy_copy, 0, wx.ALL, 10)
        grid_sizer_4_copy.Add(self.button_dld_dynlght_copy_copy, 0, wx.ALL, 10)
        sizer_6.Add(grid_sizer_4_copy, 1, 0, 0)
        sizer_22.Add(sizer_6, 1, 0, 0)
        sizer_dyn_light_main.Add(sizer_22, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.notebook_dyn_light.SetSizer(sizer_dyn_light_main)
        sizer_rc_main.Add(self.label_1_copy_copy_copy_copy_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.notebook_remote_control.SetSizer(sizer_rc_main)
        self.notebook_main.AddPage(self.notebook_1_pane_1, _("Main"))
        self.notebook_main.AddPage(self.notebook_reactor_connection, _("Reactor Connection"))
        self.notebook_main.AddPage(self.notebook_logging, _("Logging"))
        self.notebook_main.AddPage(self.notebook_reference_values, _("Reference Values"))
        self.notebook_main.AddPage(self.notebook_dyn_light, _("Dynamic Light Mode"))
        self.notebook_main.AddPage(self.notebook_remote_control, _("Remote Control"))
        sizer_main.Add(self.notebook_main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        # end wxGlade

    def StartThread(self):
        """Start the receiver thread"""        
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def StopThread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.alive.clear()          #clear alive event for thread
            self.thread.join()          #wait until thread has finished
            self.thread = None
            
    def __attach_events(self):
        #register events at the controls
        self.Bind(wx.EVT_MENU, self.OnExit, id = ID_EXIT)
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnExit(self, event):
        """Menu point Exit"""
        self.Close()

    def OnClose(self, event):
        """Called on application shutdown."""
        self.StopThread()               #stop reader thread
        self.serial.close()             #cleanup
        if not self.dataFrame == None:  #close windows, exit app
            self.dataFrame.Destroy()
        if not self.dynLightPlotFrame == None:
            self.dynLightPlotFrame.Destroy()
        if not self.odCurveFrame == None:
            self.odCurveFrame.Destroy()
        self.Destroy()
        sys.exit(0)
        
    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        text = event.data
        if DEBUG:
            print "received reactor message: " + text
        vals = text.split(",")
        # reference values
        if vals[0] == "REF": 
            self.digestReferenceValues(vals[1:])
        elif vals[0] == "MD": 
            self.digestReactorModeValues(vals[1:])
        elif vals[0] == "DATA": # sample data
            self.digestSampleValues(vals[1:])
        else:
            print "Unknown Reactor Message " + vals[0] + "!"
            if DEBUG:
                print text
                    
    def ComPortThread(self):
        """Thread that handles the incomming traffic. Reads an entire line
         and generates an SerialRxEvent, which is processed in the main thread
         """
        while self.alive.isSet():               #loop while alive event is true
            text = self.serial.readline()          #read one, with timout
            if text:                            #check if not timeout
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event)

    def OnOpenConnectReactorButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """(dis)-connect current serial connection, depending on whether a current
        connection exists"""
        if(self.serial.isOpen()):
            if DEBUG:
                print "currently connected to serial: " + self.serial.port + ". Disconnecting... "
            self.StopThread()               #stop reader thread
            self.serial.close()             #disconnect serial
            self.button_connect_serial.SetLabel("Connect") # set button to connect
            return
        else:
            try:
                self.serial.port = self.serial_connection_combo_box.GetValue()
                self.serial.baudrate = 9600
                self.serial.open()
            except serial.SerialException, e:
                dlg = wx.MessageDialog(None, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                if DEBUG:
                    print "connected to serial: " + self.serial.port
                self.StartThread()
                self.button_connect_serial.SetLabel("Disconnect") # set button to disconnect

    def OnOpenRefreshReactorListButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """refresh the list of available serial connections, as shown in the interface"""
        self.list_connections()

    def OnOpenLogfileDialogButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """select log file to store data in"""
        dirname = ""
        dlg = wx.FileDialog(self, "Choose a Log File", dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            f = os.path.join(dirname, filename)
        dlg.Destroy()
        if f:
            self.label_active_log_file.SetLabel(f)
        else:
            self.label_active_log_file.SetLabel("./log.txt")
            
    def OnOpenMeasureRefValsButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """send reactor message to aquire reference values"""
        self.sendMessage("mre","")

    def OnOpenDynLightFileDialogButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """load dynamic light program from csv file"""
        # select file to read
        dirname = ''
        dlg = wx.FileDialog(self, "Choose dynamic light definition file", dirname, "", "CSV files (*.txt;*.csv)|*.txt;*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            fp = os.path.join(dirname, filename)
        dlg.Destroy()
        # abort if no file selected
        if not fp:
            return
        
        with open(fp, 'r') as f:
            content = f.readlines()
        
        self.dynLight = []
        for l in content:
            if not l.startswith("#"):
                item = [long(x) for x in l.split(",")]
                if not (item[0] < 0 or item[1] < 0):
                    self.dynLight.append(item)
        if DEBUG:
            print "Parsed dynamic light program from " + fp + " (rows " + str(len(self.dynLight)) + ")..."
        self.dyn_light_filepath_label.SetLabel(fp)
        
    def OnOpenUploadDynLightButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """sends the dynamic light program to the reactor"""
        if self.dynLight == None:
            print "No dynamic light program loaded!"
            return
        
        for i,item in enumerate(self.dynLight):
            self.sendMessage("bp",str(i) + msgSep + str(item[0]) + msgSep + str(item[1]) + msgSep)

    def OnOpenDownloadDynLightButton(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """sends command to reactor to answer with current dynamic light program.
        """
        # TODO: implement parsing the reactor reply
        self.sendMessage("sbp","")

    def OnShowDynLightClicked(self, event):  # wxGlade: CCMainFrame.<event_handler>
        """plot loaded dynamic light profile"""
        self.dynLightPlotFrame = DynLightPlotFrame(self, wx.ID_ANY, "")
        self.dynLightPlotFrame.dynLight = self.dynLight
        self.dynLightPlotFrame.draw()
        self.dynLightPlotFrame.Show()

    def digestReferenceValues(self, values):
        """parses OD reference values sent from reactor, updates gui"""
        # store ref data 
        for i in range(0,5):
            if DEBUG:
                print "parsing values" + values[i] + " and " + values[i+5] 
            self.referenceVals1[i] = float(values[i])
            self.referenceVals2[i] = float(values[(i+5)])
        self.updateReactorData()

    def digestReactorModeValues(self, values):
        """parses mode change sent from reactor, updates gui"""
        newMode = int(values[0])
        if DEBUG:
            print "detected reactor mode change to:" + str(newMode)
        self.notebook_1_pane_1.mode_radio_box.SetSelection(newMode)

    def digestSampleValues(self, values):
        """parses sample values sent from reactor, updates gui and writes to log file"""
        if DEBUG:
            print "parsing sample data"
        # od values
        for i in range(0,5):
            self.odVals1[i] = float(values[i])
            self.odVals2[i] = float(values[(i+5)])

        # background values for both detectors
        self.bgVals[0]     = float(values[10])
        self.bgVals[1]     = float(values[11])
        # sample temperature
        self.temp          = float(values[12])
        self.lightBrightness = int(values[13])
        self.reactorMode   = int(values[14])
        self.minLight      = int(values[15])
        self.maxLight      = int(values[16])
        self.sampleRate    = int(values[17])
        self.sampleTime    = datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
        # show in gui
        self.updateReactorData()
        # write to log file
        self.logData()
        # add data to datastore
        dt = self.odVals1 + self.odVals2 + [self.lightBrightness, self.temp]
        self.dataStore.addSample(dt, VARIABLE_NAMES)
        # if activated, refresh OD curve plot
        if not self.odCurveFrame == None:
            self.odCurveFrame.draw_plot()

    def logData(self):
        """write sample to log file"""
        ls = self.assmebleLogString()
        with open(self.label_active_log_file.GetLabel(), 'a') as f:
            f.write(ls)

    def assmebleLogString(self):
        """combines last sample values into a log string"""
        ls = ""
        ls2 = ""
        for i in range(0,5):
            ls +=   str(self.odVals1[i])    + msgSep
            ls2 +=  str(self.odVals2[i])    + msgSep
        ls = str(self.sampleTime) + msgSep + ls + ls2
        ls = ls + str(self.temp) + msgSep + str(self.lightBrightness) + msgSep + str(self.reactorMode) + "\n"
        return ls

    def updateReactorData(self):
        """updates gui with current sample data"""
        # show data in gui
        self.label_od850_1.SetLabel(str(self.referenceVals1[0]))
        self.label_od850_2.SetLabel(str(self.referenceVals2[0]))
        self.label_od740_1.SetLabel(str(self.referenceVals1[1]))
        self.label_od740_2.SetLabel(str(self.referenceVals2[1]))
        self.label_odRed_1.SetLabel(str(self.referenceVals1[2]))
        self.label_odRed_2.SetLabel(str(self.referenceVals2[2]))
        self.label_odGreen_1.SetLabel(str(self.referenceVals1[3]))
        self.label_odGreen_2.SetLabel(str(self.referenceVals2[3]))
        self.label_odBlue_1.SetLabel(str(self.referenceVals1[4]))
        self.label_odBlue_2.SetLabel(str(self.referenceVals2[4]))

        self.dataFrame.od_850_label.SetLabel(str(self.odVals2[0]))
        self.dataFrame.od_740_label.SetLabel(str(self.odVals2[1]))
        self.dataFrame.od_red_label.SetLabel(str(self.odVals1[2]))
        self.dataFrame.od_green_label.SetLabel(str(self.odVals1[3]))
        self.dataFrame.od_blue_label.SetLabel(str(self.odVals1[4]))

        # background values for detector 1
        self.dataFrame.background_od_label.SetLabel(str(self.bgVals[0]))
        # self.bgVals[1] # detector 2
        # sample temperature
        self.dataFrame.temp_label.SetLabel(str(self.temp))
        # brightness
        self.dataFrame.bgt_label.SetLabel(str(self.lightBrightness)) 
        # sample temperature
        self.dataFrame.time_label.SetLabel(str(self.sampleTime))

        self.notebook_1_pane_1.text_ctrl_min_led_bght.SetValue(str(self.minLight))
        self.notebook_1_pane_1.text_ctrl_max_led_bght.SetValue(str(self.maxLight))
        self.notebook_1_pane_1.text_ctrl_sampling_rate.SetValue(str(self.sampleRate))

        
    def sendMessage(self, param, value):
        """commits message to the reactor, first the parameter name then the value(s)"""
        if(not self.serial.isOpen()):
            if DEBUG:
                print "Not connected!"
            return
        msg = param + msgSep + value + msgTerm
        self.serial.write(msg)
        if DEBUG:
            print "sending message: " + msg

    def list_connections(self):
        """provides combo box with list of available serial connections"""
        # remove all connections from combo box
        self.serial_connection_combo_box.Clear()
        # get list of connections
        av_cons = list_ports.comports()
        for path,name,hw in av_cons:
            # add combo box in main frame
            self.serial_connection_combo_box.Append(path)

# end of class CCMainFrame

class DataStore(object):
    """ A silly class buffering the data history for
        display in the plot frame.
    """
    def __init__(self, l, vn):
        """init data structures"""
        # l - number of samples of historical data to plot
        # vn - names of variables to store        
        self.data = {}
        for varNm in vn:
            self.data[varNm] = deque([float("nan")])
        self.plotL = l
        
    def addSample(self, data, vn):
        """stores new data row"""
        # adds data to the according queues, in the order of the provided names
        for i,varNm in enumerate(vn):
            self.data[varNm].append(data[i])
            if len(self.data[varNm]) > self.plotL:
                self.data[varNm].popleft()

    def getData(self, varName):
        """provides the data series with provided name"""
        return self.data[varName]
        
    def clear(self):
        """reset data structure"""
        vn = self.data.keys()
        self.data = {}
        for varNm in vn:
            self.data[varNm] = deque([float("nan")])
        
class SerialRxEvent(wx.PyCommandEvent):
    """Event used to transfer the data read from the serial connection
    to the interface thread
    """
    eventType = SERIALRX
    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)