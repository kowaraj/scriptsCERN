#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "TEST on sDDS, slot = " $Slot

#############################################################################

# 1) sel Channel0: 
# 2) set CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
# 3) set ctw0
Command="writevme "$Slot"00040 3 0000 0020 0000"
echo "sel all : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00040 3 0000 0300 0003"
echo "cos     : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00040 3 6000 c681 0004"
echo "CTW0    : " $Command
$Command
sleep 1
Command="writevme "$Slot"0004a 1 2020"
echo "up intfc: " $Command
$Command
sleep 1

Command="writevme "$Slot"00000 1 0202"
echo "IO_UPD  : " $Command
$Command
sleep 1


###

echo "Done."

fi
