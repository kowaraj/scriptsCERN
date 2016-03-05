#!/usr/bin/python

import ppm_copy
import argparse

parser = argparse.ArgumentParser(description='Some args...')
parser.add_argument('dev', metavar='device name', nargs='+',help='to composet DEV/Prop#param)')
parser.add_argument('prop', metavar='property name', nargs='+',help='to composet DEV/Prop#param)')
parser.add_argument('param', metavar='parameter name', nargs='+',help='to composet DEV/Prop#param)')
parser.add_argument('uname_src', metavar='source <username>', nargs='+',help='to compose: SPS.USER.<username>')
parser.add_argument('uname_dst', metavar='destination <username>', nargs='+',help='to compose: SPS.USER.<username>')
args = parser.parse_args()

a_dev = args.dev[0]
a_prop = args.prop[0]
a_param = args.param[0]
uname_src = 'SPS.USER.'+args.uname_src[0]
uname_dst = 'SPS.USER.'+args.uname_dst[0]

ppm_copy.copy_property_param(a_dev, a_prop, a_param, uname_src, uname_dst)
#ppm_copy.copy_param_5(a_dev, a_prop, a_param, uname_src, uname_dst)


