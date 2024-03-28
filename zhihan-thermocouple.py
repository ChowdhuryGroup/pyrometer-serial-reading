import wx
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import serial
import time
from datetime import datetime


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            None, title="Max16675 Baking temperature GUI plotter", size=(800, 800)
        )

        # Panel to hold the plot
        self.panel = wx.Panel(self)

        # Create a figure and canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.panel, -1, self.figure)

        # Create multiple self.ax1es for subplots
        self.ax1 = self.figure.add_subplot(221)  # 2x2 grid, subplot 1
        self.ax2 = self.figure.add_subplot(222)  # 2x2 grid, subplot 2
        self.ax3 = self.figure.add_subplot(223)  # 2x2 grid, subplot 3
        self.ax4 = self.figure.add_subplot(224)  # 2x2 grid, subplot 4

        # Button to generate plot
        self.plot_button = wx.Button(self.panel, label="Generate Plot")
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_generate_plot)
        self.save_plot_button = wx.Button(self.panel, label="Save Plot")
        self.save_plot_button.Bind(wx.EVT_BUTTON, self.on_save_plot)

        # Button to save data
        self.save_data_button = wx.Button(self.panel, label="Save Data")
        self.save_data_button.Bind(wx.EVT_BUTTON, self.on_save_data)

        # Layout
        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(self.plot_button, 0, wx.EXPAND | wx.ALL, 5)
        box_sizer.Add(self.save_plot_button, 0, wx.EXPAND | wx.ALL, 5)
        box_sizer.Add(self.save_data_button, 0, wx.EXPAND | wx.ALL, 5)

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(box_sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(main_sizer)

    def on_generate_plot(self, event):
        ser = serial.Serial(
            "/dev/tty.usbmodem14101", 9600
        )  # Replace with the correct port

        # Initialize lists to store temperature data

        self.start_time = time.time()
        temps_1 = []
        temps_2 = []
        times = []

        # plt.ion()

        # sc1, = self.ax1.plot([], [], marker='o',label='Temperature 1')
        # sc2, = self.ax2.plot([], [], marker='o',label='Temperature 2')
        (self.line1,) = self.ax1.plot([], [], marker="o", label="Data Series 1")
        # self.ax1.add_line(self.line1)
        (self.line2,) = self.ax2.plot([], [], marker="o", label="Data Series 2")
        # self.ax2.add_line(self.line2)
        self.ax1.set_xlabel("Time/s")
        self.ax1.set_ylabel("Temperature (C)")
        self.ax1.legend()
        self.ax1.set_title("Temperature Readings from Max16675 Sensors")
        self.ax2.set_xlabel("Time/s")
        self.ax2.set_ylabel("Temperature (C)")
        self.ax2.legend()

        def update_plot():
            try:
                # Read data from Arduino
                data = ser.readline().strip().decode()
                print(data)
                # Split the string by '|' to separate temperature values
                temp_strings = data.split("|")

                if "Temperature 1" in data and "Temperature 2" in data:
                    # Extract the temperature values and convert them to floats
                    temp_1 = float(temp_strings[0].split(":")[1].strip().rstrip("°C"))
                    temp_2 = float(temp_strings[1].split(":")[1].strip().rstrip("°C"))
                    # Append data to lists
                    time_point = time.time() - self.start_time
                    # time_point=time_point
                    times.append(time_point)
                    temps_1.append(temp_1)
                    temps_2.append(temp_2)

                    # Update line objects with new data points
                    self.line1.set_data(times, temps_1)
                    self.line2.set_data(times, temps_2)

                    # Adjust axis limits
                    self.ax1.relim()
                    self.ax1.autoscale_view()
                    self.ax2.relim()
                    self.ax2.autoscale_view()
                    # Redraw canvas
                    self.canvas.draw()
                    wx.GetApp().Yield()
                    time_plot = time.time()
                    plot_elapse = time_plot - time_point
                    print(plot_elapse)
                    # Pause to allow time for plot to update
                else:
                    pass

            except KeyboardInterrupt:
                # Close serial connection on Ctrl+C
                ser.close()

        while True:
            update_plot()

        # Function to update the plot in real-time

    def on_save_plot(self, event):
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
                filepath = os.path.join(save_path, f"{current_datetime}" + filename)
            # Save the plot
            self.figure.savefig(filepath)
            filename_dialog.Destroy()
        dialog.Destroy()

    def on_save_data(self, event):
        print("1")


app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()
