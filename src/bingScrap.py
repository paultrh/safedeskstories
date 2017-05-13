import requests
import urllib.request
import random
import os

#This API key is currently active
#30 days remaining
#Key 1: 15b80811a3d0460dbd62989feadae6bf
#Key 2: 7cededa473ab4266bf73f5eef4fc1c56

def getMarkdown(name, path):
    txt = ''
    txt += '![' + name + '](' + path + ')' + os.linesep
    return txt

def bing_search(query):
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
    # query string parameters
    payload = {'q': query}
    # custom headers
    headers = {'Ocp-Apim-Subscription-Key': '15b80811a3d0460dbd62989feadae6bf'}
    # make GET request
    r = requests.get(url, params=payload, headers=headers)
    # get JSON response
    return r.json()

def getImages(context):
    res = ''
    j = bing_search(context)
    for i in range(0, random.randint(0, max(7, len(j['value'])))):
        if (i > 7):
            break;
        res += getMarkdown(context+str(i), j['value'][i]['thumbnailUrl'])
    return res
