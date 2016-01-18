#!/bin/sh
if [ $# -eq 1 ]
then
  MasterSlot=$1
else
  MasterSlot=4


echo "Write..."


echo "DDS IO Update:"
Command=$MasterSlot"00000 1 0202"
  writevme $Command

fi
