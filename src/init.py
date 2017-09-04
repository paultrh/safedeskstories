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
import shutil




########################
#
# EDIT TO MODIFY COMPLEXITY
nbLevels = 5
nbSToryByLevel = 2
nbQuestByStory = 3  # DO NOT MODIFY UNLESS YOU KNOW WHAT YOU'RE DOING
#
#
########################


if not os.path.exists('filesystem'):
            os.makedirs('filesystem')

try:
    os.remove('Users.json')
except OSError:
    pass

try:
    shutil.rmtree('api')
except OSError:
    print("nope")
    pass

try:
    shutil.rmtree('out')
except OSError:
    print("nope")
    pass

#CMD HANDLER
def generateGraphFile():
    detail = False
    node_number = 0
    dot = Digraph(comment='The story', format='png')
    for root, dirs, files in os.walk("."):
        for file in files:
            if (file == "init.json" and not "SPAM" in root):
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
        self.required_score = required_score - 200


def generateLevelJSON(levels):
    if not os.path.exists('out'):
        os.makedirs('out')
    var = json.dumps(levels, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
    with open(os.path.join('out/Levels.json'), "w") as myfile:
            myfile.write(var)

def GetSpamUsers():
    with open('SPAM/SpamUser.config', "r") as myfile:
        content = myfile.readlines()
    content = [x.strip() for x in content[2:]]
    usersSPAM = []
    i = 0
    for elt in content:
        usersSPAM.append(User(elt, "SPAM"+str(i), "SPAM"+str(i), "SPAM SERVICE", "female/1.jpg", "fake"))
        i += 1
    return usersSPAM

def GetGoogleUsers():
    with open('GOOGLE/GoogleUser.config', "r") as myfile:
        content = myfile.readlines()
    content = [x.strip() for x in content]
    GoogleUser = []
    i = 0
    for elt in content:
        GoogleUser.append(User(elt, "GOOGLE"+str(i), "GOOGLE"+str(i), "Business", "female/1.jpg", random.choice(["fake", "legit"])))
        i += 1
    return GoogleUser


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
    userSPAM = GetSpamUsers()
    userGoogle = GetGoogleUsers()
    for elt in userSPAM:
        userFake.append(elt)
    for elt in userGoogle:
        userFake.append(elt)
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
#API.AI not implemented everywhere
scenario = ['contact']
contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
levels = []

allFrauds = []
for i in range(1, nbLevels):
    toplevel = "out/stories/" + str(i)
    local = random.choice(contries)
    fake = Faker(local)
    sender = random.choice(senders)
    for y in range(0, nbSToryByLevel):
        destiny = random.choice(scenario)
        level = toplevel + '/' + str(y + 1)
        quests = []
        idcount = 1
        for z in range(1, nbQuestByStory):
            print(destiny)
            isLast = False
            if (z == nbQuestByStory - 1):
                isLast = True
            if (destiny == 'contact'):
                quests += generateContact(idcount, sender['email'], 100, False, "plop", signature, fake, isLast, level, z)
            elif (destiny == 'company'):
                quests += generateCompany(idcount, sender['email'], 200, False, "plop", signature, fake, isLast, level, z)
            elif (destiny == 'csv_parser'):
                quests += generateCustom(idcount, sender['email'], 300, False, "plop", signature, fake, isLast, level, z)    
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
            
    levels.append(Level(str(i), i*200))
writeFakeUser(allFrauds)


generateLevelJSON(levels)
#generateGraphFile()

'''
print("sending data to API.IA ...")
apikey = '708e39a20a024927b6ce408d706ac0dc'
ids = ['46a2f0c6-3461-4483-93ef-d1d10e860d10', 'c2f7acb2-0036-4242-b975-79c69739dc18',
       'c9acdd6c-da5f-4ef7-b1fd-2177b9c66004', '992c9f16-44e3-48e3-8d46-ce1418ffe9f4']

def sendDataForFile(file, ids, apikey):
    with open(os.path.join('api', file), "r+", encoding='utf8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    listValues = []
    for elt in content:
        elt = elt.split(",")[0]
        eltDict = {"value" : elt, "synonyms" : [ elt, elt ]}
        listValues.append(eltDict)
    index = ["last_connection","name","phone_number","email"].index(file.split('.')[0])
    print("Uploading " + file.split('.')[0] + " ids " + ids[index])
    entriesDict = {"id" : ids[index], "name" : file.split('.')[0], "entries" : listValues}
    payload = json.dumps(entriesDict, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
    headers = {'Authorization': 'Bearer '+apikey, 'Content-Type': 'application/json'}
    r = requests.put("https://api.api.ai/v1/entities/"+ids[index], headers=headers,data=payload)
    print(r.content)
    print(r.status_code)
   
list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk('api/'):
    for filename in filenames:
        sendDataForFile(filename, ids, apikey)
'''
