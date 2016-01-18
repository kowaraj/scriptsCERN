import sys
from time import sleep
import spsFreqProgDDS

'''
- 20160115 - original version

'''

print 'Usage from a python shell:'
print 'import fpdds'
print 'mod_fpdds = fpdds.fpdds(4)'
print 'mod_fpdds....'
print 'import spsFreqProgDDS'
print 'm = spsFreqProgDDS.Module.slot(4)'

class fpdds(object):
        #ddsControl_upd_io = 0x0202

        #MOD_LEV2 = 0 << 8 #2-lev #not needed, but other channel uses 4 lev

        def _doUpdateDDSIO(self):
                # UpdateDDS IO
                print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

        # Synch'ing Toggle to BP Frev

        def _doSyncToggleToBPFrev(self):
                print 'Synchronize toggling to BPFrev: ddsControl = 0x1010 (b4, a/c)'
                self.m.ddsControl = 0x1010 #bit4 a/c

        # Synch'ing DDS to FpFrev

        def _selFpFrevAsDDSClock(self, x=True):
                if x:
                        print 'Select DDS sync to be FpFrev: control1 = 0x0202 (b1)'
                        self.m.control1 = 0x0202 #bit1
                else:
                        print 'Select DDS sync to be BPFrev: control1 = 0x0200 (b1)'
                        self.m.control1 = 0x0200 #bit1
        def _doSyncDDSToFpFrev(self):
                self._selDDSDataSource(0) # to VME
                self._selFpFrevAsDDSClock(1)
                self.send_to_dds(0x00000080, self.REG_FR2)
                self._doUpdateDDSIO()
                self.send_to_dds(0x00000000, self.REG_FR2)
                self._doUpdateDDSIO()
                self._selDDSDataSource(1) # to FPGA

        def _selDDSSignals(self, x):
                if x == 1:
                        print 'real'
                        self.m.debugControl2 = 0x0404
                else:
                        print 'fake'
                        self.m.debugControl2 = 0x0400

        def _strobeIntfcReady(self):
                print 'strobe to IntfcReady'
                self.m.debugControl2 = 0x0808

        def _enaVmeAccessToDDS(self, x):
                if x == 1:
                        print 'VME access'
                        self.m.ddsControl = 0x0808
                else:
                        print 'FPGA access'
                        self.m.ddsControl = 0x0800

        def _selDDS_CW(self, x, y):
                if y == 1:
                        if x == 0:
                                print 'CW0'
                                self.m.ddsControl2 = 0x0f00
                        elif x == 1:
                                print 'CW1'
                                self.m.ddsControl2 = 0x0f01
                        elif x == 2:
                                print 'CW2'
                                self.m.ddsControl2 = 0x0f02
                        elif x == 3:
                                print 'CW3'
                                self.m.ddsControl2 = 0x0f03
                        else:
                                print 'not def'
                else:
                        print 'not def'


        def _selFrevFP(self, x):
                if x == 1:
                        print 'select Fp Frev (prog) sync'
                        self.m.control1 = 0x0202
                else:
                        print 'select BP Frev (master) sync'
                        self.m.control1 = 0x0200

        def __init__(self, slot):
                self.m = spsSlaveDDSMap.Module.slot(slot)

        def reset_dds(self):
                print 'Reset DDS'
                self.m.ddsControl = self.ddsControl_reset
                sleep(0.5)
        
        def send_to_dds(self, data, reg):
                print '0x%08x'%data, ' -> ', hex(reg)
                self.m.ddsData = data
                self.m.ddsRegSel = reg
                self.m.ddsControl = self.ddsControl_upd_intfc
                
        def f2ftw(self, freq):
                ext_clk = 354600000.
                f = freq*1e+6
                ftw  = (1- f/ext_clk)*pow(2,32)
                print 'f2ftw: f = ', f, ' => ftw = ', hex(int(round(ftw)))
                return int(round(ftw))

        def setup_dds_freq(self, f1, f2, f3, f4):
                self.setup_dds_ftw(self.f2ftw(f1), self.f2ftw(f2), self.f2ftw(f3), self.f2ftw(f4))
        def setup_dds_freq_avg(self):
                self.setup_dds_ftw(0x6fa00000, 0x6fa00000, 0x6fa00000, 0x6fa00000)

        #set FTW0-3 for FreqModulation
        def setup_dds_ftw(self, FTW1, FTW2, FTW3, FTW4):
                print 'Sending FTWs...'
                self.send_to_dds(FTW1, self.REG_CFTW0)
                self.send_to_dds(FTW2, self.REG_CW1)
                self.send_to_dds(FTW3, self.REG_CW2)
                self.send_to_dds(FTW4, self.REG_CW3)

        #set CW0-3 for Amplitudeodulation
        def setup_dds_CWs_AM(self, v1,v2,v3,v4):#, ACR, CW1, CW2, CW3):
                print 'Sending FTW0 and CWs...'
                self.send_to_dds(self.f2ftw(200.0), self.REG_CFTW0)
                self.send_to_dds(v1, self.REG_ACR)
                self.send_to_dds(v2, self.REG_CW1)
                self.send_to_dds(v3, self.REG_CW2)
                self.send_to_dds(v4, self.REG_CW3)


        # setup RF1 - FTW AVG
        def setup_dds_ch1(self):
                print "Setup DDS channel 1 (RF1, Average)..."
                self.send_to_dds(self.DDS_CH1, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)


        # setup RF2 - FTW FSK
        def setup_dds_ch0(self):
                print "Setup DDS channel 0 (RF2, FSK)... "
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_FREQ | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        # setup RF2 - FTW FSK
        def setup_dds_ch0_AM(self):
                print "Setup DDS channel 0 (RF2, FSK)... "
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_AMPL | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        def setup_data(self):
                print 'Write RF On/Off offsets...'
                self.m.rfOnOffset = 0x5
                self.m.rfOffOffset = 0x550


        def init_dds(self):
                print 'Initializing DDS...'
                self._selDDSDataSource(0) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq(200, 200, 200, 200)
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq(200, 200, 200, 200)
                
                # UpdateDDS IO
                print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._selDDSDataSource(1) # to FPGA

        def sendDebugFpSLData(self, freq):
                ftw = self.f2ftw(freq)
                self.m.debugControl2 = 0x0101; #debug on
                self.m.debugFpSLFTW1 = ftw #data
                self.m.debugControl = 0x0202 #strobe
                self.m.debugControl2 = 0x0100; #debug off

        def stat(self):
                self.status()
                self.faults()
                self.controls()
                print 'clearing faults'
                self.m.control1 = 0x0101
                self.m.debugControl = 0x0101
                
        def status(self):
                print 'debugFTW1 =       ', hex(self.m.debugFTW1)
                print 'debugFTW2 =       ', hex(self.m.debugFTW2)
                print 'debugFTW1p =      ', hex(self.m.debugFTW1p)
                print 'debugFpSLFTW1rb = ', hex(self.m.debugFpSLFTW1rb)
                print 'lastDataToDDS =   ', hex(self.m.debugDDSData)
                print 'lastRegSelToDDS = ', hex(self.m.debugDDSData)
                print 'lastRegSelToDDS = ', hex((self.m.debugDDSRegSel & 0x0FFF))
                print 'send2dds state =  ', bin((self.m.debugDDSRegSel & 0xf000) >> 12)
                print ''
                print 'debugStatus.upd_p1 =        ', bool(self.m.debugStatus & 0x8000)
                print 'debugStatus.upd_p2 =        ', bool(self.m.debugStatus & 0x4000)
                print 'debugStatus.busy_p1 =       ', bool(self.m.debugStatus & 0x2000)
                print 'debugStatus.busy_p2 =       ', bool(self.m.debugStatus & 0x1000)
                print 'debugStatus.rfON =          ', bool(self.m.debugStatus & 0x0800)
                print 'debugStatus.ftw2isOnline =  ', bool(self.m.debugStatus & 0x0400)
                print 'debugStatus.AVR =           ', bool(self.m.debugStatus & 0x0200)
                print 'debugStatus.pair2isOnline = ', bool(self.m.debugStatus & 0x0100)
                print 'debugStatus.ps =            ', hex((self.m.debugStatus & 0x00F0) >> 4)
                print 'debugStatus.fpSLDataRxd =   ', bool(self.m.debugStatus & 0x0004)
                print ''
                print 'debugFlags.bpFrevDetected = ', bool(self.m.debugFlags & 0x0020)
                print 'debugFlags.send2ddsReset =  ', bool(self.m.debugFlags & 0x0010)
                print 'debugFlags.syncToFrevDone = ', bool(self.m.debugFlags & 0x0008)


        def faults(self):
                print 'faults.toggleOnOff = ', bool(self.m.faults & 0x8000)
                print 'faults.p2busy =      ', bool(self.m.faults & 0x4000)
                print 'faults.p1busy =      ', bool(self.m.faults & 0x2000)
                print 'faults.p1p2 =        ', bool(self.m.faults & 0x1000)
                print 'faults.calcFTW2 =    ', bool(self.m.faults & 0x0800)
                # print 'faults.selFrevBP =   ', bool(self.m.faults & 0x0400)
                # print 'faults.noFrev = (!)  ', bool(self.m.faults & 0x0200) 
                
        def controls(self):
                print 'control1.selSyncFpFrev = ', bool(self.m.control1 & 0x0002)
                print 'ddsControl.enaVme =      ', bool(self.m.ddsControl & 0x0008)
                print 'debugC2.selFpSLink =     ', bool(self.m.debugControl2 & 0x0001)

        def init_dds_2(self):
                print '2 Initializing DDS...'
                self._enaVmeAccessToDDS(1) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                #self.setup_dds_freq(200.22, 200.22, 200.22, 200.22)
                self.setup_dds_freq_avg()
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq(200.2, 199.5, 220.2, 220.5)
                
                # UpdateDDS IO
                print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._enaVmeAccessToDDS(0) # to FPGA

        def init_dds_AM(self):
                print 'Initializing DDS... (AmpMod)'
                self._selDDSDataSource(0) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq(200, 200, 200, 200)
                self.setup_dds_ch0_AM() # RF2 = FSK
                #scale = bits 31..22
                self.setup_dds_CWs_AM(0xffffffff, 0x7fffffff, 0xffffffff, 0xffffffff) 
                
                # UpdateDDS IO
                print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._selDDSDataSource(1) # to FPGA

if __name__ == "__main__":
        if(len(sys.argv) < 2):
                print "Argument required"
                exit(0)
        aCH = sys.argv[1]
        aFTW1  = int(sys.argv[2], 16)
        aFTW2  = int(sys.argv[3], 16)
        aFTW3  = int(sys.argv[4], 16)
        aFTW4  = int(sys.argv[5], 16)

        setup_dds(aCH, aFTW1, aFTW2, aFTW3, aFTW4)
