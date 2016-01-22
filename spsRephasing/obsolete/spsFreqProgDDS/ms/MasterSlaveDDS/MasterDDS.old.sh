#!/bin/sh
echo CW Test starting
if [ $# -eq 1 ]
then
  Slot=$1

echo Firmware
ReadFirmware.sh $Slot

echo Reset DDS
Command=$Slot"00000 1 0101"
  writevme $Command



echo Disable Fake FTW
  Command=$Slot"00012 1 1000"
  writevme $Command

echo Load Synthesizer
  echo Init Synthesizer on card $Slot
  Command=$Slot"00054 6 013F 0C48 0030 0002 4006 0004"
  writevme $Command
  echo Start Load Sequencer
  Command=$Slot"00000 1 0404"
  writevme $Command



echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 bit 6 is Lock LO Synth must result on xx7x
Command=$Slot"00006 1"
  readvme $Command



echo "set DDS Data Source to VME"
  Command=$Slot"00012 1 2000"
  writevme $Command

 echo CSR select CH0 CH2 0101 0000 
  Command=$Slot"0004A 3 0000 0050 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 cosinus
  Command=$Slot"0004A 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
#  Command=$Slot"0004A 3 32CC 0F40 0004"
  Command=$Slot"0004A 3 32e8 ece3 0004"
  writevme $Command
#echo CPW0 init 25 deg
 #Command=$Slot"0004A 3 0000 0471 0005"
 #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$Slot"0004A 3 0000 13FF 0006"
  Command=$Slot"0004A 3 0000 0000 0006"
  writevme $Command
###########
 echo CSR select CH1 CH3 1010 0000
  Command=$Slot"0004A 3 0000 00A0 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 sinus
  Command=$Slot"0004A 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
#  Command=$Slot"0004A 3 32Cc 0F40 0004"
  Command=$Slot"0004A 3 32e8 ece3 0004"
  writevme $Command
#echo CPW0 init 25 deg
 #Command=$Slot"0004A 3 0000 0471 0005"
 #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$Slot"0004A 3 0000 13FF 0006"
  Command=$Slot"0004A 3 0000 0000 0006"
  writevme $Command
############
echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command


#sleep 2

echo CSR select CH2 CH3 1100 0000
  Command=$Slot"0004A 3 0000 00C0 0000"
  writevme $Command

echo DDS Register select CTW0
  Command=$Slot"0004A 3 32e8 ece3 0004"
  writevme $Command

echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command
################################

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


#echo Enable Fake FTW / ADC
#  Command=$Slot"00012 1 1010"
#  writevme $Command

#echo trigger fake FTW
#  Command=$Slot"00012 1 1010"
#  writevme $Command


#sleep 1
echo "set DDS Data Source to SPS"
  Command=$Slot"00012 1 2020"
  writevme $Command






############
echo LoadMasterDDS finished.
else
  echo -e "\aUsage MasterDDS.sh Slot"
fi



