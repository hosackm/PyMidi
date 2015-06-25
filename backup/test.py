from _pymidi import ffi, lib

SINGLETON = None
'''This is the singleton object to ensure we don\'t
instantiate the library more than once'''
PPNULL = ffi.new('void **')


def _is_instantiated():
    global SINGLETON
    return SINGLETON is not None


def _instantiate_library():
    global SINGLETON
    SINGLETON = ffi.new('PortMidiStream **')
    num = lib.Pm_Initialize()
    if num:
        raise MidiException(num)


class PmEvent():
    def __init__(self, message, timestamp):
        self.status = message & 0xFF
        self.data1 = (message >> 8) & 0xFF
        self.data2 = (message >> 16) & 0xFF
        self.timestamp = timestamp

    @classmethod
    def events_from_buffer(cls, buf):
        return [cls(event.message, event.timestamp) for event in buf]

    @classmethod
    def create_note_on(cls, key, velocity=0):
        message = ((0x90 << 16) & 0xFF0000)
        message |= ((key << 8) & 0xFF00)
        message |= (velocity & 0xFF)
        return cls(message, 0)

    @classmethod
    def create_note_off(cls, key):
        message = ((0x80 << 16) & 0xFF0000)
        message |= ((key << 8) & 0xFF00)
        message |= (velocity & 0xFF)
        return cls(message, 0)

    def is_note_on(self):
        return self.status == 0x90

    def is_note_off(self):
        return self.status == 0x80

    def is_control(self):
        return self.status == 0xB0

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'PmEvent({}, {}, {})'.format(self.status,
                                            self.data1,
                                            self.data2)


class Input(object):
    '''_'''
    PNULL = ffi.new('void **')[0]

    def __init__(self, device_id, buffer_size=4096):
        '''_'''
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
        '''_'''
        num_events = min(num_events, self.buffer_size)
        num_events = lib.Pm_Read(self.stream, self.buffer, num_events)
        if num_events < 0:
            raise MidiException(num_events)

        events = self.buffer[0:num_events]
        return PmEvent.events_from_buffer(events)

    def poll(self):
        '''_'''
        ret = lib.Pm_Poll(self.stream)
        if ret == 1:
            return True
        elif ret == 0:
            return False
        else:
            raise MidiException(ret)

    def close(self):
        lib.Pm_Close(self.stream)


class Output(object):
    def __init__(self):
        pass


class MidiException(Exception):
    def __init__(self, errno):
        self.errno = errno

    def __str__(self):
        return lib.Pm_GetErrorText(self.errno)


def main():
    import time
    i = Input(0)
    while True:
        try:
            #print i.read()
            events = i.read()
            for e in events:
                print e, e.is_note_on()
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
