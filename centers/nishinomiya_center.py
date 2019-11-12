import os
from selenium import webdriver
from fake_useragent import UserAgent

def get_nishinomiya_center_availability(reservMon, reservDay):

    riyosya_code = os.environ.get("NISHI_ID")
    txt_password = os.environ.get("NISHI_PASS")

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('user-agent='+UserAgent().random)

    chrome_options.binary_location = os.getcwd() + "/headless-chromium"

    # ーーーここから空き情報収集ーーー

    # 予約する日付
    # reservMon = 9
    # reservDay = 20
    pracStart = 11
    parcEnd = 17

    # # 操作するブラウザーを指定
    driver = webdriver.Chrome(os.getcwd() + "/chromedriver",chrome_options=chrome_options)
    driver.get('http://yoyaku.nishi.or.jp/manabinet/Welcome.cgi')

    # ログインする
    driver.find_element_by_id('txtRiyoshaCode').send_keys(riyosya_code)
    driver.find_element_by_id('txtPassWord').send_keys(txt_password)
    driver.find_element_by_class_name('loginbtn').click()

    # 空き照会・予約
    driver.find_element_by_xpath('//*[@id="selectbox"]/ul/li[1]/a/div').click()

    # 照会方法選択「施設を指定する」
    driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[3]/td').click()

    # 公民館選択
    driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[14]/td').click() # 夙川公民館
    driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[3]/td[1]').click() # 第1集会室
    driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[4]/td[1]').click() # 第2集会室
    driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[6]/td[1]').click() # 和室

    driver.find_element_by_xpath('//*[@id="pagerbox"]/a[2]/img').click() # 次に進む

    # 予約対象区分選択
    driver.find_element_by_xpath('//*[@id="optMonth"]/option[@value='+str(reservMon)+']').click() #月入力
    driver.find_element_by_xpath('//*[@id="optDay"]/option[@value='+str(reservDay)+']').click() #日入力
    driver.find_element_by_xpath('//*[@id="radioshowweek"]').click() #7日表示
    driver.find_element_by_xpath('//*[@id="selectbox"]/ul/li[1]/a[6]/img').click() #表示
    driver.find_element_by_xpath('//*[@id="popup_ok"]').click() #確認メッセージOK

    # 予約区分計算が必要
    # ①9:00-10:30
    # ②10:30-12:00
    # ③12:30-14:00
    # ④14:00-15:30
    # ⑤15:30-17:00
    # ⑥17:30-19:00
    # ⑦19:00-20:30
    # ⑧20:30-22:00


    # tr[3]td[2]が第1集会室テーブルの左端
    # tr[15]td[2]が第2集会室テーブルの左端
    # tr[27]td[2]が和室テーブルの左端
    # 予約候補施設が増えたら修正必要

    result = []

    # 夙川第1集会室の空き状況
    for i in range(8):
        try:
            driver.find_element_by_xpath('//*[@id="facilitiesbox"]/tbody/tr/td/table/tbody/tr['+str(i+3)+']/td[2]/img')
        except:
            print("夙川第1集会室{}区分が空いてます".format(i+1))
            result.append("夙川第1集会室{}区分が空いてます".format(i+1))
        else:
            print("夙川第1集会室{}区分が空いてません".format(i+1))
            result.append("夙川第1集会室{}区分が空いてません".format(i+1))

    # 夙川第2集会室の空き状況
    for i in range(8):
        try:
            driver.find_element_by_xpath('//*[@id="facilitiesbox"]/tbody/tr/td/table/tbody/tr['+str(i+15)+']/td[2]/img')
        except:
            print("夙川第2集会室{}区分が空いてます".format(i+1))
            result.append("夙川第2集会室{}区分が空いてます".format(i+1))
        else:
            print("夙川第2集会室{}区分が空いてません".format(i+1))
            result.append("夙川第2集会室{}区分が空いてません".format(i+1))

    # 夙川和室の空き状況
    for i in range(8):
        try:
            driver.find_element_by_xpath('//*[@id="facilitiesbox"]/tbody/tr/td/table/tbody/tr['+str(i+27)+']/td[2]/img')
        except:
            print("夙川和室{}区分が空いてます".format(i+1))
            result.append("夙川和室{}区分が空いてます".format(i+1))
        else:
            print("夙川和室{}区分が空いてません".format(i+1))
            result.append("夙川和室{}区分が空いてません".format(i+1))

    # driver.find_element_by_xpath('//*[@id="mmaincolumn"]/div/table/tbody/tr[3]/td').click() # 中央公民館

    # TODO 文字列変換しているが、JSONで返却したい
    str_result = ', '.join(result)
    return str_result