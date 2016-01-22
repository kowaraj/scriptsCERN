#!/bin/sh
echo "---------------------- Frev Generation set up for VTU V4 -----------------------"
#######################################################################################
# Autor    : Gregoire Hagmann
# Group    : BE/RF/FB
# Date     : 13.09.2010
# Remark   : If you need a different function use VTUsetup.sh script
# Function : For VTU-V4. Set up of the Normal Operation, without Sync [master Frev]
#            Set for SPS operation : H=4620
# Parameter: $1 - slot number for VTU
#######################################################################################
# 
echo "Set up VTU V4 on Card $1 started"
if [ $# -eq 1 ]
then
echo
#
# Enable Double context register write access
command=$1"00000 1 ff10"
writevme $command
#
# Write B, H, W values (online and offline registers)
# H=8b38 for LHC 400MHz
# H=120C for SPS 200MHz
# H0=2000 for MasterDDS (2^13 is 8192)
#                   B2   B1   B0   H2   H1   H0   W1   W0
command=$1"0003a 8 0000 0000 0300 0000 0000 2000 0000 0000"
writevme $command
#Write Sync Detector window => disable the detector
command=$1"0005C 2 FFFF FFFF"
writevme $command
#Write Trigger Selector (soft trigger for Start, Stop, Restart)
command=$1"0000E 2 0201 FFFF"
writevme $command
#Write control register 3 (Clear Faults only)
command=$1"0000C 1 ff80"
writevme $command
#Write control register 2 (Sync op from frontpanel, Refresh Status)
command=$1"0000A 1 ff81"
writevme $command
#Write control register 1 (SwapEnabled, Counting Enable, DblReg disabled, Sync op)
command=$1"00000 1 ff60"
writevme $command
#
#Write control register 0 (1st NoSync control bit)
command=$1"00000 1 0101"
writevme $command
#Write control register 0 (2nd NoSync control bit)
command=$1"0000A 1 2020"
writevme $command
#
#Write control register 1 (Start the VTU)
command=$1"00000 1 0202"
writevme $command
#
echo "Set up finished"
else 
  echo -e "\a Please enter the slot number! [only 1 parameter]"
fi
echo "--------------------------------------------------------------------------------"
# EOF
