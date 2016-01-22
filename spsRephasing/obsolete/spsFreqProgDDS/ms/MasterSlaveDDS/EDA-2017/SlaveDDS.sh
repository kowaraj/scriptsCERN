# VTUb must be resynced from backplane


#!/bin/sh

clear
echo Open ADC Loop
adcOFF.sh

echo
#echo "Hit Return to init Frev Prog VTU and MasterDDS"
#read dummy
echo Load Frev Prog VTU
../FrevG4620.sh A
echo
echo Load MasterDDS
../MasterDDS.sh 4

#echo "Hit Return to init Slave DDS"
#read dummy
echo slave_dds_reset with phase accu reset
SlaveDDS_Init.sh

#echo "Hit Return to Close ADC loop"
#read dummy
echo "Start ADC Loop"
adcON.sh


echo "Hit Return to Sync SyncCLK to Master Frev"
#read dummy
echo SlaveDDS SyncCLK slave enable and sync to Master Frev
SyncSlaveDDS.sh
echo
echo "RF Prog RF AVG and RF FSK locked, Hit Return to continue"
#read dummy

echo
#echo "Hit Return to init Master Frev VTU"
#read dummy
echo Master Frev VTU Initialization
VTUb.sh
# Delay from RF_In to Sync_In
#writevme b00036 1 00c9
echo

echo FTW Toggle sync to Master Frev
SlaveDDS_FTWToggle_RST.sh
#echo "Hit Return to continue"
#read dummy

echo
# echo VTUb again
# VTUb.sh
# SyncSlaveDDS.sh
echo Sequence done
