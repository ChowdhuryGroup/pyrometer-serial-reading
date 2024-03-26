import serial
import atexit
import time
from serial.tools.list_ports import comports


class Arduino:
    def __init__(self, port: str):
        try:
            self.connection = serial.Serial(port, baudrate=9600)
        except serial.SerialException:
            print("Arduino not Connected")
        self.connection.timeout = 5
        time.sleep(5)
        print(f"Connected to arduino on port {port}")
        atexit.register(self.connection.close)

    def get_temperatures(self) -> tuple[float, float]:
        self.connection.reset_input_buffer()
        self.connection.write(b"r")
        line = self.connection.readline()
        data = line.decode().strip()

        temp_strings = data.split("|")
        temp_1 = float(temp_strings[0].split(":")[1].strip().rstrip("°C"))
        temp_2 = float(temp_strings[1].split(":")[1].strip().rstrip("°C"))
        return temp_1, temp_2


if __name__ == "__main__":
    test = Arduino("COM4")
    while True:
        temp_1, temp_2 = test.get_temperatures()
        print(f"Temperature 1: {temp_1} Temperature 2: {temp_2}")
