from faker import Faker
import random
import os

contries = ['en_GB', 'en_US', 'pt_BR', 'fr_FR']
functions = ['Employee', 'Manager', 'Engineer', 'Intern', 'Sales person', 'Technician', 'Consultant']
quali = ['Above', 'Under', 'Around']
subfolders = ['Affiliate', 'Charities', 'Governement Activities', 'Security Business']

local = random.choice(contries)
fake = Faker(local)

def generateJson(name, ext, theme):
    var = ""
    var = var + "{" + '\n'
    var = var + '"filename": "'+name+'",' + '\n'
    var = var + '"extension": "'+ext+'"' + '\n'
    var = var + "}"
    with open(os.path.join(theme, name + ".json"), "a+") as myfile:
        myfile.write(var)


def addCompany(theme):
    try:
        os.mkdir(theme)
    except Exception:
        pass
    companyName = fake.company()
    companyName = companyName.replace(".", "")
    companyName = companyName.replace("/", "")
    companyName = companyName.replace("\\", "")
    companyName = companyName.replace(",", "")
    company = ""
    company = company + "# " + companyName +" Company"+ '\n\n\n'
    company = company + "### Description" + '\n\n' + fake.catch_phrase() + '\n' + fake.catch_phrase() + '\n\n'
    company = company + "### Address" + '\n\n'
    company = company + "| Info | Value |" + '\n'
    company = company + "| ------ | ------ |" + '\n'
    company = company + "| Latitude | "+ str(fake.latitude()) +" |" + '\n'
    company = company + "| Longitude | "+str(fake.longitude()) +" |" + '\n'
    company = company + "| Street_address | "+str(fake.street_address()) +" |" + '\n'
    company = company + "| Postcode | "+str(fake.postcode()) +" |" + '\n'
    company = company + "| Locale | "+str(local) +" |" + '\n'
    company = company + "| City | "+str(fake.city()) +" |" + '\n\n\n'
    company = company + "### Information" + '\n\n'
    company = company + " - Legal id : " + str(random.randint(100, 1000))+ " " + str(random.randint(100, 1000)) + " " + str(random.randint(100, 1000)) + '\n'
    company = company + " - Sales revenue " + str(random.randint(10000, 100000000))+ " $" + '\n\n'
    company = company + " - Forecast turnover " + str(random.randint(10000, 100000000)) + " $" + '\n\n'
    company = company + " - Store turnover " + str(random.randint(100, 100000)) + " $" + '\n\n'
    company = company + " - Justice issue " + str(fake.boolean(chance_of_getting_true=20)) + '\n\n'
    company = company + " - Created in " + str(random.randint(1990, 2015)) + '\n\n'
    company = company + "### IT ressources" + '\n\n'
    company = company + "```sh" + '\n'
    company = company + fake.url() + '\n'
    company = company + fake.md5(raw_output=False) + '\n'
    company = company + fake.mac_processor()  + '\n'
    company = company + fake.firefox()  + '\n'
    company = company + fake.linux_platform_token()  + '\n'
    company = company + fake.opera()  + '\n'
    company = company + fake.windows_platform_token()  + '\n'
    company = company + fake.user_agent() + '\n'
    company = company + fake.chrome() + '\n'
    domain = fake.free_email_domain()
    company = company + domain   + '\n'
    company = company + "```" + '\n\n'
    company = company + "### Employees" + '\n\n'
    nbEmployee = random.randint(11, 100)
    company = company + companyName + "are composed of **" + str(nbEmployee) + "** employees" + '\n'
    company = company + "The overall satisfaction rate is " + random.choice(quali) + " **" + str(random.randint(11, 95)) + '%** \n'
    for i in range(0, nbEmployee):
        if (i == 0):
            company = company + addPeople("CEO", companyName.replace(" ", ""), domain, theme) + '\n'
        elif (i == 1):
            company = company + addPeople("CIO", companyName.replace(" ", ""), domain, theme) + '\n'
        else:
            company = company + addPeople("", companyName.replace(" ", ""), domain, theme) + '\n'
    with open(os.path.join(theme, companyName.replace(" ", "") + ".md"), "a") as myfile:
        myfile.write(company)
    generateJson(companyName.replace(" ", ""), ".docx", theme)
    generateJson("Contact"+companyName.replace(" ", ""), ".txt", theme)

def addPeople(role, company, domain, theme):
    if (role == ""):
        role = random.choice(functions)
    user = fake.name()
    people = ""
    people = people + "### " + user + '\n'
    people = people + "Phone number: " + str(fake.phone_number()) + '\n'
    people = people + "Email: " + user.replace(" ", "")+"@"+ domain + '\n'
    people = people + "Function: " + role + '\n'
    people = people + "Age: " + str(random.randint(25, 75)) + '\n'
    people = people + "Years in the field: " + str(random.randint(1, 23)) + '\n'
    people = people + "Married: " + str(fake.boolean(chance_of_getting_true=20)) + '\n'
    people = people + "Last connection: "  + fake.time(pattern="%H:%M:%S") + '\n\n'
    print(os.path.join(theme, "Contact"+company+".md"));
    with open(os.path.join(theme, "Contact"+company+".md"), "a+") as myfile:
        myfile.write(people)
    return user


print("Start")
for i in range (10):
    local = random.choice(contries)
    print(local)
    fake = Faker(local)
    addCompany(random.choice(subfolders));
print("End")
