
def rate(eval, score) : #レート計算
    if renda_sec == 0:
        return eval * (score - start_score)**2
    else:  
        if score <= base_score:
            return eval * (score - start_score)**2
        else:
            over_score = score - base_score
            renda_rate = over_score/renda_sec/100. #1秒あたりの回数
            return 100 + (10 * renda_rate/60.)



path_riron = './riron_score.txt'
path_10_no = './score_data_test_for_rate.txt'

sn_list = []
with open(path_riron) as f:
    for lines in f:
        line = lines.split("\t")
        sn_list.append([line[0], line[1], line[2], line[3][:-1], line[4][:-1]])


with open(path_10_no) as g:
    i = 0
    k = -1
    tmp_list = []
    for lines in g:
        if i % 12 == 0:
            i = 1
            k += 1
        elif i == 11:
            tmp_list.append(lines[:-1])
            sn_list[k].append(tmp_list)
            tmp_list = []
            i += 1
        else:
            tmp_list.append(lines[:-1])
            i += 1


search_song_no = 1122

for k in range(len(sn_list)):
    base_score = float(sn_list[k][3])
    max_score = float(sn_list[k][5][0])
    start_score = 750000.
    renda_sec = float(sn_list[k][4])
    renda_rate = 0.
    score_list = sn_list[k][5][1:11]

    a = 100./((base_score - start_score)**2)  #虹曲線の曲率
    max_rate = rate(a, max_score)
    music_rate = 0.
    for your_score in score_list:
        your_score  = float(your_score)
        if int(sn_list[k][0]) == search_song_no:
            print(your_score,":\t",rate(a, your_score),":\t",(rate(a, your_score)-100)/10.*60.)
        music_worst_rate = rate(a ,your_score)
        music_rate += (max_rate - rate(a ,your_score))
    if music_rate == 0:
        music_rate = "     NO DATA     "
    if music_worst_rate == 0:
        music_rate = "     NO DATA     "
    #print("\t" + str(music_rate) + "\t" + "music Diff_rate" + "\t" + sn_list[k][2])
    sn_list[k].append(music_rate)
    sn_list[k].append(music_worst_rate)




path_rate = "./music_rate_list.txt"

with open(path_rate, mode='w') as h:
    for i in range(len(sn_list)):
        if sn_list[i][4] == "0":
            renda = "No_Ren"
            sn_list[i][4] = "0.000"
        else:
            renda = "True"
        if len(sn_list[i][4]) != 5:
            for j in range(5 - len(sn_list[i][4])):
                sn_list[i][4] += "0"
            if float(sn_list[i][4]) >= 10000:
                sn_list[i][4] = sn_list[i][4][0] + "." + sn_list[i][4][2:]
        if sn_list[i][6] == "     NO DATA     ":
            sn_list[i][7] = "     NO DATA     "
        else:
            if float(sn_list[i][6]) < 0:
                sn_list[i][6] = "     NO DATA     "
                sn_list[i][7] = "     NO DATA     "
        h.write('\n'+sn_list[i][0]+'\t'+sn_list[i][1]+'\t'+renda+'\t' + sn_list[i][4] + "\t" + str(sn_list[i][6]) + "\t" + str(sn_list[i][7])+'\t'+sn_list[i][2])