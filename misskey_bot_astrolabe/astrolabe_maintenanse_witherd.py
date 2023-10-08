#from misskey import Misskey
import datetime
import schedule
import time
import sqlite3
import pandas as pd
import settings
import os
from mutagen.easyid3 import EasyID3
import csv
import urllib.parse
from lxml import html,etree
import requests
from bs4 import BeautifulSoup
import lxml.html
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options



while True:
    def input_roop():

        print('【モード選択】\n1:CSV2DB\n2:TableView\n3:AllTableView\n4:DB2CSV\n5:M3U2CSV\n6:animedb_rowdata2animedb_postdata\n7:CSV重複削除\n8:スクレイピング(複数・プリントで出力)')
        witherd = 0
        witherd = int(input("アストロラーベメンテナンスウィザードのモードを選択して下さい:"))

        print('\n規定のcsvパスを確認して下さい')
        print('CSV:' + settings.csvname)
        print('\n規定のDBパスを確認して下さい')
        print('DB:' + settings.dbname)
        print("\n【Path設定変更】\n0:変更なし\n1:CSVpathの変更\n2:DBpathの変更\n")
        path_conf_input = 0
        path_conf_input = int(input('Pathを確認し、必要に応じて変更してください:'))
        if path_conf_input == 1:
            settings.csvname = input('\n入力して下さい：')
            print('変更されました:' + settings.csvname)
        elif path_conf_input == 2:
            settings.dbname = input('\n入力して下さい：')
            print('変更されました:' + settings.dbname)
        CSV_view = 0
        CSV_view = int(input('CSVを見たかったら1、そうで無かったら2:'))
        if CSV_view == 1:
            df_a = pd.read_csv(settings.csvname)
            print(df_a)
        else :
            print('csv_test0')
        print()
        if witherd == 1:
            table_name = input("テーブル名を入力してください: ")
            data = pd.read_csv(settings.csvname)
            conn = sqlite3.connect(settings.dbname)
            data.to_sql(table_name, conn, if_exists="replace")
            conn.commit()
            conn.close()

        elif witherd == 2:
            table_name = input("テーブル名を入力してください: ")
            conn = sqlite3.connect(settings.dbname)
            # カーソルを作成する
            cursor = conn.cursor()
            # テーブルから全てのデータを取得するSQL文を実行する

            cursor.execute(f"SELECT * FROM {table_name}")
            # 結果をリストとして受け取る
            results = cursor.fetchall()
            # リストの内容を表示する
            for row in results:
                print(row)
        elif witherd == 3:
            conn = sqlite3.connect(settings.dbname)
            cursor = conn.cursor() # カーソルを作成
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'") # テーブル名を取得
            tables = cursor.fetchall() # 結果をリストとして受け取る
            print(tables) # テーブル名を表示
            conn.commit()
            conn.close()
        elif witherd == 4:
            table_name = input("テーブル名を入力してください: ")
            conn = sqlite3.connect(settings.dbname)
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            data.to_csv(settings.csvname, index=False)
            conn.close()
        elif witherd == 5:
            print('m3uのパスを確認して下さい')
            print(settings.m3uname)
            m3uchange = 0
            m3uchange = input('変更する場合は1、しない場合は0(デフォルト)')
            if m3uchange == 1:
                settings.m3uname = input("M3Uのパスを入力して下さい")
                print(settings.m3uname)
            print('1:album\n2:title\n3:artist')
            field_in = 0
            field_in = input("使いたいタグフィールドを選択して下さい")
            print(field_in)
            if field_in == '1':
                field = 'album'
                header = [field]
                with open(settings.m3uname, "r", encoding="utf-8") as f:
                    paths = [line.strip() for line in f.readlines() if line.strip().endswith(".mp3")]      
                with open(settings.csvname, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for path in paths:
                        try:
                            audio = EasyID3(path)
                            m3u_tag = audio[field][0]
                            writer.writerow([m3u_tag])
                        except Exception as e:
                            print(f"Error: {e}")
            elif field_in == '2':
                print('2test')
                field = 'title'
                header = [field]
                with open(settings.m3uname, "r", encoding="utf-8") as f:
                    paths = [line.strip() for line in f.readlines() if line.strip().endswith(".mp3")]      
                with open(settings.csvname, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for path in paths:
                        try:
                            audio = EasyID3(path)
                            m3u_tag = audio[field][0]
                            writer.writerow([m3u_tag])
                        except Exception as e:
                            print(f"Error: {e}")
            elif field_in == '3':
                field = 'artist'
                header = [field]
                with open(settings.m3uname, "r", encoding="utf-8") as f:
                    paths = [line.strip() for line in f.readlines() if line.strip().endswith(".mp3")]      
                with open(settings.csvname, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for path in paths:
                        try:
                            audio = EasyID3(path)
                            m3u_tag = audio[field][0]
                            writer.writerow([m3u_tag])
                        except Exception as e:
                            print(f"Error: {e}")
            else:
                print('00test')
        elif witherd == 6:
            print('''
これはアニメDBを元にDアニメから諸元を収集し、アストロラーベの投稿用DBを作成するコードです。    
①【手動】api.csvにtitle、url列を作成する
②【手動】title列にアニメのタイトルを入力する
③【自動処理】Phase1を始動。titleからurlを生成（検索用）=>url2、textの取得
※最初の結果のURLとタイトル。無ければnoneを入力
④【手動】api.csvを精査して手動で修正する。
※titleとtextが合っているか、noneは本当にないのか。noneのうち、クールが合体している場合は行を削除                 
⑤【自動処理】Phase2を始動。api.csvのtextからtitle2を生成（ID消去）、url2からcastブロックを取得、分類して記録する
⑥【手動】api.csvを精査して問題が無いか確認する。
※改行、特殊文字、区切り文字によるエラー、セルズレが発生する。         
⑦登録する。                  
                  ''')
            phase = int(input('Phaseを入力して下さい。1or2：'))
            if phase == 1:
                print('phase1')
                
                df = pd.read_csv(settings.csvname, encoding='utf-8') # CSVファイルを読み込みます
                url_f = r'https://animestore.docomo.ne.jp/animestore/sch_pc?searchKey=' # URLの前半部分
                url_l = '&vodTypeList=svod_tvod' # URLの後半部分
                df['url'] = url_f + df['title'].apply(urllib.parse.quote) + url_l # URLを作成して新しい列に追加します
                driver = webdriver.Chrome() # Chromeドライバーを起動します
                df['url2'] = "" # スクレイピングしたURLを格納するための空の列を作ります
                test = 0 # テスト用の変数です
                for i, row in df.iterrows(): # data frameの各行に対してループします
                    driver.get(row['url']) # URLにアクセスします
                    try:
                        url2 = 'none'
                        text = 'none'
                        element = driver.find_element(By.XPATH, '//*[@id="listContainer"]/div/section/div/a') # XPATHで要素を見つけます
                        url2 = element.get_attribute('href') # 要素のhref属性を取得します
                        df.loc[i, 'url2'] = url2 # data frameの対応する行にURLを書き込みます
                        element2 = driver.find_element(By.XPATH, '//*[@id="listContainer"]/div/section/div/a/div/h3/span') # XPATHで要素を見つけます
                        text = element.text# 要素のtext属性を取得します
                        df.loc[i, 'text'] = text # data frameの対応する行にURLを書き込みます
                    except Exception:
                        url2 = 'none'
                        text = 'none'
                        df.loc[i, 'url2'] = url2 # data frameの対応する行にURLを書き込みます
                        df.loc[i, 'text'] = text # data frameの対応する行にURLを書き込みます
                    test = test + 1 # テスト用の変数をインクリメントします
                    time.sleep(10)
                    if test == 400: # テスト用の条件です
                        break # ループを抜けます
                driver.quit() # ドライバーを終了します
                df.to_csv(settings.csvname, encoding='utf-8', index=False) # data frameをCSVファイルに書き込みます
            elif phase == 2:
                print('pahase2')
                df = pd.read_csv(settings.csvname, encoding='utf-8') # CSVファイルを読み込みます
                driver = webdriver.Chrome() # Chromeドライバーを起動します


                #df['url'] = url_f + df['title'].apply(urllib.parse.quote) + url_l # URLを作成して新しい列に追加します
                df['title2'] = "" # タイトルに含まれるIDの除去処理をするための空の列を作る
                df['row_text'] = "" # スクレイピングしたtextを格納するための空の列を作ります
                df['year'] = "" #クールの収容列を作成
                df['outline'] = "" # あらすじの収容列を作成
                df['maker'] = ""#製作会社の収容列を作成
                df['episodes'] = ""#製作会社の収容列を作成
                df['notices'] = ""#製作会社の収容列を作成
                final_t = ("Dアニメストアに情報がないか、取得に失敗しました")

                test = 0 # テスト用の変数です
    
                for i, row in df.iterrows(): # data frameの各行に対してループします
    
                    #Dアニメに記録がない場合の処理
                    if row['url2'] == 'none':
                        #print('Dアニメストアに登録された情報がありません')
                        df.loc[i, 'title2'] = row['title']
                        df.loc[i, 'url2'] = ('Dアニメストアに収録されていません')
                        df.loc[i, 'row_text'] = 'none'
                        df.loc[i, 'year'] = 'none'
                        df.loc[i, 'outline'] = 'none'
                        df.loc[i, 'maker'] = 'none'
                        df.loc[i, 'episodes'] = 'none'
                        continue
                    #ここまで

                    #タイトルのID消去
                    title = row['text']#text列を取得
                    title2 = title.split(' ')#文字列の分割
                    title2.pop()#最後の要素を削除
                    title2 = " ".join(title2)#リストを文字列にすり
                    df.loc[i, 'title2'] = title2 # data frameの対応する行にURLを書き込みます
                    #ここまで

                    options = Options()
                    options.acceptInsecureCerts = 'True'
                    driver.implicitly_wait(10)
                    driver = webdriver.Chrome(options=options)
                    driver.get(row['url2'])#url列を取得
                    try:
                        #話数取得
                        element = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[1]/h1/span') # XPATHで要素を見つけます
                        outline = str(element.text)
                        outline = outline.replace("（全", "").replace("話）", "")
                        df.loc[i, 'episodes'] = outline
                        #ここまで

                        #あらすじブロック（そのまま収容）
                        element = driver.find_element(By.CLASS_NAME, 'outlineContainer') # XPATHで要素を見つけます
                        outline = element.text
                        #print(outline)
                        df.loc[i, 'outline'] = outline
                        #ここまで

                        #キャストブロック
                        element = driver.find_element(By.CLASS_NAME, 'castContainer') # XPATHで要素を見つけます
                        cast = element.text
                        #print(cast)
                        df.loc[i, 'row_text'] = cast
                        #ここまで

                        #制作会社
                        s = cast
                        pattern = r"アニメーション制作:([^／]+)／" 
                        match = re.search(pattern, s)
                        if match:
                            #print(match.group(1))
                            df.loc[i, 'maker'] = match.group(1)
                        else:
                            #print("No match")
                            #print('=================================')
                            s = cast
                            pattern = r"アニメーション制作:([^／]+)" 
                            match = re.search(pattern, s)
                            if match:
                                #print(match.group(1))
                                df.loc[i, 'maker'] = match.group(1)
                            else:
                                #print("No match")
                                #print('=================================')
                                s = cast
                                pattern = r"制作:([^／]+)／" 
                                match = re.search(pattern, s)
                                if match:
                                    #print(match.group(1))
                                    df.loc[i, 'maker'] = match.group(1)
                                else:
                                    #print("No match")
                                    #print('=================================')
                                    pattern = r"制作:([^／]+)"
                                    match = re.search(pattern, s)
                                    if match:
                                        ##print(match.group(1))
                                        df.loc[i, 'maker'] = match.group(1)
                                    else:
                                        #print('=================================')
                                        df.loc[i, 'maker'] = final_t
                        #制作年
                        pattern = r"(\d{4})年"
                        match = re.search(pattern, s)
                        if match:
                            #print(match.group(1))
                            df.loc[i, 'year'] = match.group(1)
                        else:
                            df.loc[i, 'year'] = final_t
                    
                        #print('=================================')
        
        
                    except Exception:
                        df.loc[i, 'notices'] = '例外が発生しました'
                        print('例外')
        
                    test = test + 1 # テスト用の変数をインクリメントします
                    time.sleep(10)
                    if test == 400: # テスト用の条件です
                        break# ループを抜けます
                driver.quit() # ドライバーを終了します
                df.to_csv(settings.csvname, encoding='utf-8', index=False) # data frameをCSVファイルに書き込みます
        elif witherd == 7:
            phase = (input('列名を入力して下さい：'))

            df = pd.read_csv(settings.csvname)

            df = df.drop_duplicates(subset=phase, keep='first')

            df.to_csv(settings.csvname, encoding='utf-8', index=False) # data frameをCSVファイルに書き込みます
            print('動作が終了しました')
        elif witherd == 8:
            print('【注意】レシピの取得に特化した成形になっているため、別用途に使う場合は注意すること')
            URL_input = str(input('URL:'))
            column_input = str(input('colmun:'))
            print('1:Class_name\n2:Xpath\n3:Name\n')
            phase = int(input('要素の確定方式を選択して下さい。1or2or3：'))
            element_input = str(input(r'エレメントを入力して下さい'))
            driver = webdriver.Chrome() # Chromeドライバーを起動します
            driver.get(URL_input)

            if phase == 1:
                elements = driver.find_elements(By.CLASS_NAME, element_input) # XPATHで要素を見つけます
                for elem in elements:# テキストを表示
                    # 文字列を定義
                    text = (elem.text)
                    # 正規表現で「【】」の中の文字を空文字に置換
                    text = re.sub(r"【.*】", "", text)
                    text = re.sub(r".*！", "", text)
                    text = re.sub(r".*：", "", text)
                    text = re.sub(r".*♪", "", text)
                    text = re.sub(r"基本の", "", text)
                    text = re.sub(r"定番", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"簡単", "", text)
                    text = re.sub(r"かんたん", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"おいしい", "", text)
                    text = re.sub(r"シンプル", "", text)
                    print(text)
            elif phase == 2:
                elements = driver.find_elements(By.XPATH, element_input) # XPATHで要素を見つけます
                for elem in elements:# テキストを表示
                    # 文字列を定義
                    text = (elem.text)
                    # 正規表現で「【】」の中の文字を空文字に置換
                    text = re.sub(r"【.*】", "", text)
                    text = re.sub(r".*！", "", text)
                    text = re.sub(r".*：", "", text)
                    text = re.sub(r".*♪", "", text)
                    text = re.sub(r"基本の", "", text)
                    text = re.sub(r"定番", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"簡単", "", text)
                    text = re.sub(r"かんたん", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"おいしい", "", text)
                    text = re.sub(r"シンプル", "", text)
                    print(text)
            elif phase == 3:
                elements = driver.find_elements(By.ID, element_input) # XPATHで要素を見つけます
                for elem in elements:# テキストを表示
                    # 文字列を定義
                    text = (elem.text)
                    # 正規表現で「【】」の中の文字を空文字に置換
                    text = re.sub(r"【.*】", "", text)
                    text = re.sub(r".*！", "", text)
                    text = re.sub(r".*：", "", text)
                    text = re.sub(r".*♪", "", text)
                    text = re.sub(r"基本の", "", text)
                    text = re.sub(r"定番", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"簡単", "", text)
                    text = re.sub(r"かんたん", "", text)
                    text = re.sub(r".*屋さんの", "", text)
                    text = re.sub(r"おいしい", "", text)
                    text = re.sub(r"シンプル", "", text)
                    print(text)



    input_roop()

print('fin')
