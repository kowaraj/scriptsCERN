#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import shell_cmd as sc

root = os.path.abspath(os.path.curdir)
print('current path: ', os.path.abspath(os.path.curdir))

sc.kill(sc.pid('ALLSpsRephasingIntfc_DU_R'))
sc.kill(sc.pid('ALLSpsRephasingIntfc_DU_S'))

sc.rmshm('ALLSpsRephasingIntfcClassShm')
sc.rmshm('ALLSpsRephasingLHCClassShm') # LHC-part for NIR
sc.rmshm('ALLSpsRephasingIntfc_DU.cfv-864-agsps')
sc.rmshm('sem.ALLSpsRephasingIntfc_DU.cfv-864-agsps')
sc.rmshm('ALLVTUClassShm') # ALLVTU's shm


