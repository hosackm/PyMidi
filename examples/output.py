#!/usr/bin/env python

from __future__ import print_function
from pymidi import *
import random
import time
import sys


def test_output(device_id=None):
    print('testing output device: {}'.format(device_id))
    if device_id is None:
        device_id = get_default_output_device_id()
    try:
        stream = Output(device_id=device_id)
    except MidiException:
        print('Unable to open MIDI Device. Make sure it is connected')

    while True:
        try:
            key = random.randint(0, 127)
            vel = random.randint(60, 127)
            on = MidiNoteOn(key, vel)
            off = MidiNoteOff(key)

            stream.write_one(on)
            print(on)
            time.sleep(0.1)
            print(off)
            stream.write_one(off)
        except MidiException:
            print('Error writing MIDI Events to Output Stream')
        except KeyboardInterrupt:
            stream.close()
            sys.exit()


def usage():
    print('Usage: python {} <output_device_id>'.format(__file__))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    test_output(int(sys.argv[1]))
