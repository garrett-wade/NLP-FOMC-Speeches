from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains, keys
import time
from bs4 import BeautifulSoup
import webScrapertest
import html5lib
import datetime

driver = webdriver.Chrome()
driver.get('https://www.federalreserve.gov/newsevents/speeches.htm')
driver.maximize_window()

links = []

source = driver.page_source

raw_html = BeautifulSoup(source, 'html5lib')

for a in raw_html.find_all('a', href=True):
    if a['href'][0:19] == '/newsevents/speech/':
        if a['href'][19:25] != 'speech':
            if a['href'][19] != '2':
                if a['href'][19] != '1':
                    links.append(a['href'])

i = 0
while i < 36:
    driver.find_element_by_css_selector('a[ng-click="selectPage(page + 1, $event)"]').click()


    source = driver.page_source

    raw_html = BeautifulSoup(source, 'html.parser')

    for a in raw_html.find_all('a', href=True):
        if a['href'][0:19] == '/newsevents/speech/':
            if a['href'][19:25] != 'speech':
                if a['href'][19] != '2':
                    if a['href'][19] != '1':
                        links.append(a['href'])

    i +=1

for link in links:
    url = 'https://www.federalreserve.gov' + link
    webScrapertest.main(url)
