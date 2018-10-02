from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import os
import re
import html5lib
import datetime
import json

CWD = os.getcwd() + '\\Speeches 1996 - 2005\\'


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

#url = 'https://www.federalreserve.gov/boarddocs/speeches/1996/19961219.htm'
#url = 'https://www.federalreserve.gov/boarddocs/speeches/2005/20051214/default.htm'
#url = 'https://www.federalreserve.gov/boarddocs/speeches/2005/20050302/default.htm'


def main(url):
    html = simpleGet(url)
    soup = BeautifulSoup(html, 'html5lib')

    tables = soup.find_all('table')

    all_text =''
    for i in tables:
        all_text += i.text.strip()

    index = []

    for i in range(len(tables)):
        p_list = tables[i].select('p')
        if not p_list:
            index.append(i)

    print(index)
    print(len(tables))

    for i in sorted(index, reverse=True):
            del tables[i]

    for t in tables:
        b_list = t.find_all('b')
        if b_list:
            for i in b_list:
                i.clear()
        strong_list = t.find_all('strong')
        if strong_list:
            for s in strong_list:
                if s.text != 'Footnotes':
                    s.clear()
        a_list = t.find_all('a')
        if a_list:
            for a in a_list:
                a.clear()



    tables = [t.text.strip() for t in tables]

    speech = ' '.join(tables)
    speech = speech.split('Footnotes')
    speech = speech[0]
    speech = speech.replace('\n','')
    speech = speech.replace('\t',' ')

    re_date = re.compile(r'\w+\s\d+,\s\d+')
    re_author = re.compile(r'(Remarks by) (\w+ \w+ \w+ \w\. \w+|\w+ \w+ \w\. \w+|\w+ \w+\. \w+|\w+ \w+ \w+|\w+ \w+)')

    try:
        author = re_author.search(all_text)
        author = str(author.group())
        author = re.sub(r'Remarks by\s+', '', author).strip()
        author = author.replace('\n','')
        author = author.replace('\r','')


    except:
        author = 'AUTHOR_ERROR'

    try:
        date = re_date.search(all_text)
        date = str(date.group())
        date = datetime.datetime.strptime(date,'%B %d, %Y')
        date = datetime.datetime.strftime(date,'%Y %B, %d')

    except:
        date = 'DATE_ERROR'

    data = {}
    data['Speaker'] = author
    data['Date'] = date
    data['Speech'] = speech

    if date == 'DATE_ERROR':
        print(f'DATE_ERROR: {date} - {author} - {url}')
    elif author == 'AUTHOR_ERROR':
        print(f'AUTHOR_ERROR: {date} - {author} - {url}')
    else:
        file = f'{CWD}{date} - {author}.json'
        with open(file,'w') as outfile:
            json.dump(data,outfile,indent=4)


    #if series.loc[2].isnull():
    #    print(f'No Speech Error: {date} - {author}')

    print(len(speech))
