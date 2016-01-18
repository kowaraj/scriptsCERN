#!/bin/sh

clear

MasterSlot=4

echo "Config Master DDS Cosinus - SIN on CH0 and COS on CH1"
echo CW Test starting

#Not used in Ion crate
#echo Start VTU
#FrevG.sh b

echo Firmware
ReadFirmware.sh $MasterSlot


echo "set DDS Data Source to VME"
  Command=$MasterSlot"00012 1 2000"
  writevme $Command




echo CSR channel 0 select reg on bits [7..4]
echo CH0 only 0001 0000  0x00000010
  Command=$MasterSlot"0004A 3 0000 0010 0000"
  writevme $Command

 echo CFR init 1000 0000 0000 0000 0011 0000 0101 hex 0080 0305 sinus [0], autoclear ph accu [2], DAC full scale [9,8]
  Command=$MasterSlot"0004A 3 0000 0305 0003"
  writevme $Command

echo CTW0 init for 50 MHz
#  Command=$MasterSlot"0004A 3 1916 872B 0004"
  Command=$MasterSlot"0004A 3 1999 9999 0004"
  writevme $Command


echo CSR channel 1 select reg on bits [7..4]
echo CH1 only 0001 0000  0x00000020
  Command=$MasterSlot"0004A 3 0000 0020 0000"
  writevme $Command

 echo CFR init 1000 0000 0000 0000 0011 0000 0100 hex 0080 0304 cosinus [0], autoclear ph accu [2], DAC full scale [9,8]
  Command=$MasterSlot"0004A 3 0000 0304 0003"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command

echo CTW0 init for 50MHz
#  Command=$MasterSlot"0004A 3 1916 872B 0004"
  Command=$MasterSlot"0004A 3 1999 9999 0004"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command


echo "set DDS Data Source back to SPS"
  Command=$MasterSlot"00012 1 2020"
  writevme $Command

