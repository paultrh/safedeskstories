import requests
import urllib.request
import random
import os

#This API key is currently active
#30 days remaining
#Key 1: 6894a55bb34a4fd2b25e1ce2621824c0
#Key 2: b527d5d3c6f2433583c6f1f99751dcf2

def getMarkdown(name, path):
    txt = ''
    txt += '![' + name + '](' + path + ')' + os.linesep
    return txt

def bing_search(query):
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
    # query string parameters
    payload = {'q': query}
    # custom headers
    headers = {'Ocp-Apim-Subscription-Key': '6894a55bb34a4fd2b25e1ce2621824c0'}
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
