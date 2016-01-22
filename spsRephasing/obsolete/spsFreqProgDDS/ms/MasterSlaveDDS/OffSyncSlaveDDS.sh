#!/bin/sh
clear

#echo -e "Enter Slave DDS slot number: \c" 
#read SlaveSlot 

SlaveSlot=7


#####################################################################################################

echo "Slave DDS SW Sync Off"


 echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command

echo remove autosync
Command=$SlaveSlot"00048 3 0000 0000 0002"
writevme $Command
echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
writevme $Command



echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
writevme $Command

#sleep 1

echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command



############
echo "Sync SlaveDDS is now OFF."