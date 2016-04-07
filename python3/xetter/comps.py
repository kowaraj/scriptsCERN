from tkinter import *

class LBS(Listbox):

    def __init__(self, parent, name, elements, cb, sventry=None):

        Listbox.__init__(self, parent, selectmode=MULTIPLE, selectbackground='red')
        self.name = name
        self.parentCallback = cb
        self.sel = []
        self.selLast = ''
        self.sventry = sventry
        for i in range(len(elements)):
            self.insert(i, elements[i])
            self.bind("<<ListboxSelect>>", self.onSelect)  
            self.pack(side=TOP)



    def onSelect(self, val):
        print('onSelect of LBS called')
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.selLast = value

        if self.sventry:
            self.sventry.set(value) #display last selected in entry

        if value in self.sel:
            self.sel.remove(value)
        else:
            self.sel.append(value)

        print('onSelect of LBS: calling cb(val)')

        self.parentCallback(self.name, self.sel, value)

