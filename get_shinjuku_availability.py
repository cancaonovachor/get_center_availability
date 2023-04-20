from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
import pandas as pd
import os
import datetime

#ヘッドレス実行　※全画面用
options = webdriver.ChromeOptions()
options.add_argument('--headless')

#保存する画像ファイル名
fname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#スクショ保存ディレクトリが存在しなければ生成
if os.path.isdir("ss") == False:
    os.mkdir("ss")

# ユーザー名とパスワード
cn_username = '****'
cn_password = '****'

# 0埋め不可
month = '5'
day = '8'

# Webドライバーを起動
driver = webdriver.Chrome('./chromedriver',options=options)
# 施設予約システムにアクセス
driver.get("https://user.shinjuku-shisetsu-yoyaku.jp/chiiki/reserve/gin_menu")

# 多機能操作ボタンを探す
multi_button = driver.find_element_by_xpath("//input[@alt='多機能操作']")

# 多機能操作ボタンをクリック
multi_button.click()

# ユーザー名とパスワードを入力
username = driver.find_element_by_id('user')
password = driver.find_element_by_id('password')

username.send_keys(cn_username)
password.send_keys(cn_password)

# ログインボタンをクリック
login_button = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/form/p/input")
login_button.click()

# 「予約申込」ボタンをクリック
yoyaku_button = driver.find_element_by_xpath('//*[@id="local-navigation"]/dd/ul/li[1]/a')
yoyaku_button.click()

# 「地域センター」を選択
chiki_button = driver.find_element_by_xpath('//*[@id="contents"]/form[1]/div/div/div/div[1]/div/div[1]/select[1]/option')
chiki_button.click()
kakutei_button = driver.find_element_by_xpath('//*[@id="contents"]/form[1]/div/div/div/div[1]/div/div[1]/input[2]')
kakutei_button.click()

# 「目的」から「コーラス」を選択
mokuteki_button = driver.find_element_by_xpath('//*[@id="contents"]/form[4]/div/div/div/div[1]/div/div[1]/select/option[27]')
mokuteki_button.click()
kakutei_button = driver.find_element_by_xpath('//*[@id="contents"]/form[4]/div/div/div/div[1]/div/div[1]/input[2]')
kakutei_button.click()

# 「施設」のselectメニューから全部の施設をloop処理で選択
for i in range(len(Select(driver.find_elements_by_name('g_basyocd')[0]).options)):
    select = Select(driver.find_elements_by_name('g_basyocd')[0])
    facility = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/form/div/div/div[1]/div/div[1]/select/option[{}]'.format(i+1))
    print(facility.text)
    select.select_by_visible_text(facility.text)

kakutei_button = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/form/div/div/div[1]/div/div[1]/input[2]')  
kakutei_button.click()

# 「部屋」のselectメニューから全部の部屋をloop処理で選択
for i in range(len(Select(driver.find_elements_by_name('g_heyacd')[0]).options)):
    select = Select(driver.find_elements_by_name('g_heyacd')[0])
    room = driver.find_element_by_xpath('//*[@id="contents"]/form[5]/div/div/div/select/option[{}]'.format(i+1))
    print(room.text)
    select.select_by_visible_text(room.text)
kakutei_button = driver.find_element_by_xpath('//*[@id="contents"]/form[5]/div/div/div/p[2]/input[2]')
kakutei_button.click()

# 月をドロップダウンから選択
select = Select(driver.find_element_by_xpath('//*[@id="MM"]'))
select.select_by_value(month)
# 日をドロップダウンから選択
select = Select(driver.find_element_by_xpath('//*[@id="DD"]'))
select.select_by_value(day)

# 「検索」ボタンをクリック
search_button = driver.find_element_by_id('btnOK')
search_button.click()

# テーブルデータをdataframeとして取得
df = pd.read_html(driver.page_source)[0]
# NaNを○に変換
df = df.fillna('○')
print(df)
# テーブルデータをcsvファイルとして保存
df.to_csv('ss/shinjuku_availability'+ fname + '_' + '-' + month + '-' + day +'.csv', index=False, encoding='utf-8-sig')

#ウインドウサイズをWebサイトに合わせて変更　※全画面用
width = driver.execute_script("return document.body.scrollWidth;")
height = driver.execute_script("return document.body.scrollHeight;")
driver.set_window_size(width,height)

# スクリーンショットを保存
driver.save_screenshot('ss/shinjuku_availability_'+ fname + '_' + '-' + month + '-' + day +'.png')

# ブラウザを閉じる
driver.quit()