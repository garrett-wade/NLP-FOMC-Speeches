from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import os
import datetime
import html5lib
import re
import xml.etree.cElementTree as ET
import json

#URL = 'https://www.federalreserve.gov/newsevents/speech/brainard20180531a.htm'
CWD = os.getcwd() + '\\Speeches 2006 - present\\'

def simpleGet(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if isGoodResponse(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        logError('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def isGoodResponse(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def logError(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def main(url):

    soup = simpleGet(url)
    soup = BeautifulSoup(soup, 'html5lib')

    date = soup.find('p',{'class':'article__time'}).text
    date = datetime.datetime.strptime(date,'%B %d, %Y')
    date = datetime.datetime.strftime(date,'%Y %B, %d')

    author = soup.find('p',{'class':'speaker'}).text

    text = str(soup.find('div','col-xs-12 col-sm-8 col-md-8'))

    references_regex = re.compile(r'<strong>References</strong>')
    references = re.search(references_regex, text)

    if references:
        text = references_regex.split(text)
        del text[1]
        text = text[0]

    footnote_regex = re.compile(r'<a.+"fn1"')
    footnotes = re.search(footnote_regex, text)

    if footnotes != None:
        text = footnote_regex.split(text)
        del text[1]
        text = text[0]

    text = text.split('<')
    text = [i.replace(r'/n','') for i in text]
    text = [re.sub(r'.+>', '', i).strip() for i in text]
    text = [i for i in text if i]
    text = str(''.join(text))

    data = {}
    data['Speaker'] = author
    data['Date'] = date
    data['Speech'] = text

    file = f'{CWD}{date} - {author}.json'
    with open(file,'w') as outfile:
        json.dump(data,outfile,indent=4)
    print(len(text))


if __name__ == "__main__":
    main('https://www.federalreserve.gov/newsevents/speech/tarullo20131122a.htm')
