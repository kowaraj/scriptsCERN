#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "TEST on sDDS, slot = " $Slot


############################
echo CSR all channel select reg on bits [7..4] to reset 
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"00040 3 0000 00F0 0000"
  writevme $Command

echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command

echo Reset DDS
Command=$Slot"00000 1 0101"
writevme $Command

echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command



echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit must result on xx3x
Command=$Slot"00006 1"
  readvme $Command


echo "set DDS Data Source to VME"
  Command=$Slot"0000a 1 0200"
  writevme $Command

 echo CSR select CH0 0000 0000 0001 0000 on bit [4]
  Command=$Slot"00040 3 0000 0010 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
  Command=$Slot"00040 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
  Command=$Slot"00040 3 197f 62b6 0004"
  writevme $Command

 echo CSR select CH1 0000 0000 0010 0000 on bit [5]
  Command=$Slot"00040 3 0000 0020 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 full scale bits [9..8] and cosinus on bit [0]
  Command=$Slot"00040 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
  Command=$Slot"00040 3 197f 62b6 0004"
  writevme $Command

############
echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command
############

echo CSR all channel select reg on bits [7..4] to further prog
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"00040 3 0000 00F0 0000"
  writevme $Command


echo done.
############
fi
