from collections import OrderedDict
import json
import os
import obfuscationAlgorythm
from story import *
from copy import deepcopy

class Object(object):
    pass

class Linker():
    linkId = 0
    score = 0
    serialize = {}
    islast = 0
    level = 0
    keywords = []
    def __init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords):
        self.islast = islast
        self.score = score
        self.linkId = linkId
        self.level = level
        self.keywords = keywords
        
    def populate(self, is_good):
        if (is_good):
            a = Object()
            print(self.keywords)
            for elt in self.keywords['entities']:
                for key in elt:
                    setattr(a, key, elt[key])
            if (self.linkId == None):
                self.serialize = OrderedDict([
                    ('intent', self.keywords['intent']),
                    ('entities', a),
                    ('link', self.linkId),
                    ('score', self.score),
                  ])
            else:
                self.linkId = self.level + str(self.linkId)
                self.serialize = OrderedDict([
                    ('intent', self.keywords['intent']),
                    ('entities', a),
                    ('link', self.linkId),
                    ('score', self.score),
                  ])
        else:
            if (self.linkId == None):
                self.serialize = OrderedDict([
                    ('link', self.linkId),
                    ('score', self.score),
                  ])
            else:
                self.linkId = self.level + str(self.linkId)
                self.serialize = OrderedDict([
                    ('link', self.linkId),
                    ('score', self.score),
                  ])

class Good(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords):
        Linker.__init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords)
        self.linkId = linkId + 3
        if (islast or is_timeout):
            self.linkId = None
        self.populate(True)
        
class Bad(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords):
        Linker.__init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords)
        if is_bad:
            self.linkId = linkId + 2
        elif is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 1
        self.score = int(-score*0.5);
        self.populate(False)

class TimeOut(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords):
        Linker.__init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords)
        if is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 2
        self.score = int(-score*0.5);
        self.populate(False)
        
class Evil():
    def __init__(self, quest):
        self.quest = deepcopy(quest)
        self.parentRoot = self.quest.level
        self.quest.level = self.quest.level + '/' + 'fraud'
        self.level = self.quest.level
        self.quest.story_name = self.quest.story_name + '/' + 'fraud'

    def createFraud(self):
        self.alterateBodyContent()
        self.modifySenderEmail()
        self.quest.generateInitFile()
        story = Story([self.quest])

        return self

    def toJSON(self):
        return self.quest.toJSON()
    
    def alterateBodyContent(self):
        res = ''
        with open(os.path.join(self.parentRoot, self.quest.body), 'r') as file:
            val = file.readlines()
            val = [obfuscationAlgorythm.emailTransform(elt, 1) for elt in val]
            res += ''.join(val)
        self.quest.body = self.quest.body[:-3]+'Fraud.md'
        if not os.path.exists(self.level):
            os.makedirs(self.level)
        with open(os.path.join(self.level, self.quest.body), "w") as myfile:
            myfile.write(res)


    def modifySenderEmail(self):
        email = self.quest.sender
        email = obfuscationAlgorythm.emailTransform(email,
                                                    int(self.quest.level.split('stories/')[1][0]))
        self.quest.sender = email

        

class Quest():
    level = 0
    start_id = 0
    current_id = 0
    story_name = ""
    sender = ""
    subject = ""
    body = ""
    keywords = []
    score = 0
    is_bad = False
    is_timeout = False
    good = None
    bad = None
    timeOut = None
    content = None
    signature = ""
    islast = False
    attachement = False
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature, islast, level):
        self.level = level
        self.start_id = start_id
        self.current_id = current_id
        self.story_name = story_name
        self.sender = sender
        self.subject = subject
        self.body = body
        self.keywords = keywords
        self.score = score
        self.is_bad = is_bad
        self.is_timeout = is_timeout
        self.islast = islast
        self.content = 0
        self.signature = signature
        self.attachement = False
        
    def generateInitFile(self):
        self.evil = Evil(self)
        self.good = Good(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize
        self.bad = Bad(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize
        self.timeOut = TimeOut(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize
        self.evil.quest.good = self.good
        self.evil.quest.bad = self.bad
        self.evil.quest.timeOut = self.timeOut
        

    def timeOutBody(self):
        txt = ""
        txt += "You didn't answer me fast enought." + os.linesep
        txt += "We lost money in process." + os.linesep
        txt += "I am disappointed." + os.linesep + os.linesep
        return txt

    def setKeywords(self, keywords):
        self.keywords = keywords

        
    def toJSON(self):
        serialize = OrderedDict([
            ('name', str(self.level) + str(self.current_id)),
            ('sender', self.sender),
            ('subject', self.subject),
            ('content', self.body[:-3]),
            ('good', self.good),
            ('bad', self.bad),
            ('timeout', self.timeOut),
            ('withAttachment', self.attachement)
          ])

        return serialize
