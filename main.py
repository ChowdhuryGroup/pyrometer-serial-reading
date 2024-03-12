# pyrometer serial reading ieee754
import struct
import photrix


# Configure the serial port
def decode_ieee754(data: bytes):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack("f", data)[0]

def plotting_callback():
    return


if __name__ == "__main__":
    # Pyrometer is controlled by a mix of manual serial commands and MODBUS commands

    pyro = photrix.pyrometer("COM1")
    # Should implement buffered reading, but that's for later

    temperature_bytes = bytearray()
    current_bytes = bytearray()
    electronics_temperature_bytes = bytearray()
    diode_temperature_bytes = bytearray()

    print("Starting stream read...")
    while True:
        header_byte = pyro.get_unescaped_byte()
        if header_byte == b'\x80':
            pyro.get_unescaped_byte()
        elif header_byte == b'\x81':
            temperature_bytes = bytearray()
            for _ in range(4):
                temperature_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b'\x82':
            current_bytes = bytearray()
            for _ in range(4):
                current_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b'\x83':
            temperature_bytes = bytearray()
            current_bytes = bytearray()
            for _ in range(4):
                temperature_bytes.extend(pyro.get_escaped_byte())
            for _ in range(4):
                current_bytes.extend(pyro.get_escaped_byte())
        elif header_byte == b'\x84':
            electronics_temperature_bytes = bytearray()
            diode_temperature_bytes = bytearray()
            for _ in range(4):
                electronics_temperature_bytes.extend(pyro.get_escaped_byte())
            for _ in range(4):
                diode_temperature_bytes.extend(pyro.get_escaped_byte())
        
        output_string = ''
        if temperature_bytes != b'':
            output_string += f'Temperature (C): {decode_ieee754(temperature_bytes):+e} '
        if current_bytes != b'':
            output_string += f'Current (A): {decode_ieee754(current_bytes):+e} '
        if electronics_temperature_bytes != b'':
            output_string += f'Electronics Temp. (C): {decode_ieee754(electronics_temperature_bytes):+e} '
        if diode_temperature_bytes != b'':
            output_string += f'Diode Temp. (C): {decode_ieee754(diode_temperature_bytes):+e}'
        print(output_string)
