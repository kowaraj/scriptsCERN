#!/bin/sh

Slot=$1
Channel=$2
FTW1=$3
FTW2=$4

#FTW= 0x6000 0000   --> f~221
#FTW= 0x6800 0000   --> f~
#FTW= 0x7000 0000   --> f~200MHz
#FTW= 0x7800 0000   --> f~

#############################################################################
#select all channels
# Command="writevme "$Slot"00040 3 0000 00F0 0000" 
# echo "sel CH  : " $Command
# $Command
# sleep 0.2
# Command="writevme "$Slot"0004a 1 2020"
# echo "up      : " $Command
# $Command

# #update IO
# Command="writevme "$Slot"00000 1 0202" 
# echo "IO_UPD  : " $Command
# $Command
# sleep 0.2

# Reset
Command="writevme "$Slot"00046 1 0101" 
echo "IO_UPD  : " $Command
$Command
sleep 1

# # 2
# Command="writevme "$Slot"00040 3 0000 0000 0002" # clear FR2
# echo "2       : " $Command
# $Command
# sleep 0.2

#############################################################################
# 
# echo "press enter"
# read

#select CH1
Command="writevme "$Slot"00040 3 0000 00"$Channel"0 0000" 
echo "sel CH  : " $Command
$Command
sleep 0.2
Command="writevme "$Slot"00046 1 0404"
echo "up      : " $Command
$Command
sleep 0.2

#set 0000=2level-mod
#Command="writevme "$Slot"00040 3 0000 0100 0001" # 4-lev-mod
Command="writevme "$Slot"00040 3 0000 0000 0001" # 2-lev-mod
echo "mod     : " $Command
$Command
sleep 0.2
Command="writevme "$Slot"00046 1 0404"
echo "up      : " $Command
$Command
sleep 0.2

#set FM(b23:22=10), cos(b0=0), full-scale(b9:8=11)
#Command="writevme "$Slot"00040 3 0000 0300 0003" # no mod
Command="writevme "$Slot"00040 3 0080 0300 0003" 
echo "cos     : " $Command
$Command
sleep 0.2
Command="writevme "$Slot"00046 1 0404"
echo "up      : " $Command
$Command
sleep 0.2

#set FTWm1
Command="writevme "$Slot"00040 3 "$FTW1" 0004" 
echo "FTWm1   : " $Command
$Command
sleep 0.2
Command="writevme "$Slot"00046 1 0404"
echo "up      : " $Command
$Command
sleep 0.2
#set FTWm2
Command="writevme "$Slot"00040 3 "$FTW2" 000A"
echo "FTWm2   : " $Command
$Command
sleep 0.2
Command="writevme "$Slot"00046 1 0404"
echo "up      : " $Command
$Command
sleep 0.2
# #set FTWm3
# Command="writevme "$Slot"00040 3 7800 0000 000B"
# echo "FTWm2   : " $Command
# $Command
# sleep 0.2
# Command="writevme "$Slot"00046 1 0404"
# echo "up      : " $Command
# $Command
# sleep 0.2
# #set FTWm4
# Command="writevme "$Slot"00040 3 6000 0000 000C"
# echo "FTWm2   : " $Command
# $Command
# sleep 0.2
# Command="writevme "$Slot"00046 1 0404"
# echo "up      : " $Command
# $Command
# sleep 0.2

#update IO
Command="writevme "$Slot"00046 1 0202" 
echo "IO_UPD  : " $Command
$Command
sleep 0.2



