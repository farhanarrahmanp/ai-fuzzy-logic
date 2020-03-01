#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 19:51:45 2019

@author: Farhan
"""

"""
Model Fuzzy Sugeno
"""

import pandas as pd #Membaca file csv
import csv #Buat menulis output file


"""
Menentukan Titik followerCount nano, micro, & medium
"""
def mediumfollowerCount(followerCount):
    if(followerCount >= 75000):
        return 1
    elif(followerCount <= 65000):
        return 0
    else:
        return (followerCount - 75000)/(75000-65000)
    
def microfollowerCount(followerCount):
    if(followerCount <= 25000 or followerCount > 75000):
        return 0
    elif(followerCount > 25000 and followerCount <= 35000):
        return (followerCount - 25000) / (35000-25000)
    elif(followerCount > 35000 and followerCount <= 65000):
        return 1
    else:
        return ((75000 - followerCount)/(75000-65000))
     
def nanofollowerCount(followerCount):
    if(followerCount <= 25000):
        return 1
    elif(followerCount >= 35000):
        return 0
    else:
        return ((35000 - followerCount)/(35000-25000))
    
    
"""
Menentukan Titik engagementRate nano, micro, & medium
"""
def mediumengagementRate(engagementRate):
    if(engagementRate >= 7.5):
        return 1
    elif(engagementRate <= 6.5):
        return 0
    else:
        return (engagementRate - 6.5)/(7.5-6.5)
    
def microengagementRate(engagementRate):
    if(engagementRate <= 2.5 or engagementRate > 7.5):
        return 0
    elif(engagementRate > 2.5 and engagementRate <= 3.5):
        return (engagementRate - 2.5) / (3.5-2.5)
    elif(engagementRate > 3.5 and engagementRate <= 6.5):
        return 1
    else:
        return ((7.5 - engagementRate)/(7.5-6.5))
     
def nanoengagementRate(engagementRate):
    if(engagementRate <= 2.5):
        return 1
    elif(engagementRate >= 3.5):
        return 0
    else:
        return ((3.5 - engagementRate)/(3.5-2.5))

    
"""
Main program
"""
influencers = pd.read_csv("influencers.csv", sep=',',header =0)

colId = influencers['id'].values.tolist()
colFollowerCount = influencers['followerCount'].values.tolist()
colEngagementRate = influencers['engagementRate'].values.tolist()

colInfluencers = []

colInfluencers.append(colId)
colInfluencers.append(colFollowerCount)
colInfluencers.append(colEngagementRate)

matrixInfluencers = []

matrixFollowerCount = []
matrixEngagementRate = []


"""
Melakukan Fuzzification
"""
for i in range(len(colFollowerCount)):
    folCount = []
    folCount1 = nanofollowerCount(colFollowerCount[i])
    folCount2 = microfollowerCount(colFollowerCount[i])
    folCount3 = mediumfollowerCount(colFollowerCount[i])
    folCount.append(folCount1)
    folCount.append(folCount2)
    folCount.append(folCount3)
    matrixFollowerCount.append(folCount)
    
for i in range(len(colEngagementRate)):
    engRate = []
    engRate1 = nanoengagementRate(colEngagementRate[i])
    engRate2 = microengagementRate(colEngagementRate[i])
    engRate3 = mediumengagementRate(colEngagementRate[i])
    engRate.append(engRate1)
    engRate.append(engRate2)
    engRate.append(engRate3)
    matrixEngagementRate.append(engRate)

for i in range(len(colId)):
    matrixInfluencers.append({
                'id' : colInfluencers[0][i],
                'followerCount' : matrixFollowerCount[i],
                'engagementRate' : matrixEngagementRate[i]
            })

    
"""
fungsi keanggotaan untuk follower dan engagement
"""    
print("Derajat Keanggotaan Follower")
print("\n")
i = 1
for d in matrixInfluencers:
        print("id", i)
        if(d['followerCount'][0]) > 0:
            print("Low", d['followerCount'][0])
        if(d['followerCount'][1])> 0:
            print("Med", d['followerCount'][1])
        if(d['followerCount'][2]) > 0:
            print("Hi", d['followerCount'][2])
        print(d['followerCount'])
        print("")
        i = i+1
print("")        
print("\nDerajat Keanggotaan Engagement")
print("\n")
i = 1
for d in matrixInfluencers:
        print("id",i)    
        if(d['engagementRate'][0]) > 0:
            print("Low", d['engagementRate'][0])
        if(d['engagementRate'][1])> 0:
            print("Med", d['engagementRate'][1])
        if(d['engagementRate'][2]) > 0:
            print("Hi", d['engagementRate'][2])
        print(d['engagementRate'])
        print("")
        i = i+1


"""
Inference dan Defuzzification dengan Metode MAX
"""
minFE = []

for d in matrixInfluencers:
    arrminFE = []
    minFE1 = 0
    
    #nano FC & nano ER
    if(d['followerCount'][0] !=0 and d['engagementRate'][0] != 0):
        if(d['followerCount'][0] > d['engagementRate'][0]):
            minFE1 = d['engagementRate'][0]
        elif(d['followerCount'][0] < d['engagementRate'][0]):
            minFE1 = d['followerCount'][0]
    
    #nano FC & micro ER
    minFE2 = 0
    if(d['followerCount'][0] != 0 and d['engagementRate'][1] != 0):
        if(d['followerCount'][0] > d['engagementRate'][1]):
            minFE2 = d['engagementRate'][1]
        elif(d['followerCount'][0] < d['engagementRate'][1]):
            minFE2 = d['followerCount'][0]
    
    #nano FC & medium ER  
    minFE3 = 0
    if(d['followerCount'][0] != 0 and  d['engagementRate'][2] != 0):
        if(d['followerCount'][0] > d['engagementRate'][2]):
            minFE3 = d['engagementRate'][2]
        elif(d['followerCount'][0] < d['engagementRate'][2]):
            minFE3 = d['followerCount'][0]
    
    #micro FC & nano ER
    if(d['followerCount'][1] != 0 and d['engagementRate'][0]!= 0):
        if(d['followerCount'][1] > d['engagementRate'][0]):
            minFE1 = d['engagementRate'][0]
        elif(d['followerCount'][1] < d['engagementRate'][0]):
            minFE1 = d['followerCount'][1]
    
    #micro FC & micro ER
    if(d['followerCount'][1] != 0 and d['engagementRate'][1]!=0):
        if(d['followerCount'][1] > d['engagementRate'][1]):
            minFE2 = d['engagementRate'][1]
        elif(d['followerCount'][1] < d['engagementRate'][1]):
            minFE2 = d['followerCount'][1]
    
    #micro FC & medium ER    
    if(d['followerCount'][1] != 0 and d['engagementRate'][2] != 0):
        if(d['followerCount'][1] > d['engagementRate'][2]):
            minFE3 = d['engagementRate'][2]
        elif(d['followerCount'][1] < d['engagementRate'][2]):
            minFE3 = d['followerCount'][1]
    
    #medium FC & nano ER
    if(d['followerCount'][2] != 0 and d['engagementRate'][0] != 0):
        if(d['followerCount'][2] > d['engagementRate'][0]):
            minFE1 = d['engagementRate'][0]
        elif(d['followerCount'][2] < d['engagementRate'][0]):
            minFE1 = d['followerCount'][2]
    
    #medium FC & micro ER
    if(d['followerCount'][2] != 0 and d['engagementRate'][1]!= 0):
        if(d['followerCount'][2] > d['engagementRate'][1]):
            minFE2 = d['engagementRate'][1]
        elif(d['followerCount'][2] < d['engagementRate'][1]):
            minFE2 = d['followerCount'][2]
    
    #medium FC & nano ER    
    if(d['followerCount'][2] != 0 and d['engagementRate'][2]!=0):
        if(d['followerCount'][2] > d['engagementRate'][2]):
            minFE3 = d['engagementRate'][2]
        elif(d['followerCount'][2] < d['engagementRate'][2]):
            minFE3 = d['followerCount'][2]

    arrminFE.append(minFE1)
    arrminFE.append(minFE2)
    arrminFE.append(minFE3)
    minFE.append(arrminFE)
        
FEindex = []  
for i in range(len(minFE)):
    FEindex.append(max(minFE[i]))
    
defuzzification = []
for i in range(len(colId)):
    defuzzification.append({
                'id' : colInfluencers[0][i],
                'idxMax' : FEindex[i]
            })

    
"""
Rule
"""    
sorted_idxMax = sorted(defuzzification, key=lambda d: d['idxMax'], reverse=True)
idxLayak = []
idxTidakLayak = []
for d in sorted_idxMax:
    if(d['idxMax']>=0.5):
        idxLayak.append({
                'id' : d['id'],
                'idxMax': d['idxMax']
                })
    else:
        idxTidakLayak.append({
                'id':d['id'],
                'idxMax':d['idxMax']
                })

print("influencers terbaik")
for d in idxLayak:
    print(d['id'])

print("\ninfluencers tidak layak")    
for d in idxTidakLayak:
    print(d['id'])


"""
Memasukan data 20 influencers terbaik ke dalam file csv
"""
i=0
with open('chosen.csv', 'w') as f:
    employee_writer1 = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    print("\n20 influencers terbaik")
    for d in sorted_idxMax:
        tulis = d['id']
        employee_writer1.writerow([tulis])
        print(tulis)
        i = i+1
        if(i==20):
            break

    
    

    