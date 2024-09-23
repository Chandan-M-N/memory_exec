from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

# Encrypt a single file
def encrypt_file(file_path, output_path, key):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    if not file_path.endswith('.so'):
        # Convert the binary data to string for newline normalization
        file_text = file_data.decode('utf-8').replace('\r\n', '\n')
        normalized_data = file_text.encode('utf-8')  # Convert back to bytes
    else:
        normalized_data = file_data


    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(normalized_data, AES.block_size))

    with open(output_path, 'wb') as file:
        file.write(iv + encrypted_data)

    print(f"File '{file_path}' encrypted successfully!")


# Your encryption key
key = b'\x99M(\xa8JUZ\x1c\xa7\x0biBv\x10w?'

# Encrypt individual files outside directories
# for a in ['fn1.py', 'fn2.py', 'main.py', 'config.yaml',os.path.join('dir1', 'fn3.py'),os.path.join('dir1', 'fn4.py'),os.path.join('dir2', 'fn5.py'),os.path.join('dir2', 'config2.yaml'),'libexample.so']:
encrypt_file('libexample.so', f'libexample.so_encrypted', key)