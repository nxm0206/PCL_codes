# -*- coding: UTF-8 -*-
import wx


class OptCalFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='OptCal Version 0.0', size=(420, 620))
        self.panel = CalPanel(self)
        self.SetSizeHints(420, 620, 420, 620)
        self.Show()


class CalPanel(wx.Panel):

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
            Input_Quantity = ['Wavelength (nm)', 'Frequency (GHz)', 'Wavenumber (cm-1)']
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
            quantities = [r'Wavelength:', r'Frequency:', r'Wavenumber:']
            TextCtrl_list = ['input_text_11', 'input_text_12', 'input_text_13', 'input_text_14',
                             'input_text_21', 'input_text_22', 'input_text_23', 'input_text_24',
                             'input_text_31', 'input_text_32', 'input_text_33', 'input_text_34']
            quantities_label = [r'Mid', r'Span', r'Min', r'Max']

            # add content for each quantity box
            for i in range(len(quantities)):
                # initialize the box for quantity sizer
                quantity_Box = wx.StaticBox(self, -1, quantities[i])
                quantity_font = wx.Font(11, family=wx.ROMAN, style=wx.NORMAL, weight=wx.BOLD)
                quantity_Box.SetFont(quantity_font)
                quantity_Sizer = wx.StaticBoxSizer(quantity_Box, wx.HORIZONTAL)

                for j in range(len(quantities_label)):
                    # initialize the box for mid-span-Min-Max sizer
                    self.label_text = wx.StaticText(self, label=quantities_label[j], style=wx.ALIGN_CENTRE)
                    exec('self.' + TextCtrl_list[4 * i + j] + '= wx.TextCtrl(self)')
                    exec('self.' + TextCtrl_list[4 * i + j] + '.Disable()')
                    self.inputSizer = wx.BoxSizer(wx.HORIZONTAL)
                    self.inputSizer.Add(self.label_text, 0, wx.TOP | wx.EXPAND, 10)
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
                quantity_Sizer.Add(CS_Sizer, 1, wx.ALL | wx.EXPAND, 0)
                quantity_Sizer.Add(MM_Sizer, 1, wx.ALL | wx.EXPAND, 0)
                # add quantity box into bottomlayer Sizer
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
        if event.GetEventObject().GetLabel() == 'Frequency (GHz)':
            self.current_type = 'Freq'
        elif event.GetEventObject().GetLabel() == 'Wavenumber (cm-1)':
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
        if self.current_type == 'Freq':
            if self.current_input_type == 'Mid-Span':
                if not is_number(self.input_text_21.GetLineText(0)):
                    status = 'Please enter a valid center frequency.'
                    self.statusBar.SetStatusText(status, 0)
                elif not is_number(self.input_text_22.GetLineText(0)):
                    status = 'Please enter a valid frequency span.'
                    self.statusBar.SetStatusText(status, 0)
                else:
                    freq = float(self.input_text_21.GetLineText(0))
                    freq_b = float(self.input_text_22.GetLineText(0))
                    freq_1 = round(freq - freq_b / 2.0, 3)
                    freq_2 = round(freq + freq_b / 2.0, 3)

                    wavel_1 = round(3 * 10 ** 8 / freq_1, 3)
                    wavel_2 = round(3 * 10 ** 8 / freq_2, 3)
                    print(wavel_1)
                    print(wavel_2)
                    wavel = round((wavel_1 + wavel_2) / 2.0, 3)
                    wavel_b = round(abs(wavel_1 - wavel_2), 3)
                    print(wavel_b)

                    waven_1 = round(10 ** 7 / wavel_1, 3)
                    waven_2 = round(10 ** 7 / wavel_2, 3)
                    waven = round((waven_1 + waven_2) / 2.0, 3)
                    waven_b = round(abs(waven_1 - waven_2), 3)
                    print(wavel_b)

                    self.input_text_23.SetValue(str(freq_1))
                    self.input_text_24.SetValue(str(freq_2))

                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))
                    self.input_text_13.SetValue(str(wavel_1))
                    self.input_text_14.SetValue(str(wavel_2))

                    self.input_text_31.SetValue(str(waven))
                    self.input_text_32.SetValue(str(waven_b))
                    self.input_text_33.SetValue(str(waven_1))
                    self.input_text_34.SetValue(str(waven_2))
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
                    freq_1 = float(self.input_text_23.GetLineText(0))
                    freq_2 = float(self.input_text_24.GetLineText(0))
                    freq = round((freq_1 + freq_2) / 2.0, 3)
                    freq_b = round(abs(freq_1 - freq_2), 3)

                    wavel_1 = round(3 * 10 ** 8 / freq_1, 3)
                    wavel_2 = round(3 * 10 ** 8 / freq_2, 3)
                    print(wavel_1)
                    print(wavel_2)
                    wavel = round((wavel_1 + wavel_2) / 2.0, 3)
                    wavel_b = round(abs(wavel_1 - wavel_2), 3)
                    print(wavel_b)

                    waven_1 = round(10 ** 7 / wavel_1, 3)
                    waven_2 = round(10 ** 7 / wavel_2, 3)
                    waven = round((waven_1 + waven_2) / 2.0, 3)
                    waven_b = round(abs(waven_1 - waven_2), 3)
                    print(wavel_b)

                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))

                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))
                    self.input_text_13.SetValue(str(wavel_1))
                    self.input_text_14.SetValue(str(wavel_2))

                    self.input_text_31.SetValue(str(waven))
                    self.input_text_32.SetValue(str(waven_b))
                    self.input_text_33.SetValue(str(waven_1))
                    self.input_text_34.SetValue(str(waven_2))
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
                    waven = float(self.input_text_31.GetLineText(0))
                    waven_b = float(self.input_text_32.GetLineText(0))
                    waven_1 = round(waven - waven_b / 2.0, 3)
                    waven_2 = round(waven + waven_b / 2.0, 3)

                    wavel_1 = round(10 ** 7 / waven_1, 3)
                    wavel_2 = round(10 ** 7 / waven_2, 3)
                    wavel = round((wavel_1 + wavel_2) / 2.0, 3)
                    wavel_b = round(abs(wavel_1 - wavel_2), 3)

                    freq_1 = round(3 * 10 ** 8 / wavel_1, 3)
                    freq_2 = round(3 * 10 ** 8 / wavel_2, 3)
                    freq = round((freq_1 + freq_2) / 2.0, 3)
                    freq_b = round(abs(freq_1 - freq_2), 3)

                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))
                    self.input_text_13.SetValue(str(wavel_1))
                    self.input_text_14.SetValue(str(wavel_2))
                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))
                    self.input_text_23.SetValue(str(freq_1))
                    self.input_text_24.SetValue(str(freq_2))
                    self.input_text_33.SetValue(str(waven_1))
                    self.input_text_34.SetValue(str(wavel_2))
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
                    waven_1 = float(self.input_text_33.GetLineText(0))
                    waven_2 = float(self.input_text_34.GetLineText(0))
                    waven = round((waven_1 + waven_2) / 2.0, 3)
                    waven_b = round(abs(waven_1 - waven_2), 3)

                    wavel_1 = round(10 ** 7 / waven_1, 3)
                    wavel_2 = round(10 ** 7 / waven_2, 3)
                    wavel = round((wavel_1 + wavel_2) / 2.0, 3)
                    wavel_b = round(abs(wavel_1 - wavel_2), 3)

                    freq_1 = round(3 * 10 ** 8 / wavel_1, 3)
                    freq_2 = round(3 * 10 ** 8 / wavel_2, 3)
                    freq = round((freq_1 + freq_2) / 2.0, 3)
                    freq_b = round(abs(freq_1 - freq_2), 3)

                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))
                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))
                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))
                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))

                    self.input_text_31.SetValue(str(waven))
                    self.input_text_32.SetValue(str(waven_b))
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
                    wavel = float(self.input_text_11.GetLineText(0))
                    wavel_b = float(self.input_text_12.GetLineText(0))
                    wavel_1 = round(wavel - wavel_b / 2.0, 3)
                    wavel_2 = round(wavel + wavel_b / 2.0, 3)

                    waven_1 = round(10 ** 7 / wavel_1, 3)
                    waven_2 = round(10 ** 7 / wavel_2, 3)
                    waven = round((waven_1 + waven_2) / 2.0, 3)
                    waven_b = round(abs(waven_1 - waven_2), 3)

                    freq_1 = round(3 * 10 ** 8 / wavel_1, 3)
                    freq_2 = round(3 * 10 ** 8 / wavel_2, 3)
                    freq = round((freq_1 + freq_2) / 2.0, 3)
                    freq_b = round(abs(freq_1 - freq_2), 3)

                    self.input_text_13.SetValue(str(wavel_1))
                    self.input_text_14.SetValue(str(wavel_2))

                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))
                    self.input_text_23.SetValue(str(freq_1))
                    self.input_text_24.SetValue(str(freq_2))

                    self.input_text_31.SetValue(str(waven))
                    self.input_text_32.SetValue(str(waven_b))
                    self.input_text_33.SetValue(str(waven_1))
                    self.input_text_34.SetValue(str(waven_2))
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
                    wavel_1 = float(self.input_text_13.GetLineText(0))
                    wavel_2 = float(self.input_text_14.GetLineText(0))
                    wavel = round((wavel_1 + wavel_2) / 2.0, 3)
                    wavel_b = round(abs(wavel_1 - wavel_2), 3)

                    waven_1 = round(10 ** 7 / wavel_1, 3)
                    waven_2 = round(10 ** 7 / wavel_2, 3)
                    waven = round((waven_1 + waven_2) / 2.0, 3)
                    waven_b = round(abs(waven_1 - waven_2), 3)

                    freq_1 = round(3 * 10 ** 8 / wavel_1, 3)
                    freq_2 = round(3 * 10 ** 8 / wavel_2, 3)
                    freq = round((freq_1 + freq_2) / 2.0, 3)
                    freq_b = round(abs(freq_1 - freq_2), 3)

                    self.input_text_11.SetValue(str(wavel))
                    self.input_text_12.SetValue(str(wavel_b))

                    self.input_text_21.SetValue(str(freq))
                    self.input_text_22.SetValue(str(freq_b))
                    self.input_text_23.SetValue(str(freq_1))
                    self.input_text_24.SetValue(str(freq_2))

                    self.input_text_31.SetValue(str(waven))
                    self.input_text_32.SetValue(str(waven_b))
                    self.input_text_33.SetValue(str(waven_1))
                    self.input_text_34.SetValue(str(waven_2))
                    status = 'Conversion completed.'
                    self.statusBar.SetStatusText(status, 0)

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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


# Run the program
if __name__ == '__main__':
    app = wx.App()
    frame = OptCalFrame()
    app.MainLoop()
