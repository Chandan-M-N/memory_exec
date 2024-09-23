from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import sys
import types
import ctypes
import tempfile
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader



def decrypt_file_to_memory(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as file:
        iv = file.read(16)  # First 16 bytes are the IV
        encrypted_data = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    if '.so' in encrypted_file_path:
        return decrypted_data
    # Handle newline issues during decoding
    decrypted_text = decrypted_data.decode('utf-8', errors='ignore')

    print(f"Decrypted {encrypted_file_path}")
    return decrypted_text.replace('\r\n', '\n')  # Normalize line endings


key  = b'\x99M(\xa8JUZ\x1c\xa7\x0biBv\x10w?'


fn1_code = decrypt_file_to_memory('fn1.py_encrypted', key)
fn2_code = decrypt_file_to_memory('fn2.py_encrypted', key)
main_code = decrypt_file_to_memory('main.py_encrypted', key)
config_code = decrypt_file_to_memory('config.yaml_encrypted', key)
fn3_code = decrypt_file_to_memory(os.path.join('dir1', 'fn3.py_encrypted'),key)
fn4_code = decrypt_file_to_memory(os.path.join('dir1', 'fn4.py_encrypted'),key)
fn5_code = decrypt_file_to_memory(os.path.join('dir2', 'fn5.py_encrypted'),key)
config_code2 = decrypt_file_to_memory(os.path.join('dir2', 'config2.yaml_encrypted'), key)
so_code = decrypt_file_to_memory('libexample.so_encrypted',key)



def load_module_from_string(module_name, code):
    module = types.ModuleType(module_name)
    exec(code, module.__dict__) 
    sys.modules[module_name] = module
    print(f"Loaded module {module_name} into memory")


def load_shared_object_from_memory(decrypted_so_data):
    try:
        # Create a temporary file to hold the decrypted .so file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".so") as temp_so_file:
            temp_so_file.write(decrypted_so_data)
            temp_file_path = temp_so_file.name  # Get the temp file path

        # Check if the symlink already exists and remove it
        symlink_path = './libexample.so'
        if os.path.islink(symlink_path) or os.path.exists(symlink_path):
            os.remove(symlink_path)

        # Create a symlink to the temporary file
        os.symlink(temp_file_path, symlink_path)

        # Load the shared object into memory using ctypes
        lib = ctypes.CDLL(symlink_path)

        print(f"Shared object loaded successfully from {temp_file_path}")
        
        # Cleanup the temporary file
        os.remove(temp_file_path)

        return lib  # Return the handle of the shared object
    except Exception as e:
        print(f"Error while loading shared object from memory: {e}")
        raise Exception("Failed to load shared object from memory")
    

print(type(so_code))
handle = load_shared_object_from_memory(so_code)

dir1 = types.ModuleType('dir1')
dir2 = types.ModuleType('dir2')
sys.modules['dir2'] = dir2
sys.modules['dir1'] = dir1

# Load fn2 into the 'dir1' package
load_module_from_string('dir1.fn3', fn3_code)
load_module_from_string('dir1.fn4',fn4_code)
load_module_from_string('dir2.fn5', fn5_code)

# Step 2: Create a custom finder and loader for in-memory imports
class InMemoryFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in sys.modules:
            return spec_from_loader(fullname, InMemoryLoader())
        return None

class InMemoryLoader(Loader):
    def load_module(self, fullname):
        return sys.modules[fullname]

# Add our custom importer to the front of the meta path
sys.meta_path.insert(0, InMemoryFinder())

load_module_from_string('fn1',fn1_code)
load_module_from_string('fn2',fn2_code)
# load_module_from_string('config.yaml',config_code)
exec(main_code)




