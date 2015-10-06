#!/usr/bin/python

import sys
import time
import re
import argparse
import pylab as pl
import numpy as np
from pyjapc import PyJapc

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('arg_un', metavar='username', nargs='+',help='format: SPS.USER.username')
args = parser.parse_args()
username = 'SPS.USER.'+args.arg_un[0]
print '\n Reading data for: ', username

p = PyJapc( selector=username, incaAcceleratorName="SPS", noSet=True )

pFTW_TX     = "SpsLhcRephasing_cfv864agsps/ObsMemAcq#bufFTW"
pFTW_TX_len = "SpsLhcRephasing_cfv864agsps/ObsMemAcq#frozenAddr"
pFTW_RX     = "SpsLhcRephasing_cfv864agsps/ObsMemAcqDDS#bufFTWrxDDS"
pFTW_RX_len = "SpsLhcRephasing_cfv864agsps/ObsMemAcqDDS#frozenAddr"
    
# in: (name, data path, size path, mode)
# out: [array, len]
def get_data(label, pdata, buf_len, mode):
    global username
    #data
    buf = p.getParam(pdata)
    pbck = p.getParam( "SpsLhcRephasing_cfv864agsps/BTrainAcq#enabledPBCK" )
    print ':pbck = ', pbck
    rec = p.getParam( "SpsLhcRephasing_cfv864agsps/BTrainAcq#enabledREC" )
    print ':rec  = ', rec

    fname = label + mode
    f = open(fname, 'w')
    print 'opened file: ', fname
    f.write('user:  ' + username + '\n')
    f.write('label: ' + label + '\n')
    f.write('data:  ' + pdata + '\n')
    f.write('len:   ' + str(len(buf)) + '\n')
    f.write('mode:  ' + mode  + '\n')
    f.write('p/rec: ' + str(pbck) + str(rec)  + '\n')
    f.write('ts:    ' + str(time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))) + '\n')

    #file
    y = list()
    for i in range(len(buf)):
        val = buf[i]
        f.write(str(val)+'\n')
        y.append(float(val))
    f.close()

    return y[:]


print "Getting TX/RX data for REC, ready?"
raw_input()
size = p.getParam(pFTW_TX_len)
y  = list(get_data('FTW_TX', pFTW_TX, size, 'REC'))
size = p.getParam(pFTW_RX_len)
y  = list(get_data('FTW_RX', pFTW_RX, size, 'REC'))

print "Getting TX/RX data for PLAYBACK, ready?"
raw_input()
size = p.getParam(pFTW_TX_len)
y  = list(get_data('FTW_TX', pFTW_TX, size, 'PLAY'))
size = p.getParam(pFTW_RX_len)
y  = list(get_data('FTW_RX', pFTW_RX, size, 'PLAY'))




        







