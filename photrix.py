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

        # Assume probe might be in continuous mode, reboot to get it into MODBUS mode
        # This is done because MODBUS is more controlled, and the probe waits for commands
        self.open_serial_connection()
        atexit.register(self.connection.close)
        atexit.register(self.exit_continuous_mode)
        self.reboot()

        self.determine_baud()
        #print(f"Baud successfully determined: {self.baud}")

        print("Replicating TemperaSure startup conversation")
        self.startup_conversation()

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
        self.connection.reset_input_buffer()
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
        time.sleep(0.1)
        result = self.connection.read_all()
        if result == b'':
            return False
        if result[-1] != 3:
            input(f"The result should end with 0x03, but is {result[-1].to_bytes(1,'big').hex()}")
        return result[1:-1]

    def enter_continuous_mode(self):
        modbus.set_coil(self.connection, b"\x00\x13", b"\x00\x00")

    def exit_continuous_mode(self):
        self.continuous_mode_command(ENABLE_MODBUS_MODE)

    def startup_conversation(self):
        commands = [
            b"\x56\x56",
            b"\x50\x50",
            b"\x56\x56\xED\xDE\x4B\x01",
            b"\x53\x53",
            b"\x50\x50",
            b"\x56\x56",
            b"\x50\x50",
            b"\x52\x01\x00\x00\x08\x5B",
            b"\x56\x56",
            b"\x50\x50",
            b"\x52\x10\x02\x00\x00\x08\x58",
            b"\x52\x01\x00\x08\xFF\xA4",
            b"\x52\x01\x01\x07\xFF\xAA",
            b"\x52\x01\x10\x02\x06\xFF\xA8",
            b"\x52\x01\x10\x03\x05\xFF\xAA",
            b"\x52\x01\x04\x04\xFF\xAC",
            b"\x52\x01\x05\x10\x03\xFF\xAA",
            b"\x52\x01\x06\x10\x02\xFF\xA8",
            b"\x52\x01\x07\x01\xFF\xAA",
            b"\x52\x01\x08\x00\xFF\xA4",
            b"\x52\x01\x08\xFF\xFF\x5B",
            b"\x52\x01\x09\xFE\xFF\x5B",
            b"\x52\x01\x0A\xFD\xFF\x5B",
            b"\x52\x01\x0B\xFC\xFF\x5B",
            b"\x52\x01\x0C\xFB\xFF\x5B",
            b"\x52\x01\x0D\xFA\xFF\x5B",
            b"\x52\x01\x0E\xF9\xFF\x5B",
            b"\x52\x01\x0F\xF8\xFF\x5B",
            b"\x52\x01\x10\x10\xF7\xFF\x4B",
            b"\x52\x01\x10\x11\xF6\xFF\x4B",
            b"\x52\x01\x10\x12\xF5\xFF\x4B",
            b"\x52\x01\x13\xF4\xFF\x4B",
            b"\x52\x01\x14\xF3\xFF\x4B",
            b"\x52\x01\x15\xF2\xFF\x4B",
            b"\x52\x01\x16\xF1\xFF\x4B",
            b"\x52\x01\x17\xF0\xFF\x4B",
            b"\x52\x01\x18\xEF\xFF\x5B",
            b"\x52\x01\x19\xEE\xFF\x5B",
            b"\x52\x01\x1A\xED\xFF\x5B",
            b"\x52\x01\x1B\xEC\xFF\x5B",
            b"\x52\x01\x1C\xEB\xFF\x5B",
            b"\x52\x01\x1D\xEA\xFF\x5B",
            b"\x52\x01\x1E\xE9\xFF\x5B",
            b"\x52\x01\x1F\xE8\xFF\x5B",
            b"\x52\x01\x20\xE7\xFF\x6B",
            b"\x52\x01\x21\xE6\xFF\x6B",
            b"\x52\x01\x22\xE5\xFF\x6B",
            b"\x52\x01\x23\xE4\xFF\x6B",
            b"\x52\x01\x24\xE3\xFF\x6B",
            b"\x52\x01\x25\xE2\xFF\x6B",
            b"\x52\x01\x26\xE1\xFF\x6B",
            b"\x52\x01\x27\xE0\xFF\x6B",
            b"\x52\x01\x28\xDF\xFF\x5B",
            b"\x52\x01\x29\xDE\xFF\x5B",
            b"\x52\x01\x2A\xDD\xFF\x5B",
            b"\x52\x01\x2B\xDC\xFF\x5B",
            b"\x52\x01\x2C\xDB\xFF\x5B",
            b"\x52\x01\x2D\xDA\xFF\x5B",
            b"\x52\x01\x2E\xD9\xFF\x5B",
            b"\x52\x01\x2F\xD8\xFF\x5B",
            b"\x52\x01\x30\xD7\xFF\x4B",
            b"\x52\x01\x31\xD6\xFF\x4B",
            b"\x52\x01\x32\xD5\xFF\x4B",
            b"\x52\x01\x33\xD4\xFF\x4B",
            b"\x52\x01\x34\xD3\xFF\x4B",
            b"\x52\x01\x35\xD2\xFF\x4B",
            b"\x52\x01\x36\xD1\xFF\x4B",
            b"\x52\x01\x37\xD0\xFF\x4B",
            b"\x52\x01\x38\xCF\xFF\x5B",
            b"\x52\x01\x39\xCE\xFF\x5B",
            b"\x52\x01\x3A\xCD\xFF\x5B",
            b"\x52\x01\x3B\xCC\xFF\x5B",
            b"\x52\x01\x3C\xCB\xFF\x5B",
            b"\x52\x01\x3D\xCA\xFF\x5B",
            b"\x52\x01\x3E\xC9\xFF\x5B",
            b"\x52\x01\x3F\xC8\xFF\x5B",
            b"\x52\x01\x40\xC7\xFF\x2B",
            b"\x52\x01\x41\xC6\xFF\x2B",
            b"\x52\x01\x42\xC5\xFF\x2B",
            b"\x52\x01\x43\xC4\xFF\x2B",
            b"\x52\x01\x44\xC3\xFF\x2B",
            b"\x52\x01\x45\xC2\xFF\x2B",
            b"\x52\x01\x46\xC1\xFF\x2B",
            b"\x52\x01\x47\xC0\xFF\x2B",
            b"\x52\x01\x48\xBF\xFF\x5B",
            b"\x52\x01\x49\xBE\xFF\x5B",
            b"\x52\x01\x4A\xBD\xFF\x5B",
            b"\x52\x01\x4B\xBC\xFF\x5B",
            b"\x52\x01\x4C\xBB\xFF\x5B",
            b"\x52\x01\x4D\xBA\xFF\x5B",
            b"\x52\x01\x4E\xB9\xFF\x5B",
            b"\x52\x01\x4F\xB8\xFF\x5B",
            b"\x52\x01\x50\xB7\xFF\x4B",
            b"\x52\x01\x51\xB6\xFF\x4B",
            b"\x52\x01\x52\xB5\xFF\x4B",
            b"\x52\x01\x53\xB4\x06\xB2",
            b"\x52\x01\xFE\x80\xFF\xD2",
            b"\x52\x01\xFF\x7F\x7A\xA9",
            b"\x56\x56\xED\xDE\x52\x6C\x6F\x67\x5F\x73\x74\x61\x72\x74",
            b"\x4C\x4C",
            b"\x56\x56",
        ]
        results = []
        for command in commands:
            self.continuous_mode_command(command)
            results.append(self.continuous_mode_read())

        print("Waiting for continuous reading startup...")
        self.connection.timeout=None
        result = self.connection.read(12)
        if result != b'\x25\x30\x31\x30\x31\x33\x32\x30\x41\x30\x30\x0D':
            print("Final output before streaming is wrong...")
            print(result)

    def get_unescaped_byte(self) -> bytes:
        return self.connection.read(1)
    
    def get_escaped_byte(self) -> bytes:
        result = self.connection.read(1)
        if result == b'\x80':
            return self.connection.read(1)
        return result

    # Manual specifies this, but haven't gotten to work
    def start_sending_combined(self):
        self.continuous_mode_command(START_COMBINED)
        result = self.continuous_mode_read()
        print(result.hex())

    # Manual specifies this, but haven't gotten to work
    def start_sending_temperature(self) -> bool:
        self.continuous_mode_command(START_TEMPERATURE)
        result = self.connection.read(1)
        if result == POSITIVE_ACKNOWLEDGE:
            print("Starting to send temperature packets")
            return True
        else:
            print("Failed to start sending temperature packets")
            return False

    # Manual specifies this, but haven't gotten to work
    def stop_sending_temperature(self) -> bool:
        self.continuous_mode_command(STOP_TEMPERATURE)
        result = self.connection.read(1)
        if result == POSITIVE_ACKNOWLEDGE:
            print("Stopping sending temperature packets")
            return True
        else:
            print("Failed to stop sending temperature packets")
            return False
