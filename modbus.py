import serial


# Define the CRC-16/MODBUS function
def modbus_crc(msg: bytes) -> bytes:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="little")


def send_modbus_command(
    connection: serial.Serial, function: bytes, address: bytes, value: bytes
):
    if (len(function) != 1) or (len(address) != 2) or (len(value) != 2):
        raise ValueError("Number of bytes in arguments is incorrect")
    command_bytes = b"".join([b"\x00", function, address, value])
    command_bytes += modbus_crc(command_bytes)
    connection.write(command_bytes)


def set_register(connection: serial.Serial, address: bytes, value: bytes) -> bytes:
    send_modbus_command(connection, b"\x06", address, value)
    return connection.read(1)


def set_coil(connection: serial.Serial, address: bytes, value: bytes) -> bytes:
    send_modbus_command(connection, b"\x05", address, value)
    return connection.read(1)
