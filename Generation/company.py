import os
import json
from quest import Quest
from faker import Faker
import json
from collections import OrderedDict
import random

quali = ['Above', 'Under', 'Around']
functions = ['Employee', 'Manager', 'Engineer', 'Intern', 'Sales person', 'Technician', 'Consultant']
contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
story_type = 'Company'
init_subject = 'Investigate companies'
bad_subject = 'Wrong information'
timeout_subject = 'Transfer case'


#### DOCUMENT GENERATION ####
class CompanyModel():
    #Unique
    company = ""
    legal_id = ""
    latitude = ""
    longitude = ""
    street_address = ""


    #Not unique
    local = ""
    city = ""
    postcode = ""
    sales_revenue = ""
    forecast_turnover = ""
    store_turnover = ""
    justice_issue = ""
    created_in = ""
    description0 = ""
    description1 = ""
    nbEmployee = ""
    satisfaction_rate = ""
    domain = ""
    url = ""
    md5 = ""
    mac_processor = ""
    firefox = ""
    linux_platform_token = ""
    opera = ""
    windows_platform_token = ""
    user_agent = ""
    chrome_agent = ""
    

    def __init__(self, domain, fake):
        #Unique
        self.company = fake.company()
        self.company = self.company.replace(".", "")
        self.company = self.company.replace("/", "")
        self.company = self.company.replace("\\", "")
        self.company = self.company.replace(",", "")
        self.latitude = str(fake.latitude())
        self.longitude = str(fake.longitude())
        self.street_address = str(fake.street_address())

        #Not unique
        self.legal_id = str(random.randint(100, 1000))+ " " + str(random.randint(100, 1000)) + " " + str(random.randint(100, 1000))
        self.local = random.choice(contries)
        self.city = str(fake.city())
        self.postcode = str(fake.postcode())
        self.sales_revenue = str(random.randint(10000, 100000000))+ " $"
        self.forecast_turnover = str(random.randint(10000, 100000000)) + " $"
        self.store_turnover = str(random.randint(100, 100000)) + " $"
        self.justice_issue = str(fake.boolean(chance_of_getting_true=20))
        self.created_in = str(random.randint(1990, 2015))
        self.description0 = fake.catch_phrase()
        self.description1 = fake.catch_phrase()
        self.nbEmployee = str(random.randint(11, 100))
        self.satisfaction_rate = str(random.randint(11, 95))
        self.domain = domain
        self.url = str(fake.url())
        self.md5 = str(fake.md5(raw_output=False))
        self.mac_processor = str(fake.mac_processor())
        self.firefox = str(fake.firefox())
        self.windows_platform_token = str(fake.windows_platform_token())
        self.linux_platform_token = str(fake.linux_platform_token())
        self.user_agent = str(fake.user_agent())
        self.chrome_agent = str(fake.chrome())

        self.WriteToFile(self.company + 'Description');

    def WriteToFile(self, filename):
        company = ""
        company += "# " + self.company +" Company"+ '\n\n\n'
        company += "### Description" + '\n\n' + self.description0 + '\n' + self.description1 + '\n\n'
        company += "### Address" + '\n\n'
        company += "| Info | Value |" + '\n'
        company += "| ------ | ------ |" + '\n'
        company += "| Latitude | "+ self.latitude +" |" + '\n'
        company += "| Longitude | "+self.longitude +" |" + '\n'
        company += "| Street_address | "+self.street_address +" |" + '\n'
        company += "| Postcode | "+self.postcode +" |" + '\n'
        company += "| Locale | "+self.local +" |" + '\n'
        company += "| City | "+self.city +" |" + '\n\n\n'
        company += "### Information" + '\n\n'
        company += " - Legal id : " + self.legal_id + '\n'
        company += " - Sales revenue " + self.sales_revenue+ " $" + '\n\n'
        company += " - Forecast turnover " + self.forecast_turnover + " $" + '\n\n'
        company += " - Store turnover " + self.store_turnover + " $" + '\n\n'
        company += " - Justice issue " + self.justice_issue + '\n\n'
        company += " - Created in " + self.created_in + '\n\n'
        company += "### IT ressources" + '\n\n'
        company += "```sh" + '\n'
        company += "$ url " + self.url + '\n'
        company += "$ md5 " + self.md5 + '\n'
        company += "$ mac processor " + self.mac_processor  + '\n'
        company += "$ firefox info " + self.firefox  + '\n'
        company += "$ firefox info " + self.linux_platform_token  + '\n'
        company += "$ opera info " + self.opera  + '\n'
        company += "$ windows info " + self.windows_platform_token  + '\n'
        company += "$ user agent " + self.user_agent + '\n'
        company += "$ chrome info " + self.chrome_agent + '\n'
        company += "$ domain of the company "+ self.domain   + '\n'
        company += "```" + '\n\n'
        company += "### Employees" + '\n\n'
        company +=  self.company + " are composed of **" + self.nbEmployee + "** employees" + '\n'
        company += "The overall satisfaction rate is " + random.choice(quali)+ " **" + self.satisfaction_rate + '%** \n'

        if not os.path.exists('Story/doc/'+self.company):
            os.makedirs('Story/doc/' + self.company)
        with open(os.path.join('Story/doc/' + self.company + '/' + filename), "w+") as myfile:
            myfile.write(company)


#### QUEST GENERATION ####        
                
class Company(Quest):
    
    def __init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature):
        Quest.__init__(self, start_id, current_id, story_name, sender,
                 subject, body, keywords, score, is_bad, is_timeout, signature)


    def questionBody(self, company):
        lUnary = {'company name' : company.company,
                  'legal id' : company.legal_id ,
                  'latitude' : company.latitude,
                  'longitude' : company.longitude ,
                  'street address' : company.street_address }
        lNotUnary = {'local' : company.local ,
                     'city' : company.city ,
                     'postcode' : company.postcode ,
                     'sales revenue' : company.sales_revenue ,
                     'forecast turnover' : company.forecast_turnover,
                     'store turnover' : company.store_turnover ,
                     'presence of justice issue' : company.justice_issue ,
                     'creation date' : company.created_in ,
                     'first description' : company.description0 ,
                     'second description' : company.description1 ,
                     'number of employees' : company.nbEmployee ,
                     'satisfaction rate' : company.satisfaction_rate ,
                     'domain name' : company.domain ,
                     'url' : company.url ,
                     'md5 token' : company.md5 ,
                     'standart mac processor ' : company.mac_processor ,
                     'standart firefox signature' : company.firefox ,
                     'linux platform token' : company.linux_platform_token ,
                     'opera specification' : company.opera ,
                     'windows platform token' : company.windows_platform_token ,
                     'default user agent' : company.user_agent ,
                     'specific chrome agent' : company.chrome_agent
                     }
        txt = ""
        txt += "I am looking for : "
        res = random.choice(list(lNotUnary.items()))
        res2 = random.choice(list(lNotUnary.items()))
        while res2 == res:
            res2 = random.choice(list(lNotUnary.items()))
        
        txt += 'the ' + res[0] + ' and '
        txt += 'the ' + res2[0] + ' '
        self.keywords.append(res[1])
        self.keywords.append(res2[1])
        txt += " of a specific company whose "
        tmp = random.choice(list(lUnary.items()))
        txt += tmp[0] + " is " + tmp[1] + os.linesep
        txt += "I really need this information as soon as possible." + os.linesep
        return txt;

    def badBody(self, company):
        txt = ""
        txt += "The information you provided me were wrong." + os.linesep
        txt += "Please resend me as soon as possible the correct info." + os.linesep
        txt += "Here my previous request." + os.linesep
        
        txt += '>' + self.content.replace(os.linesep, os.linesep + '>')
        return txt

    # TODO no more hardcode
    def generateJSONforFile(self, name, ext, theme):
        var = ""
        var = var + "{" + '\n'
        var = var + '"filename": "'+name+'",' + '\n'
        var = var + '"extension": "'+ext+'"' + '\n'
        var = var + "}"
        with open(os.path.join(theme, name[:-3] + ".json"), "a+") as myfile:
            myfile.write(var)

    def generateEmail(self, company):
        txt = ""
        with open("welcomePhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
            
        if (self.body[:3] == 'ini'):
            txt += self.questionBody(company) + os.linesep + os.linesep
        elif (self.body[:3] == 'bad'):
            txt += self.badBody(company) + os.linesep + os.linesep
        else:
            txt += self.timeOutBody() + os.linesep + os.linesep
        
        with open("EndPhrase.txt", "r") as myfile:
            content = myfile.readlines()
            content = [x.strip() for x in content]
            txt += random.choice(content) + "," + os.linesep + os.linesep
        txt += self.signature + os.linesep
        if not os.path.exists('Story'):
            os.makedirs('Story')
        self.content = txt
        with open(os.path.join('Story', self.body), "w") as myfile:
            myfile.write(txt)
        self.generateJSONforFile(self.body, ".docx", 'Story')
        return txt

# NOTE : Should refactor but may divert from one quest to another
def generateCompany(start_id, sender, score, is_last, story_name, signature, fake):
    companyName = 'secuGov'

    # Create Specific Content
    questList = []
    init = Company(start_id, start_id, story_name, sender, init_subject,
            "init" + story_type  + "Quest" + str(start_id) + ".md", [], score, False, False, signature)
    init.generateEmail(CompanyModel('gmail.com', fake))
    bad = Company(start_id, start_id + 1, story_name, sender, bad_subject,
            "bad" + story_type  + "Quest" + str(start_id) + ".md", [], score, True, False, signature)
    bad.content = init.content
    bad.keywords = init.keywords
    timeOut = Company(start_id, start_id + 2, story_name, sender, timeout_subject,
            "timeOut" + story_type  + "Quest" + str(start_id) + ".md", [], score, False, True, signature)
    questList.append(init)
    questList.append(bad)
    questList.append(timeOut)

    bad.generateEmail(CompanyModel('gmail.com', fake))
    timeOut.generateEmail(CompanyModel('gmail.com', fake))
    
    # Create Fake Data
    for i in range(0, random.randint(1, 3)):
        CompanyModel('gmail.com', fake)

    return questList
