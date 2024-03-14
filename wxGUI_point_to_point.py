#refine version of wxGUI.py
#transfer data points using queue

import wx
import os
import sys
import importlib.util
from io import StringIO
import contextlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from datetime import datetime
import photrix
from main_point_to_point import Connect
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from queue import Queue

def generate_data(instance):
        run=Connect()
        run.generate_data(instance.data_queue_time, instance.data_queue_PDcurrent)
class MyFrame(wx.Frame):
    
    def __init__(self):
        super().__init__(None, title="Plot Display", size=(800, 800))
        self.figure = None
        self.canvas = None
        # Panel to hold the plot
        panel = wx.Panel(self)
        
        # Button to generate plot
        self.plot_button = wx.Button(panel, label="Generate Plot")
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_generate_plot)
        self.select_button = wx.Button(panel, label="Select File")
        self.select_button.Bind(wx.EVT_BUTTON, self.on_select)
        self.stop_button = wx.Button(panel, label="Stop")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        self.plot_panel = wx.Panel(panel)
        #self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.save_button = wx.Button(panel, label="Save Plot")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_plot)
        self.save_button.Disable()  # Disable initially until plot is generated
        self.save_data_button = wx.Button(panel, label="Save Data")
        self.save_data_button.Bind(wx.EVT_BUTTON, self.on_save_data)
        self.save_data_button.Disable()  # Disable initially until plot is generated

        # Text control to display file name
        self.file_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
          # Sizer for layout
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.stop_button, 0, wx.ALL | wx.CENTER, 5)
        button_sizer.Add(self.plot_button, 0, wx.ALL | wx.CENTER, 5)
        button_sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)
        button_sizer.Add(self.save_data_button, 0, wx.ALL | wx.CENTER, 5)

        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer.Add(self.file_text, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.select_button, 0, wx.EXPAND | wx.CENTER, 5)
        main_sizer.Add(text_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)
       
        # Add a panel to hold the plot
        main_sizer.Add(self.plot_panel, 1, wx.EXPAND)  # Add plot panel to main sizer

        panel.SetSizer(main_sizer)

        class MyClass:
            def __init__(self):
                self.data_queue_time = Queue.queue()
                self.data_queue_PDcurrent = Queue.queue() 
        self.my_instance = MyClass()
        self.thread = threading.Thread(target=generate_data, args=(self.my_instance,))
        self.thread.daemon = True
        self.thread.start()
        
    
        # Start a thread for data collection
        

    def on_select(self, event):
        wildcard = "All files (*.*)|*.*"  # You can customize the file types here
        dialog = wx.FileDialog(self, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.file_text.SetValue(path)  # Set the file path to the text control
        dialog.Destroy()
        # Sizer for layout
    
    
    def get_fitting_function(self,PDcurrent):
        fitting_code_path = self.file_text.GetValue()

        # Load the module from the file path
        spec = importlib.util.spec_from_file_location("fitting_code", fitting_code_path)
        fitting_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fitting_module)
        return fitting_module.f(PDcurrent)
       

    def on_generate_plot(self, event):
        self.save_button.Enable()
        self.save_data_button.Enable()
        '''# Path to the Python file containing the plotting code
        plotting_code_path = self.file_text.GetValue()

        # Load the module from the file path
        spec = importlib.util.spec_from_file_location("plotting_code", plotting_code_path)
        plotting_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plotting_module)
        '''
        # Create a Matplotlib figure and canvas
        self.figure = Figure()  # Set initial figure size
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.plot_panel, -1, self.figure)
        self.axes.set_xlabel('Time/s')
        self.axes.set_ylabel('Fitted Temperature/C from pyrometer photodiode current')
        '''if self.figure:
            self.figure.clear()
            self.canvas.Destroy()'''

        # Generating the plot
        #with contextlib.redirect_stdout(None):  # Redirect stdout to suppress Matplotlib messages
        while True:     
            #print(self.my_instance.data_queue_PDcurrent)
        
            
    
    # Get the most recent data points for plotting
            self.PDcurrents=[]
            self.times=[]
            self.PDcurrent_point=self.my_instance.data_queue_PDcurrent.get()
            self.time_point=self.my_instance.data_queue_time.get()
            self.fitted_temp = [self.get_fitting_function(i) for i in self.times]
            if self.figure:
                self.axes.clear()
                self.axes.scatter(self.times, self.fitted_temp)
                self.canvas.draw()
                
                #self.axes.scatter(self.my_instance.data_queue_time,self.fitted_temp)
                self.canvas.draw()
            
            #print(self.my_instance.data_queue_PDcurrent)
            #print(self.my_instance.data_queue_time)
            time.sleep(0.01)
        
        
        #self.canvas.draw()  

    def on_resize(self, event):
        if self.canvas:
            size = self.GetClientSize()
            self.canvas.SetSize(size)
            self.figure.set_size_inches(size[0]/self.canvas.GetContentScaleFactor()/self.figure.get_dpi(),
                                        size[1]/self.canvas.GetContentScaleFactor()/self.figure.get_dpi())
            self.canvas.draw()
        # Resize the canvas when the window size changes
            
    def on_stop(self, event):
        pyro = photrix.pyrometer("COM1")
        pyro.exit_continuous_mode()
        
    def on_save_plot(self, event):
    # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"{current_datetime}_plot.png"  # Default filename
    
    # Open a directory dialog to choose the save path
        dialog = wx.DirDialog(self, "Choose Save Location", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()
        
        # Prompt the user for the file name
            filename_dialog = wx.TextEntryDialog(self, "Enter file name:", "Save Plot", default_filename)
            if filename_dialog.ShowModal() == wx.ID_OK:
                filename = filename_dialog.GetValue()
                filepath = os.path.join(save_path, f"{current_datetime}"+filename+'.png')
            # Save the plot
            self.figure.savefig(filepath)
            filename_dialog.Destroy()
        dialog.Destroy()

    def on_save_data(self,event):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"{current_datetime}_data.txt"  # Default filename
    
    # Open a directory dialog to choose the save path
        dialog = wx.DirDialog(self, "Choose Save Location", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()
        
        # Prompt the user for the file name
            filename_dialog = wx.TextEntryDialog(self, "Enter file name:", "Save Data", default_filename)
            if filename_dialog.ShowModal() == wx.ID_OK:
                filename = filename_dialog.GetValue()
                filepath = os.path.join(save_path, f"{current_datetime}"+filename+'.txt')
                
            with open(filepath, 'w') as file:
                file.write("Time/C,Photodiode current/A,Fitted Temperature/C\n")
                for i in range(len(self.my_instance.data_queue_time)):
                    file.write(f"{self.my_instance.data_queue_time[i]},{self.my_instance.data_queue_PDcurrent[i]},{self.fitted_temp[i]}\n")
                
            filename_dialog.Destroy()
        dialog.Destroy()
        

    def on_close(self, event):
        #self.thread.join()  # Wait for the thread to finish
        self.Destroy()

app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()

