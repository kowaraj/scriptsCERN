#!/user/bdisoft/operational/bin/Python/PRO/bin/python 

import urllib.request
import time
import os
import sys
from scipy import misc
from numpy import ndarray
from numpy import array_equal

x = [100,200]
y = [500,1024]

xfol = './data/'+sys.argv[1]
fol = xfol+'/'
fol_out = xfol+'_out/'

files = os.listdir(fol)
print('number of files in ', fol, ' = ', len(files))
print('')

for i in range(len(files)-1):
    print('i = ',i)
    fn1 = files[i]
    fn2 = files[i+1]
    print(fn1)
    print(fn1)
    f1 = misc.imread(fol+fn1)
    f2 = misc.imread(fol+fn2)

    # fx1 = f1 ( [x[1]-x[0] , y[1]-y[0] ,3 ],'int8')
    # fx2 = f2 ( [x[1]-x[0] , y[1]-y[0] ,3 ],'int8')

    fx1 = f1[x[0]:x[1] , y[0]:y[1]]
    fx2 = f2[x[0]:x[1] , y[0]:y[1]]

    s = sum([sum(fx1[ix,iy] -fx2[ix,iy]) for ix in range(x[1]-x[0]) for iy in range(y[1]-y[0])])
    print('s = ',s)
    print('')

    if s > 1000000:
        misc.imsave(fol_out+'_'+fn1.rstrip('.png')+'_'+fn2, fx1-fx2)








    
