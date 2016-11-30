from pyjapc import PyJapc
import argparse
import json
import re
from subprocess import Popen, PIPE

def rda_get_server_dev_prop(server, dev, prop, noFile=False):

    print('')
    print('Server   : ' + server)
    print('Device   : ' + dev)
    print('Property : ' + prop)
    print('')

    p = Popen(['rda-get', '-s'+server, '-d'+dev, '-p'+prop], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    #search for scalars
    me ='Name : (\w+)\\\\nType : (\w+)\\\\nValue: (\w+[.]*[\d+]*)\\\\n'
    params = re.findall(me, str(output))

    #search for 2d arrays
    me_pre = 'Name : (\w+)\\\\nType : (arr_\w+_\w+\[\d+ \d+\])\\\\n'
    me_val = 'Value: ([\\\\n[\d+ ]*]*)\\\\n\\\\n'
    list_of_2da = re.findall(me_pre + me_val, str(output))
    print('Search for 2D-arrays: ', list_of_2da)
    if len(list_of_2da) > 0:
        found_el = list_of_2da[0]
        arr2d_name = found_el[0]
        arr2d_type = found_el[1]
        arr2d_vstr = found_el[2]
        arr = re.findall('\\\\n([\d+ ]*) ', arr2d_vstr)
        arr2d_val = list()
        [arr2d_val.append(s) for s in arr]
        arr2d = (arr2d_name, arr2d_type, arr2d_val)
        params.append(arr2d)

    params_json = json.dumps(params,sort_keys=True, indent=4, separators=(',', ': '))
    if noFile:
        print(params_json)
    else:
        params_file = open('settings_'+server+'_'+dev+'_'+prop, 'w')
        params_file.write(params_json)

def rda_get_server_dev_prop_user(server, dev, prop, user, noFile=False):

    print('')
    print('Server   : ' + server)
    print('Device   : ' + dev)
    print('Property : ' + prop)
    print('User     : ' + user)
    print('')

    p = Popen(['rda-get', '-s'+server, '-d'+dev, '-p'+prop, '-c'+user], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    #search for scalars
    me ='Name : (\w+)\\\\nType : (\w+)\\\\nValue: (\w+[.]*[\d+]*)\\\\n'
    params = re.findall(me, str(output))

    #search for 2d arrays
    me_pre = 'Name : (\w+)\\\\nType : (arr_\w+_\w+\[\d+ \d+\])\\\\n'
    me_val = 'Value: ([\\\\n[\d+ ]*]*)\\\\n\\\\n'
    list_of_2da = re.findall(me_pre + me_val, str(output))
    print('Search for 2D-arrays: ', list_of_2da)
    if len(list_of_2da) > 0:
        found_el = list_of_2da[0]
        arr2d_name = found_el[0]
        arr2d_type = found_el[1]
        arr2d_vstr = found_el[2]
        arr = re.findall('\\\\n([\d+ ]*) ', arr2d_vstr)
        arr2d_val = list()
        [arr2d_val.append(s) for s in arr]
        arr2d = (arr2d_name, arr2d_type, arr2d_val)
        params.append(arr2d)

    params_json = json.dumps(params,sort_keys=True, indent=4, separators=(',', ': '))
    if noFile:
        print(params_json)
    else:
        params_file = open('settings_'+server+'_'+dev+'_'+prop, 'w')
        params_file.write(params_json)

    
def save_property_notparams(pj, dev, prop, notparams, uname_src, dbg=False):
    ''' Copy all field of a property apart from notparams 
    '''
    prop_str = dev + '/' + prop
    pj.setSelector(uname_src)
    prop_val = pj.getParam(prop_str)

    print(json.dumps(prop_val))




    
