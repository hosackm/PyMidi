#!/usr/bin/env python

from __future__ import print_function
from pymidi import *


def main():
    import time
    import sys
    print('loading portmidi...')
    try:
        i = Input(get_default_input_device_id())
    except MidiException:
        print('Unable to open MIDI device.  Make sure it\'s connected')
        sys.exit()
    print('done!')
    while True:
        try:
            for e in i.read():
                print(e)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
