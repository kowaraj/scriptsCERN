#!/usr/bin/python

import sys
import math
from math import *


if(len(sys.argv) < 2):
	print "Argument required, eg: './xxx.py 200264525 [Hz]'"
	exit(0)

freq = int(sys.argv[1])

ext_clk = 354600000. 
ftw  = (1- freq/ext_clk)*pow(2,32)

print "Slave DDS FTW (for " + str(freq) + " Hz) = " + str(ftw)
print "hex = " + str(hex(int(ftw)))

