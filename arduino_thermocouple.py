import serial
import atexit


class Arduino:
    def __init__(self, port: str):
        self.connection = serial.Serial(port, baudrate=9600)
        atexit.register(self.connection.close)

    def get_temperatures(self) -> tuple[float, float]:
        data = self.connection.readline().strip().decode()
        temp_strings = data.split("|")
        temp_1 = float(temp_strings[0].split(":")[1].strip().rstrip("°C"))
        temp_2 = float(temp_strings[1].split(":")[1].strip().rstrip("°C"))
        return temp_1, temp_2
