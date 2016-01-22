#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "calc for mDDS on slot" $Slot

source memmap_mdds.bash

# CFP Gain
cfp_gain=998200
printf "CFP Gain = 0x%x\n" $cfp_gain
xms=$(($cfp_gain / 65536))
printf "xms = 0x%x\n" $xms
xls=$(($cfp_gain -($xms * 65536)))
printf "xls = 0x%x\n" $xls

xms_hex=`printf "%x\n" $xms`
Command="write_vme -w16 -a"$Slot$ra_cfpg" -d"$xms_hex
#echo $Command
$Command
xls_hex=`printf "%x\n" $xls`
Command="write_vme -w16 -a"$Slot$ra_cfpg2" -d"$xls_hex
$Command


# CFP Offset
x=920767342
printf '!!! modified! CFP offset'
x=895271390

printf "CFP Offset = 0x%x\n" $x

xms=$(($x / 65536))
printf "xms = 0x%x\n" $xms
xls=$(($x -($xms * 65536)))
printf "xls = 0x%x\n" $xls

xms_hex=`printf "%x\n" $xms`
Command="write_vme -w16 -a"$Slot$ra_cfpo" -d"$xms_hex
$Command
xls_hex=`printf "%x\n" $xls`
Command="write_vme -w16 -a"$Slot$ra_cfpo2" -d"$xls_hex
$Command

# ADC Gain
x=30
printf '!!! modified! ADC gain'
x=0
printf "ADC Gain = 0x%x\n" $x
x_hex=`printf "%x\n" $x`
Command="write_vme -w16 -a"$Slot$ra_adcg" -d"$x_hex
$Command

# ADC Offset
x=100 #neg!
x_hex=`printf "%04x\n" $((65536-$x))`
printf "ADC Offset = 0x%s\n" $x_hex
Command="write_vme -w16 -a"$Slot$ra_adco" -d"$x_hex
$Command


############
fi
