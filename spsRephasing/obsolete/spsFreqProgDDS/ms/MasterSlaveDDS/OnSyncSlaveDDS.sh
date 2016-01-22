#!/bin/sh


#echo -e "Enter Slave DDS slot number: \c" 
#read SlaveSlot 

SlaveSlot=7


#####################################################################################################

clear

echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command

echo slave sync enable. This must be done before anything on the FPGA
echo FR2 0000 0000 0000 0000 0000 0000 1000 0000
  Command=$SlaveSlot"00048 3 0000 0080 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

echo slave sync disable.
echo FR2 0000 0000 0000 0000 0000 0000 0000 0000
  Command=$SlaveSlot"00048 3 0000 0000 0002"
  writevme $Command

echo IO_Update DDS
  Command=$SlaveSlot"00000 1 0202"
  writevme $Command

sleep 1

echo Read Status Word I bit 4 is LockMH50 bit 5 is LockMHz125 must result on xx3x
Command=$SlaveSlot"00006 1"
  readvme $Command


echo "trigger FrevSync"
  Command=$SlaveSlot"00000 1 0404"
  writevme $Command

###########


echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command


# sleep 1

############
echo "Automatic Sync SlaveDDS enabled."