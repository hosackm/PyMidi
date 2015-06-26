#!/usr/bin/env python

from __future__ import print_function
from pymidi import *
import sys


def test_passthru(in_id, out_id):
    in_stream = Input(in_id)
    out_stream = Output(out_id)
    while True:
        try:
            for e in in_stream.read():
                event = None
                if e.is_note_on():
                    event = MidiNoteOn(e.get_key(), e.get_velocity())
                elif e.is_note_off():
                    event = MidiNoteOff(e.get_key())
                else:
                    pass  # not handled yet
                if event is not None:
                    out_stream.write_one(event)
                print(e)
        except MidiException:
            print('Error reading or writing MIDI Event')
        except KeyboardInterrupt:
            in_stream.close()
            out_stream.close()
            sys.exit()


def usage():
    print(
        'Usage: python {} <input_device_id> <output_device_id>'.format(
            __file__))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    test_passthru(int(sys.argv[1]), int(sys.argv[2]))
