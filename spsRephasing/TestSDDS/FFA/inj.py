#!/usr/bin/python

import sys
import math
from math import *
import sddsFreq as sf

h = 4620
if(len(sys.argv) < 2):
    print 'h = ', h
else:
    h = float(sys.argv[1])
    print 'h = ', h
print ""


ftw_sum = sf.sum_ftw_prime(h)

print " +----------------------------------------------+ "
print " | FTW1 + FTW2 = ", hex(int(round(ftw_sum)))
print " +----------------------------------------------+ "
print " (should be: 0xDF40'0000 or 0xDD30'0000) "
print ""
fcav0 = 200.22e+6

f = 198.5
frev = f / h
ftw1 = sf.ftw1(fcav0, frev)
ftw2 = sf.ftw2(ftw1, h)

print ' FTW1 = ', hex(int(round(ftw1)))
print ' FTW2 = ', hex(int(round(ftw2)))

x = pow(2,33)-pow(2,20)*h
print " |---------------------------------------------------------------------| "
print " | FTW2' + FTW1' = 2**33 - 2**20 * h ==> x = ", hex(int(round(x)))
print " |---------------------------------------------------------------------| "
print " (should be: 0xDF400000 or 0xDD300000) "
print " +-----------------------------------------------------+ "
print " | FTW1' = FTW2 ==> x/2 ", hex(int(round(x/2)))
print " +-----------------------------------------------------+ "
print " (should be: 0x6FA00000 or 0x6E980000)"





