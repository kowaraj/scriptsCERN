#!/bin/sh
echo QuadDDS LoadSynth running 
if [ $# -eq 1 ]
then
  Slot=$1
  echo Init Synthesizer on card $Slot
  Command=$Slot"00054 6 013F 0C48 0030 0002 4006 0004"
  writevme $Command
  echo Start Load Sequencer
  Command=$Slot"00000 1 0404"
  writevme $Command
else
  echo Usage: LoadSynth Slot
fi
echo QuadDDS LoadSynth finished.

