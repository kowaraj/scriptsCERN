#!/bin/sh

SlaveSlot=7

echo "Slave DDS FTW Toggle Reset Counter"

echo Trigger FrevSync for FTWToggle
  Command=$SlaveSlot"00000 1 0404"
  writevme $Command

echo Set FrevPHase Offset for FTWToggle
  Command=$SlaveSlot"00062 1 0001"
  writevme $Command

echo Set RFON and RFOFF Timing
  Command=$SlaveSlot"0001e 2 001 0100"
  writevme $Command
