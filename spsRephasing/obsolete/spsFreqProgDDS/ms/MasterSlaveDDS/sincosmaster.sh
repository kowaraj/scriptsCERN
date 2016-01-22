#!/bin/sh

clear

MasterSlot=4

echo "Config Master DDS Cosinus - Sinus on CH0 and CH1"
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

 echo CFR init 1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8]
  Command=$MasterSlot"0004A 3 0000 0304 0003"
  writevme $Command

echo CTW0 init for 50 MHz
  Command=$MasterSlot"0004A 3 3437 f0e5 0004"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command



echo CSR channel 1 select reg on bits [7..4]
echo CH1 only 0001 0000  0x00000020
  Command=$MasterSlot"0004A 3 0000 0020 0000"
  writevme $Command

 echo CFR init 1000 0000 0000 0000 0011 0001 0000 hex 0080 0301 sinus [0], DAC full scale [9,8]
  Command=$MasterSlot"0004A 3 0000 0305 0003"
  writevme $Command

echo CTW0 init for 50MHz
  Command=$MasterSlot"0004A 3 3437 f0e5 0004"
  writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command


echo "set DDS Data Source back to SPS"
  Command=$MasterSlot"00012 1 2020"
  writevme $Command

