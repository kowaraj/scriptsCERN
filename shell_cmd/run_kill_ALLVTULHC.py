#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import shell_cmd as sc

root = os.path.abspath(os.path.curdir)
print('current path: ', os.path.abspath(os.path.curdir))

sc.kill(sc.pid('ALLVTULHC_DU_R'))
sc.kill(sc.pid('ALLVTULHC_DU_S'))
sc.rmshm('ALLVTULHC_DU.cfv-864-agsps')
sc.rmshm('sem.ALLVTULHC_DU.cfv-864-agsps')
sc.rmshm('ALLVTULHCClassShm')







