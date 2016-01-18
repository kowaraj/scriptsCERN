#!/bin/sh

echo Opening ADC Loop
MasterSlot=4
#  Command=$MasterSlot"00014 1 0010"
  Command=$MasterSlot"00014 1 0000"
  writevme $Command

  echo ADC Offset
  Command=$MasterSlot"00016 1 0000"
  writevme $Command

echo Done