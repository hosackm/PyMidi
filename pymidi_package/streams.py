import sys
from _pymidi import ffi
from events import PmEvent


__all__ = ('Input', 'Output', 'MidiException')

# Detect OS and use correct file extension for shared library
if sys.platform == 'darwin':
    ext = 'dylib'
elif sys.platform.startswith('linux'):
    ext = 'so'
else:  # win32 or cygwin
    ext = 'dll'
lib = ffi.dlopen('.'.join(['libportmidi', ext]))
# Only initialize Portmidi once
SINGLETON = None


class MidiException(Exception):
    '''Raise this exception when something goes wrong.
    Uses Portmidi\'s Pm_GetErrorText() to describe the error that occured'''
    def __init__(self, text='', errno=None):
        if errno is not None:
            self.err = ffi.string(lib.Pm_GetErrorText(errno))
        else:
            self.err = text

    def __str__(self):
        return self.err


class Input(object):
    '''_'''
    PNULL = ffi.new('void **')[0]

    def __init__(self, device_id, buffer_size=4096):
        '''Initialize a new MIDI Input Stream and open it
        If the stream fails to open a MidiException will be raised.

        :param device_id
        :param buffer_size is the num of PmEvents that can be stored at a time
        '''
        if not _is_instantiated():
            _instantiate_library()

        self.buffer_size = buffer_size
        self.buffer = ffi.new('PmEvent []', buffer_size)
        self.device_id = device_id
        self.stream = None

        self.open_stream()
        #pp_stream = ffi.new('PortMidiStream **')
        #err = lib.Pm_OpenInput(pp_stream,
        #                       device_id,
        #                       self.PNULL,
        #                       self.buffer_size,
        #                       self.PNULL,
        #                       self.PNULL)
        #if err:
        #    raise MidiException(errno=err)
        #self.stream = pp_stream[0]

    def open_stream(self):
        pp_stream = ffi.new('PortMidiStream **')
        try:
            err = lib.Pm_OpenInput(pp_stream,
                                   self.device_id,
                                   self.PNULL,
                                   self.buffer_size,
                                   self.PNULL,
                                   self.PNULL)
            assert(err == 0)
            self.stream = pp_stream[0]
        except AssertionError:
            self.stream = None
            raise MidiException(text='Invalid Device ID')

    def is_open(self):
        return self.stream is not None

    def read(self, num_events=4096):
        '''Read MIDI events and return a list of PmEvent instances
        :param num_events the number of events to read
        :rtype list of PmEvents read from MIDI Input'''
        num_events = min(num_events, self.buffer_size)
        ret = lib.Pm_Read(self.stream, self.buffer, num_events)
        if ret < 0:
            raise MidiException(errno=ret)

        return PmEvent.events_from_buffer(self.buffer[0:num_events])

    def poll(self):
        '''Returns True if events are ready otherwise False.
        Raises an exception if there was an error calling the PmPoll()'''
        ret = lib.Pm_Poll(self.stream)
        if ret == 1:
            return True
        elif ret == 0:
            return False
        else:
            raise MidiException(errno=ret)

    def close(self):
        'Closes the MIDI Input Stream'
        lib.Pm_Close(self.stream)
        self.stream = None


class Output(object):
    def __init__(self):
        pass


def _is_instantiated():
    'Return True if Portmidi is already open else False'
    global SINGLETON
    return SINGLETON is not None


def _instantiate_library():
    'Initialize Portmidi library'
    global SINGLETON
    SINGLETON = ffi.new('PortMidiStream **')
    num = lib.Pm_Initialize()
    if num:
        raise MidiException(errno=num)
