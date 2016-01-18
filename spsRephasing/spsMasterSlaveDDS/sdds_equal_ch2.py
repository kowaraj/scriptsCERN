#!/usr/bin/python

import sdds


ftw1 = 0x74000000 
ftw2 = 0x74000000 
ftw3 = 0x74000000 
ftw4 = 0x74000000
ch = "RF2"
print "Running: setup_dds", ch,  hex(ftw1), hex(ftw2), hex(ftw3), hex(ftw4)

sdds.setup_dds(ch, ftw1, ftw2, ftw3, ftw4)



