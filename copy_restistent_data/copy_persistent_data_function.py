#!/usr/bin/python

# Description:
#
# copy <classname>'s pers.data files (including archives)
#  from: <fecpath><fecname>/data/
#  to:   ./pdata_<classname>_<fecname>_CURRENT_TIMESTAMP/data/ folder


# Versions:
#
# 2015.03.26
# - original version
#
# 2015.03.xxxxx
# - 

import argparse
import os
import subprocess
import sys
import time
import operator
import re

def f_copy_persistent_data(class_name, fec_path, fec_name):
    curr_ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    copy_path = './pdata_'+class_name+'_'+fec_name+'_'+curr_ts+'/'
    pf_name = class_name+"PersistentData.xml"

    src_files = os.path.join(fec_path, fec_name, 'data', pf_name)+'*'
    dst_path = os.path.join(copy_path, 'data')+'/'
    subprocess.call(["mkdir", "-p", dst_path])

    print 'copying: '    
    print "\twhat: ", src_files
    print "\tto:   ", dst_path
    copy_cmd = 'cp -p '+src_files+' '+dst_path
    print '\tcmd = ', copy_cmd
    subprocess.call(copy_cmd, shell=True)


        
    


                
                
            



        







