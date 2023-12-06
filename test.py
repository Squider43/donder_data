base_score = 1001200.
max_score = 1011400.
start_score = 600000.
renda_sec = 1.907
renda_rate = 0.

a = 100./((base_score - start_score)**2)
def rate(score) :
    if score <= base_score:
        return a * (score - start_score)**2
    else:
        over_score = score - base_score
        renda_rate = over_score/renda_sec/100. #1秒あたりの回数
        return 100 + (10 * renda_rate/60.)
max_count = int((renda_sec * 6000 + base_score - start_score)/1000)

max_rate = rate(max_score)
score = [
1004620,
992770,
970650,
944490,
916630,
894640,
873460,
855890,
840770,
828670
]
'''
for i in range(max_count + 1):
    your_score = i*1000+start_score
    print(your_score,":\t",rate(your_score),":\t",(rate(your_score)-100)/10.*60.)
'''
music_rate = 0
for your_score in score:
    print(your_score,":\t",rate(your_score),":\t",(rate(your_score)-100)/10.*60.)
    music_rate += (max_rate - rate(your_score))
print(music_rate)
    

