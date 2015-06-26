import subprocess
from cffi import FFI


__all__ = ('ffi',)

# Modify this location to support Linux and Windows
header = '/usr/local/Cellar/portmidi/217/include/portmidi.h'

# Run the preprocessor on the header
p = subprocess.Popen(['clang -E {}'.format(header)],
                     shell=True, stdout=subprocess.PIPE)
code = p.communicate()[0]

# These two sections of the header make cffi cough up.  They aren't used
# by portmidi.
code = code.replace('__signed', 'signed')
code = code.replace('typedef __builtin_va_list __darwin_va_list;', '')

ffi = FFI()
ffi.cdef(code)

if __name__ == '__main__':
    ffi.set_source('pymidi._pymidi', None)
    ffi.compile()
