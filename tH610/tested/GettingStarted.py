################################################################################
# © Keysight Technologies 2016
#
# You have a royalty-free right to use, modify, reproduce and distribute
# the Sample Application Files (and/or any modified version) in any way
# you find useful, provided that you agree that Keysight Technologies has no
# warranty, obligations or liability for any Sample Application Files.
#
################################################################################

import pyvisa
import sys
import time

# Change this variable to the address of your instrument
#VISA_ADDRESS = 'USB0::0x0957::0xBE18::K-86100D-50195::INSTR'

try:
    # Create a connection (session) to the instrument
    resourceManager = pyvisa.ResourceManager()
    devices = resourceManager.list_resources()
    print(devices)
    session = resourceManager.open_resource(devices[0])
except pyvisa.Error as ex:
    print('Couldn\'t connect to \'%s\', exiting now...' % devices[0])
    sys.exit()

# For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
#if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
#    session.read_termination = '\n'

# Send *IDN? and read the response
session.write('ACQ:CDIS')
session.write('*rst')
time.sleep(1)
session.write('chan1:wav wav2')
session.write('chan1:fsel filter3')
session.write('chan1:filt on')
session.write('mtest1:load:fnam "c:\\Program Files\\Keysight\\FlexDCA\\Demo\\Masks\\SONET_SDH\\001.24416 - STM008_OC24.mskx"')   #"%DEMO_DIR%\Masks\SONET_SDH\001.24416 - STM008_OC24.mskx"
session.write('mtest1:load')
session.write('mtest1:load')
session.write('mtes1:marg:meth auto')
session.write('mtes1:marg:stat on')
session.write('syst:mod eye')
session.write('aut')
#session.write(':meas:mtes:marg?)
#maskMargin=session.read()
maskMargin=session.query(':MEAS:mtes:marg?')
#maskMargin=session.query('*idn?')
print(ord(maskMargin),maskMargin)

#session.write('*IDN?')
#idn = session.read()

#print('*IDN? returned: %s' % idn.rstrip('\n'))

# Close the connection to the instrument
session.close()
resourceManager.close()

print('Done.')
