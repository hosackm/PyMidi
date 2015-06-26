from ._pymidi import ffi
from .midilib import lib


__all__ = ('PmDeviceInfo', 'MidiException', 'PmEvent')


class PmDeviceInfo():
    pass


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


class PmDeviceInfo():
    def __init__(self, structVersion, interf, name,
                 input_id, output_id, opened):
        self.structVersion = structVersion
        self.interf = ffi.string(interf)
        self.name = ffi.string(name)
        self.input = input_id
        self.output = output_id
        self.opened = opened

    @classmethod
    def from_cdata(cls, cdata):
        return PmDeviceInfo(cdata.structVersion, cdata.interf,
                            cdata.name, cdata.input, cdata.output,
                            cdata.opened)

    def __repr__(self):
        return '''PmDeviceInfo(
    structVersion = {},
    interf = {},
    name = {},
    input = {},
    output = {},
    opened = {})'''.format(self.structVersion,
                           self.interf, self.name,
                           self.input, self.output, self.opened)


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
