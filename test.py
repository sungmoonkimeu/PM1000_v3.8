import ftd3xx as ftd3
import sys

import Python_USB
import matlab

my_Novoptel = Python_USB.initialize()
print('initpm:   ')
#typePM      = matlab.uint16([2]) # activate for USB2.0 device
#DevDescrPM  = "PM1000-100M-XL-FA-NN-D 44"
typePM      = matlab.uint16([3]) # activate for USB3.0 device
DevDescrPM  = "PM1000-100M-XL-FA-N10-D 88"
okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut = my_Novoptel.initpm(typePM,  DevDescrPM,  nargout=5)
print(okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut, sep='\n')
print("initialization has completed")


# Read S3 sign setting of PM1000:
S3sign, okOut = my_Novoptel.readpm(matlab.double([512+45]), nargout=2)
print(S3sign, okOut, sep='\n')


print('closeepm: ')
okOut = my_Novoptel.closepm()
print(okOut, sep='\n')

my_Novoptel.terminate()
