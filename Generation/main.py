import os
import copy
import random
from contact import *
from graphviz import Digraph

def append_story():
    tmp = ""
    tmp += "{" + os.linesep
    tmp += "}"
    return tmp

def generateSignature(self):
    txt = ""
    '''
    FIXME Featch from back 
    txt += self.name + os.linesep
    txt += self.function
    '''
    return txt

class Story():
    quests = []
    def __init__(self, quests):
        self.quests = quests

    def toJSON(self):
        serialize = OrderedDict([
            ('quests', tuple((o.toJSON() for o in self.quests))),
        ])

        return json.dumps(serialize, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)


    def ShowGraph(self):
        tmpGlobal = []
        tmp = []
        count = 1
        for i in self.quests:
            tmp.append(i)
            if (count % 3 == 0):
                tmpGlobal.append(tuple(tmp))
                tmp =  []
            count += 1
        print(tmpGlobal)

        last_good = 0
        last_bad = 0
        dot = Digraph(comment='The story')
        for quest in tmpGlobal:
            dot.node(str(quest[0].current_id), quest[0].content.replace(os.linesep, "\\n"))
            dot.node(str(quest[1].current_id), quest[1].content.replace(os.linesep, "\\n"))
            dot.node(str(quest[2].current_id), quest[2].content.replace(os.linesep, "\\n"), style='filled', fillcolor='red')

            
            dot.edge(str(quest[0].current_id),str(quest[1].current_id), color='orange')
            dot.edge(str(quest[0].current_id),str(quest[2].current_id), color='red')
            dot.edge(str(quest[1].current_id),str(quest[2].current_id), color='red')
            if (last_good != 0 and last_bad != 0):
                dot.edge(last_good,str(quest[0].current_id), color='green')
                dot.edge(last_bad,str(quest[0].current_id), color='green')
            last_good = str(quest[0].current_id)
            last_bad = str(quest[1].current_id)
            
        dot.node("END", style='filled', fillcolor='green')
        dot.edge(last_good,"END", color='green')
        dot.edge(last_bad,"END", color='green')
        try:
            dot.render('graph.gv', view=True)
        except:
            print("no dot render found go to http://www.webgraphviz.com/')
        
        
        
idCount = 1
total_points = 100
nb_iteration = 5                                                                                                   

rootdir = os.getcwd()
sub_folders = []

for subdir, dirs, files in os.walk(rootdir):
    for folder in dirs:
        sub_folders.append(folder)

folders_ran = copy.deepcopy(sub_folders)

while (len(folders_ran) < nb_iteration):
    folders_ran.append(random.choice(sub_folders))

random.shuffle(folders_ran)
points_credit = []
for i in range(0, nb_iteration):
    points_credit.append(total_points / nb_iteration)

print(points_credit)
print(folders_ran)

quests = []
idcount = 1
for i in range(1, 4):
    quests += generate(idcount, "johndoe@gmail.com", 400, False, "plop")
    idcount += 3

story = Story(quests)


with open(os.path.join('Doc', 'init.json'), "w") as myfile:
    myfile.write(story.toJSON())
                  
story.ShowGraph()

