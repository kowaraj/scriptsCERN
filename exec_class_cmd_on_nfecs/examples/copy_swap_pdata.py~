#!/usr/bin/python

import os
import subprocess
import sys

classname = 'ALLSwitchProtect'
fecs_names = ["cfv-ux45-acsc"+str(c)+"b"+str(b)+'t' for c in range(1, 9) for b in range(1, 3)]
fecs_str = ' '.join(fecs_names)
print "fecs = ", fecs_str

subprocess.call('copy_persistent_data_class_nfecs ALLSwitchProtect /acc/dsc/lhc/ --fecs '+fecs_str, shell=True)
