# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sat Oct 12 14:20:36 2013
#

import wx
from NPDataPlotter import GraphFrame
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class npControlNotebook(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: npControlNotebook.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.label_6 = wx.StaticText(self, wx.ID_ANY, _("NinjaPBR Control"))
        self.mode_radio_box = wx.RadioBox(self, wx.ID_ANY, _("Reactor Mode"), choices=[_("Standby"), _("Light"), _("Dark"), _("Dynamic Light"), _("Error")], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.button_odPlot = wx.Button(self, wx.ID_ANY, _("OD Curve Display"))
        self.label_7 = wx.StaticText(self, wx.ID_ANY, _("Scheduled Reactor Mode"))
        self.mode_schedule_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=[_("Standby"), _("Light"), _("Dark"), _("Dynamic Light"), _("Error")], style=wx.CB_DROPDOWN)
        self.label_8 = wx.StaticText(self, wx.ID_ANY, _("Change Time"))
        self.text_ctrl_mode_change_time = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.label_1_copy_1_copy = wx.StaticText(self, wx.ID_ANY, _("Minimal Led Brightness (>=0)"), style=wx.ALIGN_CENTER)
        self.text_ctrl_min_led_bght = wx.TextCtrl(self, wx.ID_ANY, _("0"), style=wx.TE_PROCESS_ENTER)
        self.label_2_copy_copy = wx.StaticText(self, wx.ID_ANY, _("Maximal Led Brightness (<=255)"), style=wx.ALIGN_CENTER)
        self.text_ctrl_max_led_bght = wx.TextCtrl(self, wx.ID_ANY, _("255"), style=wx.TE_PROCESS_ENTER)
        self.label_3_copy_copy = wx.StaticText(self, wx.ID_ANY, _("Sampling Rate (sec)"), style=wx.ALIGN_CENTER)
        self.text_ctrl_sampling_rate = wx.TextCtrl(self, wx.ID_ANY, _("10"), style=wx.TE_PROCESS_ENTER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBOX, self.ReactorModeChangeRadioButton, self.mode_radio_box)
        self.Bind(wx.EVT_BUTTON, self.OnOdCurvePlotClicked, self.button_odPlot)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnMinBghtEntered, self.text_ctrl_min_led_bght)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnMaxBghtEntered, self.text_ctrl_max_led_bght)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSampleRateEntered, self.text_ctrl_sampling_rate)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: npControlNotebook.__set_properties
        self.label_6.SetFont(wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.mode_radio_box.SetToolTipString(_("Available reactor operation modes"))
        self.mode_radio_box.SetSelection(0)
        self.button_odPlot.SetToolTipString(_("Open plot of available OD values "))
        self.mode_schedule_combo_box.SetToolTipString(_("Select which mode to switch into"))
        self.mode_schedule_combo_box.SetSelection(-1)
        self.text_ctrl_mode_change_time.SetToolTipString(_("Time to switch mode specified above"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: npControlNotebook.__do_layout
        sizer_main_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main_content = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_mode_light = wx.BoxSizer(wx.VERTICAL)
        sizer_light_general = wx.BoxSizer(wx.VERTICAL)
        sizer_main_main.Add(self.label_6, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_mode_light.Add(self.mode_radio_box, 0, wx.ALIGN_CENTER | wx.SHAPED, 0)
        sizer_light_general.Add(self.button_odPlot, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer_mode_light.Add(sizer_light_general, 1, wx.EXPAND, 0)
        sizer_main_content.Add(sizer_mode_light, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer_13.Add(self.mode_schedule_combo_box, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_13.Add(self.label_8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer_13.Add(self.text_ctrl_mode_change_time, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_main_content.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_14.Add(self.label_1_copy_1_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_min_led_bght, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_14.Add(self.label_2_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_max_led_bght, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_14.Add(self.label_3_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_sampling_rate, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_main_content.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_main_main.Add(sizer_main_content, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main_main)
        sizer_main_main.Fit(self)
        self.Layout()
        # end wxGlade

    def ReactorModeChangeRadioButton(self, event):  # wxGlade: npControlNotebook.<event_handler>
        newMode = str(self.mode_radio_box.GetSelection())
        if not self.GetParent().GetParent().serial.isOpen():
            self.mode_radio_box.SetSelection(0)
            msgbox = wx.MessageBox('Not connected to reactor!', 
                                   'Warning', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
        else:
            if int(newMode) > 0 and not self.GetParent().GetParent().reference_values_measured:
                msgbox = wx.MessageBox('Reference values not measured before - OD values will be invalid!', 
                                       'Warning', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
            self.GetParent().GetParent().sendMessage("md",str(newMode))
            # set background color in data frame according to current mode
            self.GetParent().GetParent().dataFrame.SetBackgroundColour(self.GetParent().GetParent().mode_bg_cols[int(newMode)])

    def OnTurbidostatButtonClicked(self, event):  # wxGlade: npControlNotebook.<event_handler>
        if self.button_turbidostat_mode.GetValue():
            self.GetParent().GetParent().sendMessage("it","1") # activate turbidostat
        else:
            self.GetParent().GetParent().sendMessage("it","0") # DEactivate turbidostat

    def OnMinBghtEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("milb",str(self.text_ctrl_min_led_bght.GetValue()))
        
    def OnMaxBghtEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("malb",str(self.text_ctrl_max_led_bght.GetValue()))
        
    def OnSampleRateEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("sst",str(self.text_ctrl_sampling_rate.GetValue()))
        
    def OnTBDUpperThrsEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("uot",str(self.text_ctrl_turbido_upper_thr.GetValue()))
        
    def OnTBDLowerThrsEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("lot",str(self.text_ctrl_turbido_lower_thr.GetValue()))
        
    def OnDilutionDurEntered(self, event):  # wxGlade: npControlNotebook.<event_handler>
        self.GetParent().GetParent().sendMessage("dd",str(self.text_ctrl_turbido_dilution_len.GetValue()))
        
    def OnOdCurvePlotClicked(self, event):  # wxGlade: npControlNotebook.<event_handler>
        # show od curve plot if window not already open
        if self.GetParent().GetParent().odCurveFrame == None:
            plotFrame = GraphFrame(self.GetParent().GetParent(), self.GetParent().GetParent().dataStore, None)
            plotFrame.Show()
            self.GetParent().GetParent().odCurveFrame = plotFrame
            self.button_odPlot.Disable()
        else:
            if DEBUG:
                print "OD curve plot already open..."
# end of class npControlNotebook