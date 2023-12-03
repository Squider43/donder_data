path_song = './song_no_list.txt'
path_s_t = './song_no_title.txt'

def isInt(s):#整数変換可能か判定
    try:
        int(s,10)
    except:
         return False
    else:
         return True

sn_title = []
i = 0
with open(path_song) as f:
    tmp_no = "0"
    for lines in f:
        line = lines.split("\t")
        if i  == 10:
             print(line[-1][-6:-1])
        i += 1
        if line[-1][-6:-1] == "サヨナラ曲": #サヨナラ曲は削除済み
             continue
        elif len(line) == 1: #song_noの目次の時
             continue
        elif not isInt(line[0]): #整数変換が無理ならば前のsong_noを採用
             song = [tmp_no, line[0]]
             sn_title.append(song)
        else: #正常
             tmp_no = line[0]
             song = [line[0], line[1]]
             sn_title.append(song)
             
#print(sn_title)
length = len(sn_title)
with open(path_s_t, mode='x') as g:
    for i in range (length):
        word = sn_title[i][0]+'\t'+sn_title[i][1]
        #print(word)
        g.write("\n"+word)