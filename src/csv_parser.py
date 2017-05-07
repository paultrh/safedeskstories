#!/usr/bin/env python3

import csv
import os
from csv import DictReader


def isUnique(myList):
  mySet = set()
  for x in myList:
    if x in mySet:
        return False
    mySet.add(x)
  return True

# TMP USE FOR TESTING
with open('plop.csv', 'w+') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Name', 'Firstname', 'Age'])
    spamwriter.writerow(['doe', 'john', '21'])
    spamwriter.writerow(['doe2', 'john2', '22'])
    spamwriter.writerow(['doe3', 'john3', '21'])

class Entity(object):
    def __init__(self, pairs):
        for k,v in pairs:
            setattr(self,k,v)
    def __str__(self):
        txt = ''
        for k,v in self.__dict__.items():
            txt += k + '=' + v + ' '
        return txt

with open('plop.csv') as f:
    orders = []
    reader = DictReader(f)
    for row in reader:
        orders.append(Entity(row.items()))

attrs = []
for k,v in orders[0].__dict__.items():
    attrs.append(k)

tmp = []
uniqueElt = []
for i in range(0, len(attrs)):
    for elt in orders:
        val = [o[1] for o in elt.__dict__.items() if o[0] == attrs[i]]
        tmp.append(''.join(val))
    if (isUnique(tmp)):
        uniqueElt.append(attrs[i])
    tmp = []

print("Unique element are")
print(uniqueElt)

