import os
import copy
import random

def append_story():
    tmp = ""
    tmp += "{" + os.linesep
    tmp += "}"
    return tmp

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
for i in range(1, nb_iteration + 1):
    print('----------------------')
    print("idLink : " + str(idCount))
    print("good : " + str(idCount + 1))
    print("bad : " + str(idCount + 2))
    print("TimeOut : " + str(idCount + 3))
    print("Score : " + str(points_credit[i - 1]))
    print('----------------------')
    idCount += 4



