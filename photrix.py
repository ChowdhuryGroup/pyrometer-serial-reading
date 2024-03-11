from pymodbus.client.serial import ModbusSerialClient
from pymodbus.framer import Framer
import serial
import atexit


# Define the CRC-16/MODBUS function
def modbus_crc(msg: str) -> int:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="little")


crc = modbus_crc(b"\x00\x06\x80\x00\x70\x00")
print(b"\x00\x01" + crc)
input()
MODBUS, CONTINUOUS = (0, 1)

command_start = b"\x02"
command_end = b"\x03"
positive_acknowledge = b"\x06"

start_sending_temperature = b"\x31"
stop_sending_temperature = b"\x30"

# PhotriX powers up by default in MODBUS mode
enable_modbus_mode = b"\x4d"

command_register = 0x8000
ping_function = 0x7000

# When PhotriX sensor powers up, wait 6 seconds and remove any buffer from that time

## escape characters (due to variable length packets)
escape_character = b"\x80"
temperature_header = b"\x81"  # 4 data bytes
current_header = b"\x82"  # 4 data bytes
temperature_current_header = b"\x83"  # 8 data bytes
ambient_temperature_header = b"\x84"  # 8 data bytes


class pyrometer:

    def __init__(self, port: str):
        # Pyrometer is controlled by a mix of manual serial commands and MODBUS commands

        # Configure the serial port
        self.serial_connection = serial.Serial(
            baudrate=115200,
            timeout=2,
            bytesize=8,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )

        self.serial_connection.port = "COM1"
        atexit.register(self.serial_connection.close)

        # Configure the MODBUS client
        self.modbus_connection = ModbusSerialClient(
            port="COM1", baudrate=115200, parity="N", stopbits=1, framer=Framer.RTU
        )
        atexit.register(self.modbus_connection.close)

        # Assume probe might be in continuous mode, reboot to get it into MODBUS mode
        # This is done because MODBUS is more controlled, and the probe waits for commands
        self.switch_to_continuous_mode()
        self.reboot()

    def reboot(self):
        if self.mode == CONTINUOUS:
            self.serial_connection.write(
                bytes([0x02, 0x56, 0x56, 0xED, 0xDE, 0x4B, 0x01, 0x03])
            )
            self.serial_connection.write(bytes([0x02, 0x56, 0x56, 0x03]))

    def open_serial_connection(self):
        # This is equivalent to IOCTL_SERIAL_CLR_RTS, and is essential for probe to respond
        self.serial_connection.rts = 0
        self.serial_connection.open()

    def open_modbus_connection(self):
        self.modbus_connection.connect()
        self.modbus_connection.socket.rts = 0

    def switch_to_continuous_mode(self):
        self.modbus_connection.close()
        self.open_serial_connection()
        self.mode = CONTINUOUS

    def switch_to_modbus_mode(self):
        self.serial_connection.close()
        self.open_modbus_connection()
        self.mode = MODBUS

    def ping(self) -> bool:
        self.switch_to_modbus_mode()
        result = self.modbus_connection.write_register(command_register, ping_function)
        print(result)
        if result == positive_acknowledge:
            return True

    def determine_baud(self) -> int:
        self.switch_to_modbus_mode()
        possible_bauds = [9600, 19200, 38400, 57600, 115200]
        for baud in possible_bauds:
            print(baud)
