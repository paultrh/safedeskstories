import os
import faker

story_type = 'Contact'
init_subject = 'Starting partnership'
bad_subject = 'Wrong phone number'
timeout_subject = 'Customer went to concurrency'

def create_object(start_id, current_id, story_name, sender, subject,
        body, keywords, score, is_bad, is_timeout):
    res = "{" + os.linesep
    res += '  "story_name": "' + story_name + '",' + os.linesep
    res += '  "idLink": ' + str(current_id) + ',' + os.linesep
    res += '  "sender": "' + sender + '",' + os.linesep
    res += '  "subject": "' + subject + '",' + os.linesep
    res += '  "body": "' + body + '",' + os.linesep
    res += '  "good": {' + os.linesep
    if is_timeout:
        res += '    "score": ' + str(-score) + ',' + os.linesep
        res += '    "link": null,' + os.linesep
    else:
        res += '    "keywords": [' + os.linesep
        for i in keywords:
            res += '      "' + i + '"'
            if i != keywords[len(keywords) - 1]:
                res += ',' + os.linesep
        res += os.linesep + '    ],' + os.linesep
        res += '    "score": ' + str(score) + ',' + os.linesep
        res += '    "link": ' + str(start_id + 3) + ',' + os.linesep
    res += '  },' + os.linesep
    res += '  "bad": {' + os.linesep
    res += '    "score": ' + str(-score) + ',' + os.linesep
    if is_bad:
        res += '    "link": ' + str(start_id + 2) + ',' + os.linesep
    elif is_timeout:
        res += '    "link": null,' + os.linesep
    else:
        res += '    "link": ' + str(start_id + 1) + ',' + os.linesep
    res += '  },' + os.linesep
    res += '  "timeOut": {' + os.linesep
    res += '    "score": ' + str(-score) + ',' + os.linesep
    if not is_timeout:
        res += '    "link": ' + str(start_id + 2) + ',' + os.linesep
    else:
        res += '    "link": null,' + os.linesep
    res += '}'
    return res

def generate(start_id, sender, score, is_last, story_name):
    json = ''
    json += create_object(start_id, start_id, story_name, sender, init_subject,
            "init" + story_type  + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, False, False)
    json += ',' + os.linesep
    json += create_object(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, True, False)
    json += ',' + os.linesep
    json += create_object(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + ".md", ['izi', 'php'], score, False, True)
    print(json)

def generateQuestMail():
    print("lol")

generate(1, "johndoe@gmail.com", 400, False, "plop")
