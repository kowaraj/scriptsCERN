#!/user/bdisoft/operational/bin/Python/PRO/bin/python 

import urllib.request
import time
import os
import numpy
from scipy import misc

TIME_TO_SLEEP = 10 #seconds
scope1 = '128.141.159.143'
#scope2 = '128.141.159.33'

ts = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
fname = './data/'+ts+'/'
os.mkdir(fname)
print('fname = '+fname)


def read_scope(scope):
    response  = urllib.request.urlopen('http://'+scope+'/crt_print.png')
    image = response.read()
    print('status: '+str(response.status))
    ts_str = time.strftime('%d_%H%M%S', time.localtime(time.time()))
    print('images received @'+ts_str)
    return image, ts_str

while(1):
    im1,ts1 = read_scope(scope1)
 #   im2,ts2 = read_scope(scope2)

    f = open(fname+ts1+ '.png', 'wb')
    f.write(im1)
    f.close()

    # f = open('temp2.png', 'wb')
    # f.write(im2)
    # f.close()

  #  y1 = misc.imread('temp1.png')
  #  y2 = misc.imread('temp2.png')

    # y = numpy.ndarray([768*2,1024,3], 'uint8')
    # y[0:768,0:1024]     = y1
    # y[768:768*2,0:1024] = y2
    # misc.imsave(fname+ts1+'_'+ts2+'.png',y)
    # y = misc.imread('temp1.png')
    # y = numpy.ndarray([768,1024,3], 'uint8')
    # misc.imsave(fname+ts1+'_'+'.png',y)


    time.sleep(TIME_TO_SLEEP)


    
