#/usr/bin/python

def get_val():
    sleep(0.01)
    return cs.m.debugFpSLFTW1rb

l = [get_val() for i in range(1000)]
fd = open('fg.txt', 'w')
[fd.write(str(x)+'\n') for x in l]
fd.close     
