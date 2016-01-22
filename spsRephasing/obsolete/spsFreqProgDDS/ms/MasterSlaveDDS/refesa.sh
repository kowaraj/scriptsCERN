#!/bin/sh

clear
echo Restarting FESA MasterDDS
kill -9 ALLRfMasterDds_R ALLRfMasterDds_S
wreboot -N ALLRfMasterDds_R ALLRfMasterDds_S

echo Restarting FESA SlaveDDS

kill -9 ALLRfSlaveDds_R ALLRfSlaveDds_S
wreboot -N ALLRfSlaveDds_R ALLRfSlaveDds_S

wreboot -n ALLVTU_R ALLVTU_S
echo done
