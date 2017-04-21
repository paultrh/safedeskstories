import os
import faker
import json
from collections import OrderedDict

story_type = 'Contact'

init_subject = 'Starting partnership'
bad_subject = 'Wrong phone number'
timeout_subject = 'Customer went to concurrency'

body_init = ''

class Linker():
    linkId = 0
    score = 0
    def __init__(self, score, linkId, is_bad, is_timeout):
        self.score = score
        self.linkId = linkId

class Good(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout):
        Linker.__init__(self, score, linkId, is_bad, is_timeout)
        self.linkId = linkId + 3
        
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

class TimeOut(Linker):
    def __init__(self, score, linkId, is_bad, is_timeout):
        Linker.__init__(self, score, linkId, is_bad, is_timeout)
        if is_timeout:
            self.linkId = None
        else:
            self.linkId = linkId + 2
        self.score = -score;
        

class quest():
    start_id = 0
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
    
    def __init__(self, start_id, current_id, story_name, sender, subject, body, keywords, score, is_bad, is_timeout):
        self.start_id = current_id
        self.story_name = story_name
        self.sender = sender
        self.subject = subject
        self.body = body
        self.keywords = keywords
        self.score = score
        self.is_bad = is_bad
        self.is_timeout = is_timeout
        if is_timeout:
            self.good = TimeOut(score, start_id, is_bad, is_timeout)
        else:
            self.good = Good(score, start_id, is_bad, is_timeout)
        self.bad = Bad(score, start_id, is_bad, is_timeout)
        self.timeOut = TimeOut(score, start_id, is_bad, is_timeout)

    def toJSON(self):
        serialize = OrderedDict([
            ('start_id', self.start_id),
            ('story_name', self.story_name),
            ('sender', self.sender),
            ('subject', self.subject),
            ('body', self.body),
            ('keywords', tuple(self.keywords)),
            ('good', self.good),
            ('bad', self.bad),
            ('timeOut', self.timeOut),
          ])

        return json.dumps(serialize, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

def generate(start_id, sender, score, is_last, story_name):
    questList = []
    init = quest(start_id, start_id, story_name, sender, init_subject,
            "init" + story_type  + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, False, False)
    bad = quest(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type  + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, True, False)
    timeOut = quest(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, False, True)
    questList.append(init)
    questList.append(bad)
    questList.append(timeOut)

    for x in questList:
        print(x.toJSON())
    return questList

def generateInitQuestMail():
    res = ''
    res += '# Formules de politesse' + os.linesep
    res += body_init + os.linesep
    res += 'Formules de courtoisie' + os.linesep
    res += 'Signature' + os.linesep

generate(1, "johndoe@gmail.com", 400, False, "plop")
