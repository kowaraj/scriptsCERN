#!/usr/bin/python

import argparse
import os
import subprocess
import sys
import time
import operator
import re
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='')
parser.add_argument('x', metavar='fname1', nargs='*',help='')
# parser.add_argument('f1', metavar='fname1', nargs='*',help='')
# parser.add_argument('f2', metavar='fname2', nargs='*',help='')
# parser.add_argument('a1', metavar='a1', nargs='*',help='',default=0)
# parser.add_argument('a2', metavar='a2', nargs='*',help='',default=150000)
# parser.add_argument('b1', metavar='b1', nargs='*',help='',default=0)
# parser.add_argument('b2', metavar='b2', nargs='*',help='',default=150000)
args = parser.parse_args()
f1name = args.x[0]
f2name = args.x[1]
a1 = int(args.x[2])
b1 = int(args.x[3])
a2 = int(args.x[4])
b2 = int(args.x[5])

# f1name = args.f1
# f2name = args.f2
# a1 = int(args.a1)
# a2 = int(args.a2)
# b1 = int(args.b1)
# b2 = int(args.b2)
print 'ab = ', a1, a2, b1, b2
print 'comparing REC - PLAY'
print 'f1 = ', f1name, ', [',a1,':',b1,']'
print 'f2 = ', f2name, ', [',a2,':',b2,']'

f1 = open(f1name, 'r')
f2 = open(f2name, 'r')
y1 = list()
y2 = list()
m_exp = '(\D*)(\d+)(\D*)'

ll1 = f1.readlines()
ll2 = f2.readlines()

print 'len(f1) = ', len(ll1)
print 'len(f2) = ', len(ll2)

#first file
i = 0
for l in ll1:
    m = re.search(m_exp, l)
    if m is not None:
        if m.group(1) != '' or m.group(3) != '\n':
            continue
        y1.append(int(m.group(2)))
    i +=1

#second file
i = 0
for l in ll2:
    m = re.search(m_exp, l)
    if m is not None:
        if m.group(1) != '' or m.group(3) != '\n':
            continue
        y2.append(int(m.group(2)))
    i +=1

print 'len(y1) = ', len(y1)
print 'len(y2) = ', len(y2)

#check

y1len = len(y1)
y2len = len(y2)
#print 'comparing the chunks [a:b] = [', a, ':', b, ']'
if a1 > y1len or b1 > y1len or a2 > y2len or b2 > y2len:
    print 'index out of range = ', a1, b1, y1len, a2, b2, y2len
    exit()

yy1 = y1[a1:b1]
yy2 = y2[a2:b2]
yylen = min(len(yy1), len(yy2))

#derivatives
y1der = list()
y2der = list()
ydiff = list()
for i in range(yylen-1):
    y1der.append(yy1[i] - yy1[i+1])
    y2der.append(yy2[i] - yy2[i+1])
    ydiff.append(yy1[i] - yy2[i])
y1der.append(0) #make equal to size of y1
y2der.append(0)
ydiff.append(0)

y1der_xmax = y1der.index(max(y1der))
print '# of max(y1der) = ', y1der_xmax
y2der_xmax = y2der.index(max(y2der))
print '# of max(y2der) = ', y2der_xmax


#plot

pl.figure(1)
pl.subplot(111)
pl.scatter(range(len(yy1)), yy1, c='r',s=25)
pl.scatter(range(len(yy2)), yy2, c='g',s=25)

pl.figure(2)
ax = pl.subplot(111)
pl.plot(range(len(y1der)), y1der, 'r-o')
pl.plot(range(len(y2der)), y2der, 'g-o')
ax.set_ylim([-100, 1000])
ax.set_xlim([y1der_xmax-50,y1der_xmax+50])

pl.figure(3)
ax = pl.subplot(111)
pl.plot(range(len(ydiff)), ydiff, c='b')
ax.set_ylim([-10,10])


pl.show()












        
    


                
                
            



        







