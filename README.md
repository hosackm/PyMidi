# PyMidi
Python wrappers for the Portmidi using CFFI

## To Install
Run 
```
python setup.py install
```
Then run
```
python pymidi/build_pymidi.py
```
You can then test that pymidi was installed correctly by running `test.py`.  Make sure that you have libportmidi installed and a MIDI device connected to your computer.  `test.py` defaults to using

## Examples
There are 3 examples included:
  1. `input.py` captures MIDI events on the device ID you pass on the command line.
  2. `output.py` generates random MIDI events on the device ID you pass on the command line.
  3. `passthru.py` passes any input MIDI events from device id #1 to device id #2 you pass on the command line.

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

As long as you have libportmidi installed in a normal location everything should work.  If it's installed in an odd location, make sure you make a local copy or let ffi know where it's location is before `ffi.dlopen()` is called at the top of `midilib.py`

## Features
MIDI Input
MIDI Output

![imgur-gif](https://github.com/hosackm/gifs_for_repos/blob/master/pymidi_720_ffmpeg.gif)
