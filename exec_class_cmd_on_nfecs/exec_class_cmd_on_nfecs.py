#!/usr/bin/python

import argparse
import os
import subprocess
import sys

# Argument parser

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('classname', metavar='Fesa class name', nargs='+', help='the asdfas')
parser.add_argument('command', metavar='command to run on each fec', nargs='+', help='the asdf asdfas')
parser.add_argument('--fecs', metavar='list of cfv-ux45-acsc1b1t', nargs='+', help='the asdf asdfas')
parser.add_argument('--dbg', metavar='debug enabled', nargs='*',
                                        help='the asdf asdfas')
args = parser.parse_args()
print "args = ", args
class_name = args.classname[0]
fecs = args.fecs
cmd_to_exec = args.command[0]
dbg_arg = False if args.dbg==None else True
if dbg_arg:
    print "name = ", class_name
    print "fecs = ", fecs
    print "command = ", cmd_to_exec

for fec_name in fecs:
    print ""
    print "fec = ", fec_name
    print "-------------------------"
    print "calling  = ", cmd_to_exec, class_name, fec_name

    if dbg_arg:
        print 'Calling given cmd with --dbg flag'
        subprocess.call([cmd_to_exec, class_name, fec_name, '--dbg'])
    else:
        print 'Calling given cmd without --dbg flag'
        subprocess.call([cmd_to_exec, class_name, fec_name])

print 'done'
