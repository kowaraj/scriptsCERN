#!/bin/sh
echo Acquisition starting
if [ $# -eq 1 ]
then
  Slot=$1

echo Firmware Read
  ReadFirmware.sh $Slot

echo CReg1 Unfreeze
  Command=$Slot"00000 1 4040"
  writevme $Command

echo Read Mem Adress Position
  Command=$Slot"0000E 2"
  readvme $Command

echo Set Sampling rate 2^2 and takes about 10 sec to complete
  Command=$Slot"00012 1 0202"
  writevme $Command
  Command=$Slot"00012 1"
  readvme $Command

echo Freeze Obs
  Command=$Slot"00000 1 2020"
  writevme $Command

echo Acquire to file 25kHzObs.txt
  Command=$Slot"80000 8000"
  readvme $Command >25kHzObs.txt

echo CReg1 Unfreeze
  Command=$Slot"00000 1 4040"
  writevme $Command

echo Set Sampling rate 2^0 and takes 2.56 sec to complete
  Command=$Slot"00012 1 0200"
  writevme $Command
  Command=$Slot"00012 1"
  readvme $Command

echo pause 3 sec to complete memory
sleep 3

echo Freeze Obs
  Command=$Slot"00000 1 2020"
  writevme $Command

echo Acquire to file 100kHzObs.txt
  Command=$Slot"80000 8000"
  readvme $Command >100kHzObs.txt

echo CReg1 Unfreeze
  Command=$Slot"00000 1 4040"
  writevme $Command


############
echo ReadMem finished.
else
  echo -e "\aUsage DDSRd.sh Slot"
fi
