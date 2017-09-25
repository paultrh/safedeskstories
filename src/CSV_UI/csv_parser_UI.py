# tkinter csv parser contextualisation
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from subprocess import Popen, PIPE

class App:
    
    def __init__(self, master):
        ### PAGE 1 ATTR
        self.master = master
        self.master.minsize(width=666, height=666)
        self.contexts = []
        self.keywordsList = []
        self.entitylist = []
        self.entitylistAPI = ['sys.phone_number', 'sys.city', 'sys.email',  'sys.age']
        self.index = 0
        self.total = 0
        self.keywordsText = ''
        self.v = StringVar()

        self.getentities()
        self.getKeywords()
        self.onstart()


        ### PAGE 2 ATTR

        self.SPAMUser = StringVar()
        

        self.notebook = ttk.Notebook(master)
        self.notebook.pack()
        self.f1 = ttk.Frame(self.notebook)   # first page, which would get widgets gridded into it
        self.f2 = ttk.Frame(self.notebook)   # second page
        self.f3 = ttk.Frame(self.notebook)   # third page
        self.f4 = ttk.Frame(self.notebook)   # four page
        self.notebook.add(self.f1, text='Comprehension')
        self.notebook.add(self.f2, text='SPAM')
        self.notebook.add(self.f3, text='Templates')
        self.notebook.add(self.f4, text='GMAIL')


        #### PAGE 1

        
        self.frameTitle = Frame(self.f1)
        self.frameTitle.pack()
        self._title = Label(self.frameTitle, text="CSV Contextualisation")
        self._title.pack()
        
        self.frameKeywords = Frame(self.f1)
        self.frameKeywords.pack()
        self._keywords = Label(self.frameKeywords, textvariable=self.v)
        self._keywords.pack()

        self.contextKeywords = Frame(self.f1)
        self.contextKeywords.pack()
        self._context = Text(self.contextKeywords, height=10, width=60)
        if (len(self.contexts[0]) < 1):
            self._context.insert(END, 'Enter context, one by line...')
        else:
            self._context.insert(END, self.contexts[0])
        self._context.bind('<FocusIn>', self.on_entry_click)
        self._context.bind('<FocusOut>', self.on_focusout)
        self._context.config(fg = 'grey')
        self._context.pack()

        self.frameButton = Frame(self.f1)
        self.frameButton.pack()
        self._prev = Button(self.frameButton,text='Previous', command=self.onprev)
        self._prev.pack()
        self._next = Button(self.frameButton,text='Next', command=self.onnext)
        self._next.pack()

        self.frameIntents = Frame(self.f1)
        self.frameIntents.pack()
        self.frameIntentsR = Frame(self.frameIntents)
        self.frameIntentsR.pack(side=RIGHT)
        self.frameIntentsL = Frame(self.frameIntents)
        self.frameIntentsL.pack(side=LEFT)
        
        self.titleIntents = Label(self.frameIntentsR, text="Story Intents")
        self.titleIntents.pack()
        self.listbox = Listbox(self.frameIntentsR)
        self.listbox.bind('<<ListboxSelect>>', self.onselect)
        for elt in self.entitylist:
            self.listbox.insert(0, elt)
        self.listbox.pack()

        
        self.titleIntentsAPI = Label(self.frameIntentsL, text="API Intents")
        self.titleIntentsAPI.pack()
        self.listboxAPI = Listbox(self.frameIntentsL)
        self.listboxAPI.bind('<<ListboxSelect>>', self.onselectAPI)
        for elt in self.entitylistAPI:
            self.listboxAPI.insert(0, elt)
        self.listboxAPI.pack()
        
        self._save = Button(self.f1,text='Save', command=self.onsave)
        self._save.pack(side = BOTTOM)


        #### PAGE 2

        self.frameTitle2 = Frame(self.f2)
        self.frameTitle2.pack()
        self._title2 = Label(self.frameTitle, text="SPAM CONFIGURATION")
        self._title2.pack()

        self.subTitle2 = Frame(self.f2)
        self.subTitle2.pack()
        self.page2FrameRight = Frame(self.f2)
        self.page2FrameRight.pack(side=RIGHT)
        self.page2FrameLeft = Frame(self.f2)
        self.page2FrameLeft.pack(side=LEFT)

        self._titleListSpam = Label(self.page2FrameRight, text="VALID SPAMS")
        self._titleListSpam.pack()
        self.listboxSPAM = Listbox(self.page2FrameRight, width=40)
        self.listboxSPAM.pack()

        self._titleADDSpam = Button(self.page2FrameRight, bg="RED", text="DELETE", command=self.removeSPAM)
        self._titleADDSpam.pack()

        self._titleADDSpam = Label(self.page2FrameLeft, text="ADD SPAM email")
        self._titleADDSpam.pack()
        self.SPAMAddFIle = Entry(self.page2FrameLeft)
        self.SPAMAddFIle.pack()
        self.SPAMAddFIleButton = Button(self.page2FrameLeft,bg="GREEN", text="ADD", command=self.addSPAM)
        self.SPAMAddFIleButton.pack()

        self.SPAMFile()


        ### PAGE 3

        self.page3FrameRight = Frame(self.f3)
        self.page3FrameRight.pack(side=LEFT)
        self.page3FrameMiddle = Frame(self.f3)
        self.page3FrameMiddle.pack(side=LEFT)
        self.page3FrameLeft = Frame(self.f3)
        self.page3FrameLeft.pack(side=LEFT)

        self._title3Welcome = Label(self.page3FrameRight, text="Welcome phrase")
        self._title3Welcome.pack()
        self.EnAdd3Welcome = Entry(self.page3FrameRight)
        self.EnAdd3Welcome.pack()
        self.butAdd3Welcome = Button(self.page3FrameRight, bg="GREEN", text="ADD", command=self.addWelcome)
        self.butAdd3Welcome.pack()
        self.listbox3Welcome = Listbox(self.page3FrameRight)
        self.listbox3Welcome.pack()
        self.but3WelcomeDel = Button(self.page3FrameRight, bg="RED", text="DELETE", command=self.removeWelcome)
        self.but3WelcomeDel.pack()

        self._title3Rel = Label(self.page3FrameMiddle, text="Relaunch sentence")
        self._title3Rel.pack()
        self.EnAdd3Relaunch = Entry(self.page3FrameMiddle)
        self.EnAdd3Relaunch.pack()
        self.butAdd3Rel = Button(self.page3FrameMiddle, bg="GREEN", text="ADD", command=self.addRel)
        self.butAdd3Rel.pack()
        self.listbox3Relaunch = Listbox(self.page3FrameMiddle)
        self.listbox3Relaunch.pack()
        self.but3RelDel = Button(self.page3FrameMiddle, bg="RED", text="DELETE", command=self.removeRel)
        self.but3RelDel.pack()

        self._title3End = Label(self.page3FrameLeft, text="End phrase")
        self._title3End.pack()
        self.EnAdd3End = Entry(self.page3FrameLeft)
        self.EnAdd3End.pack()
        self.butAdd3End = Button(self.page3FrameLeft, bg="GREEN", text="ADD", command=self.addEnd)
        self.butAdd3End.pack()
        self.listbox3End = Listbox(self.page3FrameLeft)
        self.listbox3End.pack()
        self.but3EndDel = Button(self.page3FrameLeft, bg="RED", text="DELETE", command=self.removeDEL)
        self.but3EndDel.pack()

        self.WelcomeFile()
        self.RelaunchFile()
        self.EndFile()

        ### PAGE 4

        path = 'gmail.jpg'
        i = Image.open(path)
        i = i.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(i)
        panel = Label(self.f4, image = img)
        panel.image = img
        panel.pack(fill = "both", expand = "yes")

        self.butgmail = Button(self.f4, bg="GREEN", text="PROCESS", command=self.launchGMAIL)
        self.butgmail.pack()

        self.listbox4 = Listbox(self.f4, width=50)
        self.listbox4.pack()
        self.but4 = Button(self.f4, bg="RED", text="DELETE", command=self.removeGMAIL)
        self.but4.pack()

        self.ReadGmail()

    def ReadGmail(self):
        self.listbox4.delete(0, END)
        with open('../GOOGLE/GoogleUser.config', 'r+') as f:
            lines = f.read().splitlines()
            for elt in lines:
                self.listbox4.insert(END, str(elt))

    def removeGMAIL(self):
        lines = []
        with open('../GOOGLE/GoogleUser.config', 'r') as f:
            lines = f.readlines()
        with open('../GOOGLE/GoogleUser.config', 'w') as f:
            print(self.listbox4.get(ACTIVE))
            for line in lines:
                print(line + ' - ' +self.listbox4.get(ACTIVE))
                if '#' in line or (len(line) > 0 and self.listbox4.get(ACTIVE) not in line):
                    f.write(line)
        self.ReadGmail()
    
    def launchGMAIL(self):
        process = Popen(['python', 'google.py'], cwd='../', stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout)
        print(stderr)
        self.ReadGmail()
        
    def removeWelcome(self):
        lines = []
        with open('../config/welcomePhrase.txt', 'r') as f:
            lines = f.readlines()
        with open('../config/welcomePhrase.txt', 'w') as f:
            print(self.listbox3Welcome.get(ACTIVE))
            for line in lines:
                print(line + ' - ' +self.listbox3Welcome.get(ACTIVE))
                if '#' in line or (len(line) > 0 and self.listbox3Welcome.get(ACTIVE) not in line):
                    f.write(line)
        self.WelcomeFile()
        
    def removeRel(self):
        lines = []
        with open('../config/relaunch.txt', 'r') as f:
            lines = f.readlines()
        with open('../config/relaunch.txt', 'w') as f:
            print(self.listbox3Relaunch.get(ACTIVE))
            for line in lines:
                print(line + ' - ' +self.listbox3Relaunch.get(ACTIVE))
                if '#' in line or (len(line) > 0 and self.listbox3Relaunch.get(ACTIVE) not in line):
                    f.write(line)
        self.RelaunchFile()
    def removeDEL(self):
        lines = []
        with open('../config/EndPhrase.txt', 'r') as f:
            lines = f.readlines()
        with open('../config/EndPhrase.txt', 'w') as f:
            print(self.listbox3End.get(ACTIVE))
            for line in lines:
                print(line + ' - ' +self.listbox3End.get(ACTIVE))
                if '#' in line or (len(line) > 0 and self.listbox3End.get(ACTIVE) not in line):
                    f.write(line)
        self.EndFile()
        

    def addWelcome(self):
        with open('../config/welcomePhrase.txt', 'a') as f:
            if len(self.EnAdd3Welcome.get()) > 0:
                if (self.listbox3Welcome.size() == 0):
                    f.write(self.EnAdd3Welcome.get())
                else:
                    f.write("\n"+self.EnAdd3Welcome.get())
        self.EnAdd3Welcome.delete(0, END)
        self.WelcomeFile();
    def addRel(self):
        with open('../config/relaunch.txt', 'a') as f:
            if len(self.EnAdd3Relaunch.get()) > 0:
                if (self.listbox3Relaunch.size() == 0):
                    f.write(self.EnAdd3Relaunch.get())
                else:
                    f.write("\n"+self.EnAdd3Relaunch.get())
        self.EnAdd3Relaunch.delete(0, END)
        self.RelaunchFile();
    def addEnd(self):
        with open('../config/EndPhrase.txt', 'a') as f:
            if len(self.EnAdd3End.get()) > 0:
                if (self.listbox3End.size() == 0):
                    f.write(self.EnAdd3End.get())
                else:
                    f.write("\n"+self.EnAdd3End.get())
        self.EnAdd3End.delete(0, END)
        self.EndFile();

    def WelcomeFile(self):
        self.listbox3Welcome.delete(0, END)
        with open('../config/welcomePhrase.txt', 'r+') as f:
            lines = f.read().splitlines()
            for elt in lines:
                self.listbox3Welcome.insert(END, str(elt))
    def RelaunchFile(self):
        self.listbox3Relaunch.delete(0, END)
        with open('../config/relaunch.txt', 'r+') as f:
            lines = f.read().splitlines()
            for elt in lines:
                self.listbox3Relaunch.insert(END, str(elt))
    def EndFile(self):
        self.listbox3End.delete(0, END)
        with open('../config/EndPhrase.txt', 'r+') as f:
            lines = f.read().splitlines()
            for elt in lines:
                self.listbox3End.insert(END, str(elt))
    def SPAMFile(self):
        self.listboxSPAM.delete(0, END)
        with open('../SPAM/SpamUser.config', 'r+') as f:
            lines = f.read().splitlines()
            for elt in lines[2:]:
                self.listboxSPAM.insert(END, str(elt))


                

    def addSPAM(self):
        with open('../SPAM/SpamUser.config', 'a') as f:
            if len(self.SPAMAddFIle.get()) > 0:
                if (self.listboxSPAM.size() == 0):
                    f.write(self.SPAMAddFIle.get())
                else:
                    f.write("\n"+self.SPAMAddFIle.get())
        self.SPAMAddFIle.delete(0, END)
        self.SPAMFile();

    def removeSPAM(self):
        lines = []
        with open('../SPAM/SpamUser.config',"r") as f:
            lines = f.readlines()
        with open('../SPAM/SpamUser.config',"w") as f:
            print(self.listboxSPAM.get(ACTIVE))
            for line in lines:
                print(line + ' - ' +self.listboxSPAM.get(ACTIVE))
                if '#' in line or (len(line) > 0 and self.listboxSPAM.get(ACTIVE) not in line):
                    f.write(line)
        self.SPAMFile()
        
    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print(value)
        self._context.insert(END, '@' + value + ' ')
        
    def onselectAPI(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print(value)
        self._context.insert(END, '@' + value + ' ')
    
    def formatKey(self):
         self.keywordsText = ""
         for elt in self.keywordsList[self.index]:
             self.keywordsText += ' | ' +elt
         self.keywordsText += ' |'
         self.v.set(self.keywordsText)
            
    def getKeywords(self):
        with open('intents.txt', 'r+') as f:
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

    def getentities(self):
        with open('entity.txt', 'r+') as f:
            self.entitylist = f.read().splitlines()

top = Tk()
app = App(top)            
top.mainloop()
