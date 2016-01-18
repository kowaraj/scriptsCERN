#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "calc for mDDS on slot" $Slot


# CFP 
printf "Input freq = %d\n" $2
Command="read_vme -w16 -a"$Slot"00204 -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot"00206 -l1"
xls=`$Command`
ret=$((200394831 - $2 + 1048576))
f_cfp=$(($ret / 512))
printf "Sent CFP value from DSP = 0x%x\n" $f_cfp


# CFP Gain
cfp_gain=998200
printf "CFP Gain = 0x%x\n" $cfp_gain


xms=$(($cfp_gain / 65536))
printf "xms = 0x%x\n" $xms
xls=$(($cfp_gain -($xms * 65536)))
printf "xls = 0x%x\n" $xls

xms_hex=`printf "%x\n" $xms`
Command="write_vme -w16 -a"$Slot"00204 -d"$xms_hex
$Command
xls_hex=`printf "%x\n" $xls`
Command="write_vme -w16 -a"$Slot"00206 -d"$xls_hex
$Command


# CFP Offset
x=920767342
printf "CFP Offset = 0x%x\n" $x

xms=$(($x / 65536))
printf "xms = 0x%x\n" $xms
xls=$(($x -($xms * 65536)))
printf "xls = 0x%x\n" $xls

xms_hex=`printf "%x\n" $xms`
Command="write_vme -w16 -a"$Slot"00208 -d"$xms_hex
$Command
xls_hex=`printf "%x\n" $xls`
Command="write_vme -w16 -a"$Slot"0020a -d"$xls_hex
$Command

# ADC Gain
x=30
printf "ADC Gain = 0x%x\n" $x
x_hex=`printf "%x\n" $x`
Command="write_vme -w16 -a"$Slot"00200 -d"$x_hex
$Command

# ADC Offset
x=100 #neg!
x_hex=`printf "%04x\n" $((65536-$x))`
printf "ADC Offset = 0x%s\n" $x_hex
Command="write_vme -w16 -a"$Slot"00202 -d"$x_hex
$Command


############
fi
