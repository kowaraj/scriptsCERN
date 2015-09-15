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
	 call(["read_vme", "-w16", '-v', '-a40010e'])
def do_release():
	 print '! release, check:'
	 call(["write_vme", "-w16", '-a400110', '-d0x4040'])
	 call(["read_vme", "-w16", '-v', '-a40010e'])

         
def wr_vme_regdata(data32b, verbose=True):
         wr_vme('400058', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('40005a', '0x%-4x'%(data32b & 0x0000FFFF), verbose)
def wr_vme_regaddr(data32b, verbose=True):
         wr_vme('40005c', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('40005e', '0x%-4x'%(data32b & 0x0000FFFF), verbose)
def wr_obsmem_addr(data32b, verbose=True):
         wr_vme('400060', '0x%-4x'%(data32b >> 16), verbose)
         wr_vme('400062', '0x%-4x'%(data32b & 0x0000FFFF), verbose)

########################

try:
         #freeze the mem
         do_release()

         # #write 
         # N_addr = 200
         # # d = 0xa5a5a5a5
         # d = 0x3000
         # a = 0x1
         # for i in range(N_addr):
         #          wr_vme_regdata(d, verbose=False)
         #          wr_obsmem_addr(a, verbose=False)

         #          do_wr_strobe()
         #          d += 0x000f
         #          a += 0x2

except:
         print 'exception'


