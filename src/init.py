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
from csv_parser import *
from story import *
from quest import *



########################
#
# EDIT TO MODIFY COMPLEXITY
nbLevels = 5
nbSToryByLevel = 2
nbQuestByStory = 3
#
#
########################


if not os.path.exists('filesystem'):
            os.makedirs('filesystem')

try:
    os.remove('Users.json')
except OSError:
    pass

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
                            dot.node(str(quest[0].name), ''.join(contentInit).replace("\n", "\\n"))
                            dot.node(str(quest[1].name), ''.join(contentBad).replace("\n", "\\n"))
                            dot.node(str(quest[2].name), ''.join(contentTimeOut).replace("\n", "\\n"), style='filled', fillcolor='red')
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
with open("config/user.json", "r") as myfile:
    content = myfile.read()
    senders = json.loads(content)

def getSenders():
    content = ''
    with open("config/user.json", "r") as myfile:
        content = myfile.read()
    senders = json.loads(content)
    return senders
    

sender = random.choice(senders)
signature = generateSignature()

class User:
    def __init__(self, email, firstname = "Audrey2", lastname = "austin2", service = "business2", avatar = "female/1.jpg", typeU = "fake"):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.service = service
        self.avatar = avatar
        self.type = typeU


    def toJSON(self):
        serialize = OrderedDict([
            ('firstname', self.firstname),
            ('lastname', self.lastname),
            ('email', self.email),
            ('service', self.service),
            ('avatar', self.avatar),
            ('type', self.type),
          ])

        return serialize

        
class Users:
    users = []

    def __init__(self, users):
        self.users = users
        
    def toJSON(self):
        serialize = list((o.toJSON() for o in self.users))

        return json.dumps(serialize, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
    

class Level:
    name = ""
    required_score = 0
    def __init__(self, name, required_score):
        self.name = name
        self.required_score = required_score


def generateLevelJSON(levels):
    if not os.path.exists('out'):
        os.makedirs('out')
    var = json.dumps(levels, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
    with open(os.path.join('out/Levels.json'), "w") as myfile:
            myfile.write(var)

def writeFakeUser(fraudQuests):
    baseList = getSenders()
    baseEmail = [elt['email'] for elt in baseList] 
    usersFakeL = [elt.quest.sender for elt in fraudQuests if elt not in baseEmail]
    usersFakeL = list(set(usersFakeL))
    userFake = [User(elt) for elt in usersFakeL]

    # LOAD LEGIT USER
    with open('config/user.json') as data_file:    
        data = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for elt in data:
        userFake.append(User(elt.email, elt.firstname, elt.lastname, elt.service, elt.avatar, elt.type))
    usersObj = Users(userFake)
    with open(os.path.join('Users.json'), "a+") as myfile:
            myfile.write(usersObj.toJSON())

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

scenario = ['contact', 'company', 'csv_parser']
contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
levels = []

for i in range(1, nbLevels):
    toplevel = "out/stories/" + str(i)
    local = random.choice(contries)
    fake = Faker(local)
    sender = random.choice(senders)
    allFrauds = []
    for y in range(0, nbSToryByLevel):
        level = toplevel + '/' + str(y + 1)
        quests = []
        idcount = 1
        for z in range(1, nbQuestByStory):
            destiny = random.choice(scenario)
            print(destiny)
            isLast = False
            if (z == nbQuestByStory - 1):
                isLast = True
            if (destiny == 'contact'):
                quests += generateContact(idcount, sender['email'], 100, False, "plop", signature, fake, isLast, level)
            elif (destiny == 'company'):
                quests += generateCompany(idcount, sender['email'], 200, False, "plop", signature, fake, isLast, level)
            elif (destiny == 'csv_parser'):
                quests += generateCustom(idcount, sender['email'], 300, False, "plop", signature, fake, isLast, level)    
            idcount += 3
            print(' Completed')

        Legit = [elt for elt in quests if not isinstance(elt[0], Evil)]
        flattenedLegit = [val for sublist in Legit for val in sublist]
        notLegit = [elt for elt in quests if isinstance(elt[0], Evil)]
        flattenednotLegit = [val for sublist in notLegit for val in sublist]
        story = Story(flattenedLegit)
        frauds = Story(flattenednotLegit)
        allFrauds += flattenednotLegit
        
        if not os.path.exists(level):
            os.makedirs(level)
        with open(os.path.join(level, 'init.json'), "w") as myfile:
            myfile.write(story.toJSON())
        with open(os.path.join(os.path.join(level, 'fraud'), 'init.json'), "w") as myfile:
            myfile.write(frauds.toJSON())
            
    writeFakeUser(allFrauds)
    levels.append(Level(str(i), i*10))


generateLevelJSON(levels)
generateGraphFile()
