from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import os
import datetime

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

    raw_html = simpleGet(url)
    raw_html = BeautifulSoup(raw_html, 'html.parser')
    paragraphs_list = raw_html.select('p')
    indexes = []
    for i in range(len(paragraphs_list)):
        if paragraphs_list[i].strong:
            del paragraphs_list[i]['strong']
        elif paragraphs_list[i].em:
            del paragraphs_list[i]['em']
        elif paragraphs_list[i].a:
            del paragraphs_list[i]['a']
        elif paragraphs_list[i].i:
            del paragraphs_list['i']['i']
        elif paragraphs_list[i] == '':
            indexes.append(i)

    for index in sorted(indexes, reverse=True):
        del paragraphs_list[index]
    del paragraphs_list[2]
    del paragraphs_list[-1]
#    try:
#        ''.join(paragraphs_list)
#    except:
#        print(paragraphs_list)
    paragraphs_list = [(p.text).encode('utf-8') for p in paragraphs_list]
#    for i in range(len(paragraphs_list)):
#        paragraphs_list2.append((paragraphs_list[i].text).encode('utf-8'))

    s1 = pd.Series(paragraphs_list)
    s1 = s1.str.decode('utf-8')
    date = s1.loc[0]
    author = s1.loc[1]
    date = datetime.datetime.strptime(date,'%B %d, %Y')
    date = datetime.datetime.strftime(date,'%Y %B, %d')
    s1 = s1.str.strip()
    s1 = s1.str.replace('\n','')
    s1 = s1.str.replace('\r','')
    s1 = s1.str.replace('\t','')
    s1 = s1.dropna()
    print(s1)
    file = f'{CWD}{date} - {author}.csv'
    s1.to_csv(file,index=False)

if __name__ == "__main__":
    main('https://www.federalreserve.gov/newsevents/speech/bies20060428a.htm')
