#!/usr/bin/python


from subprocess import call
from time import sleep

def wr_vme(addr_s, data_s, verbose=True):
         if verbose:
                  print 'write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s
                  call(['write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s])
         else:
                  #print 'write_vme', '-w16', '-v', '-a'+addr_s, '-d'+data_s
                  call(['write_vme', '-w16', '-a'+addr_s, '-d'+data_s])

def rd_vme(addr_s, wlen=2, verbose=True):
         if verbose:
                  print "read_vme", "-w16", "-v", '-a'+addr_s, '-l'+str(wlen)
                  call(["read_vme", "-w16", "-v", addr_s, '-l2'])
         else:
                  #print "read_vme", "-w16", "-v", '-a'+addr_s, '-l'+str(wlen)
                  call(["read_vme", "-w16", addr_s, '-l2'])

def do_wr_strobe(): #write to obs mem
	 print '! wr_strobe'
	 call(["read_vme", "-w16", "-v", '-a400046', '-d0x1010'])
def do_rd_strobe(): #read from obs mem
         call(["read_vme", "-w16", '-a480000'])

def read_data_mem(sz):
         from subprocess import Popen, PIPE
         p = Popen(['read_vme', '-w16', '-a480000', '-l'+str(sz)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         return output





def do_freeze():
	 print '! freeze'
	 call(["write_vme", "-w16", '-a400110', '-d0x8080'])
	 call(["read_vme", "-w16", '-v', '-a40010e'])
def do_release():
	 print '! release, check:'
	 call(["write_vme", "-w16", '-a400110', '-d0x4040'])
	 call(["read_vme", "-w16", '-v', '-a40010e'])
def read_frz_addr():
         from subprocess import Popen, PIPE
         p = Popen(['read_vme', '-w16', '-a400106', '-l2'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         output, err = p.communicate()
         print 'frz = ', output
         return output
         
def wr_vme_regdata(data32b):
         wr_vme('400058', '0x%-4x'%(data32b >> 16), verbose=False)
         wr_vme('40005a', '0x%-4x'%(data32b & 0x0000FFFF), verbose=False)
def wr_vme_regaddr(data32b, verbose=True):         
         wr_vme('40005c', '0x%-4x'%(data32b >> 16), verbose=False)
         wr_vme('40005e', '0x%-4x'%(data32b & 0x0000FFFF), verbose=False)

#freeze the mem
do_freeze()
fa_arr = read_frz_addr().split()
fa = int(fa_arr[0],16) << 16 | int(fa_arr[1],16)
print 'fa = ', hex(fa)
raw_input("keep reading?")
N = fa
d = list()
a = 0x0
mem = read_data_mem(N)

for x in mem.split():
         xi = int(x,16)
         print hex(xi)
         d.append(xi)

#d1 = [d[(i+1)*2] for i in range(len(d)/2-1)]
#d2 = [d[(i+1)*2+1] for i in range(len(d)/2-1)]

#dder1 = [d[(i+1)*2]-d[i*2] for i in range(len(d)/2-1)]
#dder2 = [d[(i+1)*2+1]-d[i*2+1] for i in range(len(d)/2-1)]
         
import pylab as pl
#pl.plot(range(len(dder1)), dder1, c='r')
#pl.plot(range(len(dder2)), dder2, c='b')
# pl.plot(range(len(d1)), d1, c='r')
# pl.plot(range(len(d2)), d2, c='b')
#pl.plot(range(len(d)), d, c='r')

s = len(d)
#concat read
print 'd = ', [d[i] for i in range(50)]
dd = [d[i*2] | (d[i*2+1]<<16) for i in range(len(d)/2-1)]
print 'dd = ', [hex(dd[i]) for i in range(50)]
pl.figure(10)
#pl.plot(range(len(dd)), dd, c='r')
pl.scatter(range(len(dd)), dd, c='r')
ddder = [dd[i+1]-dd[i] for i in range(len(dd)-1)]
print 'ddder = ', [ddder[i] for i in range(50)]
pl.figure(11)
pl.plot(range(len(ddder)), ddder, c='b')
pl.show()

#simple read
# print 'd = ', [d[i] for i in range(s)]
# pl.figure(10)
# pl.plot(range(len(d)), d, c='r')
# dder = [d[i+1]-d[i] for i in range(len(d)-1)]
# print 'dder = ', [dder[i] for i in range(s-1)]
# pl.figure(11)
# pl.plot(range(len(dder)), dder, c='b')
# pl.show()

# #interleaved read
# d0 = [d[i*2] for i in range(len(d)/2-1)]
# d1 = [d[i*2+1] for i in range(len(d)/2-1)]
# print 'd0 = ', [hex(d0[i]) for i in range(s/2-1)]
# print 'd1 = ', [hex(d1[i]) for i in range(s/2-1)]
# pl.figure(21)
# pl.plot(range(len(d0)), d0, c='r')
# pl.figure(22)
# pl.plot(range(len(d1)), d1, c='r')
# d0der = [d0[i+1]-d0[i] for i in range(len(d0)-1)]
# d1der = [d1[i+1]-d1[i] for i in range(len(d1)-1)]
# print 'd0der = ', [d0der[i] for i in range(s/2-2)]
# print 'd1der = ', [d1der[i] for i in range(s/2-2)]
# pl.figure(23)
# pl.plot(range(len(d0der)), d0der, c='b')
# pl.figure(24)
# pl.plot(range(len(d1der)), d1der, c='b')


# pl.show()
