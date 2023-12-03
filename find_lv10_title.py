path_lv10 = './lv10.txt'
path_lv10_list = './lv10_list.txt'

lv10songs = []
with open(path_lv10) as f:
    for lines in f:
        line = lines.split("\t")
        lv10songs.append(line[0])

with open(path_lv10_list, mode='x') as g:
        g.write('\n'.join(lv10songs))


