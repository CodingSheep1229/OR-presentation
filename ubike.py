# -*- coding: utf-8 -*-
import sys
import importlib
import requests
importlib.reload(sys)
import json
import gzip
import urllib.request
import math
from openpyxl import Workbook
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
cmd = "r < map1.r --save"
os.system(cmd)

ssl._create_default_https_context = ssl._create_unverified_context
url = 'http://data.taipei/youbike'
data = urllib.request.urlretrieve(url, "data.gz")
jdata = gzip.open('data.gz', 'r').read()
data = json.loads(jdata)

pos = [] 
num = 0
wb=Workbook()


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
close_site = []

for site in data["retVal"]:
    if data["retVal"][site]["sarea"] == "大安區" and haversine(float(data["retVal"][site]["lng"]),float(data["retVal"][site]["lat"]),121.541208,25.020953) <= 1000:
        pos.append([])
        pos[num].append(data["retVal"][site]["lng"])
        pos[num].append(data["retVal"][site]["lat"])
        num += 1
        available.append(data["retVal"][site]["sbi"])
        totalcap.append(data["retVal"][site]["tot"])
        percentage = float(data["retVal"][site]["sbi"])/float(data["retVal"][site]["tot"])
        # print(num,data["retVal"][site]["sna"],data["retVal"][site]["tot"])
        close_site.append(data["retVal"][site]["snaen"])
        if percentage >= 0.8:
            In.append(0)
            Out.append(1)
        elif percentage <= 0.2:
            In.append(1)
            Out.append(0)
        else:
            In.append(1)
            Out.append(1)


dis = []
for i in range(num):
    dis.append([])
    for j in range(num):
        d = haversine(float(pos[i][0]),float(pos[i][1]),float(pos[j][0]), float(pos[j][1]))
        dis[i].append(d)

sheet = wb.active 
sheet.title = 'Sheet1'
sheet.append(close_site)
sheet.append(totalcap)
sheet.append(available)
wb.save("dis.xlsx")


P=30
S=20

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
#now = time.strftime('%m-%d-%H-%M-%S',datetime.datetime.now().timetuple())
os.system('touch ./final'+now+'.dat')
file = open('./final'+now+'.dat','w')
file.write(temp)
file.close()
dofile = open('./dofile','w')
dofile.write('option solver "../cplex";\nmodel final.mod;\ndata final'+now+'.dat;\nsolve;\ndisplay{s in 1..S} sum{i in 1..N,j in 1..N} K[i,j,s] * i;\ndisplay{s in 1..S} sum{i in 1..N,j in 1..N} K[i,j,s] * j;\ndisplay{s in 1..S} sum{i in 1..N,j in 1..N} K[i,j,s] * Load[i,j,s];')
dofile.write('display {i in 1..N} Available_bike[i]/ Total_cap[i];')
dofile.close()
cmd = '../ampl < dofile > result'+ now
os.system(cmd)

def is_Num(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False


file = open("result",'r')
b_s = []
e_s = []
wb=Workbook()
sheet = wb.active 
sheet.title = 'Sheet1'


rr = file.read()
ms = rr.split('\n')
for i in range(0,len(ms)):
    mss = ms[i].split(' ')
    cnt = 0
    if is_Num(mss[0]) or mss[0] == '':
        for j in range(len(mss)):
            if is_Num(mss[j]):
                cnt += 1
                if cnt is 2:
                    b_s.append(mss[j])
                
dis = []
sheet.append(dis)
for i in range(len(b_s)):
    if(i % (S) == 0  and i != 0):
        sheet.append(dis)
        dis = []

    dis.append(b_s[i])
sheet.append(dis)
wb.save("result.xlsx")
wb.close()
file.close()

cmd = "r < map2.r --save "
os.system(cmd)

print("DONE")

# cmd = "open result.png"
# os.system(cmd)

# cmd = "open original.png"
# os.system(cmd)

# cmd = "open result" + now
# os.system(cmd)

os.system('git add *')
os.system('git commit -m "hi"')
os.system('git push origin master')