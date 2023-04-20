# 参考
# スクリーンショット：http://holiday-programmer.net/selenium_screen_shot/

# TODO:
# 空きのある公民館のみをスクリーンショットすることまではできたので、
# その後、データテーブルを再度作成する必要がある。リストが毎回変更になるので、動的な対応が必要になる。
# また、そこから自動で場所取りを行うための処理が必要

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import os
import pandas as pd
import sys
from bs4 import BeautifulSoup

# 日付を指定
year = '2023'
month = '05'
day = '20'

#ヘッドレス実行　※全画面用
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Webドライバーを起動（動作確認したければoptionsを外す
driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
# 施設予約システムにアクセス
driver.get("https://www.11489.jp/Chuo/Web/StartPage.aspx?language=JAPANESE")

# 空き紹介・予約の申込みをname属性でクリック
application = driver.find_element_by_name('rbtnYoyaku')
application.click()

# 集会施設をname属性でクリック
shuukai = driver.find_element_by_name('dlSSCategory$ctl02$rbSSCategory')
shuukai.click()

# 施設一覧をname属性でクリック
shisetsu = driver.find_element_by_name('btnList')
shisetsu.click()

# dgShisetsuList(table属性)から、２列めと7列目のデータ取得
# TODO: 本来はここで、施設数が変動しても対応できるようにリストを取得するべき
# shisetsu_list = driver.find_element_by_id('dgShisetsuList')

# 京橋区民間をname属性でクリック
kyobashi = driver.find_element_by_name('dgShisetsuList$ctl02$chkSelectLeft')
ginza = driver.find_element_by_name('dgShisetsuList$ctl03$chkSelectLeft')
akashimachi = driver.find_element_by_name('dgShisetsuList$ctl04$chkSelectLeft')
shinkawa = driver.find_element_by_name('dgShisetsuList$ctl05$chkSelectLeft')
ningyomachi = driver.find_element_by_name('dgShisetsuList$ctl06$chkSelectLeft')
hamamatsucho = driver.find_element_by_name('dgShisetsuList$ctl07$chkSelectLeft')
tsukuda = driver.find_element_by_name('dgShisetsuList$ctl08$chkSelectLeft')
kachidoki = driver.find_element_by_name('dgShisetsuList$ctl09$chkSelectLeft')
harumi = driver.find_element_by_name('dgShisetsuList$ctl10$chkSelectLeft')
nihonbashi = driver.find_element_by_name('dgShisetsuList$ctl11$chkSelectLeft')
kyobashiplaza = driver.find_element_by_name('dgShisetsuList$ctl02$chkSelectRight')
shintomiku = driver.find_element_by_name('dgShisetsuList$ctl03$chkSelectRight')
hacchoubori = driver.find_element_by_name('dgShisetsuList$ctl04$chkSelectRight')
horidomecho = driver.find_element_by_name('dgShisetsuList$ctl05$chkSelectRight')
hisamatsucho = driver.find_element_by_name('dgShisetsuList$ctl06$chkSelectRight')
shinbabashi = driver.find_element_by_name('dgShisetsuList$ctl07$chkSelectRight')
tsukishima =  driver.find_element_by_name('dgShisetsuList$ctl08$chkSelectRight')
toshima = driver.find_element_by_name('dgShisetsuList$ctl09$chkSelectRight')
sangyokaikan = driver.find_element_by_name('dgShisetsuList$ctl10$chkSelectRight')
hotplaza = driver.find_element_by_name('dgShisetsuList$ctl11$chkSelectRight')
kyobashi.click()
ginza.click()
akashimachi.click()
shinkawa.click()
ningyomachi.click()
hamamatsucho.click()
tsukuda.click()
kachidoki.click()
harumi.click()
nihonbashi.click()
kyobashiplaza.click()
shintomiku.click()
hacchoubori.click()
horidomecho.click()
hisamatsucho.click()
shinbabashi.click()
tsukishima.click()
toshima.click()
sangyokaikan.click()
hotplaza.click()

#次へをname属性で指定してクリック
next_button = driver.find_element_by_name('ucPCFooter$btnForward')
next_button.click()

# 日付のvalueを指定
input_year = driver.find_element_by_name('txtYear')
input_month = driver.find_element_by_name('txtMonth')
input_day = driver.find_element_by_name('txtDay')
#　一旦valueを消す
input_year.clear()
input_month.clear()
input_day.clear()
input_year.send_keys(year)
input_month.send_keys(month)
input_day.send_keys(day)
# 表示期間を１日に
period = driver.find_element_by_name('rbtnDay')
period.click()
# 標示時間帯を全日に
time_zone = driver.find_element_by_name('rbtnAllday')
time_zone.click()

# 次へをclick（同じ名前だがオブジェクトとしては別なので再度指定）
next_button = driver.find_element_by_name('ucPCFooter$btnForward')
next_button.click()

# バツの場合：&nbsp;&nbsp;×&nbsp;&nbsp;
# △の場合：&nbsp;&nbsp;△&nbsp;&nbsp;
# ○の場合：&nbsp;&nbsp;○&nbsp;&nbsp;

center_list = [['kyobashi','京橋区民館','dlRepeat_ctl00_tpItem_dgTable'],
               ['kyobashi_plaza','京橋プラザ区民館','dlRepeat_ctl01_tpItem_dgTable'],
               ['ginza','銀座区民館','dlRepeat_ctl02_tpItem_dgTable'],
               ['shintomi','新富士区民館','dlRepeat_ctl03_tpItem_dgTable'],
               ['akashimachi','明石町区民館','dlRepeat_ctl04_tpItem_dgTable'],
               ['hacchobori','八丁堀句民間','dlRepeat_ctl05_tpItem_dgTable'],
               ['shinkawa','新川区民間','dlRepeat_ctl06_tpItem_dgTable'],
               ['horidomecho','堀留町区民館','dlRepeat_ctl07_tpItem_dgTable'],
               ['ningyomachi','人形町区民館','dlRepeat_ctl08_tpItem_dgTable'],
               ['hisamachu','久松町区民館','dlRepeat_ctl09_tpItem_dgTable'],
               ['hamatsucho','浜松町','dlRepeat_ctl10_tpItem_dgTable'],
               ['shinbabashi','新場橋区民館','dlRepeat_ctl11_tpItem_dgTable'],
               ['chukuda','佃区民館','dlRepeat_ctl12_tpItem_dgTable'],
               ['tsukishima','月島区民館','dlRepeat_ctl13_tpItem_dgTable'],
               ['kachidoki','勝どき区民館','dlRepeat_ctl14_tpItem_dgTable'],
               ['toshima','豊島区民間','dlRepeat_ctl15_tpItem_dgTable'],
               ['harumi','晴海区民間','dlRepeat_ctl16_tpItem_dgTable'],
               ['sangyo','産業会館','dlRepeat_ctl17_tpItem_dgTable'],
               ['nihonbashi','日本橋','dlRepeat_ctl18_tpItem_dgTable'],
               ['hot_plaza','ほっとプラザはるみ','dlRepeat_ctl19_tpItem_dgTable']]

def createAvailableDataframe(center_list):
    df = pd.DataFrame()
    for center in center_list:
        # テーブルをdataframeに変換して取得
        table = driver.find_element_by_id(center[2])
        
        df_tmp = pd.read_html(table.get_attribute('outerHTML'),skiprows=1)[0]
        # 列名を指定
        df_tmp.columns = ['部屋名','定員','空き状況']
        # id列を追加
        df_tmp['id'] = ''
        # htmlテーブルの３列目に対応するa要素内のidを各行ごとに取得
        for i in range(1,len(table.find_elements_by_tag_name('tr'))):
            # aタグが無いときは休館日なので空文字を代入
            if len(table.find_elements_by_tag_name('tr')[i].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('a')) == 0:
                fact_id = ''
            else:
                fact_id = table.find_elements_by_tag_name('tr')[i].find_elements_by_tag_name('td')[2].find_element_by_tag_name('a').get_attribute('id')
            df_tmp.loc[i-1,'id'] = fact_id
        
        # indexを振り直す
        df_tmp = df_tmp.reset_index(drop=True)
        # 部屋名にprefixをつける
        df_tmp['部屋名'] = center[1] + '_' + df_tmp['部屋名']
        df = pd.concat([df,df_tmp],axis=0)
    return df

df = createAvailableDataframe(center_list)

print(df)

# △と○のみを選択してクリック（選択△、選択○というテキストに変更する）
df = df[df['空き状況'].isin(['△','○'])]
for i in range(len(df)):
    id = df.iloc[i,3]
    # idからa要素を取得
    # idからxpathに変換
    # xpath = '//*[@id="' + id + '"]'
    a = driver.find_element_by_id(id)
    #a = driver.find_element_by_xpath(xpath)
    # テキストを変更
    # 空き状況が○の場合
    print(a)
    if df.iloc[i,2] == '○':
        a.click()
        a.send_keys(Keys.ENTER)
        #driver.execute_script("arguments[0].innerText = '選択○", a)
    elif df.iloc[i,2] == '△':
        a.click()
        a.send_keys(Keys.ENTER)
        #driver.execute_script("arguments[0].innerText = '選択△", a)
# 次へをclick（同じ名前だがオブジェクトとしては別なので再度指定）
next_button = driver.find_element_by_name('ucPCFooter$btnForward')
next_button.click()

#保存する画像ファイル名
fname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#スクショ保存ディレクトリが存在しなければ生成
if os.path.isdir("ss") == False:
    os.mkdir("ss")

#ウインドウサイズをWebサイトに合わせて変更　※全画面用
width = driver.execute_script("return document.body.scrollWidth;")
height = driver.execute_script("return document.body.scrollHeight;")
driver.set_window_size(width,height)

#スクショをPNG形式で保存
driver.get_screenshot_as_file("ss/" + fname + '_' + year + '-' + month + '-' + day +".png")

# 候補の公民館データを取得
dl_repeat = driver.find_element_by_id('dlRepeat')

# 公民館ごとにtrタグがあるのでそれを取得
df = pd.DataFrame()
# forで回してindexとtrタグを取得
for i in range(len(dl_repeat.find_elements_by_tag_name('tr'))):
    # 最後のtrタグにデータが格納されているのでそれを取得
    # NOTE: 最上層のtrだけとりだすべきだが、うまく動かないので、とりあえずむりやりtryで実施
    print('dlRepeat_ctl0{}_tpItem_dgTable'.format(i))
    print('dlRepeat_ctl0{}_tpItem_lnkShisetsu'.format(i))
    
    try:
        data_table = dl_repeat.find_element_by_id('dlRepeat_ctl{:0=2}_tpItem_dgTable'.format(i))
    except:
        continue
    print(dl_repeat.find_element_by_id('dlRepeat_ctl{:0=2}_tpItem_lnkShisetsu'.format(i)).text)
    print(data_table)
    # テーブルをdataframeに変換して取得
    df_tmp = pd.read_html(data_table.get_attribute('outerHTML'),skiprows=1)[0]
    print(df_tmp)
    # 列名を指定
    # 列数が足りなければ空白を追加（日本橋公会堂は9:00~12:00,13:00~17:00,18:00~21:30）
    if len(df_tmp.columns) < 6:
        df_tmp['21:00-22:00'] = ''
    df_tmp.columns = ['部屋名','定員','9:00-12:00','13:00-17:00','18:00-21:00（日本橋公会堂は-21:30）','21:00-22:00']

    # インデックスを振り直す
    df_tmp = df_tmp.reset_index(drop=True)
    # 部屋名にprefixをつける
    df_tmp['部屋名'] = dl_repeat.find_element_by_id('dlRepeat_ctl{:0=2}_tpItem_lnkShisetsu'.format(i)).text + '_' + df_tmp['部屋名']
    # データを追加
    df = pd.concat([df,df_tmp],axis=0)

print(df)
# csvで出力
df.to_csv("ss/" + fname + '_' + year + '-' + month + '-' + day + '.csv',index=False, encoding='utf-8-sig')

# ブラウザを閉じる
driver.quit()