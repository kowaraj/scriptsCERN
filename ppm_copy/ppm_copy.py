#!/usr/bin/python

from pyjapc import PyJapc
import argparse


'''
def copy_param(param_str, uname_src, uname_dst):
    raw_input('Copy ' + param_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
    pj = PyJapc( selector=uname_src, incaAcceleratorName="SPS", noSet=False)
    p_val = pj.getParam(param_str)
    print 'Value of {' + uname_src + '} = ', p_val

    #pj_dst = PyJapc( selector=uname_dst, incaAcceleratorName="SPS", noSet=False)
    pj.setSelector(uname_dst)
    p_val_dst = pj.setParam(param_str, p_val)
    print 'Value of {' + uname_dst + '} (read-back) = ', pj.getParam(param_str)



def copy_param_5(dev, prop, param, uname_src, uname_dst):
    param_str = dev + '/' + prop + '#' + param
    copy_param(param_str, uname_src, uname_dst)
'''

'''
def copy_property_param(pj, dev, prop, param, uname_src, uname_dst, dbg=False):
    '' 
    For property with no partial-settings allowed.
    Read all the fields in the property, modify the param given, write to destination
    ''
    prop_str = dev + '/' + prop
    if dbg == True: 
        raw_input('Copy ' + prop_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
    pj.setSelector(uname_src)
    prop_val = pj.getParam(prop_str)
    if dbg == True: 
        print 'Value of {' + uname_src + '} = ', prop_val

    if param in prop_val:
        raise RuntimeError(param + ' - Not found in ' + str(prop_val))

    pj.setSelector(uname_dst)
    prop_val_dst = pj.getParam(prop_str)
    if dbg == True: 
        print 'Value of {' + uname_dst + '} = ', prop_val_dst

    if param not in prop_val_dst: 
        raise RuntimeError(param + ' - Not found in ' + str(prop_val_dst))

    prop_val_dst[param] = prop_val[param]
    pj.setParam(prop_str, prop_val_dst)
    if dbg == True: 
        print 'Value of {' + uname_dst + '} (read-back) = ', pj.getParam(prop_str)

def copy_property_params(pj, dev, prop, params, uname_src, uname_dst, dbg=False):
'' 
    For property with no partial-settings allowed.
    Read all the fields in the property, modify the paramS given, write to destination
    ''
    prop_str = dev + '/' + prop
    if dbg == True: 
        raw_input('Copy ' + prop_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
    pj.setSelector(uname_src)
    prop_val = pj.getParam(prop_str)
    if dbg == True: 
        print 'Value of {' + uname_src + '} = ', prop_val

    for param in params:
        if param not in prop_val:
            raise RuntimeError(param + ' - Not found in ' + str(prop_val))


    pj.setSelector(uname_dst)
    prop_val_dst = pj.getParam(prop_str)
    if dbg == True: 
        print 'Value of {' + uname_dst + '} = ', prop_val_dst

    for param in params:
        if param not in prop_val_dst: 
            raise RuntimeError(param + ' - Not found in ' + str(prop_val_dst))

    for param in params:
        prop_val_dst[param] = prop_val[param]
    
    pj.setParam(prop_str, prop_val_dst)
    if dbg == True: 
        print 'Value of {' + uname_dst + '} (read-back) = ', pj.getParam(prop_str)
'''
def copy_property_notparams(pj, dev, prop, notparams, uname_src, uname_dst, dbg=False):
    ''' Copy all field of a property apart from notparams 
    '''
    prop_str = dev + '/' + prop
    if dbg == True: 
        raw_input('Copy ' + prop_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
    pj.setSelector(uname_src)
    prop_val = pj.getParam(prop_str)
    if dbg == True: 
        print('Value of {' + uname_src + '} = ', prop_val)

    pj.setSelector(uname_dst)
    prop_val_dst = pj.getParam(prop_str)
    if dbg == True: 
        print('Value of {' + uname_dst + '} = ', prop_val_dst)

    for param in prop_val.keys():
        if param in notparams:
            print('Skip parameter: ' + param)
        else:
            prop_val_dst[param] = prop_val[param]
    
    pj.setParam(prop_str, prop_val_dst)
    if dbg == True: 
        print('Value of {' + uname_dst + '} (read-back) = ', pj.getParam(prop_str))


    
