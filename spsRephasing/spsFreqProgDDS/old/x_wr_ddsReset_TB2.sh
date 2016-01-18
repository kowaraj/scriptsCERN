#!/bin/sh
if [ $# -eq 1 ]
then
  MasterSlot=$1
else
  MasterSlot=4


echo "Write..."


echo "Set DDSReset to bpTrig.TB2: => must be 0003"
Command=$MasterSlot"00026 1 0003"
  writevme $Command

fi
