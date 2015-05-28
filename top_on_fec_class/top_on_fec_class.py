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


CALL_TOP_PERIOD = 10.0 # [sec] call top over ssh every ... sec
CPU_THRESHOLD = 15. # [%] send an alert if CPU load is higher than ... %
SEND_SMS_PERIOD = 60*15. # [sec] don't send sps if the last one was sent less than ... min ago
SLEEPTIME_NODATA = 1. # sleep for ... sec if no data from ssh channel received

last_sent_ts = 0.
def send_sms_via_email(text):
    
    # At most, once in 15min
    global last_sent_ts
    current_time = time.time()
    #print 'curr = ', current_time
    #print 'last = ', last_sent_ts
    if (current_time - last_sent_ts) < SEND_SMS_PERIOD:
        #print 'no send'
        return
    last_sent_ts = current_time

    # Send the sms

    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
#    fp = open('', 'rb')
    # Create a text/plain message
    msg = MIMEText(text) #fp.read())
#    fp.close()

    # me == the sender's email address
    me = 'apashnin@cern.ch'
    # you == the recipient's email address
    you = '41764871323@mail2sms.cern.ch'

    msg['Subject'] = 'Error!'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    print 'sent'
    s.quit()


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

    stdin, stdout, stderr = client.exec_command("top -b -d "+str(CALL_TOP_PERIOD))

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
            

    log_file = open('log_' +fesa_class_name+ '_' +fec_name, 'w')
    #fault_file = open('/user/apashnin/log_error/fault_TopOnFec.log', 'w')
    #fault_file = open('/dfs/Websites/a/apashnin/log_error/fault_TopOnFec.log', 'w')
    fault_file = open('/dfs/Websites/a/apashnin/log_error/fault_TopOnFec.log', 'a')

    # mark the start of loggin in the file
    curr_ts = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    start_header = 'Started at '+ curr_ts+ ' on fec: '+fec_name+ ' (watching '+ fesa_class_name+ ')\n'
    fault_file.write(start_header)
    fault_file.flush()

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
                
                #print 'name = ', res_name
                m2 = re.search('('+fesa_class_name+')(.+)',res_name)
                #print 'cropped = ', m2
                # if res_name_cropped != fesa_class_name:
                if m2 is None:
                    continue

                if m2.group(1) == fesa_class_name:
                    if float(res_cpu) > CPU_THRESHOLD:
                        #print "res = ", res_pid, res_cpu, res_mem, res_name
                        curr_ts = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
                        msg = curr_ts+' | Error on fec: '+fec_name+' (class: '+fesa_class_name+') :: process ['+res_name+'] takes {'+res_cpu+'}% of CPU\n'
                        #print 'msg = ', msg
                        send_sms_via_email(msg)
                        fault_file.write(msg)
                        fault_file.flush()
        else:
            time.sleep(SLEEPTIME_NODATA)
            


except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)

    

        
    


                
                
            



        







