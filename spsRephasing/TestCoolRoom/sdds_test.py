import sys
from time import sleep
import spsSlaveDDSMap
print 'reload(sdds); cs = sdds.sdds(6)'
print 'cs.init_module(6)'

'''
- 20160111 - fixed FTW_AVG from 200 to 200.22
'''
print 's.setup_dds_freq("RF1", 200, 205, 210, 215)'
print 's.setup_dds_freq("RF2", 202, 207, 212, 217)'
print 'import spsSlaveDDSMap'
print 'm = spsSlaveDDSMap.Module.slot(6)'



'''
RF1 (ch1, scope_ch3)
RF2 (ch0, scope_ch4)
ctrl           in real
bit            bit
3210   ch1 ch0 2301
ps     RF1 RF2 
0000   200 202 0000
0001   200 211 0010
0010   200 207 0001
0011   200 217 0011
0011   200 217 
0111   210 217
1011   205 217
1111   215 217
'''

class sdds(object):
        ddsControl_reset = 0x0101
        ddsControl_upd_intfc = 0x0404
        ddsControl_upd_io = 0x0202

        MOD_LEV2 = 0 << 8 #2-lev #not needed, but other channel uses 4 lev
        MOD_LEV4 = 1 << 8 #4-lev #not needed, but other channel uses 4 lev
        MOD_FREQ = 2 << 22 #modulation = freq
        MOD_AMPL = 1 << 22 #modulation = amplitude
        MOD_DIS = 0 << 22 #modulation = disabled
        DAC_FULLSCALE  = 3 << 8 #full
        WAVE_COS = 0 << 0 #cos
        DDS_CH0 = 1 << 4
        DDS_CH1 = 2 << 4

        REG_CSR = 0
        REG_FR1 = 1
        REG_FR2 = 2
        REG_CFR = 3
        REG_CFTW0 = 4
        REG_ACR = 6 #amplitude control register
        REG_CW1 = 0xa
        REG_CW2 = 0xb
        REG_CW3 = 0xc

        def sdds_ftw1p2fcav(self, ftw1p):
                frev = 43286.133 #354.6MHz clock (from mDDS)
                f = (pow(2,32) - ftw1p)*frev/pow(2,19)
                #print 'fcav = ', f, ' for ftw1p = ', hex(ftw1p)
                return f

        def sdds_FTW2p(self, ftw1p):
                ftw2p = int( pow(2,33) - pow(2,20)*4620 - ftw1p )
                #print 'ftw2p = ', hex(ftw2p), ' for ftw1p = ', hex(ftw1p)
                self.sdds_ftw1p2fcav(ftw1p)
                return ftw2p

        def _doUpdateDDSIO(self):
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

        # Synch'ing Toggle to BP Frev

        def _doSyncToggleToBPFrev(self):
                #print 'Synchronize toggling to BPFrev: ddsControl = 0x1010 (b4, a/c)'
                self.m.ddsControl = 0x1010 #bit4 a/c

        # Synch'ing DDS to FpFrev

        def _selFpFrevAsDDSClock(self, x=True):
                if x:
                        #print 'Select DDS sync to be FpFrev: control1 = 0x0202 (b1)'
                        self.m.control1 = 0x0202 #bit1
                else:
                        #print 'Select DDS sync to be BPFrev: control1 = 0x0200 (b1)'
                        self.m.control1 = 0x0200 #bit1

        def _doSyncDDSToFpFrev(self):
                self._enaVmeAccessToDDS(1)
                self._selFpFrevAsDDSClock(1)
                self.send_to_dds(0x00000080, self.REG_FR2)
                self._doUpdateDDSIO()
                self.send_to_dds(0x00000000, self.REG_FR2)
                self._doUpdateDDSIO()
                self._enaVmeAccessToDDS(0)

        def _doSyncDDSToFpFrevDisable(self):
                self._enaVmeAccessToDDS(1)
                self.send_to_dds(0x00000000, self.REG_FR2)
                self._doUpdateDDSIO()
                self._enaVmeAccessToDDS(0)
        def _doSyncDDSToFpFrevEnable(self):
                self._enaVmeAccessToDDS(1)
                self.send_to_dds(0x00000080, self.REG_FR2)
                self._doUpdateDDSIO()
                self._enaVmeAccessToDDS(0)

        def _loop_doSyncDDSToFpFrevEnable(self):
                while(1):
                        self._enaVmeAccessToDDS(1)
                        self.send_to_dds(0x00000080, self.REG_FR2)
                        #self._doUpdateDDSIO()
                        self._enaVmeAccessToDDS(0)
                        sleep(0.1)
                        #print('done')

        def _loop_manualSync(self):
                print('v.0.2.013')
                while(1):
                        sleep(0.2)

                        self.init_module()
                        self.sync_manual_plus_ddsioup_plusFTW()
                        self.sync_manual_plus_ddsioup_plusFTW()
                        self.sync_manual_plus_ddsioup_plusFTW()

                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup_FAKE()
                        self.sync_manual_plus_ddsioup_FAKE()
                        self.sync_manual_plus_ddsioup_FAKE()
                        self.sync_manual_plus_ddsioup_FAKE()
                        self.sync_manual_plus_ddsioup_FAKE()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()
                        self.sync_manual_plus_ddsioup()

        def _loop_SC_Init_AutoSync_DDSIO(self):
                print('v.0.1.002')
                while(1):
                        sleep(0.2)
                        print('Start SC')
                        self.init_module()
                        ##print('Wait for 0.1s...')
                        sleep(0.1)
                        ##print('Sync 1/4 Divider')
                        self.test_AutoSync()
                        ##print('Done\n')


        def test_AutoSync_enable(self):

                print('ena autoSync. vme_ena')
                self.vme_ena()
                self.as_ena() # Enable Autosync
                #self.load_ftw()
                print('no load ftw')
                self.dds_io_up()

                # self.as_dis() # Disable Autosync
                # self.load_ftw()
                # self.dds_io_up()

                self.vme_dis()
                print('done. vme_dis')

        def test_AutoSync(self):


                # 1.
                self.vme_ena()

                self.as_ena() # Enable Autosync
                self.load_ftw()
                self.dds_io_up()

                self.as_dis() # Disable Autosync


#                self.load_ftw()
                self.dds_io_up()

                self.vme_dis()

                # --
                self.vme_ena()

                self.zero_ftw()
                self.dds_io_up()
                self.load_ftw()
                self.dds_io_up()

                self.zero_ftw()
                self.dds_io_up()
                self.load_ftw()
                self.dds_io_up()

                self.vme_dis()

                # 2.
                self.vme_ena()
                self.as_ena()
                self.dds_io_up()
                self.as_dis()
                self.dds_io_up()
                self.vme_dis()







        def vme_ena(self):
                self._enaVmeAccessToDDS(1)

        def vme_dis(self):
                self._enaVmeAccessToDDS(0)


        def master_ena(self):
                self.send_to_dds(0x00000040, self.REG_FR2)
        def master_dis(self):
                self.send_to_dds(0x00000000, self.REG_FR2)

        def as_ena(self):
                self.send_to_dds(0x00000080, self.REG_FR2)

        def as_dis(self):
                self.send_to_dds(0x00000000, self.REG_FR2)



        def sync_manual_plus_ddsioup_FAKE(self):
                self.vme_ena()

                #self.send_to_dds(0x00000001, self.REG_FR1)
                self.dds_io_up()

                self.vme_dis()

        def sync_manual_plus_ddsioup(self):
                self.vme_ena()

                self.send_to_dds(0x00000001, self.REG_FR1)
                self.dds_io_up()

                self.vme_dis()

        def sync_manual_plus_ddsioup_plusFTW(self):
                self.vme_ena()

                self.send_to_dds(0x00000001, self.REG_FR1)
                self.dds_io_up()

                self.load_ftw()
                self.dds_io_up()

                self.vme_dis()



        def dds_io_up(self):
                self._doUpdateDDSIO()

        def load_ftw(self):
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq_avg()
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq_avg()

        def zero_ftw(self):
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq_zero()
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq_zero()










        # def _selDDSSignals(self, x):
        #         if x == 1:
        #                 #print 'real'
        #                 self.m.debugControl2 = 0x0404
        #         else:
        #                 #print 'fake'
        #                 self.m.debugControl2 = 0x0400

        # def _strobeIntfcReady(self):
        #         #print 'strobe to IntfcReady'
        #         self.m.debugControl2 = 0x0808

        def _enaVmeAccessToDDS(self, x):
                if x == 1:
                        #print 'VME access'
                        self.m.ddsControl = 0x0808
                else:
                        #print 'FPGA access'
                        self.m.ddsControl = 0x0800

        def _selDDS_CW(self, x, y):
                if y == 1:
                        if x == 0:
                                #print 'CW0'
                                self.m.ddsControl2 = 0x0f00
                        elif x == 1:
                                #print 'CW1'
                                self.m.ddsControl2 = 0x0f01
                        elif x == 2:
                                #print 'CW2'
                                self.m.ddsControl2 = 0x0f02
                        elif x == 3:
                                #print 'CW3'
                                self.m.ddsControl2 = 0x0f03
                        else:
                                #print 'not def'
                                pass
                else:
                        #print 'not def'
                        pass


        def _selFrevFP(self, x):
                if x == 1:
                        #print 'select Fp Frev (prog) sync'
                        self.m.control1 = 0x0202
                else:
                        #print 'select BP Frev (master) sync'
                        self.m.control1 = 0x0200

        def __init__(self, slot):
                self.m = spsSlaveDDSMap.Module.slot(slot)

        def reset_dds(self):
                print 'Reset DDS'
                self.m.ddsControl = self.ddsControl_reset
                #print 'Wait for 0.1s'
                sleep(0.1)

        def clear_phase_acc(self):
                self.send_to_dds(0x00002000, self.REG_FR2)
                self._doUpdateDDSIO()
                self.send_to_dds(0x00000000, self.REG_FR2)
                self._doUpdateDDSIO()
                

        def send_to_dds(self, data, reg):
                #print '0x%08x'%data, ' -> ', hex(reg)
                self.m.ddsData = data
                self.m.ddsRegSel = reg
                self.m.ddsControl = self.ddsControl_upd_intfc
                
        def f2ftw(self, freq):
                ext_clk = 354600000.
                f = freq*1e+6
                ftw  = (1- f/ext_clk)*pow(2,32)
                #print 'f2ftw: f = ', f, ' => ftw = ', hex(int(round(ftw)))
                return int(round(ftw))

        def setup_dds_freq(self, f1, f2, f3, f4):
                self.setup_dds_ftw(self.f2ftw(f1), self.f2ftw(f2), self.f2ftw(f3), self.f2ftw(f4))
        def setup_dds_freq_avg(self):
                self.setup_dds_ftw(0x6fa00000, 0x6fa00000, 0x6fa00000, 0x6fa00000)
        def setup_dds_freq_zero(self):
                self.setup_dds_ftw(0x00000000, 0x00000000, 0x00000000, 0x00000000)

        #set FTW0-3 for FreqModulation
        def setup_dds_ftw(self, FTW1, FTW2, FTW3, FTW4):
                #print 'Sending FTWs...'
                self.send_to_dds(FTW1, self.REG_CFTW0)
                self.send_to_dds(FTW2, self.REG_CW1)
                self.send_to_dds(FTW3, self.REG_CW2)
                self.send_to_dds(FTW4, self.REG_CW3)

        #set CW0-3 for Amplitudeodulation
        def setup_dds_CWs_AM(self, v1,v2,v3,v4):#, ACR, CW1, CW2, CW3):
                #print 'Sending FTW0 and CWs...'
                self.send_to_dds(self.f2ftw(200.0), self.REG_CFTW0)
                self.send_to_dds(v1, self.REG_ACR)
                self.send_to_dds(v2, self.REG_CW1)
                self.send_to_dds(v3, self.REG_CW2)
                self.send_to_dds(v4, self.REG_CW3)


        # setup RF1 - FTW AVG
        def setup_dds_ch1(self):
                #print "Setup DDS channel 1 (RF1, Average)..."
                self.send_to_dds(self.DDS_CH1, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_DIS | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)


        # setup RF2 - FTW FSK
        def setup_dds_ch0(self):
                #print "Setup DDS channel 0 (RF2, FSK)... "
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_FREQ | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        # setup RF2 - FTW FSK
        def setup_dds_ch0_AM(self):
                #print "Setup DDS channel 0 (RF2, FSK)... "
                self.send_to_dds(self.DDS_CH0, self.REG_CSR)
                self.send_to_dds(self.MOD_LEV4, self.REG_FR1)
                self.send_to_dds(0, self.REG_FR2)
                self.send_to_dds(self.MOD_AMPL | self.DAC_FULLSCALE | self.WAVE_COS, self.REG_CFR)

        def setup_data(self):
                #print 'Write RF On/Off offsets...'
                self.m.rfOnOffset = 0x5
                self.m.rfOffOffset = 0x550


        def init_dds(self):
                #print 'Initializing DDS...'
                self._selDDSDataSource(0) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq(200, 200, 200, 200)
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq(200, 200, 200, 200)
                
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._selDDSDataSource(1) # to FPGA

        def sendDebugFpSLData(self, freq):
                ftw = self.f2ftw(freq)
                self.m.debugControl2 = 0x0101; #debug on
                self.m.debugFpSLFTW1 = ftw #data
                self.m.debugControl = 0x0202 #strobe
                self.m.debugControl2 = 0x0100; #debug off

        def sendDebugFpSLDataFTW(self, ftw):
                self.m.debugControl2 = 0x0101; #debug on
                self.m.debugFpSLFTW1 = ftw #data
                self.m.debugControl = 0x0202 #strobe
                #print 'debugC2.selFpSLink =     ', bool(self.m.debugControl2 & 0x0001)
                self.m.debugControl2 = 0x0100; #debug off

        def stat(self):
                self.status()
                self.faults()
                self.controls()
                #print 'clearing faults'
                self.m.control1 = 0x0101
                self.m.debugControl = 0x0101
                #print 'Frev offset   = ', self.m.frevPhaseOffset
                #print 'RF_ON offset  = ', self.m.rfOnOffset
                #print 'RF_OFF offset = ', self.m.rfOffOffset
                
        def status(self):
                #print 'debugFTW1 =       ', hex(self.m.debugFTW1)
                #print 'debugFTW2 =       ', hex(self.m.debugFTW2)
                #print 'debugFTW1p =      ', hex(self.m.debugFTW1p)
                #print 'debugFpSLFTW1rb = ', hex(self.m.debugFpSLFTW1rb)
                #print 'lastDataToDDS =   ', hex(self.m.debugDDSData)
                #print 'lastRegSelToDDS = ', hex(self.m.debugDDSData)
                #print 'lastRegSelToDDS = ', hex((self.m.debugDDSRegSel & 0x0FFF))
                #print 'send2dds state =  ', bin((self.m.debugDDSRegSel & 0xf000) >> 12)
                #print ''
                #print 'debugStatus.upd_p1 =        ', bool(self.m.debugStatus & 0x8000)
                #print 'debugStatus.upd_p2 =        ', bool(self.m.debugStatus & 0x4000)
                #print 'debugStatus.busy_p1 =       ', bool(self.m.debugStatus & 0x2000)
                #print 'debugStatus.busy_p2 =       ', bool(self.m.debugStatus & 0x1000)
                #print 'debugStatus.rfON =          ', bool(self.m.debugStatus & 0x0800)
                #print 'debugStatus.ftw2isOnline =  ', bool(self.m.debugStatus & 0x0400)
                #print 'debugStatus.AVR =           ', bool(self.m.debugStatus & 0x0200)
                #print 'debugStatus.pair2isOnline = ', bool(self.m.debugStatus & 0x0100)
                #print 'debugStatus.ps =            ', hex((self.m.debugStatus & 0x00F0) >> 4)
                #print 'debugStatus.fpSLDataRxd =   ', bool(self.m.debugStatus & 0x0004)
                #print ''
                #print 'debugFlags.bpFrevDetected = ', bool(self.m.debugFlags & 0x0020)
                #print 'debugFlags.send2ddsReset =  ', bool(self.m.debugFlags & 0x0010)
                #print 'debugFlags.syncToFrevDone = ', bool(self.m.debugFlags & 0x0008)
                pass

        def faults(self):
                #print 'faults.toggleOnOff = ', bool(self.m.faults & 0x8000)
                #print 'faults.p2busy =      ', bool(self.m.faults & 0x4000)
                #print 'faults.p1busy =      ', bool(self.m.faults & 0x2000)
                #print 'faults.p1p2 =        ', bool(self.m.faults & 0x1000)
                #print 'faults.calcFTW2 =    ', bool(self.m.faults & 0x0800)
                # #print 'faults.selFrevBP =   ', bool(self.m.faults & 0x0400)
                # #print 'faults.noFrev = (!)  ', bool(self.m.faults & 0x0200) 
                pass

        def controls(self):
                #print 'ddsControl             = ', hex(self.m.ddsControl)
                #print 'control1.selSyncFpFrev = ', bool(self.m.control1 & 0x0002)
                #print 'ddsControl.enaVme =      ', bool(self.m.ddsControl & 0x0008)
                #print 'debugC2.selFpSLink =     ', bool(self.m.debugControl2 & 0x0001)
                pass

        def init_dds_2(self):
                #print '2 Initializing DDS...'
                self._enaVmeAccessToDDS(1) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                #self.setup_dds_freq(200.22, 200.22, 200.22, 200.22)
                self.setup_dds_freq_avg()
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq(200.2, 199.5, 220.2, 220.5)
                
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._enaVmeAccessToDDS(0) # to FPGA

        def init_module(self):
                #print 'Initializing sDDS module'
                #print 'Firmware version: ', self.m.firmwareVersion
                self._enaVmeAccessToDDS(1) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq_avg()
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_freq_avg()
                
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                #self.clear_phase_acc()


                # self.as_ena() # Enable Autosync
                # self.dds_io_up()
                # self.as_dis() # Disable Autosync
                # self.dds_io_up()



                self._enaVmeAccessToDDS(0) # to FPGA

        def setup_dds_freq_ftwInjection(self):
                self._enaVmeAccessToDDS(1)
                self.setup_dds_ch0() # RF2 = FSK
                self.setup_dds_ftw(0x6e980000, 0x6e980000, 0x6e980000, 0x6e980000)
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io
                self._enaVmeAccessToDDS(0) # to FPGA

        def init_dds_AM(self):
                #print 'Initializing DDS... (AmpMod)'
                self._selDDSDataSource(0) # to VME
                self.setup_data()

                self.reset_dds()
                self.setup_dds_ch1() # RF1 = AVG
                self.setup_dds_freq(200, 200, 200, 200)
                self.setup_dds_ch0_AM() # RF2 = FSK
                #scale = bits 31..22
                self.setup_dds_CWs_AM(0xffffffff, 0x7fffffff, 0xffffffff, 0xffffffff) 
                
                # UpdateDDS IO
                #print 'Update IO DDS'
                self.m.ddsControl = self.ddsControl_upd_io

                self._selDDSDataSource(1) # to FPGA

if __name__ == "__main__":
        if(len(sys.argv) < 2):
                #print "Argument required"
                exit(0)
        aCH = sys.argv[1]
        aFTW1  = int(sys.argv[2], 16)
        aFTW2  = int(sys.argv[3], 16)
        aFTW3  = int(sys.argv[4], 16)
        aFTW4  = int(sys.argv[5], 16)

        setup_dds(aCH, aFTW1, aFTW2, aFTW3, aFTW4)
