#!/bin/python
import pandas as pd
import sys

# load names
namesDB = pd.read_csv('registrants.txt')
#print(namesDB.describe())
countTotal = namesDB.Name.count()

# load gender database
males = pd.read_csv('gender_names/male_uniq.csv',skiprows=5,names=['Name','count'])
males['gender']= 'male'
#print(males.describe())
females = pd.read_csv('gender_names/female_uniq.csv',skiprows=5,names=['Name','count'])
females['gender']= 'female'
#print(females.describe())
#unisexs = pd.read_csv('gender_names/unidex_uniq.csv')
#print(unisexs.describe())

genderDB = pd.concat([males,females],ignore_index=True)

# first names of registrants
firstNames = namesDB.Name.str.lower().str.split().str.get(0)
namesDB['firstname'] = firstNames
genderFirstNames = genderDB.Name.str.lower().str.split().str.get(0)
genderDB['firstname'] = genderFirstNames

#sys.exit(0)

def aggFunc(x) :
    return x.tolist()[0] / x.tolist()[1]

countM = 0
countF = 0
countA = 0
countU = 0
regGenders = list()
for fname in list(firstNames) :
    recsForNameDF = genderDB[ genderDB['firstname'] == fname ]
    #print( recsForNameDF )
    #print( 'Working on name: {}'.format(fname) )
    if len(recsForNameDF) > 2 :
        print('WARN: more than two entries for name: {}'.format(fname) )
    if len(recsForNameDF) == 2 :
        print('NOTICE: ambiguous name found: {}'.format(fname) )
        countA = countA + 1
        isLikelyMaleDF = recsForNameDF.groupby('firstname').agg( { 'count' : aggFunc } )
        isLikelyMale = isLikelyMaleDF['count'].ix[ fname ]
        if isLikelyMale >= 1 :
            countM = countM + 1
            regGenders.append([fname,'M'])
        else :
            countF = countF + 1
            regGenders.append([fname,'F'])
    else :
        if (recsForNameDF['gender'] == 'male' ).all() :
            print('NOTICE: male name found: {}'.format(fname) )
            countM = countM + 1
            regGenders.append([fname,'M'])
        else :
            countF = countF + 1
            print('NOTICE: female name found: {}'.format(fname) )
            regGenders.append([fname,'F'])

print('COUNTS:')
print('total registrants: {}'.format(countTotal) )
print('total resolved registrants: {}'.format(countM+countF) )
print('male: {}({:f})	female: {}({:f})	ambiguous: {}'.format(countM,float(countM)/countTotal,countF,float(countF)/countTotal,countA) )

#regFirstNameAndGenderList = pd.DataFrame( regGenders , columns=['firstname','gender'])
#regFirstNameAndGenderList.to_csv('firstNamesAndGenders.csv',index=False)

# exclude abmiguous names
#ambi = pd.merge(males,females,how='inner',on=['lower'])
#ambi['firstname'] = ambi.Name.str.lower()
#mORf = genderDB[ ~ genderDB.firstname.isin(ambi.firstname) ].head()

# use inner join to get answers
#attendeeGender = pd.merge(mORf[['firstname','gender']],pd.DataFrame(firstNames)[['Name']],how='inner', left_on=['firstname'],right_on=['Name'])

