#!/usr/bin/python

import os
import subprocess
import sys

classname = 'ALLSwitchProtect'
fecs_names = ["cfv-ux45-acsc"+str(c)+"b"+str(b)+'t' for c in range(1, 9) for b in range(1, 3)]
fecs_str = ' '.join(fecs_names)
print "fecs = ", fecs_str

subprocess.call('exec_class_cmd_on_nfecs ALLSwitchProtect restart_class_on_fec --fecs {0} --dbg'.format(fecs_str), shell=True)
