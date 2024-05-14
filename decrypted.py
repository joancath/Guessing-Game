def decode_with_key(binary_result, key):
    decoded_result = ''.join(chr(int(binary_char, 2) ^ key) for binary_char in binary_result.split())
    return decoded_result

def string_to_key(string_key):
    return sum(ord(char)for char in string_key)


def main():
    name = input("Enter name to decode:")
    string_key = input("Enter key:")

    key = string_to_key(string_key)

    decoded_name = decode_with_key(key)
    print(f"The decoded name is: {decoded_name}")

    
if __name__ == "__main__":
    main()