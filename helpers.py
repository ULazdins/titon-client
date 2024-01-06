from functools import reduce


def get_symbol_hash(msg):
    chars = [ord(x) for x in msg]

    def xor(x, y):
        return x ^ y

    return reduce(xor, chars)


def get_after_last_pipe(input_string):
    parts = input_string.rsplit("|", 1)

    if len(parts) > 1:
        return parts[1]
    else:
        # If no pipe is found, return the original string
        return input_string


def split_into_bits(number):
    # Use bin() to get the binary representation and remove the '0b' prefix
    binary_representation = bin(number)[2:]

    # Pad with leading zeros to ensure a consistent length
    padded_binary = binary_representation.zfill(8)  # Assuming 8 bits for simplicity

    # Convert the binary string to a list of integers
    bits = [int(bit) for bit in padded_binary]

    return bits
