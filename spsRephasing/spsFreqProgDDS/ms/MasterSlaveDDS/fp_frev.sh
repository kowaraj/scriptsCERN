#!/bin/sh

SlaveSlot=7

echo "set SlaveDDS front pannel Frev In"
  Command=$SlaveSlot"00012 1 1010"
  writevme $Command
