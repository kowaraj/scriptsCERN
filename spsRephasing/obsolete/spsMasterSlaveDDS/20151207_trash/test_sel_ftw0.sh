#!/bin/sh

Slot=6

#############################################################################
# 

#set debugControl: b0:3=0 (all PPCs =0)
Command="writevme "$Slot"0004a 1 0f00" 
echo "PPC     : " $Command
$Command
sleep 1


