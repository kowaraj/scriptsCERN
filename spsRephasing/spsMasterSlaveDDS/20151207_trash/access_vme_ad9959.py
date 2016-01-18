#!/usr/bin/python

import time
from time import sleep
import sys
from sys import exit

import access_vme

print 'SlaveDDS Setup script'
if len(sys.argv) < 3:
        print 'Argument required: a1=slot, a2=command. Ex: [x.py 6 init]'
        exit()

slot = arg1 = int(sys.argv[1])
arg2 = str(sys.argv[2])
print 'Arguments given: a1=%i, a2=%s' % (arg1, arg2)
slot = arg1
cmd = arg2

        
reg_addr = 6
addr = int('0x'+str(slot)+'00000', 16) + reg_addr
addr_s = str(hex(addr))
print rd_(addr_s)

print 'done.'



