#!/user/bdisoft/operational/bin/Python/PRO/bin/python

'''#    #!/usr/bin/python'''


''' Copy VTU settings for the rephasing
'''

from save_settings_to_file import * #save_property_notparams
import argparse
from pyjapc import PyJapc
from jpype import JavaException
from time import sleep

parser = argparse.ArgumentParser(description='Some args...')
parser.add_argument('uname_src', metavar='source <username>', nargs='+',help='to compose: SPS.USER.<username>')

args = parser.parse_args()
user = 'SPS.USER.'+args.uname_src[0]

### VTU - FakeFc
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_get_server_dev_prop('ALLVTULHC_DU.cfv-864-agsps', 'FakeFc_cfv864agsps', p)

### VTU - FakeFrev
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_get_server_dev_prop('ALLVTULHC_DU.cfv-864-agsps', 'FakeFrevSPS_cfv864agsps', p)

### VTU - FrevProg
for p in ['Mode', 'NormalMode', 'TriggSel']:
    rda_get_server_dev_prop_user('ALLSpsRephasingIntfc_DU.cfv-864-agsps', 'FrevProgVTU_cfv_864_agsps', p, user)

### Reph
for p in ['Settings', 'SettingsMDDS', 'SettingsR2STrim', 'SettingsSDDS']:
    rda_get_server_dev_prop_user('ALLSpsRephasingIntfc_DU.cfv-864-agsps', 'SpsLhcRephasing_cfv864agsps', p, user)

### LTIMs
for p in ['ExpertSetting']:
    for d in ['RFAGSPS1-'+str(x)+'-'+str(y) for x in [0,1] for y in range(1,9)]:
        rda_get_server_dev_prop_user('LTIM_DU.cfv-864-agsps', d, p, user)
