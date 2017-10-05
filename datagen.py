#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 07:13:18 2017

@author: rpujari
This program expects 1 argument => Output File
"""

import sys
import time
import re
import datetime
from ast import literal_eval # This is to convert string into regex


outputFile = "datagenout.txt"

if(len(sys.argv) > 1):
    outputFile = sys.argv[1]

config = {}
# Read Configuration File
with open("datagen.config", "r") as file:
    for line in file:
        attr = [x.strip() for x in line.split('=')]
        if(len(attr)>1):
            config[attr[0]]=attr[1]
        
# Time interval between sample events
interval = int(config['interval'])
# timestamp token in raw event that needs to be replaced
timestamp_token = literal_eval(config['timestamp_token'])
# the timeformat of replaced token
timestamp_format = config['timestamp_format']
timestamp = re.compile(timestamp_token)

while True:
    with open("sampledata.txt", "r") as file: 
        with open(outputFile,"a") as output:
            for line in file:
                currentTime = datetime.datetime.strftime( datetime.datetime.now(), timestamp_format)
                lineWithCurrentTime = timestamp.sub(currentTime, line)
                print(lineWithCurrentTime, file=output)
                time.sleep(interval)
    