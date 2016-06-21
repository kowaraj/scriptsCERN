
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

        frameW = Frame(self, relief=RAISED, height=600, width=300, borderwidth=2, bg='green')
        frameW.pack(fill=BOTH, side=LEFT)
        frame_class = XFrame(frameW, Settings.CLA, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='spring green', sm=SINGLE)
        frame_class.pack(fill=BOTH, side=TOP)
        frame_devs = XFrame(frameW, Settings.DEV, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='red', sm=SINGLE)
        frame_devs.pack(fill=BOTH, side=TOP)
        frame_usrs = XFrame(frameW, Settings.USR, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='blue', sm=MULTIPLE)
        frame_usrs.pack(fill=BOTH, side=TOP)
        frame_props = XFrame(frameW, Settings.PROP, self.controller, relief=RAISED, height=600, width=300, borderwidth=2, bg='purple', sm=SINGLE)
        frame_props.pack(fill=BOTH, side=TOP)

        Button(frameW, text="GET",command=self.__buttonAcquireData).pack(side=LEFT, anchor=N)
        
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

    def __updateDataFrame(self):

        dev = self.controller._query_getDevice()
        prop = self.controller._query_getProperty()

        #acqData = self.controller.getAcqDataByUsers()

        # First Listbox for User names

        for ld in self.listDict:
            self.listDict[ld].pack_forget()
        self.listDict.clear()


        listUsers = Listbox(self.frameData, selectmode=SINGLE, selectbackground='gray', exportselection=False, width=10)
        listUsers.pack(side=LEFT, fill=Y)
        self.listDict['users'] = listUsers
        uIDs = self.controller._acqdata_getUserIDs(dev)
        listUsers.insert(0, 'USER')
        for uID in uIDs:
            listUsers.insert(uID, self.controller._data_getUserByID(uID))


        # All the other Listboxes for parameters

        for pa in self.controller._acqdata_getParameterNames(dev, prop):
            listPa = Listbox(self.frameData, selectmode=SINGLE, selectbackground='magenta', exportselection=False, width=10)
            listPa.pack(side=LEFT, fill=Y)
            self.listDict[pa] = listPa
            
            listPa.insert(0, pa)
            for uID in uIDs:
                user = Controller._data_getUserByID(uID)
                listPa.insert(uID, self.controller._acqdata_getParameterValue(dev, user, prop, pa))
                #self._list.bind("<<ListboxSelect>>", self.__list_onSelect)



            

