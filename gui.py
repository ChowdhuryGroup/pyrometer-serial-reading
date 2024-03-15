# refine version of wxGUI.py
# transfer data points using queue

import wx
import os
import importlib.util
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from datetime import datetime
import photrix
import threading
import queue


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Plot Display", size=(800, 800))
        self.figure = None
        self.canvas = None
        # Panel to hold the plot
        panel = wx.Panel(self)

        # Button to generate plot
        self.plot_button = wx.Button(panel, label="Generate Plot")
        self.plot_button.Bind(wx.EVT_BUTTON, self.generate_plot_callback)
        self.select_button = wx.Button(panel, label="Select File")
        self.select_button.Bind(wx.EVT_BUTTON, self.select_file_callback)
        self.stop_button = wx.Button(panel, label="Stop Collection")
        self.stop_button.Bind(wx.EVT_BUTTON, self.stop_collection_callback)
        self.plot_panel = wx.Panel(panel)
        # self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.save_button = wx.Button(panel, label="Save Plot")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_plot_callback)
        self.save_button.Disable()  # Disable initially until plot is generated
        self.save_data_button = wx.Button(panel, label="Save Data")
        self.save_data_button.Bind(wx.EVT_BUTTON, self.save_data_callback)
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

        self.data_queue_time = queue.Queue()
        self.data_queue_PDcurrent = queue.Queue()

        app = wx.App()
        frame = MyFrame()
        frame.Show()
        app.MainLoop()

    def select_file_callback(self, event):
        wildcard = "All files (*.*)|*.*"  # You can customize the file types here
        dialog = wx.FileDialog(
            self,
            "Choose a file",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.file_text.SetValue(path)  # Set the file path to the text control
        dialog.Destroy()
        # Sizer for layout

    def get_fitting_function(self, PDcurrent):
        fitting_code_path = self.file_text.GetValue()

        # Load the module from the file path
        spec = importlib.util.spec_from_file_location("fitting_code", fitting_code_path)
        fitting_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fitting_module)
        return fitting_module.f(PDcurrent)

    def update_plot(self, time_point, PDcurrent_point):
        if self.figure:
            self.axes.clear()
            self.axes.set_xlabel("Time/s")
            self.axes.set_ylabel(
                "Fitted Temperature/C from pyrometer photodiode current"
            )

        # Add the new data points to the plot
        self.axes.scatter(time_point, PDcurrent_point)

        # Optionally, you can add labels, title, or any other plot customization here

        # Redraw the canvas to update the plot
        self.canvas.draw()

    def plot_data(self):
        while True:
            try:
                # Get the most recent data points from the queues
                time_point = self.data_queue_time.get()  # Adjust timeout as needed
                PDcurrent_point = (
                    self.data_queue_PDcurrent.get()
                )  # Adjust timeout as needed
                self.times.append(time_point)
                if not self.elapse_time:
                    self.elapse_time.append(0)
                else:
                    self.elapse_time.append(
                        self.elapse_time[-1] + time_point - self.times[-2]
                    )
                self.PDcurrents.append(PDcurrent_point)
                fitted_temp_point = self.get_fitting_function(PDcurrent_point)
                self.fitted_temp.append(fitted_temp_point)
                # Update the plot with the new data points
                self.update_plot(self.elapse_time, self.fitted_temp)
            except queue.Empty:
                pass  # Continue if the queue is empty

    def generate_plot_callback(self, event):
        self.save_button.Enable()
        self.save_data_button.Enable()

        # Create a Matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 8))  # Set initial figure size
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.plot_panel, -1, self.figure)

        self.plot_thread = threading.Thread(target=self.generate_data)
        self.plot_thread.daemon = True
        self.plot_thread.start()

        # Start the plotting thread
        self.plot_thread = threading.Thread(target=self.plot_data)
        self.plot_thread.daemon = True
        self.plot_thread.start()

        # Generating the plot
        # with contextlib.redirect_stdout(None):  # Redirect stdout to suppress Matplotlib messages

        # self.canvas.draw()

    def on_resize(self, event):
        if self.canvas:
            size = self.GetClientSize()
            self.canvas.SetSize(size)
            self.figure.set_size_inches(
                size[0] / self.canvas.GetContentScaleFactor() / self.figure.get_dpi(),
                size[1] / self.canvas.GetContentScaleFactor() / self.figure.get_dpi(),
            )
            self.canvas.draw()
        # Resize the canvas when the window size changes

    def stop_collection_callback(self, event):
        pyro = photrix.pyrometer("COM1")
        pyro.exit_continuous_mode()

    def save_plot_callback(self, event):
        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"{current_datetime}_plot.png"  # Default filename

        # Open a directory dialog to choose the save path
        dialog = wx.DirDialog(
            self,
            "Choose Save Location",
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
        )
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()

            # Prompt the user for the file name
            filename_dialog = wx.TextEntryDialog(
                self, "Enter file name:", "Save Plot", default_filename
            )
            if filename_dialog.ShowModal() == wx.ID_OK:
                filename = filename_dialog.GetValue()
                filepath = os.path.join(
                    save_path, f"{current_datetime}" + filename + ".png"
                )
            # Save the plot
            self.figure.savefig(filepath)
            filename_dialog.Destroy()
        dialog.Destroy()

    def save_data_callback(self, event):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"{current_datetime}_data.txt"  # Default filename

        # Open a directory dialog to choose the save path
        dialog = wx.DirDialog(
            self,
            "Choose Save Location",
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
        )
        if dialog.ShowModal() == wx.ID_OK:
            save_path = dialog.GetPath()

            # Prompt the user for the file name
            filename_dialog = wx.TextEntryDialog(
                self, "Enter file name:", "Save Data", default_filename
            )
            if filename_dialog.ShowModal() == wx.ID_OK:
                filename = filename_dialog.GetValue()
                filepath = os.path.join(
                    save_path, f"{current_datetime}" + filename + ".txt"
                )

            with open(filepath, "w") as file:
                file.write("Time/C,Photodiode current/A,Fitted Temperature/C\n")
                for i in range(len(self.times)):
                    file.write(
                        f"{self.times[i]},{self.PDcurrents[i]},{self.fitted_temp[i]}\n"
                    )

            filename_dialog.Destroy()
        dialog.Destroy()
