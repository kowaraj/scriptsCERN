#!/usr/bin/python

''' Copy + parameters of all the LTIM devices in cfv-864-agsps, 
    Skip - parameters:
  + busEnabled
  + clock
  - cycleName = user-specific
  + delay
  + mode
  + omask
  + outEnabled
  - payload = user-specific
  + polarity
  + pwidth
  + settingMask
  + start
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

devs_to_copy = ['RFAGSPS1-' + str(x) + '-' + str(y) for x in range(10,12) for y in range(1,9)]
a_prop = 'ExpertSetting'
params_to_copy = ['busEnabled', 'clock', 'delay', 'mode', 'omask','outEnabled', 'polarity', 'pwidth', 'settingMask', 'start']

uname_src = 'SPS.USER.'+args.uname_src[0]
uname_dst = 'SPS.USER.'+args.uname_dst[0]

pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
sleep(1)

print 'Copying params:   ' + str(params_to_copy)
print 'Copying for devs: ' + str(devs_to_copy)
print 'Copying from {' + uname_src + '} to {' + uname_dst + '}'
for dev in devs_to_copy:
    print 'Device: ' + str(dev)
    try:
        ppm_copy.copy_property_params(pj, dev, a_prop, params_to_copy, uname_src, uname_dst)
    except RuntimeError as e:
        print 'RuntimeError: ', e.args
    except JavaException as e:
        print "Caught the runtime exception : ", e.message()
        print e.stacktrace()
        q = raw_input('Do you want to continue?')
        if q != 'y':
            exit(0)
    except JException:
        print 'cern.japc.ParameterException: '
    except Exception as e:
        print 'Exception:', e.args


