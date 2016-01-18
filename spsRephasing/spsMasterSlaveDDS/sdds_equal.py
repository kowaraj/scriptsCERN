#!/usr/bin/python

import sdds


ftw1 = 0x70000000 
ftw2 = 0x70000000 
ftw3 = 0x70000000 
ftw4 = 0x70000000
ch = "RF1_RF2"
print "Running: setup_dds", ch,  hex(ftw1), hex(ftw2), hex(ftw3), hex(ftw4)

sdds.setup_dds(ch, ftw1, ftw2, ftw3, ftw4)



