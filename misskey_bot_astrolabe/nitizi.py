from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3
import pandas as pd


##############設定ファイル##############
df = pd.read_csv(r"api.csv")# 設定ファイル行き
dbname = r'api.db'# 設定ファイル行き


##############テスト用。api文のtxt保存版##############

#with open("D:\hobby\python\misskey\misskey_bot_astrolabe\misskey_bot_astrolabe\TextFile1.txt", "r", encoding="UTF-8-sig") as f: # ファイルを読み込みモードで開く
#    text = f.read() # ファイルの内容を全て読み込む
#    #print(text) # 読み込んだ内容を表示する
#text = eval(text) # ここを変更
#name1 = text["notesCount"]

##############API取得→必要値の取得##############
mk = Misskey("misskey.seitendan.com", i="UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a")
text = mk.users_show(user_id="9ib6lbdave")

name1 = text["notesCount"]
name2 = text["followersCount"]
name3 = text["followingCount"]

##############SQLToday書き込み##############
# CSV展開
#データベース操作
conn = sqlite3.connect(dbname)
cur = conn.cursor()
#数値入力
cur.execute(f"UPDATE sample SET today = {name1} WHERE name = 'notes'")
cur.execute(f"UPDATE sample SET today = {name2} WHERE name = 'followers'")
cur.execute(f"UPDATE sample SET today = {name3} WHERE name = 'following'")
#データベース操作
#sql = "SELECT * FROM sample"
#df = pd.read_sql_query(sql, conn)
conn.commit()
conn.close()

#############SQL計算#################
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# SQL文でデータを取り出す
sql = "SELECT * FROM sample"
cur.execute(sql)
# DataFrameに変換
df = pd.read_sql_query(sql, conn)
# 縦(colom:0,notes:1), 横（id:0,name:1,ye:2,to:3,）。
# 計算
result = int(df.iloc[1, 3]) - int(df.iloc[1, 2])
# 結果を表示
print(result)

# データベースとの接続を閉じる
conn.close()

############時間抽出################
conn = sqlite3.connect(dbname)
cur = conn.cursor()

sql = "SELECT * FROM time_db"
cur.execute(sql)
df = pd.read_sql_query(sql, conn)
df = pd.read_sql_query(sql, conn)
print(df)
# 縦(colom:0,notes:1), 横（id:0,name:1,ye:2,to:3,）。
dt1 = (df.iloc[0, 2]) 
dt1 = datetime.datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S.%f')

############Misskey投稿################

def nitizi():
    #api取得
    mk = Misskey("misskey.seitendan.com", i="UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a")
    mk.users_show(user_id="9ib6lbdave")
    #時間取得
    dt_now = datetime.datetime.now()
    def progre_time():
        dt2 = datetime.datetime.now()
        dt3 = dt2- dt1
        days = dt3.days
        hours, remainder = divmod(dt3.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        progre_time2 = f"{days}日{int(hours)}時{int(minutes)}分{int(seconds)}秒"
        return  progre_time2
    progre_time2 = progre_time()
    #投稿文作成
    test = ('今日のノート投稿数は' + str(name1) + '、今日のフォロワー増加数は' + str(name2) + 'でした。\n以上、日次報告を終了します。')
    test_a = ('【日次報告】' + dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒') + "アストロラーベの日次自動メンテナンスが完了しました。\n全機能は正常です。稼働時間は" + progre_time2 + '。\n' + test)
    #投稿関数
    mk.notes_create(text=test_a)
nitizi()




############SQLYesterday書き込み################
#データベース操作
conn = sqlite3.connect(dbname)
cur = conn.cursor()
#数値入力
cur.execute(f"UPDATE sample SET yesterday = {name1} WHERE name = 'notes'")
cur.execute(f"UPDATE sample SET yesterday = {name2} WHERE name = 'followers'")
cur.execute(f"UPDATE sample SET yesterday = {name3} WHERE name = 'following'")
#データベース操作
conn.commit()
conn.close()