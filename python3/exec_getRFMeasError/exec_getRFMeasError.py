#!/user/bdisoft/operational/bin/Python/PRO/bin/python

'  #!/usr/bin/python '

'''
Description:

1. read the buffers from the fesa class
2. if error
   - dump into a file (*.npy)
   - save a pic
   - send an sms

Notes:

  - pyjapc returns numpy.ndarray in python3 version

'''

import argparse
import os
import subprocess
import sys
import time
import operator
import re

from time import sleep
import signal
import sys
from pyjapc import PyJapc
import matplotlib.pyplot as plt
import numpy

parser = argparse.ArgumentParser(description='argszzz')
parser.add_argument('device', metavar='fesa instance name', nargs='+',
                                        help='')
args = parser.parse_args()
#print "args = ", args
FesaInstanceName = args.device[0]

ok_to_send = True

def send_sms_via_email(text):
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
    you = '41754111323@mail2sms.cern.ch'

    msg['Subject'] = 'Error!'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    print('sent')
    s.quit()

print(':: selector = ')
p = PyJapc( selector='', incaAcceleratorName="LHC", noSet=True)
print(':: p acquired.')
time.sleep(0.5)
p.rbacLogin('apashnin', True)
print(':: login done.')

try:
    while True:

        pe = FesaInstanceName   + "/RFMeasurementModeAcq#obError"
        pe1s = FesaInstanceName + "/RFMeasurementModeAcq#obError1s"
        e = p.getParam(pe)
        e1s = p.getParam(pe1s)
        
        if e or e1s:

            if not ok_to_send:
                print('no send')

            else:
                ok_to_send = False
                ts = str(time.strftime('%y%m%d_%H%M%S', time.localtime(time.time())))

                # BEng
                p_BEngBuffer = p.getParam(FesaInstanceName+"/RFMeasurementModeAcq#obBENG")
                if not isinstance(p_BEngBuffer, numpy.ndarray):
                    print('pyjapc.getParam returned not a numpy.ndarray (for BENG)')
                else:
                    fn = FesaInstanceName+'_dumpBEng_'+ts
                    numpy.save(fn, p_BEngBuffer)

                    f_pic = open(fn+'_pic.png', 'w')
                    fig = plt.figure()
                    plt.plot(p_BEngBuffer)
                    fig.savefig(f_pic)
                    plt.close(fig)

                # Freq
                p_FreqBuffer = p.getParam(FesaInstanceName+"/RFMeasurementModeAcq#obFreq")
                if not isinstance(p_FreqBuffer, numpy.ndarray):
                    print('pyjapc.getParam returned not a numpy.ndarray (for Freq)')
                else:
                    fn = FesaInstanceName+'_dumpFreq_'+ts
                    numpy.save(fn, p_FreqBuffer)

                    f_pic = open(fn+'_pic.png', 'w')                
                    fig = plt.figure()
                    plt.plot(p_FreqBuffer)
                    fig.savefig(f_pic)
                    plt.close(fig)

                # send
                send_sms_via_email('RFMeasErr@'+FesaInstanceName+': '+str(e)+'/'+str(e1s));

        else:
            ok_to_send = True
            print('no error')

        time.sleep(10) #10sec
            


except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    f = open('error.log', 'w')
    msg = 'Caught exception:\n for device: %s\n %s\n %s' % (FesaInstanceName, e.__class__, e)
    f.write(msg)
    f.close()
    send_sms_via_email("Exc! exec_cmd_on_fec_on_proc.py crashed: " + str(e));

    



           


                
                
            



        







