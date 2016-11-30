import sys
from time import sleep
import spsFreqProgDDS

print 'reload(mdds); cm = mdds.mdds(5)'
print 'cm.init_module()'

'''
Setup mDDS:
 - 

Mods:

 - 20160118 - fixed FTW_AVG from 200 to 200.22

'''

class mdds(object):
        C_FTWOffset_fp2mDDS = 0x1bf487fd #from mdds firmware

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


        def setADCGain(self, val):
                print 'ADC Gain = ', val
                self.m.mddsADCGain = val

        def enaVmeAccessToDDS(self,x=True):
                VME = 0x0400
                FPGA = 0x0404
                if x:
                        reg = VME 
                        print 'VME access enabled'
                else:
                        reg = FPGA
                        print 'VME access disabled'
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
                print "Setup DDS channel 0: no modulation, COS, fullscale "                
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV2, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        def setup_dds_ch1(self):
                print "Setup DDS channel 1: no modulation, SIN, fullscale "                
                self.send_to_dds(self.DDS_CH1, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV2, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_SIN, self.REG_CFR)

        def mdds_ftw2f(self, ftw):
                f = ftw * 5e+8 / pow(2,32) + 2.5e+8
                #print 'f = ', f, ' for ftw = ', hex(ftw)
                return f

        def mdds_f2ftw(self, f):
                ftw = int( (f - 2.5e+8) * pow(2,32) / 5e+8  )
                print 'for freq = ', f
                print ' -> ftw                       = ', hex(ftw)
                print ' -> ftw - C_FTWOffset_fp2mDDS = ', hex(ftw - self.C_FTWOffset_fp2mDDS)
                return ftw

        def mdds_serdesFTWOffset(self):
                k = 500e+6/pow(2,32)
                # mFTW * k = 354.6e+6 - 250e+6 
                #          = 100e+6 
                #          = 54.6e+6     +  50e+6     
                #          = 54.6e+6     +  k * fpFTW 
                # mFTW     = 54.6e+6 / k +  fpFTW 
                offset = int(round(54.6e+6 / k))
                ftw = 0x19999999
                ftw_serdes = ftw + offset
                print 'offset = ', hex(offset), ' + ', hex(ftw), ' = ', hex(ftw_serdes)

        def fpdsp_f2cfp(self, f):
                Finf_ui = 200394831
                two_to_20 = 1048576
                f_RF = f
                ret = Finf_ui - f_RF + two_to_20
                cfp_k = pow(2,-9)
                print 'cfp value = ', hex(int(ret * cfp_k)), ' for f = ', f
                
        def read_settings(self):
                print 'ADC        = ', self.m.mddsDbgADC
                print 'ADC offset = ', self.m.mddsADCOffset
                print 'ADC gain   = ', self.m.mddsADCGain
                print 'ADC calc   = ', hex(self.m.mddsDbgPhErr)
                print 'ADC rate   = ', (self.m.mddsControl & 0x000c) >> 2
                print ''
                print 'CFP        = ', self.m.mddsDbgCFP
                print 'CFP gain   = ', self.m.mddsCFPGain
                print 'CFP offset = ', self.m.mddsCFPOffset
                print ''
                print 'SerDes gain = ', self.m.mddsSerDesGain
                print 'SerDes offset = ', self.m.mddsSerDesOffset
                print ''
                print 'LPF Test FTW1 = ', hex(self.m.mddsLPFTestFTW1) , ' => f = ', self.mdds_ftw2f(self.m.mddsLPFTestFTW1),'or ', self.mdds_ftw2f(self.m.mddsLPFTestFTW1+self.C_FTWOffset_fp2mDDS)
                print 'LPF Test FTW  = ', hex(self.m.mddsLPFTestFTW2) , ' => f = ', self.mdds_ftw2f(self.m.mddsLPFTestFTW2),'or ', self.mdds_ftw2f(self.m.mddsLPFTestFTW2+self.C_FTWOffset_fp2mDDS)
                print 'LPF control   = ', hex(self.m.mddsLPFControl)
                print 'LPF control2  = ', hex(self.m.mddsLPFControl2)
                print ''
                print 'Test mode      = ', hex(self.m.mddsControl & 0x0010)
                print 'Test mode FTW1 = ', hex(self.m.mddsTestFTW1)   , ' => f = ', self.mdds_ftw2f(self.m.mddsTestFTW1)
                print 'Test mode FTW2 = ', hex(self.m.mddsTestFTW2)   , ' => f = ', self.mdds_ftw2f(self.m.mddsTestFTW2)
                print 'Test mode Ts   = ', hex(self.m.mddsTestTs)
                print ''
                ftw_cfp = self.m.mddsDbgCFPFTW
                print 'FTW (CFP)  = ', hex(ftw_cfp), ' => f = ',self.mdds_ftw2f(ftw_cfp)
                ftw_sd = self.m.serialFTW
                ftw_total = ftw_sd + self.C_FTWOffset_fp2mDDS                
                print 'FTW SerDes = ', hex(ftw_sd), ' => f = ', self.mdds_ftw2f(ftw_total)
                ftw = self.m.mddsFTW                
                print 'FTW out    = ', hex(ftw), ' => f = ', self.mdds_ftw2f(ftw)
                print ''
                print 'status: mDDS selected (not fpDDS)  = ', bool(self.m.mddsStatus & 0x0001)
                print 'control: CFP selected (not serDes) = ', bool(self.m.mddsControl & 0x0202)
                print 'control: control1                  = ', hex(self.m.control1)
                print 'mddsControl                        = ', hex(self.m.mddsControl)


        def init_settings(self):
                print 'Settings...'
                mddsc_selCFP_false = 0x0200
                mddsc_selCFP_true = 0x0202
                self.m.mddsControl = mddsc_selCFP_false            
                self.m.mddsADCGain = 0 #30 #0
                #raw_input("!!! gain set to 0, debug only")
                self.m.mddsADCOffset = -100 #0xff9c #-100
                self.m.mddsCFPGain = 998200
                self.m.mddsCFPOffset = 920767342
                self.m.mddsSerDesOffset = 0x62f6e99d
                self.m.mddsSerDesGain = 7263

        def setup_dds_out(self, ftw):
                print 'Setup dds out to FTW = ', hex(ftw), ' => f = ', self.mdds_ftw2f(ftw)
                self.setup_dds_ch0()
                self.send_to_dds(ftw, self.REG_CFTW0)
                self.setup_dds_ch1()
                self.send_to_dds(ftw, self.REG_CFTW0)
                self.update_dds_io() #up!

        def reset_module(self):
                print 'Select all channels'
                self.send_to_dds(0x000000f0, self.REG_CSR)
                self.update_dds_io() #up!
                print 'Reset DDS'
                DDS_RESET = 0x0101
                self.m.control1 = DDS_RESET
                self.update_dds_io() #up!
                print 'Status = ', hex(self.m.status1)


        def init_module(self):
                print 'Initializing mDDS module'
                print 'Firmware version: ', self.m.firmwareVersion

                self.init_settings()
                self.enaVmeAccessToDDS()
                self.reset_module()
                self.setup_dds_out(0x358e2196)
                self.enaVmeAccessToDDS(False)
                self.read_settings()

        def __init__(self, slot):
                self.m = spsFreqProgDDS.Module.slot(slot)

