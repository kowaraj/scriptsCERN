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
from copy_persistent_data_function import f_copy_persistent_data

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('classname', metavar='Fesa class name', nargs='+',
                                        help='the asdfas')
parser.add_argument('fecpath', metavar='/acc/dsc/lhc/', nargs='+',
                                        help='the asdf asdfas')
parser.add_argument('fecname', metavar='cfv-ux45-acsc1b1t', nargs='+',
                                        help='the asdf asdfas')

args = parser.parse_args()
print "args = ", args
class_name = args.classname[0]
fec_path = args.fecpath[0]
fec_name = args.fecname[0]
print "name = ", class_name
print "fecpath  = ", fec_path
print "fecname  = ", fec_name

f_copy_persistent_data(class_name, fec_path, fec_name)
print 'done'    

        
    


                
                
            



        







