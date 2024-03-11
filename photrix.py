import serial
import atexit
import modbus
import time

command_start = b"\x02"
command_end = b"\x03"
positive_acknowledge = b"\x06"

start_sending_temperature = b"\x31"
stop_sending_temperature = b"\x30"

# PhotriX powers up by default in MODBUS mode
enable_modbus_mode = b"\x4d"

command_register = b"\x80\x00"
ping_function = b"\x70\x00"

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
        self.connection = serial.Serial(
            baudrate=115200,
            timeout=2,
            bytesize=8,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )
        self.connection.port = "COM1"
        atexit.register(self.connection.close)

        self.open_serial_connection()
        # Assume probe might be in continuous mode, reboot to get it into MODBUS mode
        # This is done because MODBUS is more controlled, and the probe waits for commands
        self.reboot()

    def reboot(self):
        self.connection.write(bytes([0x02, 0x56, 0x56, 0xED, 0xDE, 0x4B, 0x01, 0x03]))
        self.connection.write(bytes([0x02, 0x56, 0x56, 0x03]))
        self.connection.close()
        time.sleep(1)
        self.open_serial_connection()

    def open_serial_connection(self):
        # This is equivalent to IOCTL_SERIAL_CLR_RTS, and is essential for probe to respond
        self.connection.rts = 0
        self.connection.open()

    def ping(self) -> bool:
        result = modbus.set_register(self.connection, command_register, ping_function)
        print(result)
        if result == positive_acknowledge:
            return True

    def determine_baud(self) -> int:
        possible_bauds = [9600, 19200, 38400, 57600, 115200]
        for baud in possible_bauds:
            print(baud)
