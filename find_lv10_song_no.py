path_lv10 = './lv10_list.txt'
path_s_t = './song_no_title.txt'
path_10_no = './lv10_song_no.txt'

def isInt(s):#整数変換可能か判定
    try:
        int(s,10)
    except:
         return False
    else:
         return True

sn_list = []
with open(path_s_t) as g:
    for lines in g:
        line = lines.split("\t")
        sn_list.append([line[0], line[1][:-1]])

lv10_list = []
with open(path_lv10) as f:
    ura = False#裏譜面
    for line in f:
        level = 4
        sn = -1
        if line[-6:-1] == "(裏譜面)": #裏譜面抽出
            ura = True
            line = line[:-6]
        else:
            ura = False
            line = line[:-1]
        for s in sn_list:
            if s[1] == line:
                sn = s[0]
        if ura:
            level = 5
        if sn == -1:
            print("not found",line)
        lv10_list.append([str(sn),str(level)])
print(lv10_list)
lv10_list = sorted(lv10_list, key=lambda x: int(x[0]))
print("sorted")
print(lv10_list)
length = len(lv10_list)
with open(path_10_no, mode='x') as h:
    for i in range(length):
        h.write('\n'+lv10_list[i][0]+'\t'+lv10_list[i][1])
        
        