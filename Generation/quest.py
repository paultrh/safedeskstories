from collections import OrderedDict
import json
import os

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
            if (self.linkId == None):
                self.serialize = OrderedDict([
                    ('keywords', []),
                    ('link', self.linkId),
                    ('score', self.score),
                  ])
            else:
                self.linkId = self.level + str(self.linkId)
                self.serialize = OrderedDict([
                    ('keywords', self.keywords),
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
        self.score = -score;
        self.populate(False)

class TimeOut(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords):
        Linker.__init__(self, score, linkId, is_bad, is_timeout, islast, level, keywords)
        if is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 2
        self.score = -score;
        self.populate(False)
        

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

    def generateInitFile(self):
        self.good = Good(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize
        self.bad = Bad(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize
        self.timeOut = TimeOut(self.score, self.start_id, self.is_bad, self.is_timeout, self.islast, self.level, self.keywords).serialize


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
          ])

        return serialize
