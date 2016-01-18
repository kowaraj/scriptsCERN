#!/bin/sh
clear

#echo -e "Enter Slave DDS slot number: \c" 
#read SlaveSlot 

MasterSlot=4


#####################################################################################################

echo "Master DDS Enable SYNC_OUT"
echo "This DDS Pin 2 output is not routed so dont use this script"

 echo "set DDS Data Source to VME2"
  Command=$MasterSlot"00012 1 2000"
  writevme $Command

echo "Enable SYNC_OUT"
echo "FR2bit6 binary 0000 0000 0100 0000"
echo "0x0040"
Command=$MasterSlot"00048 3 0000 0040 0002"
writevme $Command

echo IO_Update DDS
  Command=$MasterSlot"00000 1 0202"
writevme $Command

#sleep 1

echo "set DDS Data Source to SPS"
  Command=$MasterSlot"00012 1 2020"
  writevme $Command



############
echo "finished."