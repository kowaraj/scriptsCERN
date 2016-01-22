#!/usr/bin/python

import sdds


ftw_RF1 = 0x70000000 
ftw_RF2 = 0x74000000 
ftw = 0x78000000 




s = sdds.sdds(6)
s.reset_dds()
s.setup_dds("RF1", ftw_RF1, ftw, ftw, ftw)
s.setup_dds("RF2", ftw, ftw_RF2, ftw, ftw)






