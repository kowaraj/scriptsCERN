import sys
from time import sleep
import spsFreqProgDDS

'''
Setup mDDS:
 - 


Mods:

 - 20160118 - fixed FTW_AVG from 200 to 200.22

'''

class mdds(object):
        def setADCGain(self, val):
                print 'ADC Gain = ', val
                self.m.mddsADCGain = val

        def __init__(self, slot):
                self.m = spsFreqProgDDS.Module.slot(slot)
