# -*- coding: utf-8 -*-
"""
Created on Fri May  7 20:46:27 2021

@author: AUppal
"""

import numpy as np
import sounddevice as sd
# this can be installed by running:
# python -m pip install sounddevice
# (run from anaconda prompt if using anaconda)

# Path to \t delimited console dump from Portenta Vision shield's L/R mics
consoleDumpPath = r'C:\git\earduino\consoleOut.txt'

fs = 64000 # Hz
nBits = 16

if nBits == 16:
    stereoArr = np.loadtxt(consoleDumpPath, dtype='int16')
elif nBits == 32: # haven't tried
    stereoArr = np.loadtxt(consoleDumpPath, dtype='int32')
else:
    print('Not sure what dtype to use for {} array'.format(nBits))
    # https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html

sd.play(stereoArr, samplerate=fs, loop=False) 
# https://python-sounddevice.readthedocs.io/en/0.4.1/api/convenience-functions.html#sounddevice.play 