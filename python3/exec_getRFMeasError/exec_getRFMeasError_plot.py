#!/user/bdisoft/operational/bin/Python/PRO/bin/python

import argparse
import matplotlib.pyplot as plt
import numpy

parser = argparse.ArgumentParser(description='')
parser.add_argument('fn_dump', metavar='', nargs='+', help='')
args = parser.parse_args()
print("args = ", args)
fn = args.fn_dump[0]

dump = numpy.load(fn)
plt.plot(dump)
plt.show()





           


                
                
            



        







