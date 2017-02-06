# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@ author: Man Peng

This program puts all json files in folder, say, 'json_folder', containing
    square footage, stories, vintage information into one file, say, 'outputfile.csv'

Sample Usage:

>>> loadSomePropertyInfo2csv("json_folder", 'outputfile.csv')
"""

import json, os
import numpy as np
import fnmatch
import warnings
import re


def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def loaddict2jsonfile(dic, tojson_filename):
    """
    This function loads a dic into tojson_filename file
    loaddict2jsonfile(my_dictionary, 'myjson.json')
    """
    with open(tojson_filename, mode='w') as feedsjson:
      json.dump(dic, feedsjson, indent=4)

def createCSVfile(csvfile, header):
    if not(os.path.isfile(csvfile)):
        f = open(csvfile, 'a')
        f.write(header+"\n")
        f.close()

def write2csv(csvfile, header, line):
    createCSVfile(csvfile, header)
    if os.path.isfile(csvfile):
        f = open(csvfile, 'a')
        f.write(line+"\n")
        f.close()

## The following two functions are for evaluating the stories if some
    ## info was given in words or fractions
    ## e.g. stories field info was given '2 3/4 stories'
def evalFraction(x):
    """ for example, x = '1/2' """
    if len(re.findall(r'[0-9]/[0-9]', x))>=1:
        x_ = re.findall(r'[0-9]/[0-9]', x)[0]
        if len(x_.split('/')) == 2:
            x_new = float(x_.split('/')[0]) / float(x_.split('/')[1])
            return x_new

def evalFration2(x):
    characters = re.findall(r'[a-zA-Z]',x)
    for c in characters:
        x = x.replace(c, '')
    x = x.strip()
    x2 = x.split(' ')
    x2 = filter(lambda x: x != '', x2)
    sum_ = 0.00
    for c in x2:
        if len(c.split('/')) < 2:
            sum_ += float(c)
        else:
            if evalFraction(c) != None:
                sum_ += evalFraction(c)
    # print sum_
    return sum_


def loadSomePropertyInfo2csv(jsonfolder, csvfile):
    jsonfiles = os.listdir(os.path.join(os.getcwd(), jsonfolder))
    # make sure files are json files
    jsonfiles = filter(lambda x: fnmatch.fnmatch(x.lower(), "*.json"), jsonfiles)
    cache = {}
    for jfile in jsonfiles:
        jinfo = loadJson(os.path.join(os.path.join(os.getcwd(), jsonfolder, jfile)))
        latestkey = max(jinfo.keys())
        if latestkey in cache:
            continue
        else:
            cache[latestkey]=1
            csvinfo_dict = {}
            try:
                csvinfo_dict['year_built'] = jinfo[max(jinfo.keys())]['year_built']
            except KeyError:
                csvinfo_dict['year_built'] = ""
            try:
                storiesN = jinfo[max(jinfo.keys())]['stories']
                csvinfo_dict['stories'] = str(evalFration2(storiesN))
                csvinfo_dict['stories_original'] = storiesN
            except KeyError:
                csvinfo_dict['stories'] = "0"
                csvinfo_dict['stories_original'] = ""
            try:
                csvinfo_dict['gross_area_sqft'] = jinfo[max(jinfo.keys())]['GrossArea']
            except KeyError:
                csvinfo_dict['gross_area_sqft'] = ""
            try:
                csvinfo_dict['living_area_sqrt'] = jinfo[max(jinfo.keys())]['LivingArea']
            except KeyError:
                csvinfo_dict['living_area_sqrt'] = ""
            try:
                x = jinfo[max(jinfo.keys())]['physical_address']
                x_ = x.split(',')
                x_ = map(lambda x: x.strip(), x_)
                csvinfo_dict['physical_address'] = ", ".join(x_)
            except KeyError:
                csvinfo_dict['physical_address'] = ""
            header = csvinfo_dict.keys()
            line = map(lambda x: csvinfo_dict[x], header)
            header = map(lambda x: '"'+x+'"', header)
            # The following is to remove the , in case it's there since this is written
                # into a csv file (comman deliminated file)
            line = map(lambda x: '"'+x+'"', line)
            ",".join(line)
            write2csv(csvfile, ",".join(header), ",".join(line))

