import os
import json
from quest import Quest
from faker import Faker
import json
from collections import OrderedDict
import random
import requests


functions = ['Employee', 'Manager', 'Engineer', 'Intern', 'Sales person', 'Technician', 'Consultant']

story_type = 'Attachement'
init_subject = ['Weekly Intern investigation', 'Irregularities found in departement', 'Closing weekly intern revue']
bad_subject = 'Wrong information'
timeout_subject = 'Investigation failed'

#### DOCUMENT GENERATION ####

class Document():
    name = ""
    
    def __init__(self, name):
        self.name = name

#### QUEST GENERATION ####        
                
class Attachement(Quest):
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                 isLast, level):
        Quest.__init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                       isLast, level)
        self.attachement = True;


    def questionBody(self, document):
        lUnary = {'':''}
        lNotUnary = {'document-document' : 'document'}
        
        txt = ""
        txt += "I am looking for the "
        res = random.choice(list(lNotUnary.items()))
        txt += res[0].split("-")[1]
        self.keywords['entities'].append({ str(res[0].split("-")[0]) : res[1]})
        txt += " where i could find information about "
        tmp = random.choice(list(lUnary.items()))
        txt += document.name.split('.')[0] +'.'+ os.linesep
        txt += "I really need this document as soon as possible." + os.linesep
        return txt;

    def badBody(self):
        txt = ""
        txt += "The document you provided me were wrong." + os.linesep
        txt += "Please resend me the correct file as soon as possible." + os.linesep
        txt += "For a reminder, my previous request." + os.linesep
        
        txt += '>' + self.content.replace(os.linesep, os.linesep + '>')
        return txt

    

    def generateEmail(self, document):
        txt = ""
        with open("config/welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
            
        if (self.body[:3] == 'ini'):
            txt += self.questionBody(document) + os.linesep + os.linesep
        elif (self.body[:3] == 'bad'):
            txt += self.badBody() + os.linesep + os.linesep
        else:
            txt += self.timeOutBody() + os.linesep + os.linesep
        
        with open("config/EndPhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
        txt += self.signature + os.linesep
        if not os.path.exists(self.level):
            os.makedirs(self.level)
        self.content = txt
        with open(os.path.join(self.level, self.body), "w") as myfile:
            myfile.write(txt)
        return txt

# NOTE : Should refactor but may divert from one quest to another
def generateAttachement(start_id, sender, score, is_last, story_name, signature, fake,
                    isLast, level, z):
    companyName = 'secuGov'
    IntentName = 'FindDocumentInfo'
    # Get Doc names
    docLists = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if (".md" in file and "inputs" in root):
                docLists.append(file)
    print(docLists)

    # Create Specific Content
    
    questList = []
    init = Attachement(start_id, start_id, story_name, sender, init_subject[z],
            "init" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                   score, False, False, signature, isLast, level)
    init.generateEmail(Document(docLists[0]))
    bad = Attachement(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                  score, True, False, signature, isLast, level)
    bad.content = init.content
    bad.setKeywords(init.keywords)
    timeOut = Attachement(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                      score, False, True, signature, isLast, level)
    questList.append(init)
    questList.append(bad)
    questList.append(timeOut)

    bad.generateEmail(Document(docLists[1]))
    timeOut.generateEmail(Document(docLists[2]))

    init.generateInitFile()
    bad.generateInitFile()
    timeOut.generateInitFile()

    fraudList = []
    fraudList.append(init.evil.createFraud())
    fraudList.append(bad.evil.createFraud())
    fraudList.append(timeOut.evil.createFraud())

    return questList, fraudList
