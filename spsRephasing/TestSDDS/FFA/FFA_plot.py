#!/usr/bin/python

import sys
import math
from math import *

def ftw1p(fcav):
    frev = 354.6e+6/pow(2,13)
    #print 'frev = ', frev
    ftw = pow(2,32)-pow(2,19)*fcav/frev
    return int(ftw)

def ftw2p(ftw1p):
    ftw = 0xdf400000 - ftw1p
    return int(ftw)

fs = [int((199.0+float(x)/10)*1e+6) for x in range(15)]
ftw1p = [ftw1p(f) for f in fs]
ftw2p = [ftw2p(ftw1) for ftw1 in ftw1p]
ftwX =  [0x6fa00000 for f in fs]
print [hex(x) for x in ftw1p]
print [hex(x) for x in ftw2p]

import pylab as pl
pl.figure(0)
#pl.subplot(2,1,1)
pl.plot(fs, ftw1p, c='r',marker='o')
pl.plot(fs, ftwX, c='g',marker='o')
#pl.subplot(2,1,2)
#pl.scatter(fs, ftw2p ,c='b',s=15)
pl.plot(fs, ftw2p ,c='b',marker='o')
#pl.scatter(fs, ftwX, c='g',s=5)
pl.show()

# x = ftw1p(f_cav_197)
# print 'ftw1p_197 = ', hex(int(x))
# print 'ftw2p_197 = ', hex(int(ftw2p(x)))




