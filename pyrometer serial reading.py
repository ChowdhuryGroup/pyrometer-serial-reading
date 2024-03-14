#pyrometer serial reading ieee754
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

    # Configure the serial port
    pyro_serial = serial.Serial(
        baudrate=115200,
        timeout=2,
        bytesize=8,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
    )
    pyro_serial.port = "COM1"
    atexit.register(pyro_serial.close)

    # Configure the MODBUS client
    pyro_modbus = ModbusSerialClient(
        port="COM1", baudrate=115200, parity="N", stopbits=1, framer=Framer.RTU
    )
    atexit.register(pyro_modbus.close)

    ##### Reproducing writes sent by TemperaSure
    pyro_serial.open()
    pyro_serial.write(bytes([0x02, 0x56, 0x56, 0xED, 0xDE, 0x4B, 0x01, 0x03]))
    pyro_serial.write(bytes([0x02, 0x56, 0x56, 0x03]))
    ##########################################
    ### SEEMS like TemperaSure goes through trying incrementing baudrates until it gets a positive response, instead of straight for 115200
    time.sleep(6)
    pyro_serial.reset_input_buffer()
    pyro_serial.reset_output_buffer()
    # Technically this is a MODBUS formatted command, but we immediately go back to non-MODBUS after this, so writing it manually
    pyro_serial.write(b"\x00\x06\x80\x80\x70\x00\x84\x1B")
    time.sleep(0.1)
    print("Hopefully this is equal to 0x06: ", pyro_serial.read(9))

    pyro_serial.close()
    """
    pyro_modbus.connect()
    print("Pyrometer connected!")

    # Reproducing series of MODBUS commands sent by TemperaSure
    print(pyro_modbus.write_register(address=0x8000, value=0x7000))

    # temperature = pyrometer.read_holding_registers(address=0x0000, count=2)
    # print(temperature)
    """


'''import serial
import struct

# Configure the serial port
def decode_ieee754(data):
    if len(data) != 4:
        raise ValueError("Buffer length must be 4 bytes for IEEE 754 single precision float")
    return struct.unpack('f', data)[0]
while 1:

    try:
    # Configure the serial port
        ser = serial.Serial( port='COM1',  baudrate=115200,  timeout=2,   bytesize=8, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE)

    # Open the serial port
        #ser.open()

        try:
        # Send command to the device to request data
           command = b'\x82'  # Assuming 0x82 is the command to request data
           ser.write(command)

        # Read response from the device
           response = ser.read(1)  # Assuming the data packet is 4 bytes long
            #print(len(response))
        # Parse the data packet and decode IEEE 754 floating-point representation
           if response:
               data_value = decode_ieee754(response)
               print("Received data:", data_value)
           else:
              print("No response received from the device.")
        except serial.SerialException as e:
           print("Serial communication error:", e)
        #finally:
        # Close the serial port
               #ser.close()
    except serial.SerialException as e:
        print("Failed to open serial port:", e)
 '''




