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

def main(url):
    html = simpleGet(url)
    soup = BeautifulSoup(html, 'html5lib')
    #for p in table:
    #    print(p.find('p').text)
    #p_list = soup.find_all(lambda tag: tag.name == 'p' and not tag.attrs)
    #print(type(p_list))
    #print(len(p_list))
    p_list = soup.select('p')
    #print(p_list)
    #pprint.pprint(p_list)
    indexes = []
    for i in range(len(p_list)):
        if p_list[i].strong:
            indexes.append(i)
#        elif p_list[i].em:
#            indexes.append(i)
        elif p_list[i].a:
            indexes.append(i)
        elif p_list[i].b:
            indexes.append(i)
        elif p_list[i].i:
            indexes.append(i)

    #print(indexes)
    for index in sorted(indexes, reverse=True):
        del p_list[index]

    p_list = [p.text for p in p_list]

    info = str(soup.text)

    try:

        re_author = re.compile(r'(Remarks by) (\w+ \w+ \w+ \w\. \w+|\w+ \w+ \w\. \w+|\w+ \w+\. \w+|\w+ \w+ \w+|\w+ \w+)')
        author = re_author.search(info)
        author = str(author.group())
        author = re.sub(r'Remarks by\s+', '', author).strip()
        author = author.replace('\n','')
        author = author.replace('\r','')

    except:
        author = 'AUTHOR_ERROR'

    re_date = re.compile(r'\w+\s\d+,\s\d+')
    date = re_date.findall(info)
    date = date[1]
    try:
        date = datetime.datetime.strptime(date,'%B %d, %Y')
        date = datetime.datetime.strftime(date,'%Y %B, %d')

    except:
        date = 'DATE_ERROR'

    p_list.insert(0,date)
    p_list.insert(1,author)
    s1 = pd.Series(p_list)
    s1 = s1.str.strip()
    s1 = s1.dropna()
    s2 = s1.map(len)
    s2_1quantile = int(s2.quantile(0.25))
    s2_3quantile = int(s2.quantile(0.5))
    quant_range = 5*(s2_3quantile - s2_1quantile)
    median = int(s2.median())
    lower_bound = median - quant_range
    upper_bound = median + quant_range

    outliers = list(s2.loc[s2 > upper_bound].index)

    if 2 in outliers:
        s1 = s1.drop(2)
        outliers.remove(2)


    for i in outliers:

        s1.loc[i] = s1.loc[i].split("\n")

        indexes = []
        for i2 in range(len(s1.loc[i])):
            if s1.loc[i][i2] == '':
                indexes.append(i2)

        for index in sorted(indexes, reverse=True):
            del s1.loc[i][index]

        s1.loc[i] = s1.loc[i][0]
    outlier = s1.map(len).max()

    #file = open(f'{CWD}bad_htmls.txt','w')

    if outlier < 300:
        print(f'OUTLIER ERROR: {date} - {author} - {url}')
    elif date == 'DATE_ERROR':
        print(f'DATE_ERROR: {date} - {author} - {url}')
    elif author == 'AUTHOR_ERROR':
        print(f'AUTHOR_ERROR: {date} - {author} - {url}')
    else:
        file = f'{CWD}{date} - {author}.csv'
        s1.to_csv(file,index=False)

        #file.write(f'{date} - {author} - {url}')
    #file.close()





main('https://www.federalreserve.gov/boarddocs/speeches/1996/19961219.htm')
