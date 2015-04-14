#!/usr/bin/python

import argparse
import os
import subprocess
import sys
import time
import operator
import re

import getpass
import interactive

import paramiko
import base64
import getpass
import socket
import traceback
from paramiko.py3compat import input
try:
    import interactive
except ImportError:
    from . import interactive


import select

# setup logging
paramiko.util.log_to_file('demo_simple.log')
# Paramiko client configuration
UseGSSAPI = True             # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True
port = 22


        
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('classname', metavar='Fesa class name', nargs='+',
                                        help='the asdfas')
parser.add_argument('fecname', metavar='cfv-ux45-acsc1b1t', nargs='+',
                                        help='the asdf asdfas')

args = parser.parse_args()
print "args = ", args
fesa_class_name = args.classname[0]
fec_name = args.fecname[0]

print "name = ", fesa_class_name
print "fecs = ", '_'+fec_name


username = 'apashnin'
hostname = fec_name


# now, connect and use paramiko Client to negotiate SSH2 across the connection
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    #client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('*** Connecting...')
    client.connect(hostname)
    #client.exec_command("ls -lat")
    #stdin, stdout, stderr = client.exec_command('uptime')


    stdin, stdout, stderr = client.exec_command("top -b -d 1.0")

    # out_error = stderr.readlines()
    # if len(out_error) > 0:
    #     print "errors = ", out_error
    #     exit()

    PID_  = '(\d+)\s+'
    USER_ = '(\w+)\s+'
    PR_   = '(-*\w+)\s+'  # 20, -70, RT, -2,...
    NI_   = '(-*\w+)\s+'  # -20, 0
    VIRT_ = '(\d+[.]*[\d+]*[mg]*)\s+' 
    RES_  = '(\d+[.]*[\d+]*[mg]*)\s+'
    SHR_  = '(\d+[.]*[\d+]*[mg]*)\s+'
    S_    = '(\w+)\s+'
    CPU_  = '(\d+.\d+)\s+'
    MEM_  = '(\d+.\d+)\s+'
    TIME_ = '(\d+:\d+[.]*[\d+]*)\s+'
    CMD_  = '(\w+)'
    TAIL_ = '(.+)'
    m_exp = PID_ + USER_ + PR_ + NI_ + VIRT_ + RES_ + SHR_ + S_ + CPU_ + MEM_ + TIME_ + CMD_
    print 'ext to match = ', m_exp
            

    log_file = open('log_xxx_'+fec_name, 'w')

    # Wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                #print stdout.channel.recv(1024)
                l = stdout.readline().rstrip('\n')
                #print 'l = ', l
                m = re.search(m_exp, l)
                if m is None:
                    #print 'un-parsed line! = ', l
                    continue

                res_pid = m.group(1)
                res_cpu = m.group(9)
                res_mem = m.group(10)
                res_name = m.group(12)

                if float(res_cpu) > 0 and res_name != 'top':
                    #print "res = ", res_pid, res_cpu, res_mem, res_name
                    log_file.write(res_pid+' '+res_cpu+' '+res_mem+' '+res_name+'\n')
                    log_file.flush()




    exit()

    rem_cmd = 'top -n 5 -b'
    stdin, stdout, stderr = client.exec_command(rem_cmd)


    print "command: ", rem_cmd
    out_error = stderr.readlines()
    if len(out_error) > 0:
        print "errors = ", out_error
        exit()

    out_ok = stdout.readlines()
    print "results: \n\t\t", out_ok
    out_ok = stdout.readlines()
    print "results: \n\t\t", out_ok
    out_ok = stdout.readlines()
    print "results: \n\t\t", out_ok
    out_ok = stdout.readlines()
    print "results: \n\t\t", out_ok
    




    
    print('done')
    # chan = client.invoke_shell()
    # print(repr(client.get_transport()))
    # print('*** Here we go!\n')
    # interactive.interactive_shell(chan)
    # chan.close()
    client.close()
    exit()

    
    if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
#        client.connect(hostname, port, username, password)
        client.connect(hostname)
    else:
        # SSPI works only with the FQDN of the target host
        hostname = socket.getfqdn(hostname)
        try:
            client.connect(hostname, port, username, gss_auth=UseGSSAPI, gss_kex=DoGSSAPIKeyExchange)
        except Exception:
            password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
            client.connect(hostname, port, username, password)

        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        interactive.interactive_shell(chan)
        chan.close()
        client.close()

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)



exit()
fecs = ["cfv-ux45-acsc"+str(cav)+"b"+str(beam)+fec_postfix for cav in range(1, 9) for beam in range(1, 3)]
src_path_pre = "./test/"
pf_name_xml = fesa_class_name+"PersistentData.xml"

for fec in fecs:
    print ""
    print "fec = ", fec
    print "-------------------------"
    pf_dir = os.path.join(src_path_pre, fec, 'data')
    pf_name_original_xml = os.path.join(pf_dir, pf_name_xml)

    p = subprocess.Popen(["ls", pf_dir], stdout=subprocess.PIPE)

    # Construct the dictionary of files-date pairs

    pf_dict = dict()
    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() != None:
            break
        if out != '':
            #print "out = ", out
            
            m = re.search(pf_name_xml+'.(\d+).Z', out)
            if m:
                pf_name = out.rstrip('\n');
                pf_path = os.path.join(pf_dir, pf_name)
                pf_time_sec = os.path.getmtime(pf_path)
                t = time.localtime(pf_time_sec)
                d = time.strftime('%Y%m%d', t)
                #print "pf_path = ", pf_path, "\t\t", d, "a = ", args.date

                pf_dict[d] = pf_path



    # Sort the dict and search for the required date

    pf_sorted = reversed(sorted(pf_dict.items(), key=operator.itemgetter(0)))
    pf_found = list()
    for el in pf_sorted:
        #el:
        #('20150318', './test/cfv-ux45-acsc8b1t/data/ALLTunerControlPersistentData.xml.0.Z')
        #('20150317', './test/cfv-ux45-acsc8b1t/data/ALLTunerControlPersistentData.xml.1.Z')
        #...
        #print el
        if int(el[0]) > arg_date:
            continue

        pf_found.append(el)
        break
    #Found =  [('20150312', './test/cfv-ux45-acsc8b1t/data/ALLTunerControlPersistentData.xml.3.Z')]
    print "Found = ", pf_found

    # Do the replacement
    if len(pf_found) == 0:
        print "\n\nNo file found!"
        continue
    
    # Found pers. file (.Z)
    found_pf_date = pf_found[0][0]
    found_pf_name = pf_found[0][1]
    
    # Save a copy (just in case)
    
    curr_ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #Z-file
    found_pf_name_copy = found_pf_name+'_copy_'+curr_ts
    subprocess.call(["cp", found_pf_name, found_pf_name_copy]) #save Z-file
    print "\nCopied [", found_pf_name, "]"
    print "    to [", found_pf_name_copy, "]:"
    subprocess.call(["ls", "-la", found_pf_name_copy])

    #orig. file
    pf_name_original_copy  = pf_name_original_xml+'_copy_'+curr_ts
    subprocess.call(["cp", pf_name_original_xml, pf_name_original_copy]) #save current pers. file
    print "\nCopied [", pf_name_original_xml, "]"
    print "    to [", pf_name_original_copy, "]:"
    subprocess.call(["ls", "-la", pf_name_original_copy])
    
    # Unzip 
    print "\nUnzipped:"
    subprocess.call(["gzip", "-d", found_pf_name])
    unzipped_pf = found_pf_name.rstrip('.Z')
    subprocess.call(["ls", "-la", unzipped_pf])

    # Remove current file
    subprocess.call(["rm", "-i", pf_name_original_xml])

    # Move unzipped to current
    subprocess.call(["mv", "-i", unzipped_pf, pf_name_original_xml])
    

        
    


                
                
            



        







