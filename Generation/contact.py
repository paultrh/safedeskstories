import os
from quest import Quest
from faker import Faker
import json
from collections import OrderedDict
import random

functions = ['Employee', 'Manager', 'Engineer', 'Intern', 'Sales person', 'Technician', 'Consultant']
contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
local = random.choice(contries)
fake = Faker(local)

story_type = 'Contact'

init_subject = 'Starting partnership'
bad_subject = 'Wrong information'
timeout_subject = 'Customer went to concurrency'

body_init = ''

class User():
    name = ""
    phone_number = ""
    email = ""
    function = ""
    age = ""
    years_in_field = ""
    married = ""
    last_connection = ""
    attrDict = {}
    
    def __init__(self, domain):
        self.name = fake.name()
        self.phone_number = str(fake.phone_number())
        self.email = self.name.replace(" ", "")+"@"+ domain
        self.function = random.choice(functions)
        self.age = str(random.randint(25, 75))
        self.years_in_field = str(random.randint(1, 23))
        self.married = str(fake.boolean(chance_of_getting_true=20))
        self.last_connection = fake.time(pattern="%H:%M:%S")

    def WriteToFile(self, filename):
        people = ""
        people += "### " + user + os.linesep()
        people += "Phone number: " + str(fake.phone_number()) +  + os.linesep()
        people += "Email: " + user.replace(" ", "")+"@"+ domain +  + os.linesep()
        people += "Function: " + role +  os.linesep()
        people += "Age: " + str(random.randint(25, 75)) + os.linesep()
        people += "Years in the field: " + str(random.randint(1, 23))  + os.linesep()
        people += "Married: " + str(fake.boolean(chance_of_getting_true=20))  + os.linesep()
        people += "Last connection: "  + fake.time(pattern="%H:%M:%S")  + os.linesep() + os.linesep()
        with open(os.path.join(theme, filename), "a+") as myfile:
            myfile.write(people)

    

        
                
class Contact(Quest):
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout):
        Quest.__init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout)


    def questionBody(self, user):
        lUnary = {'name' : user.name,
                  'phone number' : user.phone_number,
                  'email' : user.email}
        lNotUnary = {'age' : user.age,
                     'marital status' : user.married,
                     'role in the company' : user.function,
                     'experience' : user.years_in_field,
                     'last connection to the IT service' : user.last_connection
                     }
        txt = ""
        txt += "I am looking for the "
        res = random.choice(list(lNotUnary.items()))
        txt += res[0]

        self.keywords.append(res[1])
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
        with open("welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
            
        if (self.body[:3] == 'ini'):
            txt += self.questionBody(user) + os.linesep + os.linesep
        elif (self.body[:3] == 'bad'):
            txt += self.badBody(user) + os.linesep + os.linesep
        else:
            txt += self.timeOutBody() + os.linesep + os.linesep
        
        with open("EndPhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
        txt += "" + os.linesep
        if not os.path.exists('Doc'):
            os.makedirs('Doc')
        self.content = txt
        with open(os.path.join('Doc', self.body), "w") as myfile:
            myfile.write(txt)
        return txt

# NOTE : Should refactor
def generate(start_id, sender, score, is_last, story_name):
    questList = []
    init = Contact(start_id, start_id, story_name, sender, init_subject,
            "init" + story_type  + "Quest" + str(start_id) + ".md", [], score, False, False)
    init.generateEmail(User('gmail.com'))
    bad = Contact(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type  + "Quest" + str(start_id) + ".md", [], score, True, False)
    bad.content = init.content
    bad.keywords = init.keywords
    timeOut = Contact(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + ".md", [], score, False, True)
    questList.append(init)
    questList.append(bad)
    questList.append(timeOut)


    bad.generateEmail(User('gmail.com'))
    timeOut.generateEmail(User('gmail.com'))

    return questList
