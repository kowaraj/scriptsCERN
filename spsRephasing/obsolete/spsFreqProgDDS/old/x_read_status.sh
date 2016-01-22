#!/bin/sh
if [ $# -eq 1 ]
then
  MasterSlot=$1
else
  MasterSlot=4


echo "Read..."


echo "Status: b4=LockMH50, b5=LockMHz125 => must be xx3x"
Command=$MasterSlot"00006 1"
  readvme $Command

echo "Backplane Trigger: => must be 0003"
Command=$MasterSlot"00026 1"
  readvme $Command

Command=$MasterSlot"00012 1"
  readvme $Command
Command=$MasterSlot"00020 2"
  readvme $Command
Command=$MasterSlot"00046 2"
  readvme $Command

fi
