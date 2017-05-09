#!/usr/bin/env python3

import csv
import os
from csv import DictReader


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

class Entity(object):
    def __init__(self, pairs):
        for k,v in pairs:
            setattr(self,k,v)
    def __str__(self):
        txt = ''
        for k,v in self.__dict__.items():
            txt += k + '=' + v + ' '
        return txt

    # TODO no more hardcode
    def generateJSONforFile(self, name, ext):
        var = ""
        var = var + "{" + '\n'
        var = var + '  "filename": "'+os.path.basename(name)+'",' + '\n'
        var = var + '  "extension": "'+ext+'"' + '\n'
        var = var + "}"
        with open(os.path.join(name + ".json"), "w") as myfile:
            myfile.write(var)
            
    def WriteToFile(self, filename):
        pass



#### QUEST GENERATION ####        
                
class Story():
    
    def __init__():
      pass

    def questionBody(self, user):
        pass
      
    def badBody(self, user):
        pass
      
    def generateEmail(self, user):
        pass



def AnalyseDataSet(filename):
  print("------- ANALYSE "+filename+" ----------")
  with open(filename, encoding="utf8") as f:
    orders = []
    reader = DictReader(f, delimiter=',')
    for row in reader:
      if not row:
        continue
      orders.append(Entity(row.items()))
      

  attrs = []
  for k,v in orders[0].__dict__.items():
      attrs.append(k)

  print(str(len(orders)) + " objects created of " + str(len(attrs)) + " attributes")
  tmp = []
  uniqueElt = []
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
            uniqueElt.append(attrs[i])
      tmp = []

  NotuniqueElt = [x for x in attrs if x not in uniqueElt]
  print("Unique element are")
  print(uniqueElt)
  print("Non unique element are")
  print(NotuniqueElt)

for subdir, dirs, files in os.walk('inputs'):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".csv"):
            AnalyseDataSet(filepath)
        else:
          print(str(filepath) + " is ignored invalid format")

#TODO
print("------- GENERATING STORIES ----------")















