#!/bin/sh
#if [ $# -eq 1 ]
#then
#  MasterSlot=$1
  MasterSlot=4

echo "Start SPS Freq Prog DDS initialisation"
echo CW Test starting

echo Firmware
ReadFirmware.sh $MasterSlot

# Put this command on FESA
echo CSR all channel select reg on bits [7..4] to reset 
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"0004A 3 0000 00F0 0000"
  writevme $Command

############
echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command

echo Reset DDS
Command=$MasterSlot"00000 1 0101"
  writevme $Command

echo Load Synthesizer
  echo Init Synthesizer on card $MasterSlot
  Command=$MasterSlot"00054 6 013F 0C48 0030 0002 4006 0004"
  writevme $Command
  echo Start Load Sequencer
  Command=$MasterSlot"00000 1 0404"
  writevme $Command

echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit 6 is Lock LO Synth must result on xx7x
Command=$MasterSlot"00006 1"
  readvme $Command


echo "set DDS Data Source to VME"
  Command=$MasterSlot"00012 1 2000"
  writevme $Command

 echo CSR select CH0 0000 0000 0001 0000 on bit [4]
  Command=$MasterSlot"0004A 3 0000 0010 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
  Command=$MasterSlot"0004A 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"0004A 3 1999 9999 0004"
  writevme $Command

 echo CSR select CH1 0000 0000 0010 0000 on bit [5]
  Command=$MasterSlot"0004A 3 0000 0020 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 full scale bits [9..8] and cosinus on bit [0]
  Command=$MasterSlot"0004A 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"0004A 3 1999 9999 0004"
  writevme $Command

############
echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command


#sleep 2

echo "set DDS Data Source to SPS"
  Command=$MasterSlot"00012 1 2020"
  writevme $Command


echo Initialisation SpsFreqProgDds finished.
############
