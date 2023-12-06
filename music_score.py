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
        res[1] = int(line[1])
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

def access_ranking_score_for_test(i, p):

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
    score_list = Soup.find_all("div", attrs={"class": "rankingDetailScore"})#全国ランキングの詳しいスコア
    #print(score_list)
    if len(score_list) == 0:
        for m in range(11):
            #print(i,p,m)
            ranking_data_test[i][m] = "-1"
        return 1
    for k in range(10):
        score_num = re.sub(r"\D", "", score_list[k].text)
        score_list[k] = score_num
    #print(score_list)
    #print("ーーーーーーーーーp is ",p,"ーーーーーーsong_no is ",i)
    if p % 100 == 0:
        idx = p/100
        idx= int(idx)
        ranking_data_test[i][idx] = score_list[0]
    else:
        ranking_data_test[i][0] = score_list[9]



headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Set-Cookie": "_token_v2=ncn23h0pp6ggvurg7o6r3bpa35; expires=Mon, 01-Jan-2024 18:18:27 GMT; path=/; domain=donderhiroba.jp",
        "Cookie": "_token_v2=5tr08dkqprnq3ujvmagre9pak1; _ga_V2WFDXJRK8=GS1.1.1701785219.9.1.1701789257.14.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Dec+06+2023+00%3A14%3A08+GMT%2B0900+(%E6%97%A5%E6%9C%AC%E6%A8%99%E6%BA%96%E6%99%82)&version=6.36.0&isIABGlobal=false&hosts=&genVendors=&consentId=987396ba-b631-40d8-a692-147ff3c5d716&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B26; _ga=GA1.2.756249038.1701536363; _gid=GA1.2.1143686782.1701536363; _gat_UA-69110980-5=1; _ga_V2WFDXJRK8=deleted; OptanonAlertBoxClosed=2023-12-02T17:03:41.473Z",
}
#cookieはどんだー広場ログイン後、アカウント選択時のhttps_reqのヘッダーのものをつかう


#song_no_max = 1237 #最大値
song_no_max = 300
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
ranking_data_test = [["0"] * 11 for _ in range(song_no_max)] #全ての曲の成績を10000個
'''
for s_num in range(song_no_max): #自分の成績をmy_score_dataに格納
    song_no = s_num + 1
    access_myscore()
print(my_score_data)

'''
page_list = [1,100,200,300,400,500,600,700,800,900,1000]
for x in range(len(lv10songs)):
    for p in page_list:
        access_ranking_score_for_test(x, p)
    print("now songno is",lv10songs[x][0],ranking_data_test[x][0])


path = './score_data_test_for_rate.txt'

with open(path, mode='w') as f:
    for i in range(len(lv10songs)):
        title = "\n\t"+"Song_No"+"\t"+str(lv10songs[i][0])+"\n"
        f.write(title)
        f.write('\n'.join(ranking_data_test[i]))




#どんだーひろばは1万位まで取得可能
#つまり、データを10000個まで拾える
#ログイン時間は10分が目安

#誰かがアクセスすれば、データを取得可能
#方針としては、ある人のある曲に対する偏差値のようなものを実装する
#偏差値はある曲の10000人の成績から推測する
#
#10000位のスコアを平均、1位のスコアを偏差値100となるように設定