#!/usr/bin/env python3

import csv
import os
from csv import DictReader
from quest import Quest
import random
import wikipediaScrap
import bingScrap

def sanityzeData(data):
  data = data.replace('_', ' ')
  return data.capitalize()

def sanityzeBytes(data):
  data = data.replace('b', ' ')
  return data

def isUnique(myList, show):
  mySet = set()
  for x in myList:
    if (show):
      print('-'+x+'-')
    if not x:
      continue
    if x in mySet:
        if (show):
          print("is a doublon ->"+x+"|") #Expose doublons if in debug configuration
          print(len(x))
        return False
    mySet.add(x)
  return True


#### DOCUMENT GENERATION ####

class EntitiyManager():

  def __init__(self, listEntity, uniqueList, nonUniqueList, description):
        self.listEntity = listEntity
        self.uniqueList = uniqueList
        self.nonUniqueList = nonUniqueList
        self.description = description

  def WriteToFile(self, filename, items, file):
      content = ''
      content += '## ' + sanityzeData(file.split('.')[0]) + os.linesep + os.linesep
      content += '### Context description' + os.linesep + os.linesep
      content += wikipediaScrap.getDescription(sanityzeData(file.split('.')[0]) , 3) +os.linesep + os.linesep
      content += '### Image Representation' + os.linesep + os.linesep
      content += bingScrap.getImages(sanityzeData(file.split('.')[0]))
      content += '### Data' + os.linesep + os.linesep
      content += '| '
      for elt in items:
         content += sanityzeData(elt[0]) + ' | '
      content += os.linesep + '| '
      for elt in items:
         content += '------ | '
      content += os.linesep + '| '
      for obj in self.listEntity:
        for elt in obj.__dict__.items():
          content += sanityzeBytes(str(elt[1])) + ' | '
        content += os.linesep + '| '
      with open(filename.split('.')[0] + '.md', "wb") as myfile:
            myfile.write(content.encode('utf8'))
  

class Entity(object):
    def __init__(self, pairs):
        for k,v in pairs:
            setattr(self,k,v)
    def __str__(self):
        txt = ''
        for k,v in self.__dict__.items():
            txt += k + '=' + v + ' '
        return txt

#### QUEST GENERATION ####        
                
class Custom(Quest):
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                 isLast, level, entityManager):
        Quest.__init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                       isLast, level)
        self.entityManager = entityManager


    def questionBody(self):
        lUnary = self.entityManager.uniqueList
        lNotUnary = self.entityManager.nonUniqueList
        txt = ""
        txt += "I am looking for the "
        find = random.choice(lUnary)
        res = random.choice(lNotUnary+lUnary)
        while res == find:
          res = random.choice(lNotUnary+lUnary)
        txt += sanityzeData(res[0])
        self.keywords.append(sanityzeData(res[1]))
        txt += " of a specific "+sanityzeData(self.entityManager.description)[:-4]+" whose "
        tmp = find
        txt += sanityzeData(tmp[0]) + " is " + sanityzeData(tmp[1]) + os.linesep
        txt += "I really need this information as soon as possible." + os.linesep
        return txt;

    def badBody(self):
        txt = ""
        txt += "The information you provided me were wrong." + os.linesep
        txt += "Please resend me as soon as possible the correct info." + os.linesep
        txt += "Here my previous request." + os.linesep
        
        txt += '>' + self.content.replace(os.linesep, os.linesep + '>')
        return txt


    def generateEmail(self):
        txt = ""
        with open("config/welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
            
        if (self.body[:3] == 'ini'):
            txt += self.questionBody() + os.linesep + os.linesep
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

def AnalyseDataSet(filename, file):
  with open(filename, encoding="utf8") as f:
    orders = []
    reader = DictReader(f, delimiter=',')
    for row in reader:
      if not row:
        continue
      elt = Entity(row.items())
      orders.append(elt)

  attrs = []
  for k,v in orders[0].__dict__.items():
      attrs.append(k)

  tmp = []
  uniqueElt = []
  NotUniqueElt = []
  for i in range(0, len(attrs)):
      for elt in orders:
          val = [o[1] for o in elt.__dict__.items() if o[0] == attrs[i]]
          if not val:
            continue
          if (val != None and val != " " and val != '' and len(val) != 0 and val):
            tmp.append(''.join(val))
      if (attrs[i] == "custom column name"):   #Use for debug
        if (isUnique(tmp, True)):
            uniqueElt.append(attrs[i])
      else:
        if (isUnique(tmp, False)):
            uniqueElt.append((attrs[i], ''.join(val)))
        else:
          NotUniqueElt.append((attrs[i], ''.join(val)))
      tmp = []
      
  if len(uniqueElt) < 1:
    return None
  
  manager = EntitiyManager(orders,  uniqueElt, NotUniqueElt, file)
  manager.WriteToFile(filename, orders[0].__dict__.items(), sanityzeData(file))
  return manager


# NOTE : Should refactor but may divert from one quest to another
def generateCustom(start_id, sender, score, is_last, story_name, signature, fake,
                    isLast, level):
    companyName = 'secuGov'
    story_type = "Custom"
    init_subject = 'Starting partnership'
    bad_subject = 'Wrong information'
    timeout_subject = 'Customer went to concurrency'

    potentialStories = []
    for subdir, dirs, files in os.walk('inputs'):
      for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".csv"):
          potentialStories.append((filepath, file))


      val = random.choice(potentialStories)
      manager = AnalyseDataSet(val[0], val[1])
      if not manager:
        continue
      print(' -> '+ val[0] +' -> ', end='')
      # Create Specific Content
      questList = []
      init = Custom(start_id, start_id, story_name, sender, init_subject,
                    "init" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", [],
                           score, False, False, signature, isLast, level, manager)
      bad = Custom(start_id, start_id + 1, story_name, sender, bad_subject,
                    "bad" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", [],
                          score, True, False, signature, isLast, level, manager)
      init.generateEmail()
      bad.content = init.content
      bad.setKeywords(init.keywords)
      timeOut = Custom(start_id, start_id + 2, story_name, sender, timeout_subject,
                    "timeOut" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", [],
                              score, False, True, signature, isLast, level, manager)
      questList.append(init)
      questList.append(bad)
      questList.append(timeOut)

      bad.generateEmail()
      timeOut.generateEmail()

      init.generateInitFile()
      bad.generateInitFile()
      timeOut.generateInitFile()

    return questList












