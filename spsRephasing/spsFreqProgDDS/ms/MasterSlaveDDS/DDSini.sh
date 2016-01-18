

echo "set DDS Data Source to VME"
  Command=$Slot"00012 1 2000"
  writevme $Command

 echo CSR select CH0 CH2 0101 0000 
  Command=$Slot"0004A 3 0000 0050 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0000 cosinus
  Command=$Slot"0004A 3 0000 0300 0003"
  writevme $Command
 echo CTW0 init
#  Command=$Slot"0004A 3 32CC 0F40 0004"
  Command=$Slot"0004A 3 3435 B94B 0004"
  writevme $Command
#echo CPW0 init 25 deg
 #Command=$Slot"0004A 3 0000 0471 0005"
 #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$Slot"0004A 3 0000 13FF 0006"
  Command=$Slot"0004A 3 0000 0000 0006"
  writevme $Command
###########
 echo CSR select CH1 CH3 1010 0000
  Command=$Slot"0004A 3 0000 00A0 0000"
  writevme $Command
 echo CFR init 0000 0011 0000 0001 sinus
  Command=$Slot"0004A 3 0000 0301 0003"
  writevme $Command
 echo CTW0 init
#  Command=$Slot"0004A 3 32Cc 0F40 0004"
  Command=$Slot"0004A 3 3435 B94B 0004"
  writevme $Command
#echo CPW0 init 25 deg
 #Command=$Slot"0004A 3 0000 0471 0005"
 #writevme $Command
 echo ACR init 0000 0000 0001 0011 1111 1111
#  Command=$Slot"0004A 3 0000 13FF 0006"
  Command=$Slot"0004A 3 0000 0000 0006"
  writevme $Command
############
echo IO_Update DDS
  Command=$Slot"00000 1 0202"
  writevme $Command

