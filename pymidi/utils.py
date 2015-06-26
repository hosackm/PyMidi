from midilib import lib
from types import PmDeviceInfo, PmEvent


__all__ = ('count_devices', 'get_default_input_device_id',
           'get_default_output_device_id', 'get_device_info',
           'set_channel_mask', 'MidiNoteOn', 'MidiNoteOff')


def count_devices():
    return lib.Pm_CountDevices()


def get_default_input_device_id():
    return lib.Pm_GetDefaultInputDeviceID()


def get_default_output_device_id():
    return lib.Pm_GetDefaultOutputDeviceID()


def get_device_info(num):
    return PmDeviceInfo.from_cdata(lib.Pm_GetDeviceInfo(num))


def set_channel_mask(stream, mask):
    return lib.Pm_SetChannelMask(stream, mask)


def MidiNoteOn(key, velocity):
    return PmEvent.create_note_on(key, velocity)


def MidiNoteOff(key):
    return PmEvent.create_note_off(key)
