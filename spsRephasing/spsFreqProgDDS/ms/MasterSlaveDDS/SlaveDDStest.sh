#!/bin/sh


echo "Start Slave DDS initialisation"
echo CW Test starting

#Not used in Ion crate
#echo Start VTU
#FrevG.sh b

echo Firmware
ReadFirmware.sh $SlaveSlot

echo Reset DDS
Command=$SlaveSlot"00000 1 0101"
  writevme $Command


echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 must result on xx3x
Command=$SlaveSlot"00006 1"
  readvme $Command


echo "trigger FrevSync"
  Command=$SlaveSlot"00000 1 0404"
  writevme $Command

echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command


echo "Average Frequency on DDS Select Channel 1 in ppcrf19, channel 2 in BA3"
echo CSR select CH1 00100 0000
#  Command=$SlaveSlot"00048 3 0000 0020 0000"
  Command=$SlaveSlot"00048 3 0000 0040 0000"
  writevme $Command

 echo "CFR init 0x1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8] = 0x0300"
  Command=$SlaveSlot"00048 3 0000 0300 0003"
  writevme $Command

# echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$SlaveSlot"00048 3 0000 13FF 0006"
#  Command=$SlaveSlot"00048 3 0000 0000 0006"
#  writevme $Command

echo DDS Register select CTW0
  Command=$SlaveSlot"00048 3 6E98 0000 0004"
  writevme $Command

echo Read CTW0 Register
  Command=$SlaveSlot"00048 3"
  readvme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo Clear all phase accus
  Command=$SlaveSlot"00048 3 0000 1080 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo Reset bit
  Command=$SlaveSlot"00048 3 0000 0080 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command


#echo pause
#sleep 5

#echo Change Profile Pin CReg4 to CTW1
#echo 0001 0000 0001 0000
#  Command=$SlaveSlot"0005E 1 F020"
#  writevme $Command

#echo pause
#sleep 5
#
#echo Change Profile Pin CReg4 to CTW2
#echo 0010 0000 0010 0000
#  Command=$SlaveSlot"0005E 1 F010"
#  writevme $Command

#echo pause
#sleep 5


#echo Change Profile Pin CReg4 to CTW3
#echo 0011 0000 0011 0000
#  Command=$SlaveSlot"0005E 1 F030"
#  writevme $Command

#echo pause
#sleep 5


#echo Change Profile Pin back to CTW0
#  Command=$SlaveSlot"0005e 1 F000"
#  writevme $Command

# sleep 2

echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command



############
echo  Initialisation SlaveDDS finished.