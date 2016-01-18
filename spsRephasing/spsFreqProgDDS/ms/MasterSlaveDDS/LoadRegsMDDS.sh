#!/bin/sh
echo CW Test starting
if [ $# -eq 1 ]
then
  Slot=$1


echo "set maximum FTW value allowed"
  Command=$Slot"0002c 2 4200 0000"
  writevme $Command


echo "set minimum FTW value allowed"
  Command=$Slot"00028 2 2e00 0005"
  writevme $Command


echo Fake FTW define
  Command=$Slot"0003a 1 59D3"
  writevme $Command

echo Fake ADC define
  Command=$Slot"00038 1 0000"
  writevme $Command


echo ADC Gain define
  Command=$Slot"00014 1 0050"
#  Command=$Slot"00014 1 0000"
  writevme $Command


echo ADC Offset define
#  Command=$Slot"00016 1 FFF0"
#  Command=$Slot"00016 1 015f"
  Command=$Slot"00016 1 0000"
  writevme $Command

echo Serial Gain define
  Command=$Slot"00018 2 000F 3B38"
  writevme $Command

echo Serial Offset define
  Command=$Slot"0001c 2 36E1 CB6E"
  writevme $Command



############
echo LoadRegsMDDS finished.
else
  echo -e "\aUsage LoadRegsMDDS.sh Slot"
fi
