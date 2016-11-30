#!/user/bdisoft/operational/bin/Python/PRO/bin/python

''' Copy LTIM prop : ExpertSetting 
'       on devices : from A-x-y to B-x-y
'        for users : from <arg> to <user_names>
'''

from ppm_copy import copy_property
from ppm_ltim import set_out_enabled

import argparse
from pyjapc import PyJapc
from jpype import JavaException
from time import sleep

parser = argparse.ArgumentParser(description='Some args...')
parser.add_argument('uname_src', metavar='source <username>', nargs='+',help='to compose: SPS.USER.<username>')
args = parser.parse_args()
user_src = 'SPS.USER.'+args.uname_src[0]
with open('users.txt', 'r') as fd:
    users = ', '.join([x.rstrip('\n') for x in fd.readlines()])

pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
sleep(1)

set_out_enabled(pj, 'SX.RF22-0-1', 'SPS.USER.SFTPRO2', 1)
exit(0)

### LTIMs
for p in ['ExpertSetting']:
    for user_dst in users:
        for [x,y] in [[x,y] for x in [0,1] for y in range(1,9)] :
            dev_src = 'SX.RF11-'+str(x)+'-'+str(y)
            dev_dst = 'SX.RF22-'+str(x)+'-'+str(y)            
            input('copy? ', p, dev_src, dev_dst, user_src, user_dst)
            #copy_property(pj, p, dev_src, dev_dst, user_src, user_dst)
