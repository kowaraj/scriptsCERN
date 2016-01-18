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

# ADC Gain
x=$2
printf "ADC Gain = 0x%x (default= 30)\n" $x
x_hex=`printf "%x\n" $x`
Command="write_vme -w16 -a"$Slot$ra_adcg" -d"$x_hex
$Command



############
fi
