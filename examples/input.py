#!/usr/bin/env python

from __future__ import print_function
from pymidi import *
import time
import sys


def test_input(device_id=None):
    print('testing input device: {}'.format(device_id))
    if device_id is None:
        device_id = get_default_input_device_id()
    print('Loading PyMidi...')
    try:
        stream = Input(device_id=device_id)
    except MidiException:
        print('Unable to open MIDI Device. Make sure it is connected')

    print('Done. Mash some keys!')

    while True:
        try:
            for event in stream.read():
                print(event)
            time.sleep(0.1)
        except KeyboardInterrupt:
            stream.close()
            sys.exit()


def usage():
    print('Usage: python {} <input_device_id>'.format(__file__))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    test_input(int(sys.argv[1]))
