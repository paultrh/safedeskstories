#!/usr/bin/env python3

import os
import random

if not os.path.exists('relaunch'):
        os.makedirs('relaunch')

body = []
with open("config/relaunch.txt", "r") as myfile:
        tmp = myfile.read()
        res = tmp.split('-')
        for elt in res:
                if elt[0] == '\n':
                        elt = elt[1:]
                body.append(elt)
        
def signature():
        txt = ''
        txt += '{{ signature }}'
        return txt
        
def generateEmail(index):
        txt = ""
        with open("config/welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep

        txt += body[i] + os.linesep + os.linesep
        
        with open("config/EndPhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep

        txt += signature()
        
        with open(os.path.join('relaunch/'+str(index) +'.md'), "w+") as myfile:
            myfile.write(txt)

for i in range(0, len(body)):
        generateEmail(i)
