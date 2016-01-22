#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "TEST on sDDS, slot = " $Slot
    n=$2


#############################################################################
# 

Command="writevme "$Slot"00040 3 0000 0010 0000" #select CH0
echo "cos     : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00040 3 0000 0300 0003" #set cos and full-scale
echo "cos     : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00040 3 6f53 c681 0004" #set FTW0
echo "CTW0    : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1
Command="writevme "$Slot"00040 3 6000 c681 0004" #set FTW1
echo "CTW0    : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00000 1 0202" #update IO
echo "IO_UPD  : " $Command
$Command
sleep 1


fi
