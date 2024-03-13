def reverse_bits(byte):
    reversed_byte = 0
    for i in range(8):
        if byte & (1 << i):
            reversed_byte |= 1 << (7 - i)
    return reversed_byte


def bytes_to_float(byte_array: bytearray) -> float:
    # Extract exponent from the first byte
    exponent = byte_array[0]

    # Extract mantissa from the last three bytes
    mantissa_bytes = byte_array[1:]
    mantissa = 0
    for i, byte in enumerate(mantissa_bytes):
        mantissa |= byte << (8 * (2 - i))

    # Construct the float value
    exponent -= 59
    fraction = mantissa / (1 << 24)
    value = fraction * 2**exponent

    return value


print(f"{reverse_bits(0b10100000):08b}")
print(bytes_to_float(bytearray(b"\xA8\x79\x1C\x8F")))
print(bytes_to_float(bytearray(b"\x28\x79\x1C\x8F")))
