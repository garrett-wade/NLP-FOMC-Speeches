# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 19:29:10 2018

@author: garrett.wade
"""
import os
import json
import re
from collections import Counter
import pandas as pd

def fileList(dir):
    '''
    Creates list of filenames in a given folder.
    dir -- directory containing files to be listed
    '''
    files = []
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        files.append(filename)

    return files

CWD = os.getcwd()

list_files = fileList(r'All Speeches')
list_speakers = []
list_positions = []
list_speechLen = []

for file in list_files:
    filepath = (CWD + "\\All Speeches\\" + file)
    with open(filepath) as json_file:
        data = json.load(json_file)
        
        speaker = data['Speaker']
        date = data['Date']
        speech = data['Speech']
        
        re_position = re.compile(r'(Vice\s+)?\w+\s+')
        re_position = re.search(re_position, speaker)
        position = re_position.group()
        list_positions.append(position)
        
        re_speaker = re.compile(r'(\w+ \w+\. \w+|\w+ \w+)$')
        re_speaker = re.search(re_speaker, speaker)
        if re_speaker:
            speaker = re_speaker.group()
            list_speakers.append(speaker)
            
        list_speechLen.append(len(speech))
        
counter_postitions = Counter(list_positions)
counter_speakers = Counter(list_speakers)
series_speechLen = pd.Series(list_speechLen)

avg_speechLen = series_speechLen.mean()
max_speechLen = series_speechLen.max()
min_speechLen = series_speechLen.min()
std_speechLen = series_speechLen.std()
var_speechLen = series_speechLen.var()1
        

