path_lv10 = './lv10.txt'
path_lv10_list = './lv10_list.txt'

lv10songs = []
with open(path_lv10) as f:
    for lines in f:
        exist = False
        line = lines.split("\t")
        for s in lv10songs:
            if s == line[0]:
                exist = True
                break
        if not exist:
            lv10songs.append(line[0])
lv10songs = sorted(lv10songs, key=lambda x: x[0])
with open(path_lv10_list, mode='x') as g:
        g.write('\n'.join(lv10songs))


