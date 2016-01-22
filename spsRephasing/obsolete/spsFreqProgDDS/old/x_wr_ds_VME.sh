#!/bin/sh
if [ $# -eq 1 ]
then
  MasterSlot=$1
else
  MasterSlot=4


echo "Write..."


echo "DDS Data Source = VME:"
Command=$MasterSlot"00012 1 0400"
  writevme $Command

fi
