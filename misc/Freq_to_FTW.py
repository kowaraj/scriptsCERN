#!/usr/bin/python

import sys
import math
from math import *


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if(len(sys.argv) < 2):
	print "Argument required, eg: './Freq_to_FTW.py 200264525 [Hz]'"
	exit(0)

freq = int(sys.argv[1])

ftw  = (2.5e+8 - freq)*pow(2,32) / 5.0e+8

print "FTW = ", ftw

