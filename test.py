from pymidi_package import *


def main():
    import time
    import sys
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
