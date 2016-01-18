#!/bin/sh

SlaveSlot=7



echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command

echo CSR channel 0 select reg on bits [7..4]
echo CH0 only 0001 0000  0x00000010
  Command=$SlaveSlot"00048 3 0000 0010 0000"
  writevme $Command

echo CTW0 init FTW1
  Command=$SlaveSlot"00048 3 6FA0 0000 0004"
  writevme $Command

 echo CTW1 init FTW2
  Command=$SlaveSlot"00048 3 6FA0 0000 000A"
  writevme $Command
  
echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command


