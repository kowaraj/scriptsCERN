#!/bin/sh
if [ $# -eq 1 ]
then
  fsk=$1" 0002"
else
  fsk="1965 0002"
fi

echo "Write..."


echo "FSK value = $fsk" 
Command="400046 2 $fsk"
writevme $Command


