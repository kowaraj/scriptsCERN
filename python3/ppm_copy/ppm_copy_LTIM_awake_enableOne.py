#!/user/bdisoft/operational/bin/Python/PRO/bin/python

''' Enable LTIM events : 
'           on devices : RF22-x-y
'             for user : SPS.USER.
'''


from ppm_ltim import set_out_enabled
from pyjapc import PyJapc

with open('users.txt', 'r') as fd:
    users = ', '.join([x.rstrip('\n') for x in fd.readlines()])

pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
sleep(1)

### LTIMs
for p in ['ExpertSetting']:
    for user_dst in users:
        for [x,y] in [[x,y] for x in [0,1] for y in range(1,9)] :
            dev_dst = 'SX.RF22-'+str(x)+'-'+str(y)            
            input('enable? ', p, dev_dst, user_dst)
            set_out_enabled(pj, dev_dst, user_dst, 1)

