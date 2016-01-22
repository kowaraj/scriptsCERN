#!/usr/bin/python

from subprocess import call
from time import sleep
import time
import sys
from sys import exit
import string

if len(sys.argv) < 3:
	print 'Argument required: a1=slot, a2=command. Ex: [x.py 6 init]'
	exit()

arg1 = int(sys.argv[1])
arg2 = str(sys.argv[2])
print 'Arguments given: a1=%i, a2=%s' % (arg1, arg2)
slot = arg1
cmd = arg2

def wr_(s, a, d):
         print 'write_vme', '-w16', '-v', '-a'+s+a, '-d'+d
         #call(['write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s])

def rd_(a, l='2'):
         from subprocess import Popen, PIPE
         cmd = ['read_vme', '-w16', '-v', '-a'+a, '-l'+l]
         print 'cmd = ', cmd
         p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         if err:
                 print 'Error: ', err
                 exit(-1)
         return output
         
curr_ts = time.strftime('%H%M%S', time.localtime(time.time()))


reg_addr = 6
addr = int('0x'+str(slot)+'00000', 16) + reg_addr
addr_s = str(hex(addr))
print rd_(addr_s)

print 'done.'



