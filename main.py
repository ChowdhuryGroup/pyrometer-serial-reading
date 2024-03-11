# pyrometer serial reading ieee754
import serial
import struct
import atexit
import photrix
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.framer import Framer
import time


# Configure the serial port
def decode_ieee754(data):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack("f", data)[0]


if __name__ == "__main__":
    # Pyrometer is controlled by a mix of manual serial commands and MODBUS commands

    pyro = photrix.pyrometer("COM1")
    pyro.ping()
