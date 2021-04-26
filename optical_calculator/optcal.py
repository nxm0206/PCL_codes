# -*- coding: UTF-8 -*-
import wx

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

class OptCalFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='OptCal Version 1.0', size=(420, 620))
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        tab1 = WavlFreqWavn(nb)
        tab2 = DeciPerc(nb)

        nb.AddPage(tab1, "\u03BB\u21CC\u03bD\u21CC\u03C3")
        nb.AddPage(tab2, "dB,dBm\u21CC\u0025,mW")
        # self.panel = CalPanel(self)
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.SetSizeHints(420, 720, 820, 720)
        self.Show()

class WavlFreqWavn(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.last_button_pressed = None
        self.create_ui()

    def create_ui(self):
        # ---------------initialize Bottom Layer Sizer-----------------------------------------
        BottomLayerSizer = wx.BoxSizer(wx.VERTICAL)

        # ---------------add title to the GUI-------------------------------------------------
        if True:
            font_title = wx.Font(12, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
            title = wx.StaticText(self, label=r'BANDWIDTH CONVERSION', style=wx.ALIGN_CENTRE)
            title.SetFont(font_title)
            titleSizer = wx.BoxSizer(wx.VERTICAL)
            titleSizer.Add(title, 0, wx.ALL | wx.EXPAND, 10)
            BottomLayerSizer.Add(titleSizer, 0, wx.EXPAND, 5)

        # ----------------initialize the two radioButtons for input type--------------------------------
        if True:
            # setup the radioButtons
            Input_Type = ['Mid-Span', 'Min-Max']
            self.rb21 = wx.RadioButton(self, 21, label=Input_Type[0], style=wx.RB_GROUP)
            self.rb22 = wx.RadioButton(self, 22, label=Input_Type[1])
            # setup a box for three radioBottons
            self.Input_type_Box = wx.StaticBox(self, -1, 'Input Type:')
            Input_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
            self.Input_type_Box.SetFont(Input_font)
            self.Input_type_Sizer = wx.StaticBoxSizer(self.Input_type_Box, wx.HORIZONTAL)
            # add the two radioButtons into the box
            self.Input_type_Sizer.Add(self.rb21, 0, wx.TOP | wx.EXPAND, 10)
            self.Input_type_Sizer.Add(self.rb22, 0, wx.TOP | wx.EXPAND, 10)
            # add the box containing two radioButtons into the Bottom layer Sizer
            BottomLayerSizer.Add(self.Input_type_Sizer, 0, wx.ALL | wx.EXPAND, 5)
            # Bind events to the three radioButtons
            self.current_input_type = 'Mid-Span'
            self.rb21.Bind(wx.EVT_RADIOBUTTON, self.InputonRadioBox)
            self.rb22.Bind(wx.EVT_RADIOBUTTON, self.InputonRadioBox)

        # ----------------initialize the three radioButtons for three quantities--------------------------------
        if True:
            # setup the radioButtons
            Input_Quantity = ['Wavelength', 'Frequency', 'Wavenumber']
            self.rb11 = wx.RadioButton(self, 11, label=Input_Quantity[0], style=wx.RB_GROUP)
            self.rb12 = wx.RadioButton(self, 12, label=Input_Quantity[1])
            self.rb13 = wx.RadioButton(self, 13, label=Input_Quantity[2])
            # setup a box for three radioBottons
            self.quantity_type_Box = wx.StaticBox(self, -1, 'Quantity Type:')
            quantity_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
            self.quantity_type_Box.SetFont(quantity_font)
            self.quantity_type_Sizer = wx.StaticBoxSizer(self.quantity_type_Box, wx.HORIZONTAL)
            # add the three redioButtons into the box
            self.quantity_type_Sizer.Add(self.rb11, 0, wx.TOP | wx.EXPAND, 10)
            self.quantity_type_Sizer.Add(self.rb12, 0, wx.TOP | wx.EXPAND, 10)
            self.quantity_type_Sizer.Add(self.rb13, 0, wx.TOP | wx.EXPAND, 10)
            # add the box containing three radioButtons into the Bottom layer Sizer
            BottomLayerSizer.Add(self.quantity_type_Sizer, 0, wx.ALL | wx.EXPAND, 5)
            # Bind events to the three radioButtons
            self.current_type = 'Wavl'
            self.rb11.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)
            self.rb12.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)
            self.rb13.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)

        # ----------------initialize the input and display of three quantities--------------------------------
        if True:
            quantities = [r'Wavelength in unit: ', r'Frequency in unit: ', r'Wavenumber in unit: ']
            TextCtrl_list = ['input_text_11', 'input_text_12', 'input_text_13', 'input_text_14',
                             'input_text_21', 'input_text_22', 'input_text_23', 'input_text_24',
                             'input_text_31', 'input_text_32', 'input_text_33', 'input_text_34']
            quantities_label = [r'Mid', r'Span', r'Min', r'Max']
            unit = [['pm', 'nm', u'\u03BC' + 'm', 'mm'],
                    ['KHz', 'MHz', 'GHz', 'THz'],
                    ['cm'+u'\u207B\u00B9', 'mm'+u'\u207B\u00B9', u'\u03BC' + 'm'+u'\u207B\u00B9', 'nm'+u'\u207B\u00B9']]
            default_unit = ['nm', 'GHz', 'cm'+u'\u207B\u00B9']
            self.current_wavl_unit = default_unit[0]
            self.current_freq_unit = default_unit[1]
            self.current_wavn_unit = default_unit[2]

            # add content for each quantity box
            for i in range(len(quantities)):
                # initialize the box for quantity sizer

                quantity_unit_text = wx.StaticText(self, label=quantities[i], style=wx.ALIGN_LEFT)
                quantity_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
                quantity_unit_text.SetFont(quantity_font)
                exec('self.combo' + str(i+1) + '= wx.ComboBox(self, choices=unit[i], value=default_unit[i])')
                quantity_unit_Sizer = wx.BoxSizer(wx.HORIZONTAL)
                quantity_unit_Sizer.Add(quantity_unit_text, 0, wx.TOP | wx.EXPAND | wx.ALL, 0)
                exec('quantity_unit_Sizer.Add(self.combo' + str(i+1) + ', 0, wx.EXPAND | wx.ALL, 0)')
                exec('self.combo' + str(i+1) + '.Bind(wx.EVT_COMBOBOX, self.OnCombo' + str(i+1) + ')')



                quantity_input_Sizer = wx.BoxSizer(wx.HORIZONTAL)
                for j in range(len(quantities_label)):
                    # initialize the box for mid-span-Min-Max sizer
                    self.label_text = wx.StaticText(self, label=quantities_label[j], style=wx.ALIGN_CENTRE)
                    exec('self.' + TextCtrl_list[4 * i + j] + '= wx.TextCtrl(self)')
                    exec('self.' + TextCtrl_list[4 * i + j] + '.Disable()')
                    self.inputSizer = wx.BoxSizer(wx.HORIZONTAL)
                    self.inputSizer.Add(self.label_text, 0, wx.TOP | wx.EXPAND, 0)
                    self.inputSizer.AddStretchSpacer(1)
                    exec('self.inputSizer.Add(self.' + TextCtrl_list[4 * i + j] + ', 0, wx.ALL | wx.EXPAND, 1)')
                    if j < 2:
                        if j == 0:
                            # initialize the box for mid-span sizer
                            CS_Box = wx.StaticBox(self, 1)
                            CS_Sizer = wx.StaticBoxSizer(CS_Box, wx.VERTICAL)
                        # add inputsizer into mid-span sizer
                        CS_Sizer.Add(self.inputSizer, 0, wx.ALL | wx.EXPAND, 0)
                    else:
                        if j == 2:
                            # initialize the box for Min-Max sizer
                            MM_Box = wx.StaticBox(self, 1)
                            MM_Sizer = wx.StaticBoxSizer(MM_Box, wx.VERTICAL)
                        # add inputsizer into Min-Max sizer
                        MM_Sizer.Add(self.inputSizer, 0, wx.ALL | wx.EXPAND, 0)

                # add mid_span box and Min-Max box into quantity sizer
                quantity_input_Sizer.Add(CS_Sizer, 1, wx.ALL | wx.EXPAND, 0)
                quantity_input_Sizer.Add(MM_Sizer, 1, wx.ALL | wx.EXPAND, 0)

                # add quantity box into bottomlayer Sizer
                quantity_Sizer = wx.BoxSizer(wx.VERTICAL)
                quantity_Sizer.Add(quantity_unit_Sizer, 0, wx.ALL | wx.EXPAND, 0)
                quantity_Sizer.Add(quantity_input_Sizer, 0, wx.ALL | wx.EXPAND, 0)
                BottomLayerSizer.Add(quantity_Sizer, 0, wx.ALL | wx.EXPAND, 5)

                # set default input box
                self.input_text_11.Enable()
                self.input_text_12.Enable()
                self.input_text_13.Disable()
                self.input_text_14.Disable()
                # BottomLayerSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)

        # ---------------add CONVERT button and bind Enter key-------------------------------------------------
        if True:
            btn_BandWidthConvert = wx.Button(self, label='CONVERT')
            self.Bind(wx.EVT_BUTTON, self.BandWidthConversion, btn_BandWidthConvert)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)
            btnSizer.Add(btn_BandWidthConvert, 0, wx.ALL, 5)
            BottomLayerSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 5)
            self.Bind(wx.EVT_CHAR_HOOK, self.on_key)

        # ---------------add author information-------------------------------------------------
        if True:
            BottomLayerSizer.AddStretchSpacer(1)
            font_author_info = wx.Font(7, family=wx.ROMAN, style=wx.NORMAL, weight=wx.LIGHT,
                                       encoding=wx.FONTENCODING_SYSTEM)
            author_info = 'By Xiaomin Nie, Copyright © 2020 Shenzhen, China'
            author_text = wx.StaticText(self, label=author_info, style=wx.ALIGN_CENTRE)
            author_text.SetFont(font_author_info)
            BottomLayerSizer.Add(author_text, 0, wx.ALL | wx.EXPAND, 5)

        # ---------------add statuBar for info display-------------------------------------------------
        if True:
            self.statusBar = wx.StatusBar(self, -1)  # 实例化 wx.StatusBar
            self.statusBar.SetFieldsCount(1)  # 状态栏分成3个区域
            # statusBar.SetStatusWidths([-1, -1, -1])  # 区域宽度比列，用负数
            # self.statusBar.SetStatusText("A Custom StatusBar...", 0)  # 给状态栏设文字
            BottomLayerSizer.Add(self.statusBar, 0, wx.ALL | wx.EXPAND, 0)
            status = 'Current selected quantity is ' + Input_Quantity[0]
            self.statusBar.SetStatusText(status, 0)

        self.SetSizer(BottomLayerSizer)
        # BottomLayerSizer.Fit(self)

    def QuantityonRadioBox(self, event):
        # defult type is wavelength
        self.current_type = 'Wavl'
        status = 'Current selected quantity is ' + event.GetEventObject().GetLabel()
        self.statusBar.SetStatusText(status, 0)
        if event.GetEventObject().GetLabel() == 'Frequency':
            self.current_type = 'Freq'
        elif event.GetEventObject().GetLabel() == 'Wavenumber':
            self.current_type = 'Wavn'
        else:
            self.current_type = 'Wavl'
        self.Enable_textinput()

    def InputonRadioBox(self, event):
        status = 'Current selected input type is ' + event.GetEventObject().GetLabel()
        self.statusBar.SetStatusText(status, 0)
        if event.GetEventObject().GetLabel() == 'Min-Max':
            self.current_input_type = 'Min-Max'


        else:
            self.current_input_type = 'Mid-Span'
        self.Enable_textinput()

    def Enable_textinput(self):
        print('current quantity type is ' + self.current_type)
        print('current Input type is ' + self.current_input_type)
        if self.current_type == 'Freq':
            if self.current_input_type == 'Min-Max':
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Disable()')
                    exec('self.input_text_2' + str(text_index) + '.Disable()')
                    exec('self.input_text_3' + str(text_index) + '.Disable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Enable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
            else:
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Disable()')
                    exec('self.input_text_2' + str(text_index) + '.Enable()')
                    exec('self.input_text_3' + str(text_index) + '.Disable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')

        elif self.current_type == 'Wavn':
            if self.current_input_type == 'Min-Max':
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Disable()')
                    exec('self.input_text_2' + str(text_index) + '.Disable()')
                    exec('self.input_text_3' + str(text_index) + '.Disable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Enable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')

            else:
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Disable()')
                    exec('self.input_text_2' + str(text_index) + '.Disable()')
                    exec('self.input_text_3' + str(text_index) + '.Enable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')

        else:
            if self.current_input_type == 'Min-Max':
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Disable()')
                    exec('self.input_text_2' + str(text_index) + '.Disable()')
                    exec('self.input_text_3' + str(text_index) + '.Disable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Enable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')

            else:
                value_str = ''
                for text_index in range(1, 3):
                    exec('self.input_text_1' + str(text_index) + '.Enable()')
                    exec('self.input_text_2' + str(text_index) + '.Disable()')
                    exec('self.input_text_3' + str(text_index) + '.Disable()')
                    exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
                    exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
                    exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
                    exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')

    def BandWidthConversion(self, event):

        if self. current_freq_unit == 'KHz':
            freq_conv = 1.0E3
        elif self. current_freq_unit == 'MHz':
            freq_conv = 1.0E6
        elif self.current_freq_unit == 'GHz':
            freq_conv = 1.0E9
        elif self.current_freq_unit == 'THz':
            freq_conv = 1.0E12
        else:
            status = 'Please specify an unit for frequency.'
            self.statusBar.SetStatusText(status, 0)

        if self.current_wavl_unit == 'pm':
            wavl_conv = 1.0E-12
        elif self.current_wavl_unit == 'nm':
            wavl_conv = 1.0E-9
        elif self.current_wavl_unit == u'\u03BC' + 'm':
            wavl_conv = 1.0E-6
        elif self.current_wavl_unit == 'mm':
            wavl_conv = 1.0E-3
        else:
            status = 'Please specify an unit for wavelength.'
            self.statusBar.SetStatusText(status, 0)

        if self.current_wavn_unit == 'cm'+u'\u207B\u00B9':
            wavn_conv = 1.0E2
        elif self.current_wavn_unit == 'mm'+u'\u207B\u00B9':
            wavn_conv = 1.0E3
        elif self.current_wavn_unit == u'\u03BC' + 'm'+u'\u207B\u00B9':
            wavn_conv = 1.0E6
        elif self.current_wavn_unit == 'nm'+u'\u207B\u00B9':
            wavn_conv = 1.0E9
        else:
            status = 'Please specify an unit for wavenumber.'
            self.statusBar.SetStatusText(status, 0)





        if self.current_type == 'Freq':
            if self.current_input_type == 'Mid-Span':
                if not is_number(self.input_text_21.GetLineText(0)):
                    status = 'Please enter a valid center frequency.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_22.GetLineText(0)):
                    status = 'Please enter a valid frequency span.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    freq = float(self.input_text_21.GetLineText(0))*freq_conv
                    freq_b = float(self.input_text_22.GetLineText(0))*freq_conv
                    freq_1 = freq - freq_b / 2.0
                    freq_2 = freq + freq_b / 2.0

                    wavel_1 = 3 * 10 ** 8 / freq_1
                    wavel_2 = 3 * 10 ** 8 / freq_2
                    wavel = (wavel_1 + wavel_2) / 2.0
                    wavel_b = abs(wavel_1 - wavel_2)

                    waven_1 = 1.0 / wavel_1
                    waven_2 = 1.0 / wavel_2
                    waven = (waven_1 + waven_2) / 2.0
                    waven_b = abs(waven_1 - waven_2)

                    self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
                    self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))

                    self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
                    self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
                    self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
                    self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))

                    self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
                    self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
                    self.input_text_33.SetValue(str(round(waven_1/wavl_conv, 3)))
                    self.input_text_34.SetValue(str(round(waven_2/wavl_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

            else:
                if not is_number(self.input_text_23.GetLineText(0)):
                    status = 'Please enter a valid minimum frequency.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_24.GetLineText(0)):
                    status = 'Please enter a valid maximum frequency.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    freq_1 = float(self.input_text_23.GetLineText(0))*freq_conv
                    freq_2 = float(self.input_text_24.GetLineText(0))*freq_conv
                    freq = (freq_1 + freq_2) / 2.0
                    freq_b = abs(freq_1 - freq_2)

                    wavel_1 = 3 * 10 ** 8 / freq_1
                    wavel_2 = 3 * 10 ** 8 / freq_2
                    wavel = (wavel_1 + wavel_2) / 2.0
                    wavel_b = abs(wavel_1 - wavel_2)

                    waven_1 = 1.0 / wavel_1
                    waven_2 = 1.0 / wavel_2
                    waven = (waven_1 + waven_2) / 2.0
                    waven_b = abs(waven_1 - waven_2)

                    self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
                    self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))

                    self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
                    self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
                    self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
                    self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))

                    self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
                    self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
                    self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
                    self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

        elif self.current_type == 'Wavn':
            if self.current_input_type == 'Mid-Span':
                if not is_number(self.input_text_31.GetLineText(0)):
                    status = 'Please enter a valid center wavenumber.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_32.GetLineText(0)):
                    status = 'Please enter a valid wavenumber bandwidth.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    waven = float(self.input_text_31.GetLineText(0))*wavn_conv
                    waven_b = float(self.input_text_32.GetLineText(0))*wavn_conv
                    waven_1 = waven - waven_b / 2.0
                    waven_2 = waven + waven_b / 2.0

                    wavel_1 = 1.0 / waven_1
                    wavel_2 = 1.0 / waven_2
                    wavel = (wavel_1 + wavel_2) / 2.0
                    wavel_b = abs(wavel_1 - wavel_2)

                    freq_1 = 3 * 10 ** 8 / wavel_1
                    freq_2 = 3 * 10 ** 8 / wavel_2
                    freq = (freq_1 + freq_2) / 2.0
                    freq_b = abs(freq_1 - freq_2)

                    self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
                    self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
                    self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
                    self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
                    self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
                    self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
                    self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
                    self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
                    self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
                    self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

            else:
                if not is_number(self.input_text_33.GetLineText(0)):
                    status = 'Please enter a valid minimum wavenumber.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_34.GetLineText(0)):
                    status = 'Please enter a valid maximum wavenumber.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    waven_1 = float(self.input_text_33.GetLineText(0))*wavn_conv
                    waven_2 = float(self.input_text_34.GetLineText(0))*wavn_conv
                    waven = (waven_1 + waven_2) / 2.0
                    waven_b = abs(waven_1 - waven_2)

                    wavel_1 = 1.0 / waven_1
                    wavel_2 = 1.0 / waven_2
                    wavel = (wavel_1 + wavel_2) / 2.0
                    wavel_b = abs(wavel_1 - wavel_2)


                    freq_1 = 3 * 10 ** 8 / wavel_1
                    freq_2 = 3 * 10 ** 8 / wavel_2
                    freq = (freq_1 + freq_2) / 2.0
                    freq_b = abs(freq_1 - freq_2)


                    self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
                    self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
                    self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
                    self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
                    self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
                    self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
                    self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
                    self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))

                    self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
                    self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

        else:
            if self.current_input_type == 'Mid-Span':
                if not is_number(self.input_text_11.GetLineText(0)):
                    status = 'Please enter a valid center wavelength.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_12.GetLineText(0)):
                    status = 'Please enter a valid wavelength bandwidth.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    wavel = float(self.input_text_11.GetLineText(0))*wavl_conv
                    wavel_b = float(self.input_text_12.GetLineText(0))*wavl_conv
                    wavel_1 = wavel - wavel_b/2.0
                    wavel_2 = wavel + wavel_b/2.0


                    waven_1 = 1.0 / wavel_1
                    waven_2 = 1.0 / wavel_2
                    waven = (waven_1 + waven_2) / 2.0
                    waven_b = abs(waven_1 - waven_2)


                    freq_1 = 3 * 10 ** 8 / wavel_1
                    freq_2 = 3 * 10 ** 8 / wavel_2
                    freq = (freq_1 + freq_2) / 2.0
                    freq_b = abs(freq_1 - freq_2)


                    self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
                    self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))

                    self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
                    self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
                    self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
                    self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))

                    self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
                    self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
                    self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
                    self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)
            else:
                if not is_number(self.input_text_13.GetLineText(0)):
                    status = 'Please enter a valid minimum wavelength.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_14.GetLineText(0)):
                    status = 'Please enter a valid maximum wavelength.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    wavel_1 = float(self.input_text_13.GetLineText(0))*wavl_conv
                    wavel_2 = float(self.input_text_14.GetLineText(0))*wavl_conv
                    wavel = (wavel_1 + wavel_2) / 2.0
                    wavel_b = abs(wavel_1 - wavel_2)

                    waven_1 = 1.0 / wavel_1
                    waven_2 = 1.0 / wavel_2
                    waven = (waven_1 + waven_2) / 2.0
                    waven_b = abs(waven_1 - waven_2)

                    freq_1 = 3 * 10 ** 8 / wavel_1
                    freq_2 = 3 * 10 ** 8 / wavel_2
                    freq = (freq_1 + freq_2) / 2.0
                    freq_b = abs(freq_1 - freq_2)


                    self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
                    self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))

                    self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
                    self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
                    self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
                    self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))

                    self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
                    self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
                    self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
                    self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

    def OnCombo1(self, event):
        status = "set current unit of wavelength to: " + self.combo1.GetValue()
        print(status)
        self.statusBar.SetStatusText(status, 0)
        self.current_wavl_unit = self.combo1.GetValue()

    def OnCombo2(self, event):
        status = "set current unit of frequency to: " + self.combo2.GetValue()
        print(status)
        self.statusBar.SetStatusText(status, 0)
        self.current_freq_unit = self.combo2.GetValue()

    def OnCombo3(self, event):
        status = "set current unit of wavenumber to: " + self.combo3.GetValue()
        print(status)
        self.statusBar.SetStatusText(status, 0)
        # self.label.SetLabel("set current unit of wavelength to: " + self.combo.GetValue())
        self.current_wavn_unit = self.combo3.GetValue()

    def on_key(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.BandWidthConversion(event)

        elif key == wx.WXK_NUMPAD_ENTER:
            self.BandWidthConversion(event)

        else:
            event.Skip()

    def closeProgram(self):
        self.Close()

class DeciPerc(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.last_button_pressed = None
        self.create_ui()

    def create_ui(self):
        # ---------------initialize Bottom Layer Sizer-----------------------------------------
        BottomLayerSizer = wx.BoxSizer(wx.VERTICAL)

        # ---------------add title to the GUI-------------------------------------------------
        if True:
            font_title = wx.Font(12, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
            title = wx.StaticText(self, label='UNIT CONVERSION', style=wx.ALIGN_CENTRE)
            title.SetFont(font_title)
            titleSizer = wx.BoxSizer(wx.VERTICAL)
            titleSizer.Add(title, 0, wx.ALL | wx.EXPAND, 10)
            BottomLayerSizer.Add(titleSizer, 0, wx.EXPAND, 5)
            Conversion_Type = ['dB\u21CC\u0025', 'dBm\u21CCmW']



        # ----------------initialize first conversion--------------------------------
        if True:
            Conversion1_StaticBox = wx.StaticBox(self, -1, Conversion_Type[0])
            Conversion1_StaticBoxSizer = wx.StaticBoxSizer(Conversion1_StaticBox, wx.HORIZONTAL)

            # # setup the radioButtons
            # Input_Quantity = ['Wavelength', 'Frequency', 'Wavenumber']
            # self.rb11 = wx.RadioButton(self, 11, label=Input_Quantity[0], style=wx.RB_GROUP)
            # self.rb12 = wx.RadioButton(self, 12, label=Input_Quantity[1])
            # self.rb13 = wx.RadioButton(self, 13, label=Input_Quantity[2])
            # # setup a box for three radioBottons
            # self.quantity_type_Box = wx.StaticBox(self, -1, 'Quantity Type:')
            # quantity_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
            # self.quantity_type_Box.SetFont(quantity_font)
            # self.quantity_type_Sizer = wx.StaticBoxSizer(self.quantity_type_Box, wx.HORIZONTAL)
            # # add the three redioButtons into the box
            # self.quantity_type_Sizer.Add(self.rb11, 0, wx.TOP | wx.EXPAND, 10)
            # self.quantity_type_Sizer.Add(self.rb12, 0, wx.TOP | wx.EXPAND, 10)
            # self.quantity_type_Sizer.Add(self.rb13, 0, wx.TOP | wx.EXPAND, 10)
            # # add the box containing three radioButtons into the Bottom layer Sizer
            # BottomLayerSizer.Add(self.quantity_type_Sizer, 0, wx.ALL | wx.EXPAND, 5)
            # # Bind events to the three radioButtons
            # self.current_type = 'Wavl'
            # self.rb11.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)
            # self.rb12.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)
            # self.rb13.Bind(wx.EVT_RADIOBUTTON, self.QuantityonRadioBox)


            self.label_text_11 = wx.StaticText(self, label='Decibel (dB)', style=wx.ALIGN_CENTRE)
            self.input_text_11 = wx.TextCtrl(self)
            self.input_text_11.Disable()

            self.inputSizer11= wx.BoxSizer(wx.HORIZONTAL)
            self.inputSizer11.Add(self.label_text_11, 0, wx.TOP | wx.EXPAND, 0)
            self.inputSizer11.AddStretchSpacer(1)
            self.inputSizer11.Add(self.input_text_11, 0, wx.ALL | wx.EXPAND, 1)

            self.label_text_12 = wx.StaticText(self, label='Percentage (\u0025)', style=wx.ALIGN_CENTRE)
            self.input_text_12 = wx.TextCtrl(self)
            self.input_text_12.Disable()
            self.inputSizer12 = wx.BoxSizer(wx.HORIZONTAL)
            self.inputSizer12.Add(self.label_text_12, 0, wx.TOP | wx.EXPAND, 0)
            self.inputSizer12.AddStretchSpacer(1)
            self.inputSizer12.Add(self.input_text_12, 0, wx.ALL | wx.EXPAND, 1)

            conversion1_Sizer = wx.BoxSizer(wx.VERTICAL)
            conversion1_Sizer.Add(self.inputSizer11, 0, wx.ALL | wx.EXPAND, 0)
            conversion1_Sizer.Add(self.inputSizer12, 0, wx.ALL | wx.EXPAND, 0)

            Conversion1_StaticBoxSizer.Add(conversion1_Sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

            btn_Conversion1 = wx.Button(self, label='CONVERT')
            self.Bind(wx.EVT_BUTTON, self.Conversion1, btn_Conversion1)
            btn_Conversion1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
            btn_Conversion1_Sizer.Add(btn_Conversion1, 0, wx.ALL, 5)
            Conversion1_StaticBoxSizer.Add(btn_Conversion1_Sizer, 0, wx.ALL | wx.CENTER, 5)
            self.Bind(wx.EVT_CHAR_HOOK, self.on_key)

        # ----------------initialize second conversion--------------------------------
        if True:
            Conversion2_StaticBox = wx.StaticBox(self, -1, Conversion_Type[1])
            Conversion2_StaticBoxSizer = wx.StaticBoxSizer(Conversion2_StaticBox, wx.HORIZONTAL)

            self.label_text_21 = wx.StaticText(self, label='Optical Power in dBm', style=wx.ALIGN_CENTRE)
            self.input_text_21 = wx.TextCtrl(self)
            self.input_text_21.Disable()

            self.inputSizer21 = wx.BoxSizer(wx.HORIZONTAL)
            self.inputSizer21.Add(self.label_text_21, 0, wx.TOP | wx.EXPAND, 0)
            self.inputSizer21.AddStretchSpacer(1)
            self.inputSizer21.Add(self.input_text_21, 0, wx.ALL | wx.EXPAND, 1)

            self.label_text_22 = wx.StaticText(self, label='Optical Power in mW', style=wx.ALIGN_CENTRE)
            self.input_text_22 = wx.TextCtrl(self)
            self.input_text_22.Disable()
            self.inputSizer22 = wx.BoxSizer(wx.HORIZONTAL)
            self.inputSizer22.Add(self.label_text_22, 0, wx.TOP | wx.EXPAND, 0)
            self.inputSizer22.AddStretchSpacer(1)
            self.inputSizer22.Add(self.input_text_22, 0, wx.ALL | wx.EXPAND, 1)

            conversion2_Sizer = wx.BoxSizer(wx.VERTICAL)
            conversion2_Sizer.Add(self.inputSizer21, 0, wx.ALL | wx.EXPAND, 0)
            conversion2_Sizer.Add(self.inputSizer22, 0, wx.ALL | wx.EXPAND, 0)

            Conversion2_StaticBoxSizer.Add(conversion2_Sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

            btn_Conversion2 = wx.Button(self, label='CONVERT')
            self.Bind(wx.EVT_BUTTON, self.Conversion2, btn_Conversion2)
            btn_Conversion2_Sizer = wx.BoxSizer(wx.HORIZONTAL)
            btn_Conversion2_Sizer.Add(btn_Conversion2, 0, wx.ALL, 5)
            Conversion2_StaticBoxSizer.Add(btn_Conversion2_Sizer, 0, wx.ALL | wx.CENTER, 5)
            self.Bind(wx.EVT_CHAR_HOOK, self.on_key)




            BottomLayerSizer.Add(Conversion1_StaticBoxSizer, 0, wx.ALL | wx.EXPAND, 5)

            BottomLayerSizer.Add(Conversion2_StaticBoxSizer, 0, wx.ALL | wx.EXPAND, 5)


        # ----------------initialize the input and display of three quantities--------------------------------
    #     if True:
    #         quantities = [r'Wavelength in unit: ', r'Frequency in unit: ', r'Wavenumber in unit: ']
    #         TextCtrl_list = ['input_text_11', 'input_text_12', 'input_text_13', 'input_text_14',
    #                          'input_text_21', 'input_text_22', 'input_text_23', 'input_text_24',
    #                          'input_text_31', 'input_text_32', 'input_text_33', 'input_text_34']
    #         quantities_label = [r'Mid', r'Span', r'Min', r'Max']
    #         unit = [['pm', 'nm', u'\u03BC' + 'm', 'mm'],
    #                 ['KHz', 'MHz', 'GHz', 'THz'],
    #                 ['cm'+u'\u207B\u00B9', 'mm'+u'\u207B\u00B9', u'\u03BC' + 'm'+u'\u207B\u00B9', 'nm'+u'\u207B\u00B9']]
    #         default_unit = ['nm', 'GHz', 'cm'+u'\u207B\u00B9']
    #         self.current_wavl_unit = default_unit[0]
    #         self.current_freq_unit = default_unit[1]
    #         self.current_wavn_unit = default_unit[2]
    #
    #         # add content for each quantity box
    #         for i in range(len(quantities)):
    #             # initialize the box for quantity sizer
    #
    #             quantity_unit_text = wx.StaticText(self, label=quantities[i], style=wx.ALIGN_LEFT)
    #             quantity_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
    #             quantity_unit_text.SetFont(quantity_font)
    #             exec('self.combo' + str(i+1) + '= wx.ComboBox(self, choices=unit[i], value=default_unit[i])')
    #             quantity_unit_Sizer = wx.BoxSizer(wx.HORIZONTAL)
    #             quantity_unit_Sizer.Add(quantity_unit_text, 0, wx.TOP | wx.EXPAND | wx.ALL, 0)
    #             exec('quantity_unit_Sizer.Add(self.combo' + str(i+1) + ', 0, wx.EXPAND | wx.ALL, 0)')
    #             exec('self.combo' + str(i+1) + '.Bind(wx.EVT_COMBOBOX, self.OnCombo' + str(i+1) + ')')
    #
    #
    #
    #             quantity_input_Sizer = wx.BoxSizer(wx.HORIZONTAL)
    #             for j in range(len(quantities_label)):
    #                 # initialize the box for mid-span-Min-Max sizer
    #                 self.label_text = wx.StaticText(self, label=quantities_label[j], style=wx.ALIGN_CENTRE)
    #                 exec('self.' + TextCtrl_list[4 * i + j] + '= wx.TextCtrl(self)')
    #                 exec('self.' + TextCtrl_list[4 * i + j] + '.Disable()')
    #                 self.inputSizer = wx.BoxSizer(wx.HORIZONTAL)
    #                 self.inputSizer.Add(self.label_text, 0, wx.TOP | wx.EXPAND, 0)
    #                 self.inputSizer.AddStretchSpacer(1)
    #                 exec('self.inputSizer.Add(self.' + TextCtrl_list[4 * i + j] + ', 0, wx.ALL | wx.EXPAND, 1)')
    #                 if j < 2:
    #                     if j == 0:
    #                         # initialize the box for mid-span sizer
    #                         CS_Box = wx.StaticBox(self, 1)
    #                         CS_Sizer = wx.StaticBoxSizer(CS_Box, wx.VERTICAL)
    #                     # add inputsizer into mid-span sizer
    #                     CS_Sizer.Add(self.inputSizer, 0, wx.ALL | wx.EXPAND, 0)
    #                 else:
    #                     if j == 2:
    #                         # initialize the box for Min-Max sizer
    #                         MM_Box = wx.StaticBox(self, 1)
    #                         MM_Sizer = wx.StaticBoxSizer(MM_Box, wx.VERTICAL)
    #                     # add inputsizer into Min-Max sizer
    #                     MM_Sizer.Add(self.inputSizer, 0, wx.ALL | wx.EXPAND, 0)
    #
    #             # add mid_span box and Min-Max box into quantity sizer
    #             quantity_input_Sizer.Add(CS_Sizer, 1, wx.ALL | wx.EXPAND, 0)
    #             quantity_input_Sizer.Add(MM_Sizer, 1, wx.ALL | wx.EXPAND, 0)
    #
    #             # add quantity box into bottomlayer Sizer
    #             quantity_Sizer = wx.BoxSizer(wx.VERTICAL)
    #             quantity_Sizer.Add(quantity_unit_Sizer, 0, wx.ALL | wx.EXPAND, 0)
    #             quantity_Sizer.Add(quantity_input_Sizer, 0, wx.ALL | wx.EXPAND, 0)
    #             BottomLayerSizer.Add(quantity_Sizer, 0, wx.ALL | wx.EXPAND, 5)
    #
    #             # set default input box
    #             self.input_text_11.Enable()
    #             self.input_text_12.Enable()
    #             self.input_text_13.Disable()
    #             self.input_text_14.Disable()
        BottomLayerSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
    #
        # ---------------add CONVERT button and bind Enter key-------------------------------------------------
        # if True:

    #
        # ---------------add author information-------------------------------------------------
        if True:
            BottomLayerSizer.AddStretchSpacer(1)
            font_author_info = wx.Font(7, family=wx.ROMAN, style=wx.NORMAL, weight=wx.LIGHT,
                                       encoding=wx.FONTENCODING_SYSTEM)
            author_info = 'By Xiaomin Nie, Copyright © 2020 Shenzhen, China'
            author_text = wx.StaticText(self, label=author_info, style=wx.ALIGN_CENTRE)
            author_text.SetFont(font_author_info)
            BottomLayerSizer.Add(author_text, 0, wx.ALL | wx.EXPAND, 5)
    #
        # ---------------add statuBar for info display-------------------------------------------------
        if True:
            self.statusBar = wx.StatusBar(self, -1)  # 实例化 wx.StatusBar
            self.statusBar.SetFieldsCount(1)  # 状态栏分成3个区域
            # statusBar.SetStatusWidths([-1, -1, -1])  # 区域宽度比列，用负数
            # self.statusBar.SetStatusText("A Custom StatusBar...", 0)  # 给状态栏设文字
            BottomLayerSizer.Add(self.statusBar, 0, wx.ALL | wx.EXPAND, 0)
            status = 'Current selected quantity is '
            self.statusBar.SetStatusText(status, 0)

        self.SetSizer(BottomLayerSizer)
        # BottomLayerSizer.Fit(self)
    #
    # def QuantityonRadioBox(self, event):
    #     # defult type is wavelength
    #     self.current_type = 'Wavl'
    #     status = 'Current selected quantity is ' + event.GetEventObject().GetLabel()
    #     self.statusBar.SetStatusText(status, 0)
    #     if event.GetEventObject().GetLabel() == 'Frequency':
    #         self.current_type = 'Freq'
    #     elif event.GetEventObject().GetLabel() == 'Wavenumber':
    #         self.current_type = 'Wavn'
    #     else:
    #         self.current_type = 'Wavl'
    #     self.Enable_textinput()
    #
    # def InputonRadioBox(self, event):
    #     status = 'Current selected input type is ' + event.GetEventObject().GetLabel()
    #     self.statusBar.SetStatusText(status, 0)
    #     if event.GetEventObject().GetLabel() == 'Min-Max':
    #         self.current_input_type = 'Min-Max'
    #
    #
    #     else:
    #         self.current_input_type = 'Mid-Span'
    #     self.Enable_textinput()
    #
    # def Enable_textinput(self):
    #     print('current quantity type is ' + self.current_type)
    #     print('current Input type is ' + self.current_input_type)
    #     if self.current_type == 'Freq':
    #         if self.current_input_type == 'Min-Max':
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Enable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #         else:
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Enable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #
    #     elif self.current_type == 'Wavn':
    #         if self.current_input_type == 'Min-Max':
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Enable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #
    #         else:
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Enable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #
    #     else:
    #         if self.current_input_type == 'Min-Max':
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Enable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #
    #         else:
    #             value_str = ''
    #             for text_index in range(1, 3):
    #                 exec('self.input_text_1' + str(text_index) + '.Enable()')
    #                 exec('self.input_text_2' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index) + '.SetValue(value_str)')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.Disable()')
    #                 exec('self.input_text_1' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_2' + str(text_index + 2) + '.SetValue(value_str)')
    #                 exec('self.input_text_3' + str(text_index + 2) + '.SetValue(value_str)')
    #
    def Conversion1(self, event):
        status = 'conversion1'
        self.statusBar.SetStatusText(status, 0)

    def Conversion2(self, event):
        status = 'conversion2'
        self.statusBar.SetStatusText(status, 0)


    #
    #     if self. current_freq_unit == 'KHz':
    #         freq_conv = 1.0E3
    #     elif self. current_freq_unit == 'MHz':
    #         freq_conv = 1.0E6
    #     elif self.current_freq_unit == 'GHz':
    #         freq_conv = 1.0E9
    #     elif self.current_freq_unit == 'THz':
    #         freq_conv = 1.0E12
    #     else:
    #         status = 'Please specify an unit for frequency.'
    #         self.statusBar.SetStatusText(status, 0)
    #
    #     if self.current_wavl_unit == 'pm':
    #         wavl_conv = 1.0E-12
    #     elif self.current_wavl_unit == 'nm':
    #         wavl_conv = 1.0E-9
    #     elif self.current_wavl_unit == u'\u03BC' + 'm':
    #         wavl_conv = 1.0E-6
    #     elif self.current_wavl_unit == 'mm':
    #         wavl_conv = 1.0E-3
    #     else:
    #         status = 'Please specify an unit for wavelength.'
    #         self.statusBar.SetStatusText(status, 0)
    #
    #     if self.current_wavn_unit == 'cm'+u'\u207B\u00B9':
    #         wavn_conv = 1.0E2
    #     elif self.current_wavn_unit == 'mm'+u'\u207B\u00B9':
    #         wavn_conv = 1.0E3
    #     elif self.current_wavn_unit == u'\u03BC' + 'm'+u'\u207B\u00B9':
    #         wavn_conv = 1.0E6
    #     elif self.current_wavn_unit == 'nm'+u'\u207B\u00B9':
    #         wavn_conv = 1.0E9
    #     else:
    #         status = 'Please specify an unit for wavenumber.'
    #         self.statusBar.SetStatusText(status, 0)
    #
    #
    #
    #
    #
    #     if self.current_type == 'Freq':
    #         if self.current_input_type == 'Mid-Span':
    #             if not is_number(self.input_text_21.GetLineText(0)):
    #                 status = 'Please enter a valid center frequency.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_22.GetLineText(0)):
    #                 status = 'Please enter a valid frequency span.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 freq = float(self.input_text_21.GetLineText(0))*freq_conv
    #                 freq_b = float(self.input_text_22.GetLineText(0))*freq_conv
    #                 freq_1 = freq - freq_b / 2.0
    #                 freq_2 = freq + freq_b / 2.0
    #
    #                 wavel_1 = 3 * 10 ** 8 / freq_1
    #                 wavel_2 = 3 * 10 ** 8 / freq_2
    #                 wavel = (wavel_1 + wavel_2) / 2.0
    #                 wavel_b = abs(wavel_1 - wavel_2)
    #
    #                 waven_1 = 1.0 / wavel_1
    #                 waven_2 = 1.0 / wavel_2
    #                 waven = (waven_1 + waven_2) / 2.0
    #                 waven_b = abs(waven_1 - waven_2)
    #
    #                 self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
    #                 self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
    #
    #                 self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
    #                 self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
    #                 self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
    #                 self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
    #
    #                 self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
    #                 self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
    #                 self.input_text_33.SetValue(str(round(waven_1/wavl_conv, 3)))
    #                 self.input_text_34.SetValue(str(round(waven_2/wavl_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #
    #         else:
    #             if not is_number(self.input_text_23.GetLineText(0)):
    #                 status = 'Please enter a valid minimum frequency.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_24.GetLineText(0)):
    #                 status = 'Please enter a valid maximum frequency.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 freq_1 = float(self.input_text_23.GetLineText(0))*freq_conv
    #                 freq_2 = float(self.input_text_24.GetLineText(0))*freq_conv
    #                 freq = (freq_1 + freq_2) / 2.0
    #                 freq_b = abs(freq_1 - freq_2)
    #
    #                 wavel_1 = 3 * 10 ** 8 / freq_1
    #                 wavel_2 = 3 * 10 ** 8 / freq_2
    #                 wavel = (wavel_1 + wavel_2) / 2.0
    #                 wavel_b = abs(wavel_1 - wavel_2)
    #
    #                 waven_1 = 1.0 / wavel_1
    #                 waven_2 = 1.0 / wavel_2
    #                 waven = (waven_1 + waven_2) / 2.0
    #                 waven_b = abs(waven_1 - waven_2)
    #
    #                 self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
    #                 self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
    #
    #                 self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
    #                 self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
    #                 self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
    #                 self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
    #
    #                 self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
    #                 self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
    #                 self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
    #                 self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #
    #     elif self.current_type == 'Wavn':
    #         if self.current_input_type == 'Mid-Span':
    #             if not is_number(self.input_text_31.GetLineText(0)):
    #                 status = 'Please enter a valid center wavenumber.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_32.GetLineText(0)):
    #                 status = 'Please enter a valid wavenumber bandwidth.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 waven = float(self.input_text_31.GetLineText(0))*wavn_conv
    #                 waven_b = float(self.input_text_32.GetLineText(0))*wavn_conv
    #                 waven_1 = waven - waven_b / 2.0
    #                 waven_2 = waven + waven_b / 2.0
    #
    #                 wavel_1 = 1.0 / waven_1
    #                 wavel_2 = 1.0 / waven_2
    #                 wavel = (wavel_1 + wavel_2) / 2.0
    #                 wavel_b = abs(wavel_1 - wavel_2)
    #
    #                 freq_1 = 3 * 10 ** 8 / wavel_1
    #                 freq_2 = 3 * 10 ** 8 / wavel_2
    #                 freq = (freq_1 + freq_2) / 2.0
    #                 freq_b = abs(freq_1 - freq_2)
    #
    #                 self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
    #                 self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
    #                 self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
    #                 self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
    #                 self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
    #                 self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
    #                 self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
    #                 self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
    #                 self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
    #                 self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #
    #         else:
    #             if not is_number(self.input_text_33.GetLineText(0)):
    #                 status = 'Please enter a valid minimum wavenumber.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_34.GetLineText(0)):
    #                 status = 'Please enter a valid maximum wavenumber.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 waven_1 = float(self.input_text_33.GetLineText(0))*wavn_conv
    #                 waven_2 = float(self.input_text_34.GetLineText(0))*wavn_conv
    #                 waven = (waven_1 + waven_2) / 2.0
    #                 waven_b = abs(waven_1 - waven_2)
    #
    #                 wavel_1 = 1.0 / waven_1
    #                 wavel_2 = 1.0 / waven_2
    #                 wavel = (wavel_1 + wavel_2) / 2.0
    #                 wavel_b = abs(wavel_1 - wavel_2)
    #
    #
    #                 freq_1 = 3 * 10 ** 8 / wavel_1
    #                 freq_2 = 3 * 10 ** 8 / wavel_2
    #                 freq = (freq_1 + freq_2) / 2.0
    #                 freq_b = abs(freq_1 - freq_2)
    #
    #
    #                 self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
    #                 self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
    #                 self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
    #                 self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
    #                 self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
    #                 self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
    #                 self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
    #                 self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
    #
    #                 self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
    #                 self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #
    #     else:
    #         if self.current_input_type == 'Mid-Span':
    #             if not is_number(self.input_text_11.GetLineText(0)):
    #                 status = 'Please enter a valid center wavelength.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_12.GetLineText(0)):
    #                 status = 'Please enter a valid wavelength bandwidth.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 wavel = float(self.input_text_11.GetLineText(0))*wavl_conv
    #                 wavel_b = float(self.input_text_12.GetLineText(0))*wavl_conv
    #                 wavel_1 = wavel - wavel_b/2.0
    #                 wavel_2 = wavel + wavel_b/2.0
    #
    #
    #                 waven_1 = 1.0 / wavel_1
    #                 waven_2 = 1.0 / wavel_2
    #                 waven = (waven_1 + waven_2) / 2.0
    #                 waven_b = abs(waven_1 - waven_2)
    #
    #
    #                 freq_1 = 3 * 10 ** 8 / wavel_1
    #                 freq_2 = 3 * 10 ** 8 / wavel_2
    #                 freq = (freq_1 + freq_2) / 2.0
    #                 freq_b = abs(freq_1 - freq_2)
    #
    #
    #                 self.input_text_13.SetValue(str(round(wavel_1/wavl_conv, 3)))
    #                 self.input_text_14.SetValue(str(round(wavel_2/wavl_conv, 3)))
    #
    #                 self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
    #                 self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
    #                 self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
    #                 self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
    #
    #                 self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
    #                 self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
    #                 self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
    #                 self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #         else:
    #             if not is_number(self.input_text_13.GetLineText(0)):
    #                 status = 'Please enter a valid minimum wavelength.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             elif not is_number(self.input_text_14.GetLineText(0)):
    #                 status = 'Please enter a valid maximum wavelength.'
    #                 self.statusBar.SetStatusText(status, 0)
    #             else:
    #                 wavel_1 = float(self.input_text_13.GetLineText(0))*wavl_conv
    #                 wavel_2 = float(self.input_text_14.GetLineText(0))*wavl_conv
    #                 wavel = (wavel_1 + wavel_2) / 2.0
    #                 wavel_b = abs(wavel_1 - wavel_2)
    #
    #                 waven_1 = 1.0 / wavel_1
    #                 waven_2 = 1.0 / wavel_2
    #                 waven = (waven_1 + waven_2) / 2.0
    #                 waven_b = abs(waven_1 - waven_2)
    #
    #                 freq_1 = 3 * 10 ** 8 / wavel_1
    #                 freq_2 = 3 * 10 ** 8 / wavel_2
    #                 freq = (freq_1 + freq_2) / 2.0
    #                 freq_b = abs(freq_1 - freq_2)
    #
    #
    #                 self.input_text_11.SetValue(str(round(wavel/wavl_conv, 3)))
    #                 self.input_text_12.SetValue(str(round(wavel_b/wavl_conv, 3)))
    #
    #                 self.input_text_21.SetValue(str(round(freq/freq_conv, 3)))
    #                 self.input_text_22.SetValue(str(round(freq_b/freq_conv, 3)))
    #                 self.input_text_23.SetValue(str(round(freq_1/freq_conv, 3)))
    #                 self.input_text_24.SetValue(str(round(freq_2/freq_conv, 3)))
    #
    #                 self.input_text_31.SetValue(str(round(waven/wavn_conv, 3)))
    #                 self.input_text_32.SetValue(str(round(waven_b/wavn_conv, 3)))
    #                 self.input_text_33.SetValue(str(round(waven_1/wavn_conv, 3)))
    #                 self.input_text_34.SetValue(str(round(waven_2/wavn_conv, 3)))
    #                 status = 'Conversion completed.'
    #                 self.statusBar.SetStatusText(status, 0)
    #
    # def OnCombo1(self, event):
    #     status = "set current unit of wavelength to: " + self.combo1.GetValue()
    #     print(status)
    #     self.statusBar.SetStatusText(status, 0)
    #     self.current_wavl_unit = self.combo1.GetValue()
    #
    # def OnCombo2(self, event):
    #     status = "set current unit of frequency to: " + self.combo2.GetValue()
    #     print(status)
    #     self.statusBar.SetStatusText(status, 0)
    #     self.current_freq_unit = self.combo2.GetValue()
    #
    # def OnCombo3(self, event):
    #     status = "set current unit of wavenumber to: " + self.combo3.GetValue()
    #     print(status)
    #     self.statusBar.SetStatusText(status, 0)
    #     # self.label.SetLabel("set current unit of wavelength to: " + self.combo.GetValue())
    #     self.current_wavn_unit = self.combo3.GetValue()
    #
    def on_key(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.Conversion1(event)

        elif key == wx.WXK_NUMPAD_ENTER:
            self.Conversion1(event)

        else:
            event.Skip()

    def closeProgram(self):
        self.Close()



# Run the program
if __name__ == '__main__':
    app = wx.App()
    frame = OptCalFrame()
    app.MainLoop()
