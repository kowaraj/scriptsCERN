#!/usr/bin/python

from pyjapc import PyJapc
import argparse


def copy_property(pj, prop, dev_src, dev_dst, uname_src, uname_dst):
    ''' 
    Copy all the fields of the property
        from : dev_src and user_src
          to : dev_dst and user_dst
    '''
    prop_str = dev_src + '/' + prop
    pj.setSelector(uname_src)
    prop_val = pj.getParam(prop_str)

    pj.setSelector(uname_dst)
    prop_str_dst = dev_dst + '/' + prop
    prop_val_dst = pj.getParam(prop_str_dst)
    for param in prop_val.keys():
        prop_val_dst[param] = prop_val[param]
    
    pj.setParam(prop_str_dst, prop_val_dst)

def copy_param(pj, prop, param, dev_src, dev_dst, uname_src, uname_dst):
    ''' 
    Copy param the fields of the property
        from : dev_src and user_src
          to : dev_dst and user_dst
    '''
    param_str = dev_src + '/' + prop + '#' + param
    pj.setSelector(uname_src)
    val = pj.getParam(param_str)

    pj.setSelector(uname_dst)
    param_str_dst = dev_dst + '/' + prop + '#' + param
    pj.setParam(param_str_dst, val)

def _NIY_load_property(pj, prop, dev_src, dev_dst, uname_src, uname_dst, dbg=False):
    ''' 
    Set all field of a property
    from a file for: dev_src and user_src
                 to: dev_dst and user_dst
    '''
    prop_str = dev + '/' + prop
    if dbg == True: 
        input('Copy ' + prop_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
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


def _NIY_save_property(pj, prop, dev_src, uname_src, dbg=False):
    ''' 
    Save to file all field of a property
             from: dev_src and user_src
    to a file for: dev_src and user_src
    '''
    prop_str = dev + '/' + prop
    if dbg == True: 
        input('Copy ' + prop_str + ' from: ' + uname_src + ' to: ' + uname_dst + '?')
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

    
