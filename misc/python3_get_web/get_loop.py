#!/user/bdisoft/operational/bin/Python/PRO/bin/python 

import urllib.request
import time
import os

TIME_TO_SLEEP = 10 #seconds
scope1 = 'cfo-864-as5g01'
scope2 = 'cfo-864-as5g02'
ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
fname1 = './data/'+ts+'_'+scope1+'/'
fname2 = './data/'+ts+'_'+scope2+'/'
os.mkdir(fname1)
os.mkdir(fname2)

def read_scope(scope, fname):
    response  = urllib.request.urlopen('http://'+scope+'/crt_print.png')
    image = response.read()
    print('status: '+str(response.status))
    ts_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('images received @'+ts_str)
    f = open(fname + 'img_'+ ts_str + '.png', 'wb')
    f.write(image)
    f.close()

while(1):
    read_scope(scope1, fname1)
    read_scope(scope2, fname2)

    time.sleep(TIME_TO_SLEEP)


    
