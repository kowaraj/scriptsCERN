from pyjapc import PyJapc
import argparse

def set_out_enabled(pj, dev, uname, val):
    ''' 
    To enable/disable the LTIM event for dev, uname
    '''
    prop_str = dev + '/ExpertSetting'
    pj.setSelector(uname)
    prop_val = pj.getParam(prop_str)
    prop_val['outEnabled'] = val
    pj.setParam(prop_str, prop_val)



    
