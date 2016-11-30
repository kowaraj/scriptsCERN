#!/user/bdisoft/operational/bin/Python/PRO/bin/python

''' Restore rephasing settings (LTIMs) from file
'''

from restore_settings_from_file import * 
import argparse
from pyjapc import PyJapc
from jpype import JavaException
from time import sleep

parser = argparse.ArgumentParser(description='Some args...')
parser.add_argument('uname_src', metavar='source <username>', nargs='+',help='to compose: SPS.USER.<username>')
args = parser.parse_args()
user = 'SPS.USER.'+args.uname_src[0]

### LTIMs
for prop in ['ExpertSettings']:    
    server = 'ALLSpsRephasingIntfc_DU.cfv-864-agsps'
    device = 'SpsLhcRephasing_cfv864agsps'
    rda_set_server_dev_prop_users(server, device , prop, user_from, user_to)



