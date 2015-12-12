#!/usr/bin/python

import sys
import math
from math import *

H_AVG = 4620.
if(len(sys.argv) < 2):
    print 'H_AVG (default) = ', H_AVG
else:
    H_AVG = float(sys.argv[1])
    print 'H_AVG = ', H_AVG


def ftw1(fcav, frev):
    FTW1 = pow(2,19) * fcav / frev
    return FTW1
def ftw2(ftw1, h):
    FTW2 = pow(2,20) * h - ftw1
    return FTW2

FTW1_plus_FTW2 = pow(2,20)*H_AVG
print "FTW1 + FTW2 = ", FTW1_plus_FTW2
print "FTW1 + FTW2 = ", hex(int(round(FTW1_plus_FTW2)))

Fcav_0 = 200.22e+6

print 'At injection:'
F_i = 198.5e+6
Frev_i = F_i / H_AVG
FTW1_i = ftw1(Fcav_0, Frev_i)
FTW2_i = ftw2(FTW1_i, H_AVG)
print ' FTW1 = ', hex(int(round(FTW1_i)))
print ' FTW2 = ', hex(int(round(FTW2_i)))

print 'At transition:'
F_t = 200.22e+6
Frev_t = F_t / H_AVG
FTW1_t = ftw1(Fcav_0, Frev_t)
FTW2_t = ftw2(FTW1_t, H_AVG)
print ' FTW1 = ', hex(int(round(FTW1_t)))
print ' FTW2 = ', hex(int(round(FTW2_t)))

print 'Above transition:'
print ' FTW1 = FTW2 = FTW1_transition', hex(int(round(FTW1_t)))
print ' H = 4620 (fixed)'
print ' Fcav != Fcav_0, increasing'


print 'DDS FTWs calculations:'
print " FTW1' = 2**32 - FTW1"
print " FTW2' = 2**33 - 2**20 * H_AVG - FTW1'"
x = pow(2,33)-pow(2,20)*H_AVG
print " FTW2' + FTW1' = 2**33 - 2**20 * H_AVG ==> x = ", hex(int(round(x)))
print " Then, for FTW1' = FTW2 ==> x/2 ", hex(int(round(x/2)))
print " (one of: 0x6FA00000 or 0x6E980000) ?"


