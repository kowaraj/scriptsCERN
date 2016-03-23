from subprocess import Popen, PIPE

import os
import re

def run_bg(cmd_str):
    if 'y' == raw_input('execute? ' + str(cmd_str.split(' '))):
        p = Popen(cmd_str.split(' '), stdout=PIPE, stderr=None)
        
    else:
        print('skipped')

def run(cmd_str):
    if 'y' == raw_input('execute? ' + str(cmd_str.split(' '))):
        p = Popen(cmd_str.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        print(output, err)
    else:
        print('skipped')

def kill(pid):
    if pid:
        run('sudo kill '+ pid)

def pid(name):
    p = Popen(['ps', '-eo', 'pid,command'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    for line in output.split('\n'):
        if name in line:
            pid_ = re.match('\s*(\d+)', line).group(1)
            print('process name: ', name, 'of pid = ', pid_)
            return pid_

