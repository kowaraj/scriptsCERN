#!/bin/sh

SlaveSlot=7

echo "set DDS Data Source to SPS"
  Command=$SlaveSlot"00012 1 2020"
  writevme $Command
