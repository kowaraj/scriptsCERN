echo "------------------------ Normal Mode set up for VTU V4 --------------------------"
# VTU V4 , Set up of the Normal Operation, with FrontPanel Sync at LHC Frev (11.2KHz), Test of the Front Panel Test point
#!/bin/sh
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
# B=8b25 for 400MHz, B=8430 for 380 MHz (about)
# H=8b38 for 400MHz, H=8442 for 380MHz
#                   B2   B1   B0   H2   H1   H0   W1   W0
command=$1"0003a 8 0000 0000 8B24 0000 0000 2000 0000 0000"
writevme $command
#Write Sync Detector window
command=$1"0005C 2 0000 ADD4"
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
echo "Set up finished"
else 
  echo "\a Please enter the slot number! [only 1 parameter]"
fi
# ---------------------------    EOF -----------------------------------

