import os
import ftd3xx as ftd3
import sys
import time


pathToExecutable = ('C:\\Program Files\\GNU Octave\\Octave-6.2.0\\mingw64\\bin\\octave-cli.exe')
os.environ['OCTAVE_EXECUTABLE'] = pathToExecutable


from oct2py import Oct2Py
oc = Oct2Py(temp_dir='R:\\')
oc.temp_dir

# oc.addpath('..\\PM1000_v3.8\\PythonSupport\\OCT6'); # for GNU Octave, version 6.1.0
# oc.addpath('..\\PM1000_v3.8\\PythonSupport\\COM'); # for GNU Octave, version 6.1.0
# oc.addpath('..\\PythonSupport\\OCT6'); # for GNU Octave, version 6.1.0
# oc.addpath('..\\PythonSupport\\COM');
oc.addpath('R:\\OCT6'); # for GNU Octave, version 6.1.0
oc.addpath('R:\\COM'); # for GNU Octave, version 6.1.0

stri = input('Select PM1000 device (0) or look it up in LastDevPM.mat (1 or "enter"):')
if stri=='0':
    oc.initpm(0)
else:
    oc.initpm()
# dummy is a dictionary. We read its elements.
dummy       = oc.load('LastDevPM.mat',  'LastDevDescr', 'LastDevType')
DevDescrPM  = dummy['LastDevDescr']
typePM      = dummy['LastDevType' ]

print(DevDescrPM, typePM, sep='\n')
ok = oc.writepm(512+1,10)
res, ok = oc.readpm(512+1, nout=2)
print("ATE=", res, ok, sep='\n')
a= 0
for i in range(10):
    start_time = time.time()
    tS0, OK = oc.readburstpm(a,0,1023,512+24, nout=2)
    print("Data reading time is %s seconds" % (time.time() - start_time))
#print(tS0)

ok = oc.closepm()