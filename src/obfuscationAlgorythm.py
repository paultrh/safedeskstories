import random
import string

#### UTILS ####
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def getRandomChar():
    return random.choice(string.ascii_letters)

def swap(s, i, j):
    lst = list(s);
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

#### TRANSFORM OPERATIONS ####

def dotsTransform(mail):
    nbDots = mail.count('.')
    if nbDots == 0:
        return mail
    mail = rreplace(mail, '.', '', random.randint(1, nbDots))
    return mail

def insertChar(mail):
    position = random.randint(0,len(mail)-1);
    res = mail[:position] + getRandomChar() + mail[position:]
    return res

def removeChar(mail):
    position = random.randint(0,len(mail)-1);
    res = mail[:position] + mail[position+1:]
    return res

def swapChar(mail):
    position1 = random.randint(0,len(mail)-1);
    position2 = random.randint(0,len(mail)-1);
    if position1 == position2:
        return removeChar(mail)
    res = swap(mail, position1, position2)
    return res

#### ALGORYTHM ####

transformList = ['dotsTransform', 'insertChar', 'removeChar', 'swapChar']
#complexity between 1 and 5
def emailTransform(mail, complexity):
    if (len(mail)) < 3:
        return mail
    if complexity <= 0:
        complexity = 2
    elif complexity > 5:
        complexity = 5
    newEmail = mail
    for i in range(complexity):
        res = random.choice(transformList)
        if (res == 'dotsTransform'):
            newEmail = dotsTransform(newEmail)
        elif (res == 'insertChar'):
            newEmail = insertChar(newEmail)
        elif (res == 'removeChar'):
            newEmail = removeChar(newEmail)
        elif (res == 'swapChar'):
            newEmail = swapChar(newEmail)
    return newEmail


