#!/bin/sh

clear
echo changing HnumSel on SlaveDDS
SlaveSlot=7

command=$SlaveSlot"0001C 1 0202"
writevme $command

echo Changing VTU for h4653
FrevG4653.sh a
echo done
