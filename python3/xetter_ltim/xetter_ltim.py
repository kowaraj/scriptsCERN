#!/user/bdisoft/operational/bin/Python/PRO/bin/python

''' PyJapc-based app. to copy/save/load fesa settings
'   from dev1 / user2 to dev3 / user4
'''

from ppm_copy import copy_property, copy_param
from comps import *
import argparse
from pyjapc import PyJapc
import json

import tkinter
from tkinter import *
from tkinter import messagebox


from pyjapc import PyJapc
from time import sleep

from face import Face



if __name__ == '__main__':

    root = Tk()
    root.geometry("1200x800")
    
    print('main')
    app = Face(root)

    print('main loop')
    root.mainloop()
