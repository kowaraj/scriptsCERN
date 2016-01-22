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


print '========================================'
print 'Do     : Cold reset on the crate...'
raw_input("ok?")
print 'Result : Nothing initialized. No signals'
raw_input("ok?")

print '========================================'
from subprocess import call
call(['write_vme', '-w16', '-v', '-a30007a', '-d0x8080'])
print 'Done   : Send IRQ1 to DSP on fpDSP module (slot3, control2, bit7)'
print 'Resul  : fpDSP started FTW transmition to fpDDS and mDDS over SerDes and CPF SCL'
print '         front panel LEDs blinking'
raw_input("ok?")

### Seq. step 1

print '========================================'
print 'Frequency Program DDS reset'
fpdds_i.init_module()
print 'Done   : fpDDS initialized. '
print 'Check  : fpDDS generates F RF Prog = 200MHz'
print 'Next!  : Do the RESET on FrevProg VTU and SoftStart'
raw_input("ok?")

print '========================================'
print 'Master DDS reset'
mdds_i.init_module()
print 'Done   : mDDS initialized. '
print 'Check  : mDDS generates sDDS clock = 354.6MHz + Error'
raw_input("ok?")
print ''
mdds_i.setADCGain(0) #zero gain to simulate the open loop
print 'Done   : Synchro loop OFF: mDDS ADC Gain = 0'
print 'Check  : mDDS generates sDDS clock = 354.6MHz exactly, err = 0'
raw_input("ok?")

print '========================================'
print 'Slave DDS reset'
sdds_i.init_module()
print 'Done   : sDDS initialized. '
print 'Check  : sDDS generates RF1 = RF_AVG = 199981934.46Hz'
print '       :                RF2 = RF_FSK = RF_AVG'
print 'Next!  : Do the RESET on FrevMaster VTU and SoftStart'
raw_input("ok?")

### Seq. step 2

print '========================================'
print '1/5 divider reset - NOT needed in the lab'
print 'ok.'


### Seq. step 3 

print '========================================'
print 'Synchro loop ON'
mdds_i.setADCGain(30) #simulate the closed loop
print 'Done   : Synchro loop ON: mDDS ADC Gain = 30'
print 'Result : RF Prog and RF_AVG and RF_FSK are all in phase'
print 'Check  : mDDS generates sDDS clock = 354.6MHz + error'
print 'Check2 : sDDS RF1 (RF_AVG) == RF_Prog (fpDDS) == 200MHz'
raw_input("ok?")

### Seq. step 4

print '========================================'
print 'Resynchronize 1/4 divider in DDS'
#print 'removed for test!!! '
sdds_i._doSyncDDSToFpFrev()
print 'Done   : sDDS\'s AD9959 DDS RF2 reg, Auto-sync enabled (and dis).'
print 'Result : Clock divider by4 sync\'d with FrevProg (sDDS front panel)'
print 'Check  : ? '
raw_input("ok?") 

### Seq. step 5

print '========================================'
print 'Resynchronize FrevMaster on FrevProg'
print 'Do!    : restart FrevMaster VTU to sync with FrevProg'
print 'Result : FrevMaster points to same bucket as FrevProg'
print 'Check  : predefined const delay b/w FrevMaster and FrevProg pulses'
raw_input("ok?") #check the results

### Seq. step 6

print '========================================'
print 'Frequency toggling resync on Frev'
sdds_i._doSyncToggleToBPFrev()
print 'Done   : Toggling f1/f2 synced to FrevMaster (Back-plane)'
print 'Result : The uncertainty is 2.8ns as 1/4 of SYNC_CLK (one REF_CLK period)'
print 'Notes  : Done with the operation at h=4620, from now on FTW1 and FTW2 can differ'
raw_input("ok?")


### Seq. step 7

print '========================================'
print 'Start FSK modulation'
sdds_i.sendDebugFpSLDataFTW(0x6e980000)
print 'Done   : send 0x6e980000 as FTW1 (debug Fp SL Data)'
print 'Result : ph_error = 2.8degrees masx at 200MHz (40ps)'
raw_input("ok?")

print 'Done.'






