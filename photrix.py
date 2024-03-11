import serial
import atexit
import modbus
import time

COMMAND_START = b"\x02"
COMMAND_END = b"\x03"
POSITIVE_ACKNOWLEDGE = b"\x06"

# PhotriX powers up by default in MODBUS mode
ENABLE_MODBUS_MODE = b"\x4d\x4d"

START_TEMPERATURE = b"\x31\x31"  # may not be right, haven't gotten to work
STOP_TEMPERATURE = b"\x30\x30"
START_COMBINED = b"\x56\x56"

command_register = b"\x80\x00"
ping_function = b"\x70\x00"

## escape characters (due to variable length packets)
ESCAPE = b"\x80"
TEMPERATURE_HEADER = b"\x81"  # 4 data bytes
CURRENT_HEADER = b"\x82"  # 4 data bytes
COMBINED_HEADER = b"\x83"  # 8 data bytes
AMBIENT_HEADER = b"\x84"  # 8 data bytes


class pyrometer:

    def __init__(self, port: str):
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

        # Assume probe might be in continuous mode, reboot to get it into MODBUS mode
        # This is done because MODBUS is more controlled, and the probe waits for commands
        self.open_serial_connection()
        self.reboot()

        self.baud = self.determine_baud()
        print(f"Baud successfully determined: {self.baud}")

    def reconnect(self, baudrate=None):
        if baudrate == None:
            self.connection.close()
            self.open_serial_connection()
        else:
            self.connection.close()
            self.connection.baudrate = baudrate
            self.open_serial_connection()

    def reboot(self):
        self.connection.write(bytes([0x02, 0x56, 0x56, 0xED, 0xDE, 0x4B, 0x01, 0x03]))
        self.connection.write(bytes([0x02, 0x56, 0x56, 0x03]))
        time.sleep(2)

    def open_serial_connection(self):
        # This is equivalent to IOCTL_SERIAL_CLR_RTS, and is essential for probe to respond
        # By default, pyserial sets RTS pin high
        self.connection.rts = 0
        self.connection.open()

    def ping(self) -> bool:
        result = modbus.set_register(self.connection, command_register, ping_function)
        if result == POSITIVE_ACKNOWLEDGE:
            print("Probe responded to ping!")
            return True
        else:
            print("Probe didn't respond to ping...")
            return False

    def determine_baud(self) -> int:
        possible_bauds = [115200, 9600, 19200, 38400, 57600]
        for baud in possible_bauds:
            print(f"Testing for connection with {baud} baud")
            self.reconnect(baud)
            if self.ping():
                return baud
        print("None of the possible bauds worked, are you sure the connection is good?")

    def continuous_mode_command(self, command_bytes: bytes):
        bytes_to_send = b"".join([COMMAND_START, command_bytes, COMMAND_END])
        self.connection.write(bytes_to_send)

    def continuous_mode_read(self) -> bytes:
        result = self.connection.read_until(b"\x03")
        return result[1:-1]

    def enter_continuous_mode(self):
        modbus.set_coil(self.connection, b"\x00\x13", b"\x00\x00")

    def exit_continuous_mode(self):
        self.continuous_mode_command(ENABLE_MODBUS_MODE)

    def start_sending_combined(self):
        self.continuous_mode_command(START_COMBINED)
        result = self.continuous_mode_read()
        print(result.hex())

    def start_sending_temperature(self) -> bool:
        self.continuous_mode_command(START_TEMPERATURE)
        result = self.connection.read(1)
        if result == POSITIVE_ACKNOWLEDGE:
            print("Starting to send temperature packets")
            return True
        else:
            print("Failed to start sending temperature packets")
            return False

    def stop_sending_temperature(self) -> bool:
        self.continuous_mode_command(STOP_TEMPERATURE)
        result = self.connection.read(1)
        if result == POSITIVE_ACKNOWLEDGE:
            print("Stopping sending temperature packets")
            return True
        else:
            print("Failed to stop sending temperature packets")
            return False
