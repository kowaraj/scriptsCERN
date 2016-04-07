from tkinter import *

class LBS(Listbox):

    def __init__(self, parent, name, elements, cb, sventry=None):

        Listbox.__init__(self, parent, selectmode=MULTIPLE, selectbackground='red', exportselection=False)
        self.name = name
        self.parentCallback = cb
        self.sel = []
        self.sventry = sventry

        for i in range(len(elements)):
            self.insert(i, elements[i])
            self.bind("<<ListboxSelect>>", self.onSelect)  
            self.pack(side=TOP)



    def onSelect(self, val):
        print('onSelect of LBS called')
        sender = val.widget
        idx = sender.curselection()
        values = [sender.get(i) for i in idx]
        print('values = ', values)

        if len(values) > len(self.sel): # selected
            last = set(values).difference(self.sel).pop()
        else: # un-selected
            last = values[0] if len(values)>0 else 'nothing selected'

        print('last = ', last)
        self.sel = values
        if self.sventry:
            self.sventry.set(last) #display the last
        self.parentCallback(self.name, values, last)

