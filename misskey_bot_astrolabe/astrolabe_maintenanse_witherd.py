#from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3
import pandas as pd
import settings
import os
from mutagen.easyid3 import EasyID3
import csv

while True:
    def input_roop():

        print('【モード選択】\n1:CSV2DB\n2:TableView\n3:AllTableView\n4:DB2CSV\n5:M3U2CSV\n')
        witherd = 0
        witherd = int(input("アストロラーベメンテナンスウィザードのモードを選択して下さい:"))
        print(witherd)
        if witherd == 1:
            print('CSV2DBが選択されました')
        elif witherd == 2:
            print('TableViewが選択されました')
        elif witherd == 3:
            print('AllTableViewが選択されました')
        elif witherd == 4:
            print('DB2CSV')
        elif witherd == 5:
            print('M3U2CSV')
        else:
            pass

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
            print('変更されました:' + settings.dbnamee)
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

    

    input_roop()

print('fin')
