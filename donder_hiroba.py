import requests
import re
from bs4 import BeautifulSoup

path_lv10 = "./lv10_song_no.txt"
lv10songs = [] #song_no情報格納
with open(path_lv10) as f:
    for lines in f:
        res = [0,0]
        line = lines.split("\t")
        res[0] = int(line[0])
        res[1] = int(line[1][:-1])
        lv10songs.append(res)
#print(lv10songs)
url_myscore = 'https://donderhiroba.jp/score_detail.php'
url_rank = 'https://donderhiroba.jp/rank_detail.php'

def access_myscore(): #データから必要な情報を抜き取るもの
    params = {
        #'genre': genre, 
        'level': level, 
        "song_no": song_no
    }

    req = requests.get(url_myscore, params=params, headers=headers)

    html = req.text
    Soup = BeautifulSoup(html, "html.parser")

    #print("Json",req.text)
    ranking = Soup.find("div", attrs={"class": "ranking"})#全国ランキング
    if ranking is None:
        my_score_data.append([-1, -1, -1, -1, -1, -1, -1])
    else:
        high_score = Soup.find("div", attrs={"class": "high_score"})#ハイスコア
        good_cnt = Soup.find("div", attrs={"class": "good_cnt"})#良の数
        combo_cnt = Soup.find("div", attrs={"class": "combo_cnt"})#最大コンボ数O
        ok_cnt = Soup.find("div", attrs={"class": "ok_cnt"})#可の数
        pound_cnt = Soup.find("div", attrs={"class": "pound_cnt"})#連打数
        ng_cnt = Soup.find("div", attrs={"class": "ng_cnt"})#不可の数
        my_score_data.append([ranking.text[2:-2], re.sub(r"\D", "", high_score.text), re.sub(r"\D", "", good_cnt.text), re.sub(r"\D", "", combo_cnt.text), re.sub(r"\D", "", ok_cnt.text), re.sub(r"\D", "", pound_cnt.text), re.sub(r"\D", "", ng_cnt.text)])

def access_ranking(i, p):

    s_num = lv10songs[i][0]
    level = lv10songs[i][1]

    params_rank = {
        'rank': rank, 
        'area': area, 
        'song_no': s_num,
        'level': level,
        'page': p,
    }
    req = requests.get(url_rank, params=params_rank, headers=headers)

    html = req.text
    Soup = BeautifulSoup(html, "html.parser")

    #print("Json",req.text)
    idx = 0
    for score in Soup.find_all("div", attrs={"class": "rankingDetailScore"}):#全国ランキングの詳しいスコア
        score_num = re.sub(r"\D", "", score.text)
        #print(score_num)
        ranking_data[i][(p-1)*10 + idx] = score_num
        idx += 1



headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Set-Cookie": "_token_v2=ncn23h0pp6ggvurg7o6r3bpa35; expires=Mon, 01-Jan-2024 18:18:27 GMT; path=/; domain=donderhiroba.jp",
        "Cookie": "_gid=GA1.2.1685829405.1701572607; OptanonAlertBoxClosed=2023-12-03T03:28:24.027Z; _token_v2=fe19vucnejnu870h1ac9euq167; _gat_UA-69110980-5=1; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Dec+04+2023+06%3A23%3A54+GMT%2B0900+(%E6%97%A5%E6%9C%AC%E6%A8%99%E6%BA%96%E6%99%82)&version=6.36.0&isIABGlobal=false&hosts=&genVendors=&consentId=1817849f-c451-43c9-804c-ef6072acae20&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B26; _ga=GA1.1.834249191.1701572607; _ga_V2WFDXJRK8=GS1.1.1701638624.5.1.1701638643.41.0.0",
}
#cookieはどんだー広場ログイン後、アカウント選択時のhttps_reqのヘッダーのものをつかう


#song_no_max = 1237 #最大値
song_no_max = 1237
genre_max = 7 #ジャンル最大値
level_max = 5 #レベル最大値
page_max = 1 #ページ最大値

taiko_no = 490008833663
genre = 6
level = 4
song_no = 354
area = 0
page = 0
rank = 3

my_score_data = []
ranking_data = [["0"] * 10 for _ in range(song_no_max)] #全ての曲の成績を10000個
'''
for s_num in range(song_no_max): #自分の成績をmy_score_dataに格納
    song_no = s_num + 1
    access_myscore()
print(my_score_data)

'''

for i in range(len(lv10songs)):
    print("now songno is",lv10songs[i][0])
    for p in range(1,page_max+1):
        access_ranking(i, p)
print(ranking_data[0])


path = './score_data_10.txt'

with open(path, mode='x') as f:
    for i in range(len(lv10songs)):
        title = "\t"+"Song_Number is"+"\t"+str(lv10songs[i][0])+"\n"
        f.write(title)
        f.write('\n'.join(ranking_data[i]))




#どんだーひろばは1万位まで取得可能
#つまり、データを10000個まで拾える
#ログイン時間は10分が目安

#誰かがアクセスすれば、データを取得可能
#方針としては、ある人のある曲に対する偏差値のようなものを実装する
#偏差値はある曲の10000人の成績から推測する
#
#10000位のスコアを平均、1位のスコアを偏差値100となるように設定