#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "TEST on sDDS, slot = " $Slot

Command="writevme "$Slot"00000 1 0101"
echo "rst dds : " $Command
$Command

sleep 4

###

Command="writevme "$Slot"00040 3 0000 00F0 0000"
echo "sel ch  : " $Command
$Command
sleep 1

Command="writevme "$Slot"00000 1 0202"
echo "io upd  : " $Command
$Command
sleep 1

Command="writevme "$Slot"00000 1 0101"
echo "rst dds : " $Command
$Command
sleep 1

Command="writevme "$Slot"00000 1 0202"
echo "io upd  : " $Command
$Command
sleep 1

Command="readvme "$Slot"00006 1"
echo "rd st   : " $Command
$Command
sleep 1
read

# clear FR1, FR2
Command="writevme "$Slot"00040 3 0000 0000 0001"
echo "clr FR1 : " $Command
$Command
sleep 1
Command="writevme "$Slot"00040 3 0000 0000 0002"
echo "clr FR2 : " $Command
$Command
sleep 1
read

#############################################################################

# 1) sel Channel0: 
# 2) set CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
# 3) set ctw0

Command="writevme "$Slot"00040 3 0000 0020 0000"
echo "sel CH0 : " $Command
$Command
sleep 1
read

Command="writevme "$Slot"00040 3 0000 0300 0003"
echo "sin     : " $Command
$Command
sleep 1
read

Command="writevme "$Slot"00040 3 6f53 c681 0004"
#Command="writevme "$Slot"00040 3 6fa0 0000 0004"
#Command="writevme "$Slot"00040 3 0000 0000 0004"
echo "CTW0    : " $Command
$Command
sleep 1
read

exit

# 1) sel Channel1: 
# 2) set CFR init 0000 0011 0000 0001 full scale bits [9..8] sinus on bit [0]
# 3) set ctw0

Command="writevme "$Slot"00040 3 0000 0020 0000"
echo "sel CH1 : " $Command
$Command
sleep 1
read

Command="writevme "$Slot"00040 3 0000 0300 0003"
echo "cos     : " $Command
$Command
sleep 1
read

#Command="writevme "$Slot"00040 3 6fa0 0000 0004"
Command="writevme "$Slot"00040 3 0000 0000 0004"
#Command="writevme "$Slot"00040 3 1999 9999 0004"
echo "CTW0    : " $Command
$Command
sleep 1
read

############

Command="writevme "$Slot"00000 1 0202"
echo "io upd  : " $Command
$Command
sleep 1

echo "Done."

fi
