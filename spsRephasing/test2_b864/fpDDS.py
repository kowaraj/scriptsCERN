import sys
from time import sleep
import spsFreqProgDDS
print 'reload(fpdds); cf = fpdds.fpdds(4)'
print 'cf.init_module()'

'''
Setup fpDDS:
 - 


Mods:

 - 20160119 - original version

'''

class fpdds(object):
        REG_CSR = 0
        REG_FR1 = 1
        REG_FR2 = 2
        REG_CFR = 3
        REG_CFTW0 = 4
        REG_ACR = 6 #amplitude control register
        REG_CW1 = 0xa
        REG_CW2 = 0xb
        REG_CW3 = 0xc

        MOD_LEV2 = 0 << 8 #2-lev #not needed, but other channel uses 4 lev
        MOD_LEV4 = 1 << 8 #4-lev #not needed, but other channel uses 4 lev
        MOD_FREQ = 2 << 22 #modulation = freq
        MOD_AMPL = 1 << 22 #modulation = amplitude
        MOD_DIS = 0 << 22 #modulation = disabled
        DAC_FULLSCALE  = 3 << 8 #full
        WAVE_COS = 0 << 0 #cos
        WAVE_SIN = 1 << 0 #sin
        DDS_CH0 = 1 << 4
        DDS_CH1 = 2 << 4


        def enaVmeAccessToDDS(self,x=True):
                VME = 0x0400
                FPGA = 0x0404
                reg = VME if x else FPGA
                print 'VME access', 'enabled' if x else 'disabled'
                print 'reg = ', hex(reg)
                self.m.control2 = reg

        def send_to_dds(self, data, reg):
                print '0x%08x'%data, ' -> ', hex(reg)
                self.m.ddsData = data
                self.m.ddsRegSel = reg
        
        def update_dds_io(self):
                print 'Update DDS IO\n'
                self.m.control1 = 0x0202 #bit1
   
        def setup_dds_ch0(self):
                print "Setup DDS channel 0: no modulation, SIN, fullscale "                
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV2, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_SIN, self.REG_CFR)

        def setup_dds_ch1(self):
                print "Setup DDS channel 1: no modulation, COS, fullscale "                
                self.send_to_dds(self.DDS_CH1, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV2, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        def fpdds_f2ftw(self, f):
                ftw = (2.5e+8 - f) * pow(2,32) / 5e+8
                return ftw

        def fpdds_ftw2f(self, ftw):
                f = 2.5e+8 - ftw * 5e+8 / pow(2,32)
                return f

        def setup_dds_out(self, ftw):
                print 'Setup DDS out to FTW = ', hex(ftw), ':  ', self.fpdds_ftw2f(ftw)
                self.setup_dds_ch0()
                self.send_to_dds(ftw, self.REG_CFTW0)
                self.setup_dds_ch1()
                self.send_to_dds(ftw, self.REG_CFTW0)
                self.update_dds_io() #up!

        def read_settings(self):
                ftw_sd = self.m.serialFTW
                f_sd = ftw_sd * 5e+8 / pow(2,32) + 2.5e+8
                print 'FTW SerDes = ', hex(ftw_sd), '=> f = ', f_sd
                ftw_fsk = self.m.fskFTW
                f_fsk = ftw_fsk * 5e+8 / pow(2,32) + 2.5e+8
                print 'FTW FSK = ', hex(ftw_fsk), '=> f = ', f_fsk
                print ''
                print 'status: mDDS selected (not fpDDS)  = ', bool(self.m.mddsStatus & 0x0001)
                print 'control: CFP selected (not serDes) = ', bool(self.m.mddsControl & 0x0202)

        def init_module(self):
                print 'Initializing fpDDS module'
                print 'Firmware version: ', self.m.firmwareVersion
                self.enaVmeAccessToDDS()

                print 'Select all channels'
                self.send_to_dds(0x000000f0, self.REG_CSR)
                self.update_dds_io() #up!
                print 'Reset DDS'
                DDS_RESET = 0x0101
                self.m.control1 = DDS_RESET
                print 'Status = ', hex(self.m.status1)

                self.setup_dds_out(0x19999999)
                

                print 'Select all channels (for later programming? may not be needed)'
                self.send_to_dds(0x000000f0, self.REG_CSR)

                # print '!!! Keep VME access for fpDDS - for testing only!'
                # self.setup_dds_out(0x1a1f9999)
                # raw_input("!!!set to 0x1a1f9999")
                self.enaVmeAccessToDDS(False)
                
        def __init__(self, slot):
                self.m = spsFreqProgDDS.Module.slot(slot)
                print 'Check if it is really a fpDDS, not mDDS'
                print 'not impl.yet'
