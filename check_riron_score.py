import requests
import urllib.parse as par
from bs4 import BeautifulSoup
import re

url = "https://wikiwiki.jp/taiko-fumen/%E5%8F%8E%E9%8C%B2%E6%9B%B2/%E3%81%8A%E3%81%AB"

#urlには
#https://wikiwiki.jp/taiko-fumen/ + quote(収録曲) + / + quote(おに) + / quote(曲名)

#理論値を計算するコード

def check_th_score(num, name, level):

    if level == "5":
        name += "(裏譜面)"
    name = par.quote(name)
    
    url_req = url + "/" + name
    if num == "1221":
        url_req = "https://wikiwiki.jp/taiko-fumen/収録曲/おに/Garakuta%20Doll%20Play%28裏譜面%29#double"
    if num == "1223":
        url_req = "https://wikiwiki.jp/taiko-fumen/収録曲/おに/KAGEKIYO%20源平討魔伝メドレー%28裏譜面%29#double"
    req = requests.get(url_req)

    html = req.text
    #html = '<div class="h-scrollable"><table><thead><tr><th colspan="9" style="font-size:20px; text-align:center;">カルメン 組曲一番終曲(裏譜面)</th></tr><tr><th colspan="2" style="text-align:center;">バージョン<a id="notetext_1"  class="note_super tooltip"data-tippy-theme="light"data-tippy-allowHTML="true"data-tippy-interactive="true"data-tippy-content="&lt;p&gt;太字は初出&lt;/p&gt;&lt;div style=&quot;text-align: right;&quot;&gt;&lt;a href=&quot;#notefoot_1&quot;&gt;脚注 *1 へ&lt;/a&gt;&lt;/div&gt;">*1</a></th><th style="text-align:center;">ジャンル</th><th style="text-align:center;">難易度</th><th style="text-align:center;">最大コンボ数</th><th colspan="2" style="text-align:center;">天井スコア</th><th style="text-align:center;">初項</th><th style="text-align:center;">公差</th></tr></thead><tbody><tr><td rowspan="2" style="text-align:center;"><strong>AC16.3.10</strong><a id="notetext_2"  class="note_super tooltip"data-tippy-theme="light"data-tippy-allowHTML="true"data-tippy-interactive="true"data-tippy-content="&lt;p&gt;段位道場内でのみプレイ可能&lt;/p&gt;&lt;div style=&quot;text-align: right;&quot;&gt;&lt;a href=&quot;#notefoot_2&quot;&gt;脚注 *2 へ&lt;/a&gt;&lt;/div&gt;">*2</a></td><td rowspan="2" style="text-align:center;"></td><td style="background-color:#fdc000; text-align:center;"><strong>キッズ</strong></td><td rowspan="4" style="text-align:center;">★×10</td><td rowspan="4" style="text-align:center;"><strong>957</strong></td><td rowspan="3" style="text-align:center;"><strong>1004850点</strong></td><td rowspan="4" style="text-align:center;">＋連打</td><td rowspan="3" style="text-align:center;">1050点</td><td rowspan="3" style="text-align:center;">-</td></tr><tr><td style="background-color:gold; text-align:center;"><strong>クラシック</strong><br class="spacer">(メイン)</td></tr><tr><td style="text-align:center;">AC16.4.5SP</td><td style="text-align:center;"></td><td rowspan="2" style="background-color:gold; text-align:center;"><strong>クラシック</strong></td></tr><tr><td style="text-align:center;"></td><td style="text-align:center;">RC</td><td style="text-align:center;"><strong>1200610点</strong></td><td style="text-align:center;">370点</td><td style="text-align:center;">90点</td></tr></tbody></table></div>'

    Soup_main = BeautifulSoup(html, "html.parser")

    text_hscroll = Soup_main.find_all("div", attrs={"class": "h-scrollable"})#ハイスコア
    text_content = Soup_main.find("div", attrs={"id": "content"})
    if len(text_hscroll) <= 2:
        return ["ERROR IS HAPPEND", "-1"]
    renda_sec = "0"
    Soup_li = BeautifulSoup(str(text_content), "html.parser")
    text_li = Soup_li.find_all("li")
    for li in text_li:
        sent = li.text
        #例外処理
        if sent[:3] == "連打秒":
            idx = sent.find("合計約")
            renda_sec = sent[idx+3:idx+8]
            print("phase1:", renda_sec)
            if renda_sec == "秒数目安・":
                idx = sent.find("合計")
                renda_sec = sent[idx+2:idx+7]
            print("phase2:", renda_sec)
            if renda_sec == "打秒数目安":
                idx = sent.find("約")
                renda_sec = sent[idx+1:idx+6]
            print("phase3:", renda_sec,"\n")
            #renda_sec.find("秒")
            #renda_sec = renda_sec
            break

        
    for i in range(len(text_hscroll)):
        Soup_strong = BeautifulSoup(str(text_hscroll[i]), "html.parser")
        text_strong = Soup_strong.find_all("strong")
        strong_word_list = []
        for strong_element in text_strong:
            strong_word_list.append(strong_element.text)
        riron_score = 0
        for i in range(1,len(strong_word_list)+1):
            if len(strong_word_list[-i]) <= 5:
                continue
            try:
                riron_score = int(strong_word_list[-i][:-1])
                return [riron_score, renda_sec]
            except:
                continue


sn_list = [] #星10の情報が格納
path_data = "./lv10_song_no.txt"
with open(path_data) as f:
    for lines in f:
        line = lines.split("\t")
        sn_list.append([line[0], line[1], line[2][:-1]])


for i in range (len(sn_list)):

    song_no = sn_list[i][0]
    level = sn_list[i][1]
    name = sn_list[i][2]
    th_score = check_th_score(song_no, name, level)#理論値
    sn_list[i].append(th_score)
    print(sn_list[i])

path_s_t = "./riron_score.txt"
print_data = []
with open(path_s_t, mode="w") as g:
    for i in range (len(sn_list)):
        word = "\n" + sn_list[i][0] + "\t" + sn_list[i][1] + "\t" + sn_list[i][2] + "\t" + str(sn_list[i][3][0]) + "\t" + str(sn_list[i][3][1])
        g.write(word)