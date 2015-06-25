# PyMidi
Python wrappers for the Portmidi using CFFI

## To Build
Run `python build_pymidi.py` and a file `_pymidi.py` will be created in the same directory.  Then you can run `python pymidi.py` to start capturing MIDI events on the default MIDI input device.

## Dependencies
```
libpormidi, CFFI
```
To install libportmidi on Mac type:
```
brew install portmidi
```
To install CFFI type:
```
pip install CFFI
```

As long as you have libportmidi installed in a normal location everything should work.  If it's installed in an odd location, make sure you make a local copy or let ffi know where it's location is before `ffi.dlopen()` is called at the top of `pymidi.py`

## Features
MIDI Device Input

![imgur-gif](../master/img/pymidi_720_ffmpeg.gif)
