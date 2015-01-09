# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 16:08:36 2015

@author: james
"""

import numpy as np

file = 'aas225-all-talks.txt'


raw = open(file).read().splitlines()

gender = []
catagory = []
sessionID = []

for i,line in enumerate(raw):
   if i % 5 == 3:
        a, b, = line.split(',')
        catagory.append(a)
        gender.append(b)
   if i % 5 == 0:
        sessionID.append(line[0:3])


