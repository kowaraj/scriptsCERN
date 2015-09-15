#!/usr/bin/python


from subprocess import call
from time import sleep

##########################

def wr_vme(addr_s, data_s, verbose=True):
         if verbose:
                  print 'write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s
                  call(['write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s])
         else:
                  #print 'write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s
                  call(['write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s])

def rd_vme(addr_s, wlen=2, verbose=True):
         if verbose:
                  print "read_vme", "-w16", "-v", '-a'+addr_s, '-l'+str(wlen)
                  call(["read_vme", "-w16", "-v", addr_s, '-l2'])
         else:
                  #print "read_vme", "-w16", "-v", '-a'+addr_s, '-l'+str(wlen)
                  call(["read_vme", "-w16", "-v", addr_s, '-l2'])

def do_wr_strobe():
	 print '! wr_strobe'
	 call(["write_vme", "-w16", '-a400046', '-d0x1010'])
def do_freeze():
	 print '! freeze'
	 call(["write_vme", "-w16", '-a400110', '-d0x8080'])
	 call(["read_vme", "-w16", '-v', '-a40011e'])
def do_release():
	 print '! release, check:'
	 call(["write_vme", "-w16", '-a400110', '-d0x4040'])
	 call(["read_vme", "-w16", '-v', '-a40011e'])

         
def wr_vme_regdata(data32b, verbose=True):
         wr_vme('400058', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('40005a', '0x%-4x'%(data32b & 0x0000FFFF), verbose)
def wr_vme_regaddr(data32b, verbose=True):
         wr_vme('40005c', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('40005e', '0x%-4x'%(data32b & 0x0000FFFF), verbose)
def wr_obsmem_addr(data32b, verbose=True):
         wr_vme('400060', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('400062', '0x%-4x'%(data32b & 0x0000FFFF), verbose)
def read_data():
         from subprocess import Popen, PIPE
         p = Popen(['read_vme', '-w16', '-a480004'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         return output
def read_data_dbg():
         from subprocess import Popen, PIPE
         p = Popen(['read_vme', '-w16', '-v', '-a40004c', '-l12'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         return output
def read_data_ml():
         from subprocess import Popen, PIPE
         p = Popen(['read_vme', '-w16', '-v', '-a400064', '-l7'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         return output

########################


do_release()
wr_vme_regdata(0xcaca)
wr_obsmem_addr(0x0)
do_wr_strobe()
raw_input("1f")
wr_vme_regdata(0xbaba)
wr_obsmem_addr(0x1f)
do_wr_strobe()
raw_input("20")
wr_vme_regdata(0xdede)
wr_obsmem_addr(0x20)
do_wr_strobe()
raw_input("21")
wr_vme_regdata(0xfafa)
wr_obsmem_addr(0x21)
do_wr_strobe()
# wr_vme_regdata(0xadad)
# wr_obsmem_addr(0x23)
# do_wr_strobe()

do_freeze()
wr_vme_regaddr(0x0)
ret = read_data()
print 'ret = ', ret
raw_input()

# retdbg = read_data_dbg()
# print 'dbg = \n', retdbg
# retml = read_data_ml()
# print 'ml = \n', retml

ret = read_data()
print 'ret = ', ret
# retdbg = read_data_dbg()
# print 'dbg = \n', retdbg
# retml = read_data_ml()
# print 'ml = \n', retml




# wr_vme_regaddr(0x1f)
# ret = read_data()
# print 'ret = ', ret
# wr_vme_regaddr(0x20)
# ret = read_data()
# print 'ret = ', ret







