import sys
from _pymidi import ffi

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
    def __init__(self, errno):
        self.errno = errno

    def __str__(self):
        return lib.Pm_GetErrorText(self.errno)


class PmEvent():
    '''Represents a Portmidi event.  A midi event is a 24 bit
    hex value that contains a status, an 8 bit key value, and
    an 8 bit velocity value.

    PmEvent(message) returns an instance of PmEvent from a 24 bit integer

    PmEvent also creates helper functions to instantiate events
    without having to deal with bit masking:

    create_note_on(key): returns a Note On PmEvent with velocity = 0
    create_note_on(key, velocity): returns a Note On PmEvent

    create_note_off(key): returns a Note Off PmEvent with velocity = 127

    events_from_buffer(buf): returns a list of PmEvent instances
    from a buffer of cdata PmEvent structs from the cffi interface
    '''
    def __init__(self, message, timestamp=0):
        self.message = message
        self.timestamp = timestamp

    def get_status(self):
        'Return the status of this PmEvent'
        return self.message & 0xFF

    def get_key(self):
        'Return the key (data1) of this PmEvent'
        return (self.message >> 8) & 0xFF

    def get_velocity(self):
        'Return the velocity (data2) of this PmEvent'
        return (self.message >> 16) & 0xFF

    def is_note_on(self):
        '''Returns True if a PmEvent is a Note On event
        Otherwise returns False'''
        return self.get_status() == 0x90

    def is_note_off(self):
        '''Returns True if a PmEvent is a Note Off event
        Otherwise returns False
        '''
        return self.get_status() == 0x80

    def is_control(self):
        '''Returns True if a PmEvent is a Control event
        Otherwise returns False'''
        return self.get_status() == 0xB0

    @classmethod
    def events_from_buffer(cls, buf, gen=False):
        '''Returns a list of PmEvent instances
        from a buffer of cdata PmEvent structs from the cffi interface'''
        return [cls(event.message) for event in buf]

    @classmethod
    def create_note_on(cls, key, velocity=0):
        '''create_note_on(key) returns a Note On PmEvent with velocity = 0
        create_note_on(key, velocity) returns a Note On PmEvent'''
        message = ((0x90 << 16) & 0xFF0000)
        message |= ((key << 8) & 0xFF00)
        message |= (velocity & 0xFF)
        return cls(message, 0)

    @classmethod
    def create_note_off(cls, key):
        'Returns a Note Off PmEvent instance'
        message = ((0x80 << 16) & 0xFF0000)
        message |= ((key << 8) & 0xFF00)
        message |= 0x7F
        return cls(message)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'PmEvent(Status: {}, Note: {}, Velocity: {})'.format(
            self.get_status(),
            self.get_key(),
            self.get_velocity())

    def __eq__(self, other):
        '''PmEvents are considered equal if they have
        the same message and timestamp'''
        return ((self.message == other.message) and
                (self.timestamp == self.timestamp))

    def deepcopy(self):
        'Return a deep copy of this object.  Not just a reference'
        return self.__class__(self.message, self.timestamp)


class Input(object):
    '''_'''
    PNULL = ffi.new('void **')[0]

    def __init__(self, device_id=None, buffer_size=4096):
        '''Initialize a new MIDI Input Stream and open it
        If the stream fails to open a MidiException will be raised.

        :param device_id
        :param buffer_size is the num of PmEvents that can be stored at a time
        '''
        if device_id is None:
            device_id = lib.Pm_GetDefaultInputDevice()
        if device_id < 0:
            raise MidiException('Device ID must be a positive integer')

        if not _is_instantiated():
            _instantiate_library()

        self.buffer_size = buffer_size
        self.buffer = ffi.new('PmEvent []', buffer_size)
        pp_stream = ffi.new('PortMidiStream **')

        err = lib.Pm_OpenInput(pp_stream,
                               device_id,
                               self.PNULL,
                               self.buffer_size,
                               self.PNULL,
                               self.PNULL)
        if err:
            raise MidiException(err)

        self.stream = pp_stream[0]

    def read(self, num_events=4096):
        '''Read MIDI events and return a list of PmEvent instances
        :param num_events the number of events to read
        :rtype list of PmEvents read from MIDI Input'''
        num_events = min(num_events, self.buffer_size)
        ret = lib.Pm_Read(self.stream, self.buffer, num_events)
        if ret < 0:
            raise MidiException(ret)

        s = slice(0, num_events)
        return PmEvent.events_from_buffer(self.buffer[s])

    def poll(self):
        '''Returns True if events are ready otherwise False.
        Raises an exception if there was an error calling the PmPoll()'''
        ret = lib.Pm_Poll(self.stream)
        if ret == 1:
            return True
        elif ret == 0:
            return False
        else:
            raise MidiException(ret)

    def close(self):
        'Closes the MIDI Input Stream'
        lib.Pm_Close(self.stream)


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
        raise MidiException(num)


def main():
    import time
    print 'loading portmidi...'
    try:
        i = Input(0)
    except MidiException:
        print 'Unable to open MIDI device.  Make sure it\'s connected'
        sys.exit()
    print 'done!'
    while True:
        try:
            for e in i.read():
                print e
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
