from _pymidi import ffi, lib


def count_devices():
    return lib.Pm_CountDevices()


def get_default_input_device_id():
    return lib.Pm_GetDefaultInputDeviceID()


def get_default_output_device_id():
    return lib.Pm_GetDefaultOutputDeviceID()


def get_device_info(num):
    return lib.Pm_GetDeviceInfo(num)


def set_channel_mask(stream, mask):
    return lib.Pm_SetChannelMask(stream, mask)
