#!/usr/bin/env python

# BASICS
import os
import copy
import random
from graphviz import Digraph
from collections import namedtuple
import json
import sys

# CUSTOM
from contact import *
from company import *

def Usage():
    print("python [Folder To Generate Graph] [Output]")
    print("if no args then the script generate DATA")

#CMD HANDLER
print(len(sys.argv))
if (len(sys.argv) > 3):
    Usage()
if (len(sys.argv) > 1  and len(sys.argv) < 4):
    dot = Digraph(comment='The story')
    if not os.path.exists(sys.argv[2]):
            os.makedirs(sys.argv[2])
    with open(sys.argv[1] + '/init.json') as data_file:
        story = json.loads(data_file.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        tmpGlobal = []
        tmp = []
        count = 1
        for x in story:
            tmp.append(x)
            if (count % 3 == 0):
                tmpGlobal.append(tuple(tmp))
                tmp =  []
            count += 1

        last_good = 0
        last_bad = 0
        for quest in tmpGlobal:
            print(quest)
            contentInit = ""
            contentBad = ""
            contentTimeOut = ""
            with open(sys.argv[1] + '/' + quest[0].content + '.md') as data_file:
                contentInit = data_file.read()
            with open(sys.argv[1] + '/' + quest[1].content + '.md') as data_file:
                contentBad = data_file.read()
            with open(sys.argv[1] + '/' + quest[2].content + '.md') as data_file:
                contentTimeOut = data_file.read()
            dot.node(str(quest[0].name), contentInit.replace('\n', "\\n"))
            dot.node(str(quest[1].name), contentBad.replace('\n', "\\n"))
            dot.node(str(quest[2].name), contentTimeOut.replace('\n', "\\n"), style='filled', fillcolor='red')

                
            dot.edge(str(quest[0].name),str(quest[1].name), color='orange')
            dot.edge(str(quest[0].name),str(quest[2].name), color='red')
            dot.edge(str(quest[1].name),str(quest[2].name), color='red')
            if (last_good != 0 and last_bad != 0):
                dot.edge(last_good,str(quest[0].name), color='green')
                dot.edge(last_bad,str(quest[0].name), color='green')
            last_good = str(quest[0].name)
            last_bad = str(quest[1].name)
                
        dot.node("END", style='filled', fillcolor='green')
        dot.edge(last_good,"END", color='green')
        dot.edge(last_bad,"END", color='green')
        try:
            dot.render(sys.argv[2] + '/graph.gv', view=True)
        except:
            print("no dot render found go to http://www.webgraphviz.com/")
            
    exit()
    
    

# Generate signature for the whole story
def generateSignature():
    txt = ""
    txt += sender['firstname'] + " " + sender['lastname'] + os.linesep
    txt += sender['service'] + " service"
    return txt

# Load possible senders
with open("user.txt", "r") as myfile:
    content = myfile.read()
    senders = json.loads(content)

sender = random.choice(senders)
signature = generateSignature()


class Level:
    name = ""
    required_score = 0
    def __init__(self, name, required_score):
        self.name = name
        self.required_score = required_score

class Story():
    quests = []
    def __init__(self, quests):
        self.quests = quests

    def toJSON(self):
        serialize = list((o.toJSON() for o in self.quests))

        return json.dumps(serialize, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

    #DUMB TEST
    def ShowGraph(self):
        tmpGlobal = []
        tmp = []
        count = 1
        for i in self.quests:
            tmp.append(i)
            if (count % 3 == 0):
                tmpGlobal.append(tuple(tmp))
                tmp =  []
            count += 1

        last_good = 0
        last_bad = 0
        dot = Digraph(comment='The story')
        for quest in tmpGlobal:
            dot.node(str(quest[0].current_id), quest[0].content.replace(os.linesep, "\\n"))
            dot.node(str(quest[1].current_id), quest[1].content.replace(os.linesep, "\\n"))
            dot.node(str(quest[2].current_id), quest[2].content.replace(os.linesep, "\\n"), style='filled', fillcolor='red')

            
            dot.edge(str(quest[0].current_id),str(quest[1].current_id), color='orange')
            dot.edge(str(quest[0].current_id),str(quest[2].current_id), color='red')
            dot.edge(str(quest[1].current_id),str(quest[2].current_id), color='red')
            if (last_good != 0 and last_bad != 0):
                dot.edge(last_good,str(quest[0].current_id), color='green')
                dot.edge(last_bad,str(quest[0].current_id), color='green')
            last_good = str(quest[0].current_id)
            last_bad = str(quest[1].current_id)
            
        dot.node("END", style='filled', fillcolor='green')
        dot.edge(last_good,"END", color='green')
        dot.edge(last_bad,"END", color='green')
        try:
            dot.render('graph.gv', view=True)
        except:
            print("no dot render found go to http://www.webgraphviz.com/")
        
def generateLevelJSON(levels):
    var = json.dumps(levels, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
    with open(os.path.join('out/Levels.json'), "w") as myfile:
            myfile.write(var)
        
idCount = 1
total_points = 100
nb_iteration = 5                                                                                                   

rootdir = os.getcwd()
sub_folders = []

for subdir, dirs, files in os.walk(rootdir):
    for folder in dirs:
        sub_folders.append(folder)

points_credit = []
for i in range(0, nb_iteration):
    points_credit.append(total_points / nb_iteration)

scenario = ['contact', 'company']
contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
levels = []
        
for i in range(1, 3):
    toplevel = "out/stories/" + str(i)
    local = random.choice(contries)
    fake = Faker(local)
    for y in range(0, 3):
        level = toplevel + '/' + str(y + 1)
        quests = []
        idcount = 1
        maxi = 4
        for z in range(1, maxi):
            destiny = random.choice(scenario)
            isLast = False
            if (z == maxi - 1):
                isLast = True
            if (destiny == 'contact'):
                quests += generateContact(idcount, sender['email'], 100, False, "plop", signature, fake, isLast, level)
            elif (destiny == 'company'):
                quests += generateCompany(idcount, sender['email'], 100, False, "plop", signature, fake, isLast, level)
            idcount += 3

        story = Story(quests)

        
        if not os.path.exists(level):
            os.makedirs(level)
        with open(os.path.join(level, 'init.json'), "w") as myfile:
            myfile.write(story.toJSON())
    levels.append(Level(str(i), i*10))


generateLevelJSON(levels)
