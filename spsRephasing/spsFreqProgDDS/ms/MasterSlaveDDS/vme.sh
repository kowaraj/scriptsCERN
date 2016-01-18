#!/bin/sh

SlaveSlot=7

echo "set DDS Data Source to VME"
  Command=$SlaveSlot"00012 1 2000"
  writevme $Command
