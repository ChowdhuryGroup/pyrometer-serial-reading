import pymodbus

command_start = b"\x02"
command_end = b"\x03"
positive_acknowledge = b"\x06"

start_sending_temperature = b"\x31"
stop_sending_temperature = b"\x30"

# PhotriX powers up by default in MODBUS mode
enable_modbus_mode = b"\x4d"

command_register = b"\x80\x00"

# When PhotriX sensor powers up, wait 6 seconds and remove any buffer from that time

## escape characters (due to variable length packets)
escape_character = b"\x80"
temperature_header = b"\x81"  # 4 data bytes
current_header = b"\x82"  # 4 data bytes
temperature_current_header = b"\x83"  # 8 data bytes
ambient_temperature_header = b"\x84"  # 8 data bytes
