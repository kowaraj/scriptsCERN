#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "Init mDDS on slot" $Slot


source memmap_mdds.bash

#General
echo "- Firmware - "
Command="read_vme -w16 -a"$Slot$ra_stat" -l1"
x=`$Command`
echo $x "(bit0: 1 -> MasterDDS, 0 -> fpDDS)"
echo "- Selector FTW to CFP/SerDes - "
Command="read_vme -w16 -a"$Slot$ra_ctrl" -l1"
x=`$Command`
echo $x "(bit1: 1 -> CFP, 0 -> SerDes)"



#ADC 
echo "- ADC - "
Command="read_vme -w16 -a"$Slot$ra_adc" -l1"
x=`$Command`
echo "Debug ADC = 0x"$x", "$((16#$x))
#ADC Gain
Command="read_vme -w16 -a"$Slot$ra_adcg" -l1"
x=`$Command`
printf "ADC Gain = 0x%s\n" $x
#ADC Offset
Command="read_vme -w16 -a"$Slot$ra_adco" -l1"
x=`$Command`
printf "ADC Offset = 0x%s\n" $x

#CFP
echo "- CFP - "
Command="read_vme -w16 -a"$Slot$ra_cfp" -l1"
x=`$Command`
echo "Debug CFP = 0x"$x", "$((16#$x))
# CFP Gain
Command="read_vme -w16 -a"$Slot$ra_cfpg" -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot$ra_cfpg2"-l1"
xls=`$Command`
x=$((16#$xms * 65536 + 16#$xls))
printf "CFP Gain = 0x%x\n" $x
# CFP Offset
Command="read_vme -w16 -a"$Slot$ra_cfpo" -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot$ra_cfpo2" -l1"
xls=`$Command`
x=$((16#$xms * 65536 + 16#$xls))
printf "CFP Offset = 0x%x\n" $x

echo "- FTW - "
# CFP FTW
Command="read_vme -w16 -a"$Slot$ra_cfpftw" -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot$ra_cfpftw2" -l1"
xls=`$Command`
x=$((16#$xms * 65536 + 16#$xls))
printf "Debug CFP FTW = 0x%x\n" $x
# Frequency from CFP FTW
f=$(($x*500000000 / 4294967296 + 250000000))
printf "mDDS Freq without ADC Error = %d\n" $f

# mDDS FTW 
Command="read_vme -w16 -a"$Slot$ra_ftw" -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot$ra_ftw2" -l1"
xls=`$Command`
x=$((16#$xms * 65536 + 16#$xls))
printf "mDDS FTW = 0x%x\n" $x
# Frequency from FTW
f=$(($x*500000000 / 4294967296 + 250000000))
printf "mDDS Freq = %d\n" $f




############
fi
