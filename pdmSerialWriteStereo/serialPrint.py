# -*- coding: utf-8 -*-
"""
Created on Sat May  8 20:11:21 2021

@author: AUppal
"""
# https://problemsolvingwithpython.com/11-Python-and-External-Hardware/11.04-Reading-a-Sensor-with-Python/

import serial
# Note, if using py3, run: 
#    pip install pyserial
# if using py2, 
#   pip install serial 
# https://stackoverflow.com/questions/41199876/attributeerror-module-serial-has-no-attribute-serial

import sounddevice as sd
# this can be installed by running:
# python -m pip install sounddevice
# (run from anaconda prompt if using anaconda)

import numpy as np
import matplotlib.pyplot as plt
import time
    
#print(serial.tools.list_ports.comports())
TIMEOUT_s = 10 # time to wait on serial read

# Parameters from Arduino code
BAUD_RATE = 115200
BUFFER_SIZE = 32000*2*2 # 128 kbytes to get 1s of 16-bit stereo data @32kHz
SAMPLE_BITS = 16
SAMPLE_RATE = 32000

# set up the serial line
ser = serial.Serial('COM6', BAUD_RATE, timeout=TIMEOUT_s)
# Might get SerialException: could not open port 'COM6': PermissionError(13, 'Access is denied.', None, 5)
# if Arduino IDE is still connected to the board

# Use a big try/finally loop to always close serial when exiting script
try: 
    # Read and play serial data
    for i in range(5):
        # Start timer
        START_TIME = time.time()
        
        buffer = ser.read(BUFFER_SIZE)  # read ~1s buffer of stereo data
        #print(buffer)
        
        if buffer == b'Failed to start PDM!\r\n':
            print('Check if PDM rate is supported.')
            break
        
        elif len(buffer) == 0:
            print('No data!')
            break # out of this loop, we don't have data!
            
        else:
            if SAMPLE_BITS == 16:
                # need enough bytes (8bits/byte) to get two stereo samples
                extraSamples = len(buffer) % (2*SAMPLE_BITS/8) 
                if extraSamples > 0:
                    buffer = buffer[:-int(extraSamples)] # trim buffer to get last L/R samples
                    print(buffer)
                
                # Bytes to int16 samples
                intArr = np.frombuffer(buffer, dtype='int16')
                #https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html
                
            elif SAMPLE_BITS == 32: # not tested
                intArr = np.frombuffer(buffer, dtype='int32')
                
            else:
                print('Not sure what dtype to use for {} array'.format(SAMPLE_BITS))

            # Is the buffer still valid?            
            if len(buffer) == 0:
                print('Truncated buffer to size 0? Debug me!')

            else:
                print('Finished capture in {:.2f}s...'.format(time.time()-START_TIME))
                
                # Reshape to a 2-column matrix for sounddevice playback
                stereoArr = np.reshape(intArr, (-1, 2))
                # https://stackoverflow.com/questions/12575421/convert-a-1d-array-to-a-2d-array-in-numpy
                
                # Display the data
                plt.figure(i)
                plt.plot(stereoArr)
                
                print('Playing data!')
                sd.play(stereoArr, samplerate=SAMPLE_RATE, loop=False) 
    

finally:
    print('Closing serial link before exiting...')
    ser.close()