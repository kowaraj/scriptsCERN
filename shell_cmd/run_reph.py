#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import shell_cmd as sc

root = os.path.abspath(os.path.curdir)
print('current path: ', os.path.abspath(os.path.curdir))

sc.kill(sc.pid('ALLVTULHC_DU_R'))
sc.kill(sc.pid('ALLVTULHC_DU_S'))
sc.kill(sc.pid('ALLSpsRephasingIntfc_DU_R'))
sc.kill(sc.pid('ALLSpsRephasingIntfc_DU_S'))

sc.run('sudo rm /dev/shm/ALLVTULHC_DU.cfv-864-agsps')
sc.run('sudo rm /dev/shm/ALLVTU*')
sc.run('sudo rm /dev/shm/ALLSpsRephasing*')
sc.run('sudo rm /dev/shm/sem.ALLVTU*')
sc.run('sudo rm /dev/shm/sem.ALLSpsRephasing*')

os.chdir(os.path.join(os.path.abspath(os.path.curdir),u'ALLVTULHC_DU/src/test/cfv-864-agsps'))
print('current path: ', os.path.abspath(os.path.curdir))
sc.run_bg('../../../build/bin/L865/ALLVTULHC_DU_R -instance ./reph_protons__FakeFc_FakeFrev.instance')
sc.run_bg('../../../build/bin/L865/ALLVTULHC_DU_S -instance ./reph_protons__FakeFc_FakeFrev.instance')
os.chdir(root)

os.chdir(os.path.join(os.path.abspath(os.path.curdir),u'ALLSpsRephasingIntfc_DU/src/test/cfv-864-agsps'))
print('current path: ', os.path.abspath(os.path.curdir))
sc.run_bg('../../../build/bin/L865/ALLSpsRephasingIntfc_DU_R -instance ./reph_protons_Reph_VTUFrevProg.instance')
sc.run_bg('../../../build/bin/L865/ALLSpsRephasingIntfc_DU_S -instance ./reph_protons_Reph_VTUFrevProg.instance')
os.chdir(root)






