#!/bin/sh

echo Closing ADC Loop
MasterSlot=4

echo ADC Gain
  Command=$MasterSlot"00014 1 0010"
#  Command=$MasterSlot"00014 1 fffb"
  writevme $Command

echo ADC Offset
#  Command=$MasterSlot"00016 1 0010"
  Command=$MasterSlot"00016 1 2400"
  writevme $Command

echo Done