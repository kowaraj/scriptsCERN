from subprocess import Popen, PIPE

import os
import re

def rmshm(shm_name):
    ''' Remove shared memory if exists
    '''
    if shmexist(shm_name):
        run('sudo rm /dev/shm/'+shm_name)

def run_bg(cmd_str):
    ''' Run command on background, stderr isn't redirected
    '''
    if 'y' == raw_input('execute? ' + str(cmd_str.split(' '))):
        FNULL = open(os.devnull, 'w')
        p = Popen(cmd_str.split(' '), stdout=FNULL, stderr=FNULL) 
        
    else:
        print('skipped')

def run_bg_broken(cmd_str):
    ''' Run command on background, stderr isn't redirected
    '''
    if 'y' == raw_input('execute? ' + str(cmd_str.split(' '))):
        p = Popen(cmd_str.split(' '), stdout=None, stderr=None) # !!! get's stuck with PIPE
        
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
    ''' Return PID of the process
    '''
    p = Popen(['ps', '-eo', 'pid,command'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    for line in output.split('\n'):
        if name in line:
            pid_ = re.match('\s*(\d+)', line).group(1)
            print('process name: ', name, 'of pid = ', pid_)
            return pid_

def shmexist(name):
    ''' Return True if shared memory exists, False otherwise
    '''
    p = Popen(['ls', '-la', '/dev/shm/'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    for line in output.split('\n'):
        if name in line:
            print('Shmem exist: ', name)
            return True
    return False

