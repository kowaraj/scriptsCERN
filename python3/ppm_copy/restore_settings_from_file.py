import json
from subprocess import Popen, PIPE

def rda_convert_val(valstr):
    if valstr == 'false':
        return '0'
    if valstr == 'true':
        return '1'
    return valstr

def rda_set_server_dev_prop_user(server, dev, prop, user='', noFile=False):

    print('')
    print('Server   : ' + server)
    print('Device   : ' + dev)
    print('Property : ' + prop)
    print('User     : ' + user)
    print('')

    fd = open('settings_'+server+'_'+dev+'_'+prop, 'r')
    pstr = json.loads(fd.read())
    print(pstr)

    nstr = ','.join([p[0] for p in pstr])
    tstr = ','.join([p[1] for p in pstr])
    vstr = ','.join([rda_convert_val(p[2]) for p in pstr])

    if user:
        args = ['rda-set', '-s'+server, '-d'+dev, '-p'+prop, '-c'+user, '-f', nstr, '-t', tstr, '-v', vstr]
    else:
        args = ['rda-set', '-s'+server, '-d'+dev, '-p'+prop,            '-f', nstr, '-t', tstr, '-v', vstr]
    print('args = [', args, ']')
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    print(output, err)

def rda_set_server_dev_prop_users(server, dev, prop, user_from, user_to):
    ''' Read from FILE for 'user_from' and set to the 'user_to'
    '''

    print('')
    print('Server   : ' + server)
    print('Device   : ' + dev)
    print('Property : ' + prop)
    print('User_from: ' + user_from)
    print('User_to  : ' + user_to)
    print('')

    here: unfinished thing.... 

    fd = open('settings_'+server+'_'+dev+'_'+prop+'_'+user_from, 'r')
    pstr = json.loads(fd.read())
    print(pstr)
    nstr = ','.join([p[0] for p in pstr])
    tstr = ','.join([p[1] for p in pstr])
    vstr = ','.join([rda_convert_val(p[2]) for p in pstr])
    
    args = ['rda-set', '-s'+server, '-d'+dev, '-p'+prop, '-c'+user, '-f', nstr, '-t', tstr, '-v', vstr]

    print('args = [', args, ']')
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    print(output, err)

def rda_setNo2dArr_server_dev_prop_user(server, dev, prop, user='', noFile=False):

    print('')
    print('Server   : ' + server)
    print('Device   : ' + dev)
    print('Property : ' + prop)
    print('User     : ' + user)
    print('')

    fd = open('settings_'+server+'_'+dev+'_'+prop, 'r')
    pstr = json.loads(fd.read())
    print('params = ', pstr)

    nstr = ''
    tstr = ''
    vstr = ''
    for p in pstr:
        t = str(p[1])
        if '_2d' not in t:
            nstr += p[0] + ','
            tstr += t + ','
            vstr += rda_convert_val(p[2]) + ','
        else:
            print('Skipped type: ', t)
    nstr = nstr.rstrip(',')
    tstr = tstr.rstrip(',')
    vstr = vstr.rstrip(',')
    

    if user:
        args = ['rda-set', '-s'+server, '-d'+dev, '-p'+prop, '-c'+user, '-f', nstr, '-t', tstr, '-v', vstr]
    else:
        args = ['rda-set', '-s'+server, '-d'+dev, '-p'+prop,            '-f', nstr, '-t', tstr, '-v', vstr]
    print('args = [', args, ']')
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    print('output = ', output)
    print('errors = ', err)

    




    
