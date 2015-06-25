import subprocess
from cffi import FFI


__all__ = ('ffi',)


p = subprocess.Popen(['clang -E include/portmidi.h'],
                     shell=True, stdout=subprocess.PIPE)
code = p.communicate()[0]

ffi = FFI()
ffi.cdef(code)

if __name__ == '__main__':
    ffi.set_source('_pymidi', None)
    ffi.compile()
