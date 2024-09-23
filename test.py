import os

if os.path.exists('./libexample.so'):
    print("yes\n")
    os.remove('./libexample.so')
os.remove('/tmp/tmppyc_i88_.so')
