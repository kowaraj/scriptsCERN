#!/bin/sh
#if [ $# -eq 1 ]
#then
#  MasterSlot=$1
  MasterSlot=4

echo "Start SPS Freq Prog DDS initialisation"
echo CW Test starting

echo Firmware
ReadFirmware.sh $MasterSlot

echo "Get Temperature"
  Command=$MasterSlot"00012 1 0202"
  writevme $Command

Command=$MasterSlot"000E6 1"
  readvme $Command

echo "Get Serial Number"
  Command=$MasterSlot"00012 1 0101"
  writevme $Command

Command=$MasterSlot"000F4 4"
  readvme $Command

echo Select Serial IN serdes
  Command=$MasterSlot"00012 1 0100"
  writevme $Command


############################
# Put this command on FESA
echo CSR all channel select reg on bits [7..4] to reset 
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"00040 3 0000 00F0 0000"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command

echo Reset DDS
Command=$MasterSlot"00000 1 0101"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command



echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit must result on xx3x
Command=$MasterSlot"00006 1"
  readvme $Command


echo "set DDS Data Source to VME"
  Command=$MasterSlot"00012 1 0400"
  writevme $Command

 echo CSR select CH0 0000 0000 0001 0000 on bit [4]
  Command=$MasterSlot"00040 3 0000 0010 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
  Command=$MasterSlot"00040 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"00040 3 1965 0000 0004"
  writevme $Command

 echo CSR select CH1 0000 0000 0010 0000 on bit [5]
  Command=$MasterSlot"00040 3 0000 0020 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 full scale bits [9..8] and cosinus on bit [0]
  Command=$MasterSlot"00040 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"00040 3 1965 0000 0004"
  writevme $Command

############
echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command
############

echo CSR all channel select reg on bits [7..4] to further prog
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"00040 3 0000 00F0 0000"
  writevme $Command


#sleep 2

#echo "set DDS Data Source to SPS"
#  Command=$MasterSlot"00012 1 0404"
#  writevme $Command


echo Initialisation SpsFreqProgDds finished.
############
