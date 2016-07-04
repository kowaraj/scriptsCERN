
import tkinter
from tkinter import *
from tkinter import messagebox

from comps import *

from dbdict import DBDict
from controller import Controller
from controller import Settings

class Face(Frame):


    def __init__(self, parent):
        print('face')
        Frame.__init__(self, parent)
        self.parent = parent

        self.controller = Controller()
        self.db = DBDict()

        self.__initUI()
        print('face done')


    def __initUI(self):

        self.parent.title("LTIM Reader")
        self.pack(fill=BOTH, expand=True)

        # West panel

        frameW = Frame(self, relief=RAISED, height=600, width=300, borderwidth=2, bg='gray')
        frameW.pack(fill=BOTH, side=LEFT)
        frame_class = XFrame(frameW, Settings.CLA, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='gray', sm=SINGLE)
        frame_class.pack(fill=BOTH, side=TOP)
        frame_devs = XFrame(frameW, Settings.DEV, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='gray', sm=MULTIPLE)
        frame_devs.pack(fill=BOTH, side=TOP)
        frame_usrs = XFrame(frameW, Settings.USR, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='gray', sm=MULTIPLE)
        frame_usrs.pack(fill=BOTH, side=TOP)
        frame_props = XFrame(frameW, Settings.PROP, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='gray', sm=SINGLE)
        frame_props.pack(fill=BOTH, side=TOP)

        Button(frameW, text="GET",command=self.__buttonAcquireData).pack(side=TOP, anchor=N)
        
        frameS = SetFrame(frameW, self.controller, relief=RAISED, height=600, width=300, borderwidth=5, bg='pink')
        frameS.pack(fill=BOTH, side=TOP)

        # North panel

        frameN = InfoFrame(self, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='brown')
        frameN.pack(fill=BOTH, side=TOP)
        
        # Center panel

        self.frameData = Frame(self, relief=RAISED, height=600, width=300, borderwidth=2, bg='Yellow')
        self.frameData.pack(fill=BOTH, side=LEFT)

        self.listDict = {}
        self.__updateDataFrame()

    def __buttonAcquireData(self):
        self.controller.acquireData()
        self.__updateDataFrame()

    def __list_lb00_onSelect(self, val):
        print('lb00 onSelect of LBS called, on: '+ self._name)
        #print('dir = '+str(dir(val)))
        sender = val.widget
        #print('dir = '+str(dir(sender)))

        idx = sender.curselection()
        values = [sender.get(i) for i in idx]
        print('values = ', values)

    def __list_lb0_onSelect(self, val):
        print('lb0 onSelect of LBS called, on: '+ self._name)
        sender = val.widget
        idx = sender.curselection()
        values = [sender.get(i) for i in idx]
        print('values = ', values)


    def __list_lb_i_onSelect(self, val):
        print('lb_i onSelect of LBS called, on: '+ self._name)
        sender = val.widget
        print('name = ', sender.name)

        idx = sender.curselection()
        values = [sender.get(i) for i in idx]
        print('values = ', values)
        self.controller._setquery_setParameter(sender.name, values[0])


    def __updateDataFrame(self):

        devs = self.controller._query_getDevices()
        prop = self.controller._query_getProperty()

        # Clean-up the previous data

        for ld in self.listDict:
            self.listDict[ld].pack_forget()
        self.listDict.clear()


        # Populate the frame with Listboxes:

        # First ListBox for the names of Device
        lb0 = Listbox(self.frameData, selectmode=SINGLE, selectbackground='gray', exportselection=False, width=10)
        lb0.bind("<<ListboxSelect>>", self.__list_lb0_onSelect)
        lb0.pack(side=LEFT, fill=Y)
        self.listDict['LB0'] = lb0

        # Second ListBox for the names of User
        lb00 = Listbox(self.frameData, selectmode=SINGLE, selectbackground='gray', exportselection=False, width=7)
        lb00.bind("<<ListboxSelect>>", self.__list_lb00_onSelect)
        lb00.pack(side=LEFT, fill=Y)
        self.listDict['LB00'] = lb00
        
        # All the other Listboxes for parameters
        dev_0 = devs[0]
        print('dev_0 = '+str(dev_0))
        params = self.controller._acqdata_getParameterNames(dev_0, prop)
        for param in params:
            lb_i = ColumnLB(self.frameData, param, _sm=SINGLE, _sbg='magenta', _ex=False, _width=10)
            lb_i.bind("<<ListboxSelect>>", self.__list_lb_i_onSelect)
            lb_i.pack(side=LEFT, fill=Y)
            self.listDict[param] = lb_i
            


        # Populate the LisBoxes with the data

        header_do_reprint = False
        header_print = True

        pos_i = 0
        for dev in devs:

            if header_print:
                # param names
                for param in self.listDict.keys():
                    lb = self.listDict[param]
                    if param == 'LB0':
                        lb.insert(pos_i, '----------')
                    else:
                        lb.insert(pos_i, param)
                pos_i +=1
                if not header_do_reprint:
                    header_print = False

            # device name in lb0
            for param in self.listDict.keys():
                lb = self.listDict[param]
                if param == 'LB0':
                    lb.insert(pos_i, dev)
                else:
                    lb.insert(pos_i, '----------')
            pos_i +=1



            # user-name / property data
            uIDs = self.controller._acqdata_getUserIDs(dev)
            for uID in uIDs:
                user = self.controller._data_getUserByID(uID)

                # # user name in lb00
                # for param in self.listDict.keys():
                #     lb = self.listDict[param]
                #     if param == 'LB00':
                #         lb.insert(pos_i, user)
                #     else:
                #         lb.insert(pos_i, ' ')
                # pos_i +=1

                # user name in lb0 / param value in the rest
                for param in self.listDict.keys():
                    lb = self.listDict[param]
                    if param == 'LB0':
                        lb.insert(pos_i, ' ')
                    elif param == 'LB00': 
                        lb.insert(pos_i, user)
                    else:
                        param_val = self.controller._acqdata_getParameterValue(dev, user, prop, param)
                        lb.insert(pos_i, param_val)
                pos_i +=1



            

