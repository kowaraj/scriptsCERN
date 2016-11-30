#!/user/bdisoft/operational/bin/Python/PRO/bin/python


''' Restore rephasing settings from file
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

# ### VTU - FakeFc
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_setNo2dArr_server_dev_prop_user('ALLVTULHC_DU.cfv-864-agsps', 'FakeFc_cfv864agsps', p)

# ### VTU - FakeFrev
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_setNo2dArr_server_dev_prop_user('ALLVTULHC_DU.cfv-864-agsps', 'FakeFrevSPS_cfv864agsps', p)

# ### VTU - FrevProg
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_setNo2dArr_server_dev_prop_user('ALLSpsRephasingIntfc_DU.cfv-864-agsps', 'FrevProgVTU_cfv_864_agsps', p, user)

### Reph
for p in ['Settings', 'SettingsMDDS', 'SettingsR2STrim', 'SettingsSDDS']:
    rda_set_server_dev_prop_user('ALLSpsRephasingIntfc_DU.cfv-864-agsps', 'SpsLhcRephasing_cfv864agsps', p, user)



