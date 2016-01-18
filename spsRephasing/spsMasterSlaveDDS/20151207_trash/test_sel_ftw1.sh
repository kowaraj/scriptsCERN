#!/bin/sh

Slot=6

#############################################################################
# 

#set debugControl: b0:3=F (all PPCs =1)
Command="writevme "$Slot"0004a 1 0f0F" 
echo "PPC     : " $Command
$Command
sleep 1



