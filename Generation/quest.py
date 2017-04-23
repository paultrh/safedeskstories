from collections import OrderedDict
import json
import os

class Linker():
    linkId = 0
    score = 0
    serialize = {}
    def __init__(self, score, linkId, is_bad, is_timeout):
        self.score = score
        self.linkId = linkId
        
        
    def populate(self):
        self.serialize = OrderedDict([
            ('linkId', self.linkId),
            ('score', self.score),
          ])

class Good(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout):
        Linker.__init__(self, score, linkId, is_bad, is_timeout)
        self.linkId = linkId + 3
        self.populate()
        
class Bad(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout):
        Linker.__init__(self, score, linkId, is_bad, is_timeout)
        if is_bad:
            self.linkId = linkId + 2
        elif is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 1
        self.score = -score;
        self.populate()

class TimeOut(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout):
        Linker.__init__(self, score, linkId, is_bad, is_timeout)
        if is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 2
        self.score = -score;
        self.populate()
        

class Quest():
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
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature):
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
        if is_timeout:
            self.good = TimeOut(score, start_id, is_bad, is_timeout).serialize
        else:
            self.good = Good(score, start_id, is_bad, is_timeout).serialize
        self.bad = Bad(score, start_id, is_bad, is_timeout).serialize
        self.timeOut = TimeOut(score, start_id, is_bad, is_timeout).serialize

        self.content = 0
        self.signature = signature

    def timeOutBody(self):
        txt = ""
        txt += "You didn't answer me fast enought." + os.linesep
        txt += "We lost money in process." + os.linesep
        txt += "I am disappointed." + os.linesep + os.linesep
        return txt


    def toJSON(self):
        serialize = OrderedDict([
            ('current_id', self.current_id),
            ('story_name', self.story_name),
            ('sender', self.sender),
            ('subject', self.subject),
            ('body', self.body),
            ('keywords', tuple(self.keywords)),
            ('good', self.good),
            ('bad', self.bad),
            ('timeOut', self.timeOut),
          ])

        return serialize
