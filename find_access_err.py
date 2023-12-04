import requests
import urllib.parse as par
from bs4 import BeautifulSoup
import re

sn_list = [] #星10の情報が格納
path_s_t = "./riron_score_last.txt"
with open(path_s_t) as f:
    for lines in f:
        line = lines.split("\t")
        if line[4][:-1] == "-1":
           sn_list.append([line[0], line[1], line[2], line[3]])

path_s_t_a = "./ac_err_list.txt"
print_data = []
with open(path_s_t_a, mode="w") as g:
    for i in range (len(sn_list)):
        word = "\n" + sn_list[i][0] + "\t" + sn_list[i][1] + "\t" + sn_list[i][2]+ "\t" + sn_list[i][3]
        g.write(word)