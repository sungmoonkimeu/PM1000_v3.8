import os
import ftd3xx as ftd3
import sys
import time

pathToExecutable = ('C:\\Program Files\\GNU Octave\\Octave-6.2.0\\mingw64\\bin\\octave-cli.exe')
os.environ['OCTAVE_EXECUTABLE'] = pathToExecutable

# Filename octavethread.py
import threading
from oct2py import octave

class OctaveThread(threading.Thread):

    def __init__(self, name='octave-thread'):
        super(OctaveThread, self).__init__(name=name)
        self.start()


    def run(self):
        octave.addpath('./COM') # add sub directory containing my .m files
        octave.addpath('./OCT6')  # add sub directory containing my .m files
        # octave.eval('my_octave_init_script') #optionally executes my_octave_init_script.m
        # when using 'eval' any variables are available within the next script as well
        # execute my_octave_script.m which has an endless loop and will never return
        octave.eval('initpm')
        octave.eval('initpm2')

        octave.eval('my_octave_script2')
