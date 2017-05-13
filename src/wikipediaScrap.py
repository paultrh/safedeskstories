from wikipedia import *


def getDescription(theme, nbLine):
    txt = wikipedia.summary(theme, sentences=nbLine)
    return txt
