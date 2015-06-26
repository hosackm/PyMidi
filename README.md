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

![imgur-gif](../master/img/pymidi_720_ffmpeg.gif)
