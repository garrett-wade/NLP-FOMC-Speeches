from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains, keys
import time

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import webScraper2test


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
for i in range(1996,2006):
    year = str(i)
    links = []
    html = simpleGet(f'https://www.federalreserve.gov/newsevents/speech/{year}speech.htm')
    raw_html = BeautifulSoup(html, 'html.parser')
    for a in raw_html.find_all('a', href=True):
        if a['href'][0:25] == f'/boarddocs/speeches/{year}/':
            links.append(a['href'])

    for link in links:
        link = 'https://www.federalreserve.gov' + link
        webScraper2test.main(link)
