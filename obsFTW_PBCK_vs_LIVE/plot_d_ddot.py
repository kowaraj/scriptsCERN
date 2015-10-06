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
parser.add_argument('f1', metavar='fname1', nargs='+',help='the asdfas')
parser.add_argument('a', metavar='a', nargs='+',help='the asdf asdfas')
parser.add_argument('b', metavar='b', nargs='+',help='the asdf asdfas')
args = parser.parse_args()
f1name = args.f1[0]
a = int(args.a[0])
b = int(args.b[0])
print 'comparing REC - PLAY'
print "name of file1 = ", f1name
print "a = ", a
print "b = ", b

f1 = open(f1name, 'r')
m_exp = '(\D*)(\d+)(\D*)'
y1 = list()
ll1 = f1.readlines()
print 'size of file1 = ', len(ll1)

#first file
i = 0
for l in ll1:
    m = re.search(m_exp, l)
    if m is not None:
        if m.group(1) != '' or m.group(3) != '\n':
            continue
        y1.append(int(m.group(2)))
    i +=1
ylen = len(y1)
print 'size of y1 = ', len(y1)

a = 0 if a == 0 else a
b = ylen-100 if b == 0 else b
print 'comparing the chunks [a:b] = [', a, ':', b, ']'
if a > ylen or b > ylen:
    print 'index out of range = ', a, b, ylen
    exit()

y1der = [y1[i] - y1[i+1] for i in range(len(y1)-1)]

#plot
pl.figure(0)
pl.subplot(2,1,1)
pl.scatter(range(a,b),y1[a:b],c='r',s=15)
pl.subplot(2,1,2)
pl.scatter(range(a,b-1),y1der[a:b-1],c='b',s=15)
pl.show()












        
    


                
                
            



        







