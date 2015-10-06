#!/usr/bin/python

import argparse
import os
import subprocess
import sys
import time
import operator
import re


#import numpy
#import ndarray

#TODO: plot to see the monotonicity of the freq meas (by counter)

###########################        

import pylab as pl
import numpy as np

#args
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('f1', metavar='fname1', nargs='+',help='')
parser.add_argument('f2', metavar='fname2', nargs='+',help='')
parser.add_argument('offset', metavar='offset', nargs='+',help='')
parser.add_argument('offset2', metavar='offset2', nargs='+',help='')
args = parser.parse_args()
#print "args = ", args
f1name = args.f1[0]
f2name = args.f2[0]
of = int(args.offset[0])
of2 = int(args.offset2[0])
print 'comparing REC - PLAY'
print "name of file1 = ", f1name
print "name of file2 = ", f2name
print "offset = ", of
print "offset2 = ", of2

f1 = open(f1name, 'r')
f2 = open(f2name, 'r')
m_exp = '(\d+.\d+),(\d+.\d+E\d+)'
n = 150000
y1 = list()
y2 = list()

ll1 = f1.readlines()
ll2 = f2.readlines()

print 'size of file1 = ', len(ll1)
print 'size of file2 = ', len(ll2)
print 'size to compare = ', n

#first file
i = 0
for l in ll1[of:]:
    m = re.search(m_exp, l)    
    if m is not None:
        y1.append(float(m.group(2)))
    
    i +=1
    if i >= n:
        break

#second file
i = 0

for l in ll2[of2:]:
    m = re.search(m_exp, l)
    if m is not None:
        y2.append(float(m.group(2)))

    i +=1
    if i >= n:
        break


print 'size of y1 = ', len(y1)
print 'size of y2 = ', len(y2)

#check

ylen = min(len(y1), len(y2))
if len(y1) != len(y2):
    print "-- warning --> not equal sizes"    

a = 0 #60000
b = 1000 #80000
print 'comparing the chunks [a:b] = [', a, ':', b, ']'
if a > ylen or b > ylen:
    print 'index out of range = ', a, b, ylen
    exit()

#derivatives
y1der = list()
y2der = list()
ydiff = list()
for i in range(ylen-1):
    y1der.append(y1[i] - y1[i+1])
    y2der.append(y2[i] - y2[i+1])
    ydiff.append(y1[i] - y2[i])
y1der.append(0) #make equal to size of y1
y2der.append(0)
ydiff.append(0)

#plot
# pl.subplot(1,3,1) #raw values
# pl.scatter(range(b-a),y1[a:b],c='r',s=25)
# pl.scatter(range(b-a),y2[a:b],c='g',s=25)

# pl.subplot(1,3,2) #der1, der2
#pl.plot(range(ylen),y1der)
# pl.scatter(range(b-a),y1der[a:b],c='r',s=25)
# pl.scatter(range(b-a),y2der[a:b],c='g',s=25)


# derivative

ax = pl.subplot(111)
pl.plot(range(b-a),y1der[a:b],c='r')
pl.plot(range(b-a),y2der[a:b],c='g')
#ax.set_xlim([0.0,1000.0])
#ax.set_ylim([-100,20])

# pl.subplot(1,3,3) #diff
# pl.scatter(range(b-a),ydiff[a:b])
pl.show()












        
    


                
                
            



        







