#!/bin/sh
set -euo pipefail
Slot=$1
Channel=$2
FTW1=$3
FTW2=$4

#############################################################################
# to VME
Command="writevme "$Slot"00046 1 0808" 
echo "to_VME  : " $Command
$Command
sleep 0.2

# on offset
# Command="writevme "$Slot"00020 1 50" 
# echo "on_offs : " $Command
# $Command
# sleep 0.2
# # off offset
# Command="writevme "$Slot"00022 1 150" 
# echo "off_offs: " $Command
# $Command
# sleep 0.2

Command="writevme "$Slot"00040 3 0000 0000 0002" # clear FR2
echo "2       : " $Command
$Command
sleep 0.2


#update IO
Command="writevme "$Slot"00046 1 0202" 
echo "IO_UPD  : " $Command
$Command
sleep 0.2

# to FPGA
# Command="writevme "$Slot"00046 1 0800" 
# echo "to_FPGA : " $Command
# $Command
# sleep 1


