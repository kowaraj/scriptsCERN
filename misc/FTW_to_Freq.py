#!/usr/bin/python

import sys
import math
from math import *


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if(len(sys.argv) < 2):
	print "Argument required, eg: './FTW_to_Freq.py 426108602'"
	exit(0)

ftw = int(sys.argv[1])

freq  = 2.5e+8 - ftw*5.0e+8/pow(2,32)

print "Freq = ", freq

