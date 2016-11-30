#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import shell_cmd as sc


# processes

sc.pid('ALLVTULHC_DU_R')
sc.pid('ALLVTULHC_DU_S')
sc.pid('ALLSpsRephasingIntfc_DU_R')
sc.pid('ALLSpsRephasingIntfc_DU_S')

# shared mem

sc.shmexist('ALLVTULHC_DU.cfv-864-agsps')
sc.shmexist('sem.ALLVTULHC_DU.cfv-864-agsps')
sc.shmexist('ALLVTULHCClassShm')

sc.shmexist('ALLVTUClassShm')

sc.shmexist('ALLSpsRephasingIntfcClassShm')
sc.shmexist('ALLSpsRephasingIntfc_DU.cfv-864-agsps')
sc.shmexist('sem.ALLSpsRephasingIntfc_DU.cfv-864-agsps')




