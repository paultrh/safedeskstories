import os
import json
from quest import Quest
from faker import Faker
import json
from collections import OrderedDict
import random
import requests


functions = ['Employee', 'Manager', 'Engineer', 'Intern', 'Sales person', 'Technician', 'Consultant']

story_type = 'Contact'
init_subject = ['Weekly Intern investigation', 'Irregularities found in departement', 'Closing weekly intern revue']
bad_subject = 'Wrong information'
timeout_subject = 'Investigation failed'


#### DOCUMENT GENERATION ####

class User():
    level = 0
    name = ""
    phone_number = ""
    email = ""
    function = ""
    age = ""
    years_in_field = ""
    married = ""
    last_connection = ""
    attrDict = {}
    companyName = ""
    
    def __init__(self, domain, companyName, fake, level):
        self.level = level
        self.companyName = companyName
        self.name = fake.name()
        self.phone_number = str(fake.phone_number()).replace('(', '').replace(')', '')
        self.email = self.name.replace(" ", "")+"@"+ domain
        self.function = random.choice(functions)
        self.age = str(random.randint(25, 75))
        self.years_in_field = str(random.randint(1, 23))
        self.married = str(fake.boolean(chance_of_getting_true=20))
        self.last_connection = fake.time(pattern="%H:%M:%S")

        self.WriteToFile(self.companyName + 'Contact');

    # TODO no more hardcode
    def generateJSONforFile(self, name, ext):
        var = ""
        var = var + "{" + '\n'
        var = var + '  "filename": "'+os.path.basename(name)+'",' + '\n'
        var = var + '  "extension": "'+ext+'"' + '\n'
        var = var + "}"
        with open(os.path.join(name + ".json"), "w") as myfile:
            myfile.write(var)
        self.generateAPI_CSVFile();
    
    def generateAPI_CSVFile(self):
        if not os.path.exists('api'):
            os.makedirs('api')
        for attr, value in self.__dict__.items():
            if (attr in ["last_connection","name","phone_number","email"]):
                with open("api/"+attr+".csv", "a+", encoding='utf8') as myfile:
                    value = value.replace(",", ".")
                    if (attr == "name"):
                        print(value)
                    myfile.write('"'+value+'","'+value+'"'+'\n')
            
            
    def WriteToFile(self, filename):
        filenameOrigin = filename
        people = ""
        people += "### " + self.name + os.linesep
        people += "Phone number: " + self.phone_number + os.linesep
        people += "Email: " + self.email + os.linesep
        people += "Function: " + self.function +  os.linesep
        people += "Age: " + self.age + os.linesep
        people += "Years in the field: " + self.years_in_field + os.linesep
        people += "Married: " + self.married + os.linesep
        people += "Last connection: "  + self.last_connection  + os.linesep + os.linesep
        folder = (self.level + '/doc/' + self.companyName).replace(" ", "")
        filename = (self.level + '/doc/' + self.companyName + '/' + filename).replace(" ", "")

        if not os.path.exists('filesystem/secugov'):
            os.makedirs('filesystem/secugov')
        tmp = (self.level.split('/')[2] + self.level.split('/')[3])
        with open(os.path.join('filesystem/secugov/'+tmp+filenameOrigin +'.md'), "a+") as myfile:
            myfile.write(people)
        self.generateJSONforFile('filesystem/secugov/'+tmp+filenameOrigin, "txt")


    

#### QUEST GENERATION ####        
                
class Contact(Quest):
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                 isLast, level):
        Quest.__init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature,
                       isLast, level)


    def questionBody(self, user):
        lUnary = {'name' : user.name,
                  'phone number' : user.phone_number,
                  'email' : user.email}
        lNotUnary = {'Age-age' : user.age,
                     'Function-role in the company' : user.function,
                     'Years_in_field-experience' : user.years_in_field,
                     'LastConnection-last connection to the IT service' : user.last_connection
                     }
        txt = ""
        txt += "I am looking for the "
        res = random.choice(list(lNotUnary.items()))
        txt += res[0].split("-")[1]
        self.keywords['entities'].append({ str(res[0].split("-")[0]) : res[1]})
        txt += " of a specific employee whose "
        tmp = random.choice(list(lUnary.items()))
        txt += tmp[0] + " is " + tmp[1] + os.linesep
        txt += "I really need this information as soon as possible." + os.linesep
        return txt;

    def badBody(self, user):
        txt = ""
        txt += "The information you provided me were wrong." + os.linesep
        txt += "Please resend me as soon as possible the correct info." + os.linesep
        txt += "Here my previous request." + os.linesep
        
        txt += '>' + self.content.replace(os.linesep, os.linesep + '>')
        return txt

    

    def generateEmail(self, user):
        txt = ""
        with open("config/welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
            
        if (self.body[:3] == 'ini'):
            txt += self.questionBody(user) + os.linesep + os.linesep
        elif (self.body[:3] == 'bad'):
            txt += self.badBody(user) + os.linesep + os.linesep
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
def generateContact(start_id, sender, score, is_last, story_name, signature, fake,
                    isLast, level, z):
    companyName = 'secuGov'
    IntentName = 'FindUserInfo'
    # Create Fake Data
    for i in range(0, random.randint(5, 15)):
        User('gmail.com', companyName, fake, level)

    # Create Specific Content
    questList = []
    init = Contact(start_id, start_id, story_name, sender, init_subject[z],
            "init" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                   score, False, False, signature, isLast, level)
    init.generateEmail(User('gmail.com', companyName, fake, level))
    bad = Contact(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                  score, True, False, signature, isLast, level)
    bad.content = init.content
    bad.setKeywords(init.keywords)
    timeOut = Contact(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + level.replace('/', '') + ".md", { 'intent' : IntentName, 'entities' : []},
                      score, False, True, signature, isLast, level)
    questList.append(init)
    questList.append(bad)
    questList.append(timeOut)

    bad.generateEmail(User('gmail.com', companyName, fake, level))
    timeOut.generateEmail(User('gmail.com', companyName, fake, level))

    init.generateInitFile()
    bad.generateInitFile()
    timeOut.generateInitFile()

    fraudList = []
    fraudList.append(init.evil.createFraud())
    fraudList.append(bad.evil.createFraud())
    fraudList.append(timeOut.evil.createFraud())
    
    

    # Create Fake Data
    for i in range(0, random.randint(5, 15)):
        User('gmail.com', companyName, fake, level)

    return questList, fraudList
