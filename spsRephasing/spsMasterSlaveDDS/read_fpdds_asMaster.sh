#!/bin/sh
if [ $# -eq 0 ]; then
    echo "enter the slot number!"
    exit
else
    Slot=$1
    echo "Init sDDS on slot" $Slot


#ADC
Command="read_vme -w16 -a"$Slot"0020c -l1"
x=`$Command`
echo "Debug ADC = 0x"$x", "$((16#$x))

#CFP
Command="read_vme -w16 -a"$Slot"0020e -l1"
x=`$Command`
echo "Debug CFP = 0x"$x", "$((16#$x))

# CFP FTW
Command="read_vme -w16 -a"$Slot"00210 -l1"
xms=`$Command`
Command="read_vme -w16 -a"$Slot"00212 -l1"
xls=`$Command`
x=$((16#$xms * 65536 + 16#$xls))
printf "Debug CFP FTW = 0x%x\n" $x




############
fi
