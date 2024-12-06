# pyrometer serial reading ieee754
import struct
import photrix
import time
import datetime
import atexit
import SS_fitting


def decode_ieee754(data: bytes):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack(">f", data)[0]


if __name__ == "__main__":
    # Pyrometer is controlled by a mix of manual serial commands and MODBUS commands

    pyro = photrix.pyrometer("COM1")
    # Should implement buffered reading, but that's for later

    data_file = open(f"data/{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.tsv", "w")
    atexit.register(data_file.close)
    data_file.write(
        "Time(s)\tPhotodiode_Current(A)\tFit_Temperature(C)\tSputter_Gun_Temperature(C)\n"
    )

    temperature_bytes = bytearray()
    current_bytes = bytearray()
    electronics_temperature_bytes = bytearray()
    diode_temperature_bytes = bytearray()
    current = -1
    fit_temperature = -1
    sputter_temperature = -1

    print("Starting stream read...")
    start_time = time.time()
    i = 0
    while True:
        header_byte = pyro.get_unescaped_byte()
        if header_byte == b"\x80":
            pyro.get_unescaped_byte()
        elif header_byte == b"\x81":
            temperature_bytes = bytearray()
            for _ in range(4):
                temperature_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b"\x82":
            current_bytes = bytearray()
            for _ in range(4):
                current_bytes.extend(pyro.get_escaped_byte())
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
            for _ in range(4):
                diode_temperature_bytes.extend(pyro.get_escaped_byte())
        pyro.connection.reset_input_buffer()

        output_string = ""
        measurement_time = time.time() - start_time
        output_string += f"Time (s): {measurement_time:6.2f} "

        if current_bytes != b"":
            current = decode_ieee754(current_bytes)
            # TemperaSure Sets negative values to 1.e-17, and Zhihan wants to replicate this behavior
            if current < 0:
                current = 1.0e-17
            output_string += f"Current (A): {current:+e} "
            fit_temperature = SS_fitting.temperature_from_current(current)
            output_string += f"Fit Temperature (C): {fit_temperature:+e}"

        if False:
            if temperature_bytes != b"":
                temperature = decode_ieee754(temperature_bytes)
                output_string += f"Temperature (C): {temperature:+e} "
            if electronics_temperature_bytes != b"":
                output_string += f"Electronics Temp. (C): {decode_ieee754(electronics_temperature_bytes):+e} "
            if diode_temperature_bytes != b"":
                output_string += (
                    f"Diode Temp. (C): {decode_ieee754(diode_temperature_bytes):+e}"
                )

        output_string += f" Sputter Gun Temperature (C): {sputter_temperature:+e}"

        print(output_string)
        data_file.write(
            f"{measurement_time}\t{current}\t{fit_temperature}\t{sputter_temperature}\n"
        )

        i += 1
