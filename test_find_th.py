import requests
import urllib.parse as par
from bs4 import BeautifulSoup
import re

url = "https://wikiwiki.jp/taiko-fumen/%E5%8F%8E%E9%8C%B2%E6%9B%B2/%E3%81%8A%E3%81%AB"

#urlには
#https://wikiwiki.jp/taiko-fumen/ + quote(収録曲) + / + quote(おに) + / quote(曲名)

#理論値を計算するコード

def check_th_score(num, name, level):

    if level == "5":
        name += "(裏譜面)"
    name_url = par.quote(name)

    url_req = url + "/" + name_url
    print(name  + "\t" + url_req + "\n")


sn_list = [] #星10の情報が格納
path_s_t = "./ac_err_list.txt"
with open(path_s_t) as f:
    for lines in f:
        line = lines.split("\t")
        sn_list.append([line[0], line[1], line[2]])
    
#sn_list = sn_list[:10]

for i in range (len(sn_list)):
    level = sn_list[i][1]
    name = sn_list[i][2]
    check_th_score(i, name, level)#理論値
    #print(sn_list[i])