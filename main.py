# pyrometer serial reading ieee754
import struct
import photrix
import time


def decode_ieee754(data: bytes):
    if len(data) != 4:
        raise ValueError(
            "Buffer length must be 4 bytes for IEEE 754 single precision float"
        )
    return struct.unpack(">f", data)[0]

def plotting_callback():
    return

import photrix
import time

class Connect:
    # Initialize pyro as a class attribute
    pyro = photrix.pyrometer("COM1")

    def __init__(self):
        self.temperature_bytes = bytearray()
        self.current_bytes = bytearray()
        self.electronics_temperature_bytes = bytearray()
        self.diode_temperature_bytes = bytearray()
        self.time_elapse = []
        self.Time = []
        self.PDcurrents = []
        self.Temps = []
        

    def generate_data(self,times,PDcurrent_list):
        
        while True:
            # Access pyro using the class attribute
            header_byte = Connect.pyro.get_unescaped_byte()
            if header_byte == b"\x80":
                Connect.pyro.get_unescaped_byte()
            elif header_byte == b"\x81":
                self.temperature_bytes = bytearray()
                for _ in range(4):
                    self.temperature_bytes.extend(Connect.pyro.get_escaped_byte())
            elif header_byte == b"\x82":
                self.current_bytes = bytearray()
                for _ in range(4):
                    self.current_bytes.extend(Connect.pyro.get_escaped_byte())
                
                #put in threads/socket (from Zhihan)
                
            elif header_byte == b"\x83":
                self.temperature_bytes = bytearray()
                self.current_bytes = bytearray()
                for _ in range(4):
                    self.temperature_bytes.extend(Connect.pyro.get_escaped_byte())
                for _ in range(4):
                    self.current_bytes.extend(Connect.pyro.get_escaped_byte())
            '''elif header_byte == b"\x84":
                self.electronics_temperature_bytes = bytearray()
                self.diode_temperature_bytes = bytearray()
                for _ in range(4):
                    self.electronics_temperature_bytes.extend(Connect.pyro.get_escaped_byte())
                for _ in range(4):
                    self.diode_temperature_bytes.extend(Connect.pyro.get_escaped_byte())'''
            if self.current_bytes != b"":
                PDcurrent_point = decode_ieee754(self.current_bytes)
                time_point = time.time()
                self.Time.append(time_point)
        
                self.PDcurrents.append(PDcurrent_point)
                PDcurrent_list.append(PDcurrent_point)
                times.append(time_point)
                #times.append(time_point)
                '''if not times:
                    times.append(0)  # Start with time elapsed = 0
                else:
                    times.append(times[-1] + time_point - self.Time[-1])
                 '''                   
                    

            '''output_string = ""
            if self.temperature_bytes != b"":
                output_string += f"Temperature (C): {decode_ieee754(self.temperature_bytes):+e} "
            if self.current_bytes != b"":
                output_string += f"Current (A): {decode_ieee754(self.current_bytes):+e} "
            if self.electronics_temperature_bytes != b"":
                output_string += f"Electronics Temp. (C): {decode_ieee754(self.electronics_temperature_bytes):+e} "
            if self.diode_temperature_bytes != b"":
                output_string += (
                    f"Diode Temp. (C): {decode_ieee754(self.diode_temperature_bytes):+e}"
                )
            print(output_string)
            pass'''
