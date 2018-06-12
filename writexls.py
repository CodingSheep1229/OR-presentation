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

def is_Num(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

file = open("result06-09-20-08-58",'r')

b_s = []
e_s = []
wb=Workbook()
sheet = wb.active 
sheet.title = 'Sheet1'


rr = file.read()
ms = rr.split('\n')
for i in range(5,len(ms)):
    mss = ms[i].split(' ')
    cnt = 0
    if is_Num(mss[0]) or mss[0] == '':
        for j in range(len(mss)):
            if is_Num(mss[j]):
                cnt += 1
                if cnt is 2:
                    b_s.append(mss[j])
                
print(b_s)
S = 20
dis = []
sheet.append(dis)
for i in range(len(b_s)):
    if(i % S == 0 and i != 0):
        sheet.append(dis)
        dis = []
    dis.append(b_s[i])
sheet.append(dis)
wb.save("result.xlsx")
wb.close()

file.close()
