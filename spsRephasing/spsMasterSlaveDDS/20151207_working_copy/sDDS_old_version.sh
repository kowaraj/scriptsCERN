#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
  SlaveSlot=$1
  echo "Init sDDS on slot" $SlaveSlot


echo "Start Slave DDS initialisation"

echo Firmware
ReadFirmware.sh $SlaveSlot

echo Reset DDS, as you see it is not Master Reset, it only resets selected channel, so do it again later
Command=$SlaveSlot"00000 1 0101"
  writevme $Command

sleep 4

echo Set DDSIOupdate synced to SyncCLK instead of Frev
Command=$SlaveSlot"00012 1 8080"
writevme $Command

#sleep 1

echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 must result on xx3x
Command=$SlaveSlot"00006 1"
  readvme $Command


echo here starts SlaveDDS Init

#sleep 1


echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command

echo CSR all channel select reg on bits [7..4] to reset
echo CH0 only 1111 0000  0x000000F0
  Command=$SlaveSlot"00048 3 0000 00F0 0000"
  writevme $Command

echo Reset DDS
Command=$SlaveSlot"00000 1 0101"
  writevme $Command

sleep 4

##################

echo CSR channel 0 select reg on bits [7..4]
echo CH0 only 0001 0000  0x00000010
  Command=$SlaveSlot"00048 3 0000 0010 0000"
  writevme $Command


echo FR1 init 4-Level Modulation bits [9,8] can only work with 2 channels so we chose channel 0 channel 1.
echo See Table 7 and Table 10 of datasheet
echo 0000 0000 0000 0000 0000 0011 0000 0000 16 level
echo 0000 0000 0000 0000 0000 0001 0000 0000 4 level
  Command=$SlaveSlot"00048 3 0000 0100 0001"
  writevme $Command

 echo CFR init 1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8], Freq Modulation [23]
 echo and Freq Modulation [23,22]
  Command=$SlaveSlot"00048 3 0080 0300 0003"
  writevme $Command

# echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$SlaveSlot"00048 3 0000 13FF 0006"
#  Command=$SlaveSlot"00048 3 0000 0000 0006"
#  writevme $Command

#echo IO_Update DDS
#  Command=$SlaveSlot"00000 1 0202"
#  writevme $Command

echo CTW0 init
#  Command=$SlaveSlot"00048 3 71C7 1C7C 0004"
  Command=$SlaveSlot"00048 3 6FA0 0000 0004"
#echo injection Frequency
# Command=$SlaveSlot"00048 3 91A0 4208 0004"
  writevme $Command

 echo CTW1 init
#  Command=$SlaveSlot"00048 3 6D78 E384 000A"
  Command=$SlaveSlot"00048 3 6FA0 0000 000A"
#echo injection Frequency
#  Command=$SlaveSlot"00048 3 8F1F BDF8 000A"
  writevme $Command

 echo CTW2 init
#  Command=$SlaveSlot"00048 3 71C7 1C7C 000B"
  Command=$SlaveSlot"00048 3 6FA0 0000 000B"
#echo injection Frequency
#  Command=$SlaveSlot"00048 3 91A0 4208 000B"
  writevme $Command

 echo CTW3 init
#  Command=$SlaveSlot"00048 3 6D78 E384 000C"
  Command=$SlaveSlot"00048 3 6FA0 0000 000C"
#echo injection Frequency
#  Command=$SlaveSlot"00048 3 8F1F BDF8 000C"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command


###########


echo "Average Frequency on DDS Select Channel 1 in ppcrf19, channel 2 in BA3"
echo CSR select CH1 0010 0000
  Command=$SlaveSlot"00048 3 0000 0020 0000"
  writevme $Command

echo CFR init 0x1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8]
  Command=$SlaveSlot"00048 3 0000 0300 0003"
  writevme $Command

echo DDS Register select Average Frequency CTW0
  Command=$SlaveSlot"00048 3 6FA0 0000 0004"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo CH0 and CH1 initialization complete
 sleep 1

echo Autoclear Phase Accus
echo FR2 0010 0000 0000 0000
  Command=$SlaveSlot"00048 3 0000 2000 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo Disable Autoclear Phase Accus
echo FR2 0000 0000 0000 0000 0000 0000 0000 0000
  Command=$SlaveSlot"00048 3 0000 0000 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo phase accus started together
sleep 1

sleep 1

echo slave sync enable.
echo FR2 0000 0000 0000 0000 0000 0000 1000 0000
  Command=$SlaveSlot"00048 3 0000 0080 0002"
  writevme $Command
echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command

sleep 1

echo Trigger FrevSync for FTWToggle
  Command=$SlaveSlot"00000 1 0404"
  writevme $Command

echo Set FrevPHase Offset for FTWToggle
  Command=$SlaveSlot"00062 1 0000"
  writevme $Command

echo Set RFON and RFOFF Timing
  Command=$SlaveSlot"0001e 2 0025 0350"
  writevme $Command


#FrevG4620.sh b

############
echo  Initialization SlaveDDS finished, change SlaveDDS FTW to 0x 6E98 0000

fi
