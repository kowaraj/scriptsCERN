#!/bin/sh
echo CW Test starting
if [ $# -eq 1 ]
then
  Slot=$1

echo CReg4 DDSRead Mode
  Command=$Slot"0005E 1 0101"
  writevme $Command

echo Select DDS CTW0
  Command=$Slot"0004C 1 0004"
  writevme $Command
echo Read DDS CTW0
  Command=$Slot"00014 2"
  readvme $Command

echo Select DDS CTW1
  Command=$Slot"0004C 1 000A"
  writevme $Command
echo Read DDS CTW0
  Command=$Slot"00014 2"
  readvme $Command

echo Select DDS CTW2
  Command=$Slot"0004C 1 000B"
  writevme $Command
echo Read DDS CTW0
  Command=$Slot"00014 2"
  readvme $Command

echo Select DDS CTW3
  Command=$Slot"0004C 1 000C"
  writevme $Command
echo Read DDS CTW0
  Command=$Slot"00014 2"
  readvme $Command

echo CReg4 DDS Write Mode
  Command=$Slot"0005E 1 0100"
  writevme $Command


############
echo ReadDDS finished.
else
  echo -e "\aUsage DDSRd.sh Slot"
fi
