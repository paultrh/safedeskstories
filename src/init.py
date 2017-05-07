#!/usr/bin/env python3

# BASICS
import os
import copy
import random
from graphviz import Digraph
from collections import namedtuple
import json
import sys
from subprocess import check_call

# CUSTOM
from contact import *
from company import *

if not os.path.exists('filesystem'):
            os.makedirs('filesystem')

#CMD HANDLER
def generateGraphFile():
    detail = False
    node_number = 0
    dot = Digraph(comment='The story', format='png')
    for root, dirs, files in os.walk("."):
        for file in files:
            if (file == "init.json"):
                with open(os.path.join(root, file)) as data_file:
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
                    dot.node("level " + root.split("stories")[1][1:][0], "level " +  root.split("stories")[1][1:][0])
                    for quest in tmpGlobal:
                        contentInit = ""
                        contentBad = ""
                        contentTimeOut = ""
                        with open(os.path.join(root, quest[0].content) + '.md') as data_file:
                            contentInit = [x.rstrip() for x in data_file.read().splitlines()]
                        with open(os.path.join(root, quest[1].content) + '.md') as data_file:
                            contentBad = data_file.read()
                        with open(os.path.join(root, quest[2].content) + '.md') as data_file:
                            contentTimeOut = data_file.read()
                        if (detail):
                            dot.node(str(quest[0].name), ''.join(contentInit).replace("\n", ""))
                            dot.node(str(quest[1].name), ''.join(contentBad).replace("\n", ""))
                            dot.node(str(quest[2].name), ''.join(contentTimeOut).replace("\n", ""), style='filled', fillcolor='red')
                        else:
                            dot.node(str(quest[0].name), str(quest[0].name))
                            dot.node(str(quest[1].name), str(quest[1].name))
                            dot.node(str(quest[2].name), str(quest[2].name), style='filled', fillcolor='red')

                        if (quest == tmpGlobal[0]):
                            dot.edge("level " + root.split("stories")[1][1:][0], str(quest[0].name));

                        dot.edge(str(quest[0].name),str(quest[1].name), color='orange', label=str(quest[0].bad.score))
                        dot.edge(str(quest[0].name),str(quest[2].name), color='red', label=str(quest[0].timeout.score))
                        dot.edge(str(quest[1].name),str(quest[2].name), color='red', label=str(quest[0].timeout.score))
                        if (last_good != 0 and last_bad != 0):
                            dot.edge(last_good,str(quest[0].name), color='green', label=str(quest[0].good.score))
                            dot.edge(last_bad,str(quest[0].name), color='green', label=str(quest[0].good.score))
                        last_good = str(quest[0].name)
                        last_bad = str(quest[1].name)
                                
                    dot.node("END"+str(node_number), style='filled', fillcolor='green')
                    dot.edge(last_good,"END"+str(node_number), color='green')
                    dot.edge(last_bad,"END"+str(node_number), color='green')
                    node_number = node_number + 1
                    try:
                        dot.render('graph.gv', view=True)
                    except:
                        pass
                    
                    

# Generate signature for the whole story
def generateSignature():
    txt = ""
    txt += sender['firstname'] + " " + sender['lastname'] + os.linesep
    txt += sender['service'] + " service"
    return txt

# Load possible senders
with open("config/user.txt", "r") as myfile:
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
    sender = random.choice(senders)
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
generateGraphFile()