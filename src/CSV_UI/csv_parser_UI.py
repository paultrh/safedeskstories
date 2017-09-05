# tkinter csv parser contextualisation
from tkinter import *

class App:
    
    def __init__(self, master):
        self.master = master
        self.contexts = []
        self.keywordsList = []
        self.index = 0
        self.total = 0
        self.keywordsText = ''
        self.v = StringVar()
        
        self.getKeywords()
        self.onstart();
        
        self.frameTitle = Frame(master)
        self.frameTitle.grid(row=0,column=0)
        self._title = Label(self.frameTitle, text="CSV Contextualisation")
        self._title.grid(row=0,column=0)
        
        self.frameKeywords = Frame(master)
        self.frameKeywords.grid(row=1,column=0)
        self._keywords = Label(self.frameKeywords, textvariable=self.v)
        self._keywords.grid(row=1,column=0)

        self.contextKeywords = Frame(master)
        self.contextKeywords.grid(row=2,column=0)
        self._context = Text(self.contextKeywords, height=2, width=30)
        if (len(self.contexts[0]) < 1):
            self._context.insert(END, 'Enter context, one by line...')
        else:
            self._context.insert(END, self.contexts[0])
        self._context.bind('<FocusIn>', self.on_entry_click)
        self._context.bind('<FocusOut>', self.on_focusout)
        self._context.config(fg = 'grey')
        self._context.grid(row=2,column=0)

        self.frameButton = Frame(master)
        self.frameButton.grid(row=3,column=0)
        self._prev = Button(self.frameButton,text='Previous', command=self.onprev)
        self._prev.grid(row=3,column=1)
        self._next = Button(self.frameButton,text='Next', command=self.onnext)
        self._next.grid(row=3,column=2)

        self.frameSave = Frame(master)
        self.frameSave.grid(row=4,column=0)
        self._save = Button(self.frameSave,text='Save', command=self.onsave)
        self._save.grid(row=4,column=1)

    def formatKey(self):
         self.keywordsText = ""
         for elt in self.keywordsList[self.index]:
             self.keywordsText += ' | ' +elt
         self.keywordsText += ' |'
         self.v.set(self.keywordsText)
            
    def getKeywords(self):
        with open('keywords.txt', 'r+') as f:
            lines = f.read().splitlines()
            self.keywordsList = []
            tmp = []
            print(lines)
            for elt in lines:
                if (elt == '#'):
                    self.keywordsList.append(tmp)
                    tmp = []
                else:
                    tmp.append(elt)
            self.keywordsList.append(tmp)
            self.total = len(self.keywordsList)
            for i in range(0, self.total + 1):
                self.contexts.append('')
            self.formatKey()
                    
    def on_entry_click(self, event):
        if 'Enter context' in self._context.get('1.0', END):
           self._context.delete('1.0', END) # delete all the text in the entry
           self._context.insert('1.0', '') #Insert blank for user input
           self._context.config(fg = 'black')

    def on_focusout(self, event):
        if self._context.get("1.0", END) == '':
            self._context.insert(END, 'Enter context, one by line...')
            self._context.config(fg = 'grey')

    def onnext(self):
        self.savetmp()
        if (self.index < len(self.keywordsList) - 1):
            self.index += 1
            self.formatKey()
            self._context.delete('1.0', END) # delete all the text in the entry
            self._context.insert('1.0', '') #Insert blank for user input
            self._context.insert(END, self.contexts[self.index])
        
    def onprev(self):
        self.savetmp()
        if (self.index > 0):
            self.index -= 1
            self.formatKey()
            self._context.delete('1.0', END) # delete all the text in the entry
            self._context.insert('1.0', '') #Insert blank for user input
            self._context.insert(END, self.contexts[self.index])

    def savetmp(self):
        data = self._context.get('1.0', END)
        if ('Enter context' not in self._context.get('1.0', END)):
            self.contexts[self.index] = data
            
    def onstart(self):
        with open('context.txt', 'r+') as f:
            lines = f.read().splitlines()
        c = -1
        for elt in lines:
            if (elt != ''):
                if (elt == '###########'):
                    print('new index')
                    c += 1
                else:
                    print('insert val')
                    self.contexts[c] += elt + '\n'
        print('context infered')
        print(self.contexts)
    
    def onsave(self):
        data = ''
        for elt in self.contexts:
            data += '\n###########\n'
            if (elt != ''):
                tmp = elt.split('\n')
                tmp = [x for x in tmp if x != '']
                data += '\n'.join(tmp)
        print(data)
        with open('context.txt', 'w+') as f:
            f.write(data)
        print('Saved')

top = Tk()
app = App(top)            
top.mainloop()
