# -*- coding: utf-8 -*-
import sys
import importlib
import requests
importlib.reload(sys)
import json
import gzip
import urllib.request
import math
#from openpyxl import Workbook
import os
import ssl
import time
import datetime
import calendar

# context = ssl._create_unverified_context()
# data= urllib.request.urlopen('http://data.taipei/youbike',context=context).read()
# output = data.decode('utf-16')
# print(output)
# exit()
ssl._create_default_https_context = ssl._create_unverified_context
url = 'http://data.taipei/youbike'
data = urllib.request.urlretrieve(url, "data.gz")
jdata = gzip.open('data.gz', 'r').read()
data = json.loads(jdata)

pos = [] 
num = 0
# wb=Workbook()


def haversine(lon1, lat1, lon2, lat2): 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r * 1000

In=[]
Out=[]
available=[]
totalcap=[]

for site in data["retVal"]:
    if(data["retVal"][site]["sarea"] == "大安區"):
        pos.append([])
        pos[num].append(data["retVal"][site]["lat"])
        pos[num].append(data["retVal"][site]["lng"])
        num += 1
        available.append(data["retVal"][site]["sbi"])
        totalcap.append(data["retVal"][site]["tot"])
        percentage = float(data["retVal"][site]["sbi"])/float(data["retVal"][site]["tot"])
        if percentage <= 0.5:
            In.append(1)
            Out.append(0)
        elif percentage > 0.5:
            In.append(0)
            Out.append(1)
        else:
            In.append(0)
            Out.append(0)


dis = []
for i in range(num):
    dis.append([])
    for j in range(num):
        d = haversine(float(pos[i][0]),float(pos[i][1]),float(pos[j][0]), float(pos[j][1]))
        dis[i].append(d)




P=30
S=20
num=20


temp=''
temp += 'param N := '+str(num)+';\n'
temp += 'param P := '+str(P)+';\n'
temp += 'param S := '+str(S)+';\n'
temp += 'param Var_cost := 0.1;\n'
temp += 'param Fixed_cost := 500;\n'
temp += 'param Dis:'
for i in range(num):
    temp += '\t'+ str(i+1)
temp += '\t:=\n'
for i in range(num):
    temp += '\t' + str(i+1)
    for j in range(num):
        temp += '\t' + str(dis[i][j])
    temp += '\n'
temp = temp[:-1]+';\n'

temp += 'param In :=\n'
for i in range(num):
    temp += '\t' + str(i+1) + '\t' + str(In[i]) + '\n'
temp = temp[:-1]+';\n'

temp += 'param Out :=\n'
for i in range(num):
    temp += '\t' + str(i+1) + '\t' + str(Out[i]) + '\n'
temp = temp[:-1]+';\n'

temp += 'param Available_bike :=\n'
for i in range(num):
    temp += '\t' + str(i+1) + '\t' + str(available[i]) + '\n'
temp = temp[:-1]+';\n'

temp += 'param Total_cap :=\n'
for i in range(num):
    temp += '\t' + str(i+1) + '\t' + str(totalcap[i]) + '\n'
temp = temp[:-1]+';\n'


now=''
#now = str(calendar.timegm(datetime.datetime.now().timetuple()))
os.system('touch final'+now+'.dat')
file = open('final'+now+'.dat','w')
file.write(temp)
file.close()

os.system('../ampl < dofile > result')
