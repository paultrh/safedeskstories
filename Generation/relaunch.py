#!/usr/bin/env python3

import os
import random

if not os.path.exists('relaunch'):
        os.makedirs('relaunch')

body = []
with open("relaunch.txt", "r") as myfile:
        body = myfile.read()
        body = body.split('-')


def signature():
        txt = ''
        txt += '{{ signature }}'
        return txt
        
def generateEmail(index):
        txt = ""
        with open("welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep

        txt += body[i] + os.linesep + os.linesep
        
        with open("EndPhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep

        txt += signature()
        
        with open(os.path.join('relaunch/'+str(index) +'.md'), "w+") as myfile:
            myfile.write(txt)

for i in range(0, len(body)):
        generateEmail(i)
