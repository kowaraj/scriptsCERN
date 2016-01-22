#!/bin/sh

echo -e "Enter Master DDS slot number: \c" 
read MasterSlot 
echo -e "Enter ADC offset value[decimal]: \c" 
read ADCOff 

RegVal=ADCOff
if (( RegVal < 0 )); then  #Test if negative value
(( RegVal = 65536 + RegVal ))
fi
#Conversion in Hex
echo "decimal : $RegVal"
RegVal=`echo "obase=16;ibase=10;scale=0; ("$RegVal");" | bc`
echo "hex : $RegVal"

command=$MasterSlot"00016 1 "$RegVal 
writevme $command
echo "Write hexa value to ADC offset register"
#echo "$command"



echo "--------------------------------------------------------------------------------"
# EOF
