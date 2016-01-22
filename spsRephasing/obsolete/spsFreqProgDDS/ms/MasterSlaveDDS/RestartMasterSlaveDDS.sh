#!/bin/sh

#echo -e "Enter Master DDS slot number: \c" 
#read MasterSlot 
#echo -e "Enter Slave DDS slot number: \c" 
#read SlaveSlot 

MasterSlot=4
SlaveSlot=7

echo "Start Master DDS initialisation"
echo CW Test starting

echo Firmware
ReadFirmware.sh $MasterSlot

echo Reset DDS
Command=$MasterSlot"00000 1 0101"
  writevme $Command

sleep 2

echo Disable Fake FTW
  Command=$MasterSlot"00012 1 1000"
  writevme $Command

echo Load Synthesizer
  echo Init Synthesizer on card $MasterSlot
  Command=$MasterSlot"00054 6 013F 0C48 0030 0002 4006 0004"
  writevme $Command
  echo Start Load Sequencer
  Command=$MasterSlot"00000 1 0404"
  writevme $Command



echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit 6 is Lock LO Synth must result on xx7x
Command=$MasterSlot"00006 1"
  readvme $Command



echo "set DDS Data Source to VME"
  Command=$MasterSlot"00012 1 2000"
  writevme $Command

 echo CSR select CH0 0001 0000 
  Command=$MasterSlot"0004A 3 0000 0010 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 cosinus
  Command=$MasterSlot"0004A 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"0004A 3 3437 F0E5 0004"
#  Command=$MasterSlot"0004A 3 32CC 0F40 0004"
#  Command=$MasterSlot"0004A 3 32e8 ece3 0004"
  writevme $Command

 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$MasterSlot"0004A 3 0000 13FF 0006"
  Command=$MasterSlot"0004A 3 0000 0000 0006"
  writevme $Command
############
#echo IO_Update DDS
#  Command=$MasterSlot"00000 1 0202"
#  writevme $Command

###########
 echo CSR select CH1 0010 0000
  Command=$MasterSlot"0004A 3 0000 0020 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 sinus
  Command=$MasterSlot"0004A 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
  Command=$MasterSlot"0004A 3 3437 F0E5 0004"
#  Command=$MasterSlot"0004A 3 32Cc 0F40 0004"
#  Command=$MasterSlot"0004A 3 32e8 ece3 0004"
  writevme $Command

 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$MasterSlot"0004A 3 0000 13FF 0006"
  Command=$MasterSlot"0004A 3 0000 0000 0006"
  writevme $Command
############
echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
  writevme $Command


#sleep 2


echo "set maximum FTW value allowed"
  Command=$MasterSlot"0002c 2 4200 0000"
  writevme $Command


echo "set minimum FTW value allowed"
  Command=$MasterSlot"00028 2 2e00 0005"
  writevme $Command


echo Fake FTW define
  Command=$MasterSlot"0003a 1 59D3"
  writevme $Command

echo Fake ADC define
  Command=$MasterSlot"00038 1 0000"
  writevme $Command


echo ADC Gain define
  Command=$MasterSlot"00014 1 0100"
#  Command=$MasterSlot"00014 1 0000"
  writevme $Command


echo ADC Offset define
#  Command=$MasterSlot"00016 1 FFF0"
#  Command=$MasterSlot"00016 1 015f"
  Command=$MasterSlot"00016 1 0000"
  writevme $Command

echo Serial Gain define
  Command=$MasterSlot"00018 2 000F 3B38"
  writevme $Command

echo Serial Offset define
  Command=$MasterSlot"0001c 2 36E1 CB6E"
  writevme $Command


#echo Enable Fake FTW / ADC
#  Command=$MasterSlot"00012 1 1010"
#  writevme $Command

#echo trigger fake FTW
#  Command=$MasterSlot"00012 1 1010"
#  writevme $Command


#sleep 1
echo "set DDS Data Source to SPS"
  Command=$MasterSlot"00012 1 2020"
  writevme $Command


echo Initialisation MasterDDS finished.
sleep 1
#####################################################################################################

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


#echo Set FrevPHase Offset
#  Command=$SlaveSlot"00062 1 ffff"
#  writevme $Command

echo Set RFON and RFOFF Timing from hex 1 to 200
  Command=$SlaveSlot"0001e 2 0025 0150"
  writevme $Command

echo CSR channel 0 select reg on bits [7..4]
echo CH0 CH1  0011 0000  0x00000030
echo CH0 only 0001 0000  0x00000010
  Command=$SlaveSlot"00048 3 0000 0010 0000"
  writevme $Command

echo FR1 init 4-Level Modulation bits [9,8] can only work with 2 channels so we chose channel 0 channel 1.
echo See Table 7 and Table 10 of datasheet
echo 0000 0000 0000 0000 0000 0011 0000 0000 16 level
echo 0000 0000 0000 0000 0000 0001 0000 0000 4 level
  Command=$SlaveSlot"00048 3 0000 0100 0001"
  writevme $Command

echo Do we need Multidevice Sync Slave enable ? hex 0000 0080 in that case.
echo FR2 0000 0000 0000 0000 0000 0000 1000 0000
  Command=$SlaveSlot"00048 3 0000 0080 0002"
#  Command=$SlaveSlot"00048 3 0000 0000 0002"
  writevme $Command

 echo CFR init 1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8]
 echo and Freq Modulation [23,22]
#  Command=$SlaveSlot"00048 3 0080 0300 0003"
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
  Command=$SlaveSlot"00048 3 71C7 1C7C 0004"
# Command=$SlaveSlot"00048 3 6FA0 0000 0004"
  writevme $Command

 echo CTW1 init
  Command=$SlaveSlot"00048 3 6D78 E384 000A"
#  Command=$SlaveSlot"00048 3 6FA0 0000 000A"
  writevme $Command

 echo CTW2 init
  Command=$SlaveSlot"00048 3 71C7 1C7C 000B"
#  Command=$SlaveSlot"00048 3 6FA0 0000 000B"
  writevme $Command

 echo CTW3 init
  Command=$SlaveSlot"00048 3 6D78 E384 000C"
#  Command=$SlaveSlot"00048 3 6FA0 0000 000C"
  writevme $Command




# echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$SlaveSlot"00048 3 0000 13FF 0006"
#  Command=$SlaveSlot"00048 3 0000 0000 0006"
#  writevme $Command

###########

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command


echo "Average Frequency on DDS Select Channel 1 in ppcrf19, channel 2 in BA3"
echo CSR select CH1 0010 0000
  Command=$SlaveSlot"00048 3 0000 0020 0000"
  writevme $Command

echo CFR init 0x1000 0000 0000 0000 0011 0000 0000 hex 0080 0300 cosinus [0], DAC full scale [9,8]
  Command=$SlaveSlot"00048 3 0000 0300 0003"
  writevme $Command

echo DDS Register select CTW0
  Command=$SlaveSlot"00048 3 6FA0 0000 0004"
  writevme $Command

# echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$SlaveSlot"00048 3 0000 13FF 0006"
#  Command=$SlaveSlot"00048 3 0000 0000 0006"
#  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo Clear Phase Accus
  Command=$SlaveSlot"00048 3 0000 1080 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo Reset Bit Clear Phase Accus
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