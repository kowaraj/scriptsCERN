#!/usr/bin/python

''' Copy VTU settings for the rephasing
'''

import ppm_copy
import argparse
from pyjapc import PyJapc
from jpype import JavaException
from time import sleep

parser = argparse.ArgumentParser(description='Some args...')
parser.add_argument('uname_src', metavar='source <username>', nargs='+',help='to compose: SPS.USER.<username>')
parser.add_argument('uname_dst', metavar='destination <username>', nargs='+',help='to compose: SPS.USER.<username>')
args = parser.parse_args()

devs_to_copy = ['FrevProgVTU_cfv_864_agsps']
props_to_copy = ['Mode', 'NormalMode', 'TriggSel']
params_not_to_copy = ['cycleName']

uname_src = 'SPS.USER.'+args.uname_src[0]
uname_dst = 'SPS.USER.'+args.uname_dst[0]

pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
sleep(1)

print '---'
print 'params:   ' + str(params_not_to_copy)
print 'devs: ' + str(devs_to_copy)
print 'users: from {' + uname_src + '} to {' + uname_dst + '}'

for dev in devs_to_copy:
    for a_prop in props_to_copy:

        print 'Device: ' + str(dev) + ', property: ' + str(a_prop)
        try:
            ppm_copy.copy_property_notparams(pj, dev, a_prop, params_not_to_copy, uname_src, uname_dst, dbg=True)
        except RuntimeError as e:
            print 'RuntimeError: ', e.args
        except JavaException as e:
            print "Caught the runtime exception : ", e.message()
            print e.stacktrace()
            exit(0) if (raw_input('Do you want to continue?') != 'y') else 'continue'
        except JException:
            print 'cern.japc.ParameterException: '
        except Exception as e:
            print 'Exception:', e.args


