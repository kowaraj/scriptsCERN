#!/usr/bin/python

import argparse
import os
import subprocess
import sys
import time
import operator
import re

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('classname', metavar='Fesa class name', nargs='+', help='the asdfas')
parser.add_argument('fecpath', metavar='/acc/dsc/lhc/', nargs='+', help='the asdf asdfas')
parser.add_argument('fecname', metavar='cfv-ux45-acsc1b1t', nargs='+', help='the asdf asdfas')


args = parser.parse_args()
print "args = ", args
fesa_class_name = args.classname[0]
fec_postfix = args.fecpostfix[0]
print "name = ", fesa_class_name
print "fecs = ", '_'+fec_postfix


fecs = ["cfv-ux45-acsc"+str(c)+"b"+str(b)+fec_postfix for c in range(1, 9) for b in range(1, 3)] #test on one
src_path_pre = "/acc/dsc/lhc/"
dst_path_pre = "./test/"

pf_name_xml = fesa_class_name+"PersistentData.xml"

for fec in fecs:
    print ""
    print "fec = ", fec
    print "-------------------------"
    src_files = os.path.join(src_path_pre, fec, 'data', pf_name_xml)+'*'
    dst_path = os.path.join(dst_path_pre, fec, 'data')+'/'
    subprocess.call(["mkdir", "-p", dst_path])
    
    print "what: ", src_files
    print "to:   ", dst_path
    subprocess.call(["cp", "-p", src_files, dst_path])
    

        
    


                
                
            



        







