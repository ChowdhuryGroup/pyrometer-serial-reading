import struct
import photrix
import time
import datetime
import ss_fit
import atexit
import gui

use_GUI = False


def decode_ieee754(data: bytes):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack(">f", data)[0]


if use_GUI:
    gui = gui.MyFrame()

# Pyrometer is controlled by a mix of manual serial commands and MODBUS commands

data_file = open(f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.tsv", "w")
atexit.register(data_file.close)
data_file.write(
    "Time(s)\tPhotodiode_Current(A)\tFit_Temperature(C)\tElectronics_Temperature(C)\tPhotodiode_Temperature\n"
)

pyro = photrix.pyrometer("COM1")
# Should implement buffered reading, but that's for later

temperature_bytes = bytearray()
current_bytes = bytearray()
electronics_temperature_bytes = bytearray()
diode_temperature_bytes = bytearray()

start_time = time.time()
times = []
currents = []
fit_temperatures = []
electronics_temperatures = []
diode_temperatures = []

print("Starting stream read...")
while True:
    header_byte = pyro.get_unescaped_byte()
    if header_byte == b"\x80":
        pyro.get_unescaped_byte()
    elif header_byte == b"\x81":
        temperature_bytes = bytearray()
        for _ in range(4):
            temperature_bytes.extend(pyro.get_escaped_byte())
        temperature = decode_ieee754(temperature_bytes)
    elif header_byte == b"\x82":
        current_bytes = bytearray()
        for _ in range(4):
            current_bytes.extend(pyro.get_escaped_byte())
        current = decode_ieee754(current_bytes)
    elif header_byte == b"\x83":
        temperature_bytes = bytearray()
        current_bytes = bytearray()
        for _ in range(4):
            temperature_bytes.extend(pyro.get_escaped_byte())
        for _ in range(4):
            current_bytes.extend(pyro.get_escaped_byte())
    elif header_byte == b"\x84":
        electronics_temperature_bytes = bytearray()
        diode_temperature_bytes = bytearray()
        for _ in range(4):
            electronics_temperature_bytes.extend(pyro.get_escaped_byte())
        electronics_temperature = decode_ieee754(electronics_temperature_bytes)
        for _ in range(4):
            diode_temperature_bytes.extend(pyro.get_escaped_byte())
        diode_temperature = decode_ieee754(diode_temperature_bytes)

    fit_temperature = ss_fit.temperature_from_current(current)

    output_string = ""
    if temperature_bytes != b"":
        output_string += f"Internal Temperature (C): {temperature:+e} "
    output_string += f"Fit Temperature (C): {fit_temperature:+e}"
    if current_bytes != b"":
        output_string += f"Current (A): {current:+e} "

    if False:
        if electronics_temperature_bytes != b"":
            output_string += f"Electronics Temp. (C): {electronics_temperature:+e} "
        if diode_temperature_bytes != b"":
            output_string += f"Diode Temp. (C): {diode_temperature:+e}"
    print(output_string)

    times.append(time.time() - start_time)
    currents.append(current)
    fit_temperatures.append(fit_temperature)
    electronics_temperatures.append(electronics_temperature)
    diode_temperatures.append(diode_temperature)

    data_file.write(
        f"{times[-1]}\t{current}\t{fit_temperature}\t{electronics_temperature}\t{diode_temperature}\n"
    )
