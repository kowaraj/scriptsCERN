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

from pyjapc import PyJapc
from time import sleep

class DBDict:

    K_PROP    = 'property'
    K_PARAM   = 'parameter'
    K_DEV_SRC = 'device' #
    K_USR_SRC = 'user' #
    K_DEV_DST = 'device_dst'
    K_USR_DST = 'user_dst'

'''
dict = {'devices' : [
                     { 'name'         : 'VTUFrevAllawake1', 
                       'class'        : 'ALLVTULHC', 
                       'fec'          : 'cfv-ba3-allawake3', 
                       'pers-data'    : 'du-name.class-name', 
                       'copy-in-file' : 'filename'...'
                     }
                     ...
                    ]
        'classes' : [
                     {'name' : 'ALLVTULHC', 'properties' : ['Mode', 'Status', ..], ...
                     ...
                    ]

'''

    DB_FILENAME = 'db.json'

    def __init__(self):

        with open(self.DB_FILENAME, 'r') as fd:
            self.data = json.loads(fd.read())
        
    def srcDev(self):
        return self.data[self.K_DEV_SRC]

    def srcUsr(self):
        return self.data[self.K_USR_SRC]

    def prop(self):
        return self.data[self.K_PROP]
        
    def __saveDB(self):
        import shutil
        shutil.move(self.DB_FILENAME, self.DB_FILENAME+'.bak')
        with open(self.DB_FILENAME, 'w') as fd:
            fd.write(json.dumps(self.data))
            fd.close()
        
    def __updateDB(self):
        if name in self.data[self.K_DEV_SRC]:
            self.data[self.K_DEV_SRC].remove(name)
        else:
            self.data[self.K_DEV_SRC].append(name)
        self.__updateSaveDB()

class Face(Frame):
    #TODO: change the structure of the dictionary: dev - acc - class - props - params - values - 

    def __init__(self, parent):

        self.doGetOnPropSelection = False
        self.pj = PyJapc(selector='will be set later', incaAcceleratorName="SPS", noSet=False)
        #sleep(1)

        Frame.__init__(self, parent)
        self.parent = parent

        self.db = DBDict()
        self.queryDict = {DBDict.K_PROP : [], DBDict.K_PARAM : [], DBDict.K_DEV_SRC : [], DBDict.K_USR_SRC: [], DBDict.K_DEV_DST:[], DBDict.K_USR_DST:[]}
        self.selDict   = {DBDict.K_PROP : '', DBDict.K_PARAM : '', DBDict.K_DEV_SRC : '', DBDict.K_USR_SRC: ''}

        self.svSelectedDev = StringVar()
        self.svSelectedProp = StringVar()
        self.svCommand = StringVar()

        self.initUI()


    def cbUpdateQuery(self, name, selList, last):
        print('name = ', name)
        print('sel =  ', selList)

        if name == DBDict.K_PARAM: #selList is a dict of {pName : pValue}
            sel = [el[:el.find(':')] for el in selList] #extract param names
            i = self.lbsProperty.index(ACTIVE)
            propi = self.lbsProperty.get(i) #last selected prop in the listbox
            print('prop i = ', propi)
            self.lbsProperty.selection_clear(0,END)
            self.lbsProperty.selection_set(i)
            self.selDict[DBDict.K_PROP] = propi
            self.queryDict[DBDict.K_PROP] = [propi]
        else:
            sel = selList[:]

        print('sel*=  ', sel)

        self.selDict[name] = last
        self.queryDict[name] = sel

        self.__updateQuery()
        self.__updateSelProp()

        if name == DBDict.K_PROP:
            ds = self.selDict[DBDict.K_DEV_SRC]
            ps = self.selDict[DBDict.K_PROP]
            us = self.selDict[DBDict.K_USR_SRC]
            if len(ds) > 0 and len(ps) > 0 and len(us) > 0:
                if self.doGetOnPropSelection:
                    self.__getParameters()

            


    def __updateSelProp(self):
        s = self.selDict[DBDict.K_DEV_SRC]+'/'+self.selDict[DBDict.K_PROP]+' @'+self.selDict[DBDict.K_USR_SRC]
        self.svSelectedProp.set(s)


    def __updateQuery(self):
        self.t_cmd.delete(1.0, END )
        queryStr = 'COPY FROM: \n'+\
                   ' property     : ' + ', '.join(self.queryDict[DBDict.K_PROP]) +'\n'+\
                   ' parameters   : ' + ', '.join(self.queryDict[DBDict.K_PARAM]) +'\n'+\
                   ' from devices : ' + ', '.join(self.queryDict[DBDict.K_DEV_SRC]) +'\n'+\
                   ' from users   : ' + ', '.join(self.queryDict[DBDict.K_USR_SRC]) +'\n'+\
                   'COPY TO:' +'\n'+\
                   ' to devices   : ' + ', '.join(self.queryDict[DBDict.K_DEV_DST]) +'\n'+\
                   ' to users     : ' + ', '.join(self.queryDict[DBDict.K_USR_DST])
        selectedStr = self.selDict[DBDict.K_DEV_SRC] + self.selDict[DBDict.K_PROP]  + ' @'+self.selDict[DBDict.K_USR_SRC] 
        self.t_cmd.insert(1.0, queryStr)




    def __updateLBS(self):
        self.lbsDeviceSrc.delete(0, END)
        self.lbsDeviceDst.delete(0, END)
        for name in self.db.srcDev():
            self.lbsDeviceSrc.insert(END, name) 
            self.lbsDeviceDst.insert(END, name)


    def __addDeviceName(self, e):
        name = e.widget.get()
        self.db.__updateDB()
        self.__updateLBS()


    def __getParameters(self):

        prop_str = self.selDict[DBDict.K_DEV_SRC]+'/'+self.selDict[DBDict.K_PROP]
        #input(prop_str)

        user = self.selDict[DBDict.K_USR_SRC]
        self.pj.setSelector(user)
        prop_val = self.pj.getParam(prop_str)

        self.textDebug.insert(END, str(prop_val))
        self.__recreateDataFrame(prop_val)


    def __copyParametersDev_u2u(self):
        pass

    def __copyParametersUsr_d2d(self):
        pass


    def __copyParameters(self):

        prop = self.queryDict[DBDict.K_PROP]
        param = self.queryDict[DBDict.K_PARAM]
        dev_src = self.queryDict[DBDict.K_DEV_SRC]
        dev_dst = self.queryDict[DBDict.K_DEV_DST]
        user_src = self.queryDict[DBDict.K_USR_SRC]
        user_dst = self.queryDict[DBDict.K_USR_DST]

        print('copy prop = ', prop)
        print('copy param = ', param)
        print('copy dev_src = ', dev_src)
        print('copy dev_dst = ', dev_dst)
        print('copy user_src = ', user_src)
        print('copy user_dst = ', user_dst)

        srcDev   = self.queryDict[DBDict.K_DEV_SRC][0]
        srcUser  = self.queryDict[DBDict.K_USR_SRC][0]
        ps       = self.queryDict[DBDict.K_PROP]
        params   = self.queryDict[DBDict.K_PARAM]
        dstDevs  = self.queryDict[DBDict.K_DEV_DST]
        dstUsers = self.queryDict[DBDict.K_USR_DST]
        for dstDev in dstDevs:
            for dstUser in dstUsers:
                if len(params) == 0:
                    for p in ps:
                        pstr = 'Copying: property ('+ p+ ') from dev@user ('+ srcDev+'@'+srcUser+') to dev@user ('+ dstDev+'@'+dstUser+')'
                        print(pstr)
                        #tkMessageBox.showinfo("Warning! Are you sure?", pstr)
                        ret = input(pstr)
                        if ret != 'yes':
                            continue
                        copy_property(self.pj , p, srcDev, dstDev, srcUser, dstUser)
                else:
                    if len(ps) != 1:
                        raise RuntimeError('selected parameters for more than 1 property')

                    p = ps[0]
                    for param in params:
                        pstr = 'Copying: param ('+param+') of property ('+ p+ ') from dev@user ('+ srcDev+'@'+srcUser+') to dev@user ('+ dstDev+'@'+dstUser+')'
                        print(pstr)
                        #tkMessageBox.showinfo("Warning! Are you sure?", pstr)
                        ret = input(pstr)
                        if ret != 'yes':
                            continue
                        copy_param(self.pj , p, param, srcDev, dstDev, srcUser, dstUser)
                        

    def __recreateDataFrame(self, dataDict):

        self.lbsParamData.delete(0, END)
        for k in dataDict.keys():
            s = k +': '+ str(dataDict[k])
            self.lbsParamData.insert(END, s)


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
        self.lbsDeviceSrc = LBS(f_from_dev, DBDict.K_DEV_SRC, self.db.srcDev(), self.cbUpdateQuery, sventry=self.svSelectedDev, _sm=SINGLE)
        # Device_src - entry
        e = Entry(f_from_dev, textvariable=self.svSelectedDev)
        e.bind("<Return>", self.__addDeviceName)
        e.pack(side=TOP, fill=X)


        f_from_user = Frame(f_from, relief=RAISED, height=300, width=100, borderwidth=1, bg='blue')
        f_from_user.pack(fill=X)
        l_usr = Label(f_from_user, text="Users", width=6)
        l_usr.pack(side=TOP, padx=5, pady=5)
        # User_src
        Lb_usr = LBS(f_from_user, DBDict.K_USR_SRC, self.db.srcUsr(), self.cbUpdateQuery, _sm=SINGLE)


        f_control = Frame(self, relief=RAISED, height=300, width=200, borderwidth=2, bg='yellow')
        f_control.pack(fill=Y, side=LEFT)

        # Frame - Control - Top

        f_control_top = Frame(f_control, relief=RAISED, height=300, width=200, borderwidth=2, bg='cyan')
        f_control_top.pack(fill=Y, side=TOP)

        l_selected = Label(f_control_top, textvariable=self.svSelectedProp, width=6)
        l_selected.pack(fill=X, side=TOP, padx=5, pady=5)

        Button(f_control_top, text="GET",command=self.__getParameters).pack(side=LEFT, anchor=N)
        Button(f_control_top, text="COPY",command=self.__copyParameters).pack(side=LEFT, anchor=N)

        f_control_prop = Frame(f_control_top, relief=RAISED, height=200, width=200, borderwidth=2, bg='green')
        f_control_prop.pack(fill=Y, side=TOP)

        # Property - listbox
        els = ["NormalMode", "Status", "Mode"]
        self.lbsProperty = LBS(f_control_prop, DBDict.K_PROP, els, self.cbUpdateQuery)

        # Frame - Control - Bottom

        f_control_bottom= Frame(f_control, relief=RAISED, height=300, width=200, borderwidth=2, bg='magenta')
        f_control_bottom.pack(fill=Y, side=TOP)

        # Frame - Control - Bottom - Current prop data (entry)
        Label(f_control_bottom, textvariable=self.svSelectedProp).pack(side=TOP, fill=X)

        self.f_control_data = Frame(f_control_bottom, relief=RAISED, height=400, width=200, borderwidth=2, bg='blue')
        self.f_control_data.pack(fill=BOTH, side=TOP)

        valsDict = ['a: 1', 'b: 2']
        # Devices_dst
        self.lbsParamData = LBS(self.f_control_data, DBDict.K_PARAM, valsDict, self.cbUpdateQuery)


        f_control_cmd = Frame(f_control_top, relief=RAISED, height=400, width=200, borderwidth=2, bg='grey')
        f_control_cmd.pack(fill=X, side=TOP)
        self.t_cmd = Text(f_control_cmd, height=10)
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
        self.lbsDeviceDst = LBS(f_to_dev, DBDict.K_DEV_DST, self.db.srcDev(), self.cbUpdateQuery)

        f_to_user = Frame(f_to, relief=RAISED, height=300, width=100, borderwidth=1, bg='blue')
        f_to_user.pack(fill=X)

        l_usr = Label(f_to_user, text="Users", width=6)
        l_usr.pack(side=TOP, padx=5, pady=5)
        Lb_usr = LBS(f_to_user, DBDict.K_USR_DST, self.db.srcUsr(), self.cbUpdateQuery)




if __name__ == '__main__':

    root = Tk()
    root.geometry("1200x800")
    
    app = Face(root)

    root.mainloop()
