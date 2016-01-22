#!/bin/sh
echo CW Test starting
if [ $# -eq 1 ]
then
  Slot=$1

echo Reset DDS
Command=$Slot"00000 1 0101"
  writevme $Command

echo Load Synthesizer
  echo Init Synthesizer on card $Slot
  Command=$Slot"00052 6 013F 0C48 0030 0002 0006 0004"
  writevme $Command
  echo Start Load Sequencer
  Command=$Slot"00000 1 0404"
  writevme $Command

echo Load FG Address
Command=$Slot"0006A 1 000F"
  writevme $Command
sleep 1


echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit 6 is Lock LO Synth must result on xx7x
Command=$Slot"00006 1"
  readvme $Command




echo Change DDS Data Source from Register 200062 to 200048 and VME_FG disable
Command=$Slot"00012 1 3000"
  writevme $Command
#sleep 1

 echo CSR select CH0 CH2 0101 0000 
  Command=$Slot"00048 3 0000 0050 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 sinus
  Command=$Slot"00048 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
  Command=$Slot"00048 3 32CC 0F40 0004"
  writevme $Command
 #echo CPW0 init 25 deg
  #Command=$Slot"00048 3 0000 0471 0005"
  #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
  Command=$Slot"00048 3 0000 13FF 0006"
  writevme $Command
############
 echo CSR select CH1 CH3 1010 0000
  Command=$Slot"00048 3 0000 00A0 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 cosinus
  Command=$Slot"00048 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
  Command=$Slot"00048 3 32CC 0F40 0004"
  writevme $Command
 #echo CPW0 init 25 deg
  #Command=$Slot"00048 3 0000 0471 0005"
  #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
  Command=$Slot"00048 3 0000 13FF 0006"
  writevme $Command
############
echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command
#sleep 1

echo Change DDS Data Source from 200062 or 200048 to FG and VME_FG disable
echo bit 4 and bit 5 of Ctrl world II 0011 0000

Command=$Slot"00012 1 2020"
  writevme $Command
#sleep 1





############
echo LoadDDS finished.
else
  echo -e "\aUsage DualFreqProg.sh Slot"
fi



