import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager
import math

matplotlib.rcParams['font.family'] = 'Hiragino Sans GB'

path_riron = './music_rate_list.txt'

sn_list = []
with open(path_riron) as f:
    for lines in f:
        line = lines.split("\t")
        sn_list.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6][:-1]])

plt.figure(figsize=(8, 8))
for i in range(len(sn_list)):
    if sn_list[i][4] != "     NO DATA     ":
        x = float(sn_list[i][5])
        #y = math.sqrt(float(sn_list[i][4]))
        y = float(sn_list[i][4])
        label = sn_list[i][6]
        plt.text(x, y, label, fontsize=4)
        plt.scatter(x, y, marker='o', label=label)
plt.xlabel('rate_at_rank10000')
plt.ylabel('music_rate')
plt.show()
#plt.figure(figsize=(6,10))
