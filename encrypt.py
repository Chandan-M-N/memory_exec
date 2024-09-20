from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

#Encrypting the file
def encrypt_file(file_path, output_path, key):

    with open(file_path, 'rb') as file:
        file_data = file.read()

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    with open(output_path, 'wb') as file:
        file.write(iv + encrypted_data)

    print(f"File '{file_path}' encrypted successfully!")

# key = get_random_bytes(16)  # AES-128 requires a 16-byte key
# print(key)
for a in ['fn1.py','fn2.py','main.py']:
    encrypt_file(a, f'{a}_encrypted.py', b'\x99M(\xa8JUZ\x1c\xa7\x0biBv\x10w?')

#key b'\x99M(\xa8JUZ\x1c\xa7\x0biBv\x10w?'