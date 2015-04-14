#!/usr/bin/python

import os
import subprocess
import sys

# list of VTU fecs:
f1 = 'vb1 vb2 hb1 hb2 test'
p1 = ['cfv-sr4-adt' + x for x in f1.split(' ')]
f2 = 'b1 b2'
p2 = ['cfv-sr4-apw' + x for x in f2.split(' ')]
p3 = ['cfv-ux45-apw' + x for x in f2.split(' ')]
fecs = p1+p2+p3
fecs_str = ' '.join(fecs)
print "fecs = ", fecs_str

subprocess.call('copy_persistent_data_class_nfecs ALLVTU /acc/dsc/lhc/ --fecs '+fecs_str, shell=True)
