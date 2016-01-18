#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    
    echo "calc for mDDS on slot" $Slot


if [ $# -lt 2 ]; then
    echo "enter the value!"
    exit
fi

source memmap_mdds.bash

# sel CFP
x=$2
printf "Sel CFP bit: 0x0202 to mddsControl (0x0200 for SerDes FTW), value = 0x %s\n" $x
Command="write_vme -w16 -a"$Slot$ra_ctrl" -d"$x
$Command



############
fi
