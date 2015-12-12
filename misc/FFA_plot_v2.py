#!/usr/bin/python

## v.2: Fcav0 = const, Frev changing!

import sys
import math
from math import *

H = 4620
FTW_AVG = 0x6FA00000
F_AVG = 200220000

def ftw1p(frev):
    fcav = 200.22e+6
    ftw = pow(2,32)-pow(2,19)*fcav/frev
    return int(ftw) if ftw < FTW_AVG else FTW_AVG

def ftw2p(ftw1p):
    ftw = 0xdf400000 - ftw1p
    return int(ftw)

def fcav(frev):
    ftw1p = FTW_AVG
    fcav = (pow(2,32)- ftw1p) * frev / pow(2,19)
    return int(fcav) if fcav > F_AVG else F_AVG

def f2(frev, ftw2p):
    print frev, ftw2p
    f = (pow(2,32)- ftw2p) * frev / pow(2,19)
    return int(f)

frevs = [42737. + 100*x for x in range(10)]
fcavs = [fcav(frev) for frev in frevs]
fX = [F_AVG for f in frevs]

print "FTW1' is the value received from the function and sent to DDS"
ftw1ps = [ftw1p(frev) for frev in frevs]
ftw2ps = [ftw2p(ftw) for ftw in ftw1ps]
ftwX = [FTW_AVG for f in frevs]
f2s = [f2(frev, ftw) for frev, ftw in zip(frevs,ftw2ps)]
print f2s

# print [hex(x) for x in ftw1ps]
print [hex(x) for x in ftw2ps]

import pylab as pl
pl.figure(0)
pl.subplot(2,1,1)
pl.plot(frevs, ftw1ps, c='r',marker='o')
pl.plot(frevs, ftwX, c='g',marker='o')
pl.plot(frevs, ftw2ps ,c='b',marker='o')
pl.subplot(2,1,2)
#pl.scatter(frevs, ftw2p ,c='b',s=15)
pl.plot(frevs, fcavs, c='m',marker='^')
pl.plot(frevs, fX ,c='g',marker='_')
pl.plot(frevs, f2s ,c='c',marker='v')
#pl.scatter(frevs, ftwX, c='g',s=5)
pl.show()





