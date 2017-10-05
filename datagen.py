#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 07:13:18 2017

@author: rpujari
This program expects 1 argument => Output File
"""

import sys
import os
import daemon
import time
import re
import datetime
from ast import literal_eval # This is to convert string into regex


outputFilePath = "./datagenout.txt"

if(len(sys.argv) > 1):
    outputFilePath = sys.argv[1]
    outputDir, outputFile = os.path.split(os.path.expanduser(outputFilePath))
    if os.path.exists(outputDir) == False:
        sys.exit("The directory path doesnot exist")
        

testmode = False
if(len(sys.argv) > 2):
    if(sys.argv[2] == 'testmode'):
        testmode = True

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

def write_events():
    while True:
        with open("sampledata.txt", "r") as file: 
            with open(outputFilePath,"a") as output:
                for line in file:
                    currentTime = datetime.datetime.strftime( datetime.datetime.now(), timestamp_format)
                    lineWithCurrentTime = timestamp.sub(currentTime, line)
                    if(testmode == True):
                        print(lineWithCurrentTime)
                    else:
                        output.write(lineWithCurrentTime)  
                    time.sleep(interval)

def run():
    write_events()
        
if __name__ == "__main__":
    run()
    