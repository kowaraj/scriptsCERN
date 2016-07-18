from tkinter import *

class ColumnLB(Listbox):

    def __init__(self, parent, _name, _sm=SINGLE, _sbg='magenta', _ex=False, _width=10):
        Listbox.__init__(self, parent, selectmode=_sm, selectbackground=_sbg, exportselection=_ex, width=_width)
        self.name = _name

class SetFrame(Frame):
    '''
    '''
    def __init__(self, parent, controller, relief=RAISED, height=200, width=100, borderwidth=2, bg='brown'):

        Frame.__init__(self, parent, relief=relief, height=height, width=width, borderwidth=borderwidth, bg=bg)

        self._parent = parent
        self._controller = controller
        self._controller.addCallbackSetFrame(self)

        self._tvLabelSetVal= StringVar()
        self._labelProp = Label(self, textvariable=self._tvLabelSetVal, width=15)
        self._labelProp.pack(side=TOP, fill=X, padx=5, pady=5)

        self._tvEntrySetVal = StringVar()
        self._eSetVal = Entry(self, textvariable=self._tvEntrySetVal)
        self._eSetVal.bind("<Return>", self.__eSetVal_onEnter)
        self._eSetVal.pack(side=TOP, fill=X)

        self._tvEntrySetType = StringVar()
        self._eSetType = Entry(self, textvariable=self._tvEntrySetType)
        self._eSetType.bind("<Return>", self.__eSetType_onEnter)
        self._eSetType.pack(side=TOP, fill=X)

        Button(self, text="SET", command=self.__buttonSetData).pack(side=TOP, anchor=N)


    def __buttonSetData(self):
        print("buttonSetData: " + self._tvEntrySetVal.get())
        vtype = self._tvEntrySetType.get()
        print("buttonSetType: " + vtype)
        self._controller._setquery_setParameterValue(self._tvEntrySetVal.get())
        self._controller._setquery_setParameterType(vtype)
        self._controller._driveHardware()


    def __eSetVal_onEnter(self, e):
        val = e.widget.get()
        print('__eSetVal_onEnter: '+ str(val))
        print('__eSetVal_onEnter: '+ str(type(val)))
        self._controller._setquery_setParameterValue(val)

    def __eSetType_onEnter(self, e):
        val = e.widget.get()
        print('__eSetType_onEnter: '+ str(val))
        print('__eSetType_onEnter: '+ str(type(val)))
        self._controller._setquery_setParameterType(val)


    def setFrameCallback(self):
        self.__updateView()

    def __updateView(self):
        print('SetFrame: __updateView called')

        q = self._controller.getSetQuery()
        print('q = ' +str(q))
        self._tvLabelSetVal.set(str(q['Parameter']))
        self._tvEntrySetVal.set(str(q['Value']))
        self._tvEntrySetType.set(str(q['Type']))



class InfoFrame(Frame):
    '''
    '''
    def __init__(self, parent, controller, relief=RAISED, height=200, width=100, borderwidth=2, bg='brown'):

        Frame.__init__(self, parent, relief=relief, height=height, width=width, borderwidth=borderwidth, bg=bg)

        self._parent = parent
        self._controller = controller
        self._controller.addCallbackInfoFrame(self)

        self._tvSelDev = StringVar()
        self._eSelDev = Entry(self, textvariable=self._tvSelDev)
        self._eSelDev.bind("<Return>", self.__eSelDev_onEnter)
        self._eSelDev.pack(side=TOP, fill=X)

        self._tvSelProp = StringVar()
        self._eSelProp = Entry(self, textvariable=self._tvSelProp)
        self._eSelProp.bind("<Return>", self.__eSelProp_onEnter)
        self._eSelProp.pack(side=TOP, fill=X)

        self._tvQuery = StringVar()
        self._labelQuery = Label(self, textvariable=self._tvQuery, width=200)
        self._labelQuery.pack(side=LEFT, padx=5, pady=5)
        self.__updateView()

    def __eSelDev_onEnter(self, e):
        val = e.widget.get()
        print('__eSelDev_onEnter: '+ str(val))
        self._controller.updateQuery(self._controller.DEV, val)
        self.__updateView()

    def __eSelProp_onEnter(self, e):
        val = e.widget.get()
        print('__eSelProp_onEnter: '+ str(val))
        self._controller.updateQuery(self._controller.PROP, val)
        self.__updateView()

    def infoFrameCallback(self):
        self.__updateView()

    def __updateView(self):
        print('__updateView called')
        q = self._controller.getQuery()
        self._tvQuery.set(str(q))

        


class XFrame(Frame):
    '''
    HyperFrame contains:
    - parent: a parent Frame
    - controller: a controller
    '''

    LB_HEIGHT = 5

    def __init__(self, parent, name, controller, relief=RAISED, height=200, width=100, borderwidth=2, bg='purple', sm=SINGLE):

        Frame.__init__(self, parent, relief=relief, height=height, width=width, borderwidth=borderwidth, bg=bg)

        self._name = name
        self._parent = parent
        self._controller = controller

        print('XF name = '+self._name)
        self._sel = []


        self._label = Label(self, text=self._name, width=15)
        self._label.pack(side=TOP, padx=5, pady=5)

        self._tv = StringVar()

        self._entry = Entry(self, textvariable=self._tv)
        self._entry.bind("<Return>", self.__entry_onEnter)
        self._entry.pack(side=TOP, fill=X)

        self._sm = sm
        self._list = Listbox(self, selectmode=sm, selectbackground='red', exportselection=False, height=self.LB_HEIGHT)
        self.__list_populate()
        self._list.bind("<<ListboxSelect>>", self.__list_onSelect)
        self._list.pack(side=TOP, fill=X)

        self._button = Button(self, text="Select All", command=self.__buttonSelectAll)
        self._button.pack(side=TOP, anchor=N)

    def update(self):
        print('XFrame.update: '+self._name)
        self.__list_populate()

    def __list_populate(self):
        self._list.delete(0,END)
        d = self.__data_getData()
        print('List: '+ str(d))
        for i in range(len(d)):
            #print(str(i))
            self._list.insert(i, d[i])


    def __data_getData(self):
        d = self._controller.getData(self._name)
        return d

    def __controller_update(self, value):
        self._controller.update(self._name, value)

    def __controller_updateQuery(self, value):
        self._controller.updateQuery(self._name, value)
        



    def __list_onSelect(self, val):
        print('onSelect of LBS called, on: '+ self._name)
        sender = val.widget
        #idx = sender.curselection()
        #values = [sender.get(i) for i in idx]
        self.__list_updateSelection(sender)

    def __list_updateSelection(self, l):
        idx = l.curselection()
        values = [l.get(i) for i in idx]
        print('values = ', values)

        if len(values) > len(self._sel): # selected
            last = set(values).difference(self._sel).pop()
        else: # un-selected
            last = values[0] if len(values)>0 else 'nothing selected'
        print('last = ', last)
        
        self._sel = values


        self._tv.set(last) #display the last
        if self._sm == SINGLE:
            self.__controller_updateQuery(last)
        else:
            self.__controller_updateQuery(values)

    def __entry_onEnter(self, e):
        '''
        Add element from the list (Remove, if existed).
        '''
        val = e.widget.get()
        print('__entry_onEnter: '+self._name+' / '+val)
        self.__list_updateContent(self._name, val)


    def __list_updateContent(self, name, value):
        self.__controller_update(value)
        self._list.delete(0, END)
        self.__list_populate()


    def __buttonSelectAll(self):
        ''' 
        Button command to select all in the list (Clear all, if selected).
        '''
        if self._list.size() == len(self._list.curselection()): #if all selected
            self._list.selection_clear(0, END)
        else:
            self._list.select_set(0, END)

        self.__list_updateSelection(self._list)




