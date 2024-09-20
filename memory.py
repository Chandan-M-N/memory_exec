from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys
import types

#Decrypt file without saving into disk
def decrypt_file_to_memory(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as file:
        iv = file.read(16)  # First 16 bytes are the IV
        encrypted_data = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    print(f"Decrypted {encrypted_file_path}\n")

    return decrypted_data.decode('utf-8')

#Loading the decrypted file into the memory
def load_module_from_string(module_name, code):
    module = types.ModuleType(module_name)
    exec(code, module.__dict__)
    sys.modules[module_name] = module
    print(f"Loaded module {module} to memory")

key = b'\x99M(\xa8JUZ\x1c\xa7\x0biBv\x10w?' 

fn1_code = decrypt_file_to_memory('fn1.py_encrypted.py', key)
fn2_code = decrypt_file_to_memory('fn2.py_encrypted.py', key)

load_module_from_string('fn1', fn1_code)
load_module_from_string('fn2', fn2_code)

main_code = decrypt_file_to_memory('main.py_encrypted.py', key)

#Executing the main.py
exec(main_code)