#!/user/bdisoft/operational/bin/Python/PRO/bin/python

''' PyJapc-based app. to copy/save/load fesa settings
'   from dev1 / user2 to dev3 / user4
'''

from ppm_copy import copy_property
from comps import *
import argparse
from pyjapc import PyJapc
import json
from tkinter import *
from pyjapc import PyJapc
from time import sleep

class Face(Frame):
    K_PROP    = 'property'
    K_PARAM   = 'parameter'
    K_DEV_SRC = 'device' #
    K_USR_SRC = 'user' #
    K_DEV_DST = 'device_dst'
    K_USR_DST = 'user_dst'

    DB_FILENAME = 'db.json'

    def __init__(self, parent):

        self.pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
        #sleep(1)

        Frame.__init__(self, parent)
        self.parent = parent

        with open(self.DB_FILENAME, 'r') as fd:
            self.dbDict = json.loads(fd.read())

        self.queryDict = {self.K_PROP : [], self.K_PARAM : [], self.K_DEV_SRC : [], self.K_USR_SRC: [], self.K_DEV_DST:[], self.K_USR_DST:[]}
        self.selDict   = {self.K_PROP : '',                    self.K_DEV_SRC : '', self.K_USR_SRC: ''}

        self.svSelectedDev = StringVar()
        self.svSelectedProp = StringVar()
        self.svCommand = StringVar()

        self.initUI()


    def cbUpdateQuery(self, name, sel, last):
        self.selDict[name] = last
        self.queryDict[name] = sel

        self.__updateQuery()
        self.__updateSelProp()


    def __updateSelProp(self):
        s = self.selDict[self.K_DEV_SRC]+'/'+self.selDict[self.K_PROP]+' @'+self.selDict[self.K_USR_SRC]
        self.svSelectedProp.set(s)


    def __updateQuery(self):
        self.t_cmd.delete(1.0, END )
        queryStr = 'copy'+\
                   '\n property     : ' + ','.join(self.queryDict[self.K_PROP]) +\
                   '\n parameters   : ' + ','.join(self.queryDict[self.K_PARAM]) +\
                   '\n from devices : ' + ','.join(self.queryDict[self.K_DEV_SRC]) +\
                   '\n for users    : ' + ','.join(self.queryDict[self.K_USR_SRC])
        selectedStr = self.selDict[self.K_DEV_SRC] + self.selDict[self.K_PROP]  + ' @'+self.selDict[self.K_USR_SRC] 
        self.t_cmd.insert(1.0, queryStr)


    def __updateSaveDB(self):
        import shutil
        shutil.move(self.DB_FILENAME, self.DB_FILENAME+'.bak')
        with open(self.DB_FILENAME, 'w') as fd:
            fd.write(json.dumps(self.dbDict))
            fd.close()


    def __updateLBS(self):
        self.lbsDeviceSrc.delete(0, END)
        self.lbsDeviceDst.delete(0, END)
        for name in self.dbDict[self.K_DEV_SRC]:
            self.lbsDeviceSrc.insert(END, name) 
            self.lbsDeviceDst.insert(END, name)


    def __addDeviceName(self, e):

        name = e.widget.get()

        #update and save db
        if name in self.dbDict[self.K_DEV_SRC]:
            self.dbDict[self.K_DEV_SRC].remove(name)
        else:
            self.dbDict[self.K_DEV_SRC].append(name)
        self.__updateSaveDB()
        self.__updateLBS()


    def __getParameters(self):

        prop_str = self.selDict[self.K_DEV_SRC]+'/'+self.selDict[self.K_PROP]
        #input(prop_str)

        user = self.selDict[self.K_USR_SRC]
        self.pj.setSelector(user)
        prop_val = self.pj.getParam(prop_str)

        self.textDebug.insert(END, str(prop_val))
        self.__recreateDataFrame(prop_val)


    def __copyParametersDev_u2u(self):
        pass

    def __copyParametersUsr_d2d(self):
        pass


    def __copyParameters(self):

        prop = self.selDict[self.K_PROP]
        param = self.selDict[self.K_PARAM]
        dev_src = self.selDict[self.K_DEV_SRC]
        dev_dst = self.selDict[self.K_DEV_DST]
        user_src = self.selDict[self.K_USR_SRC]
        user_dst = self.selDict[self.K_USR_DST]

        print('copy prop = ', prop)
        print('copy param = ', param)
        print('copy dev_src = ', dev_src)
        print('copy dev_dst = ', dev_dst)
        print('copy user_src = ', user_src)
        print('copy user_dst = ', user_dst)

        return
        
        input('!!!! NIY!!! ')


        # for p in self.selDict[self.K_PROP]:
        #     user = self.selDict[self.K_USR_SRC][0]
            
            
        #     for [x,y] in [[x,y] for x in [0,1] for y in range(1,9)] :
        #     dev_src = 'SX.RF11-'+str(x)+'-'+str(y)
        #     dev_dst = 'SX.RF22-'+str(x)+'-'+str(y)            
        #     input('copy? ', p, dev_src, dev_dst, user_src, user_dst)
        #     #copy_property(pj, p, dev_src, dev_dst, user_src, user_dst)



        # user = self.selDict[self.K_USR_SRC]
        # pj.setSelector(user)
        # prop_val = pj.getParam(prop_str)

        # self.textDebug.insert(END, str(prop_val))
        # self.__recreateDataFrame(prop_val)


    def __recreateDataFrame(self, data):
        for ch in self.f_control_data.winfo_children():
            ch.destroy()

        i = 0
        for k in data.keys():
            l1 = Label(self.f_control_data, anchor='w', text=k, width=20)
            l1.grid(row=i, column=0)
            t1 = Text(self.f_control_data, height=1)
            t1.insert('1.0', data[k])
            t1.grid(row=i, column=1)
            i = i+1

    def initUI(self):

        self.parent.title("Title")
        self.pack(fill=BOTH, expand=True)
        
        f_from = Frame(self, relief=RAISED, height=600, width=300, borderwidth=2, bg='red')
        f_from.pack(fill=BOTH, side=LEFT)

        f_from_dev = Frame(f_from, relief=RAISED, height=200, width=100, borderwidth=2, bg='green')
        f_from_dev.pack(fill=X)
        l_dev = Label(f_from_dev, text="Devices", width=6)
        l_dev.pack(side=TOP, padx=5, pady=5)

        # Device_src - listbox
        els = ["VTUFrevAllion1", "VTUFrevAllawake1", "VTUFrevAllproton1"]
        self.lbsDeviceSrc = LBS(f_from_dev, self.K_DEV_SRC, self.dbDict[self.K_DEV_SRC], self.cbUpdateQuery, sventry=self.svSelectedDev)
        # Device_src - entry
        e = Entry(f_from_dev, textvariable=self.svSelectedDev)
        e.bind("<Return>", self.__addDeviceName)
        e.pack(side=TOP, fill=X)


        f_from_user = Frame(f_from, relief=RAISED, height=300, width=100, borderwidth=1, bg='blue')
        f_from_user.pack(fill=X)
        l_usr = Label(f_from_user, text="Users", width=6)
        l_usr.pack(side=TOP, padx=5, pady=5)
        # User_src
        Lb_usr = LBS(f_from_user, self.K_USR_SRC, self.dbDict[self.K_USR_SRC], self.cbUpdateQuery)


        f_control = Frame(self, relief=RAISED, height=300, width=200, borderwidth=2, bg='yellow')
        f_control.pack(fill=Y, side=LEFT)

        f_control_top = Frame(f_control, relief=RAISED, height=300, width=200, borderwidth=2, bg='cyan')
        f_control_top.pack(fill=Y, side=TOP)

        f_control_bottom= Frame(f_control, relief=RAISED, height=300, width=200, borderwidth=2, bg='magenta')
        f_control_bottom.pack(fill=Y, side=TOP)

        l_selected = Label(f_control_top, textvariable=self.svSelectedProp, width=6)
        l_selected.pack(fill=X, side=TOP, padx=5, pady=5)

        Button(f_control_top, text="GET",command=self.__getParameters).pack(side=LEFT, anchor=N)
        Button(f_control_top, text="COPY",command=self.__copyParameters).pack(side=LEFT, anchor=N)

        f_control_prop = Frame(f_control_top, relief=RAISED, height=200, width=200, borderwidth=2, bg='green')
        f_control_prop.pack(fill=Y, side=TOP)

        # Property - listbox
        els = ["NormalMode", "Status", "Mode"]
        self.lbsProperty = LBS(f_control_prop, self.K_PROP, els, self.cbUpdateQuery)

        self.f_control_data = Frame(f_control_bottom, relief=RAISED, height=400, width=200, borderwidth=2, bg='blue')
        self.f_control_data.pack(fill=Y, side=TOP)

        vals = {'a': 1, 'b': 2}
        self.__recreateDataFrame(vals)

        f_control_cmd = Frame(f_control_top, relief=RAISED, height=400, width=200, borderwidth=2, bg='grey')
        f_control_cmd.pack(fill=X, side=TOP)
        self.t_cmd = Text(f_control_cmd, height=5)
        self.t_cmd.insert(END, "some default text")
        self.t_cmd.pack(side=TOP)

        f_control_debug = Frame(f_control_bottom, relief=SUNKEN, height=400, width=200, borderwidth=2, bg='grey')
        f_control_debug.pack(fill=Y, side=TOP)
        self.textDebug = Text(f_control_debug, height=10)
        self.textDebug.pack(side=TOP)

        f_to = Frame(self, relief=RAISED, height=600, width=300, borderwidth=2, bg='pink')
        f_to.pack(fill=BOTH, side=LEFT)

        f_to_dev = Frame(f_to, relief=RAISED, height=200, width=100, borderwidth=2, bg='green')
        f_to_dev.pack(fill=X)

        l_dev = Label(f_to_dev, text="Devices", width=6)
        l_dev.pack(side=TOP, padx=5, pady=5)

        # Devices_dst
        self.lbsDeviceDst = LBS(f_to_dev, self.K_DEV_SRC, self.dbDict[self.K_DEV_SRC], self.cbUpdateQuery)

        f_to_user = Frame(f_to, relief=RAISED, height=300, width=100, borderwidth=1, bg='blue')
        f_to_user.pack(fill=X)

        l_usr = Label(f_to_user, text="Users", width=6)
        l_usr.pack(side=TOP, padx=5, pady=5)
        Lb_usr = LBS(f_to_user, self.K_USR_DST, self.dbDict[self.K_USR_SRC], self.cbUpdateQuery)




if __name__ == '__main__':

    root = Tk()
    root.geometry("1200x800")
    
    app = Face(root)

    root.mainloop()
