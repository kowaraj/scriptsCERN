#!/bin/sh

clear
echo Restarting FESA MasterDDS and SlaveDDS
wreboot -N ALLRfMasterDds_R ALLRfMasterDds_S ALLRfSlaveDds_R ALLRfSlaveDds_S
echo done
