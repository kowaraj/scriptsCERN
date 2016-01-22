#!/bin/sh
echo ReadFreq starting
if [ $# -eq 1 ]
then
  Slot=$1



echo FTW Status 6 bits are error ADC or Greatest than MaxFTW or Lower than MinFTW or Ovl on Sum or Ovf on SerdesSum or Ovl on ADC sum
  Command=$Slot"0003c"
  readvme $Command 1

echo DDSDataSource bin 00X0 0000 and Fake Status bin 000X 0000
  Command=$Slot"00012"
  readvme $Command 1


echo SPS FTW Frequency
  Command=$Slot"00030"
  readvme $Command 1

echo ADC Input Value
  Command=$Slot"00032"
  readvme $Command 1

echo AnStg1
  Command=$Slot"00064"
  readvme $Command 1
 
echo SPS ADC Side
  Command=$Slot"00066"
  readvme $Command 2

echo SPS NEW FTW Frequency
  Command=$Slot"0003e"
  readvme $Command 2

echo Data Sent to DDS
  Command=$Slot"00042"
  readvme $Command 2

echo Digital Stage 1
  Command=$Slot"0006a"
  readvme $Command 2

echo Digital Part
  Command=$Slot"0006e"
  readvme $Command 2

echo fSum
  Command=$Slot"00072"
  readvme $Command 2

echo FTWa
  Command=$Slot"00076"
  readvme $Command 2




############
echo ReadFreq finished.
else
  echo -e "\aUsage ReadFreq.sh Slot"
fi



