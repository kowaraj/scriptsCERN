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


# plotting
pl.ion()
f1 = pl.figure(1)
f1p = f1.add_subplot(111)
f1pp, = f1p.plot(1, 1, 'r-') # Returns a tuple of line objects, thus the comma
f2 = pl.figure(2)
f2p = f2.add_subplot(111)
f2pp, = f2p.plot(1, 1, 'g-') # Returns a tuple of line objects, thus the comma
f3 = pl.figure(3)
f3p = f3.add_subplot(111)
f3pp, = f3p.plot(1, 1, 'b-') # Returns a tuple of line objects, thus the comma


def upd_plot_pers(f1, f1p, f1pp, yd, xd, ymin, ymax, xmin, xmax):
    # f1pp.set_ydata(yd)
    # f1pp.set_xdata(xd)
    f1p.plot(xd,yd)
    f1p.set_ylim([ymin,ymax])
    f1p.set_xlim([xmin,xmax])
    f1.canvas.draw()

def upd_plot(f1, f1p, f1pp, yd, xd, ymin, ymax, xmin, xmax):
    f1pp.set_ydata(yd)
    f1pp.set_xdata(xd)
    f1p.set_ylim([ymin,ymax])
    f1p.set_xlim([xmin,xmax])
    f1.canvas.draw()

        
def callb( label, data):
    print( "New value for {0} is: {1}".format(label, data[0]) )
    l = len(data)
    print 'l = ', l
    global username


    pbck = str(p.getParam( "SpsLhcRephasing_cfv864agsps/BTrainAcq#enabledPBCK" ))
    rec = str(p.getParam( "SpsLhcRephasing_cfv864agsps/BTrainAcq#enabledREC" ))
    curr_ts = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))
 
    fname = 'dump'+str(pbck)+str(rec)+str(curr_ts)
    f = open(fname, 'w')
    print 'opened file: ', fname

    f.write('user:  ' + username + '\n')
    f.write('label: ' + label + '\n')
    f.write('len:   ' + str(l) + '\n')
    f.write('p/rec: ' + str(pbck) + str(rec)  + '\n')
    f.write('ts:    ' + curr_ts + '\n')
    
    y = np.zeros(l, dtype=np.int)
    for i in range(l):
        val = data[i]
        f.write(str(val)+'\n')
        np.put(y,i,int(val))
    f.close()

    yder = [y[i] - y[i+1] for i in range(len(y)-1)]


    upd_plot(f1, f1p, f1pp, y, range(len(y)), min(y), max(y), 0, len(y)-1)
    print 'f1 = ', len(y), min(y), max(y), 0, len(y)-1
    yder_xmax = yder.index(max(yder))
    print '# of max(yder) = ', yder_xmax
    if min(yder) < 0:
        yder_xmin = yder.index(min(yder))
        print '# of min(yder) = ', yder_xmin
        print 'min = ', y[yder_xmin]

    upd_plot_pers(f2, f2p, f2pp, yder, range(len(yder)), 0, max(yder), yder_xmax-20, yder_xmax+20)
    print 'f2 = ', len(yder), min(yder), max(yder), 0, len(yder)-1

        

    yder2 = yder[yder_xmax:]
    upd_plot_pers(f3, f3p, f3pp, yder2, range(len(yder2)), 0, max(yder2), -20, 20)
    print 'f3 = ', len(yder2), min(yder2), max(yder2), -10, len(yder2)-1
    #pl.scatter(range(len(y)), y, c='r',s=15)
    #pl.scatter(range(len(yder)), yder, c='b',s=15)
    time.sleep(0.05)
    raw_input()
    
p.subscribeParam( pFTW_TX, callb)
p.startSubscriptions()
        
while True:
    time.sleep(0.5)
    print '.',

p.stopSubscriptions()




        







