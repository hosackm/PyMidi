from _pymidi import ffi
import sys

# detect OS and load lib
if sys.platform.startswith('linux'):
    ext = 'so'
elif sys.platform.startswith('darwin'):
    ext = 'dylib'
else:
    ext = 'dll'
lib = ffi.dlopen('.'.join(['libportmidi', ext]))
