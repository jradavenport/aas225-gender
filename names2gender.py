#!/bin/python
import pandas as pd

# load names
namesDB = pd.read_csv('registrants.txt')
print(namesDB.describe())

# load gender database
males = pd.read_csv('gender_names/male_uniq.csv',skiprows=5,names=['Name','count'])
males['gender']= 'male'
print(males.describe())
females = pd.read_csv('gender_names/female_uniq.csv',skiprows=5,names=['Name','count'])
females['gender']= 'female'
print(females.describe())
#unisexs = pd.read_csv('gender_names/unidex_uniq.csv')
#print(unisexs.describe())

genderDB = pd.concat([males,females])

# frist names of registrants
firstNames = namesDB.Name.str.lower().str.split().str.get(0)
namesDB['firstname'] = firstNames
genderFirstNames = genderDB.Name.str.lower().str.split().str.get(0)
genderDB['firstname'] = genderFirstNames

# exclude abmiguous names
ambi = pd.merge(males,females,how='inner',on=['lower'])
ambi['firstname'] = ambi.Name.str.lower()
mORf = genderDB[ ~ genderDB.firstname.isin(ambi.firstname) ].head()

# use inner join to get answers
attendeeGender = pd.merge(mORf[['firstname','gender']],pd.DataFrame(firstNames)[['Name']],how='inner', left_on=['firstname'],right_on=['Name'])

