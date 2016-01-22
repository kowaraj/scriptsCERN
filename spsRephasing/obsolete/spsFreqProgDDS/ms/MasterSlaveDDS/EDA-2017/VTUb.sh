#!/bin/sh
#clear
#Fesa is Version 7 on ppcrf15


Slot=b

HtimesT="4620"
#HtimesT="4653"

Bunch="291"
Delay="0"
## echo "Slot = "$Slot

# echo "HtimesT =" $HtimesT
# echo "Bunch =" $Bunch
# echo "Delay =" $Delay
  HT0="$HtimesT"

  HT0="$HtimesT"
  : $((HT0 = $HT0 & 0xffff))

  HT1="$HtimesT"
  : $((HT1 = $HT1 >> 16))
  : $((HT1 = $HT1 & 0xffff))


  HT2="$HtimesT"
  : $((HT2 = $HT2 >> 32))
  : $((HT2 = $HT2 & 0xffff))

# echo "HT0 =" $HT0 # 4620
# echo "HT1 =" $HT1 # 0
# echo "HT2 =" $HT2 # 0

B0="$Delay"
  : $((B0 = $B0  & 0xffff))

  B1="$Delay"
  : $((B1 = $B1 >> 16))
  : $((B1 = $B1 & 0xffff))

  B2="$Delay"
  : $((B2 = $B2 >> 32))
  : $((B2 = $B2 & 0xffff))

# echo Convert the values to Hex
  B0=`echo "obase=16;ibase=10; "$B0";" | bc`
  B1=`echo "obase=16;ibase=10; "$B1";" | bc`
  B2=`echo "obase=16;ibase=10; "$B2";" | bc`

# echo "B0 = " $B0 # 120C
# echo "B1 = " $B1 # 0
# echo "B2 = " $B2 # 0

StartSel="0"
StopSel="1"
RestartSel="2"

# echo "Combined is = " F$RestartSel$StartSel$StopSel FFFF


# Start programming VTU



#Stop VTU and enable writing in both context register
    command=$Slot"00000 1 3010"
    writevme $command
    
#Clear faults
    command=$Slot"0000C 1 8080"
#   writevme $command

#Enable counting
    command=$Slot"00000 1 3020"
#    writevme $command

W0="0000"

# echo Write B2 B1 etc
# echo "writevme "$Slot"0003a 8 "$B2" "$B1" "$B0" "$HT2" "$HT1" "$HT0" A000 "$W0
#    command=$Slot"0003a 8 "$B2" "$B1" "$B0" "$HT2" "$HT1" "$HT0" A000 "$W0
    command=$Slot"0003a 8 0000 0000 4819 0000 0000 120C 0000 0000"
# echo writevme 1"0003a 8 0000 0000 4819 0000 0000 120C 0000 0000"
    writevme $command
# echo optimal delay on B0 = 4819

# echo Write 0E register
# echo "writevme "$Slot"0000E 2 F$RestartSel$StartSel$StopSel FFFF"

    command=$Slot"0000E 2 F$RestartSel$StartSel$StopSel FFFF"
    writevme $command

# echo "Write control register 3"
    command=$Slot"0000C 1 ff80"
    writevme $command
# echo Write control register 2 - Sync op from frontpanel, Refresh Status
    command=$Slot"0000A 1 ff81"
    writevme $command
# echo Write control register 1 - SwapEnabled, Counting Enable, DblReg disabled, Sync op
    command=$Slot"00000 1 ff60"
    writevme $command

# echo Write sync delay
    command=$Slot"00036 1 0000"

# echo Write Sync Detector window
    command=$Slot"0005C 2 0000 2D6C"
    writevme $command


# echo Input selection FPannel or BPlane for the sync
    command=$Slot"0000A 1 0101"
    writevme $command

# echo Start the VTU - Soft Start
    command=$Slot"00000 1 0202"
    writevme $command

    
    # echo -e "\nVTU started! [If soft start used]"
    # echo "Set up finished"

#EOF
