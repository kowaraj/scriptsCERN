#!/user/mojedasa/python/Python-2.7.11/python

'''
mods:
- 20160119 - added fpdds, mdds
- 20160118 - open synchro loop moved before sdds re-init
- 20160118 - original version

'''
import fpdds
fpdds_i = fpdds.fpdds(4)
import mdds
mdds_i = mdds.mdds(5)
import sdds
sdds_i = sdds.sdds(6)



#Cold reset
print ''
print 'Do a Cold reset on the crate...'
raw_input("ok?")



### Seq. step 1

print '=============================='
print 'Before injection (fpDDS reset)'
fpdds_i.init_module()
raw_input("ok?")

print '============================='
print 'Before injection (mDDS reset)'
mdds_i.init_module()
raw_input("ok?")
print 'Synchro loop OFF'
mdds_i.setADCGain(0) #zero gain to simulate the open loop
raw_input("ok?") #check the results

print '======================================='
print 'Before injection (Ions Slave DDS reset)'
sdds_i.init_module()
raw_input("ok?")





### Seq. step 2

print ''
print '1/5 divider reset - NOT needed in the lab'
print 'ok.'


### Seq. step 3 

print ''
print 'Synchro loop ON'
mdds_i.setADCGain(30) #simulate the closed loop
raw_input("ok?") #check the results


### Seq. step 4

print ''
print 'Resynchronize 1/4 divider in DDS'
sdds_i._doSyncDDSToFpFrev()
raw_input("ok?") #check the results


### Seq. step 5

print ''
print 'Resynchronize Master Frev on Frev prog'
print 'Do the SoftRestart for the MasterFrev VTU'
raw_input("ok?") #check the results


### Seq. step 6

print ''
print 'Frequency toggling resync on Frev'
sdds_i._doSyncToggleToBPFrev()
raw_input("ok?")


### Seq. step 7

print ''
print 'Start FSK modulation: send 0x6e980000 as FTW1 (debug Fp SL Data)'
sdds_i.sendDebugFpSLDataFTW(0x6e980000)
raw_input("ok?")


print ''
print 'done.'
## seq





