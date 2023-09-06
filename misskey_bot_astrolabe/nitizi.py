from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3
import pandas as pd
import settings
from DBReader import DBReader
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO
logger = getLogger('astrolabe_logs.nitizi')

conn = sqlite3.connect(settings.dbname)
cur = conn.cursor()



##############設定ファイル##############
df = pd.read_csv(settings.csvname)# 設定ファイル行き


##############テスト用。api文のtxt保存版##############

#with open("D:\hobby\python\misskey\misskey_bot_astrolabe\misskey_bot_astrolabe\TextFile1.txt", "r", encoding="UTF-8-sig") as f: # ファイルを読み込みモードで開く
#    text = f.read() # ファイルの内容を全て読み込む
#    #print(text) # 読み込んだ内容を表示する
#text = eval(text) # ここを変更
#name1 = text["notesCount"]

##############API取得→必要値（整数）の取得##############

mk = Misskey(settings.ADRESS, i=settings.TOKEN)
text = mk.users_show(user_id = settings.AI_ID)
#print(text)
name1 = int(text["notesCount"])
name2 = int(text["followersCount"])
name3 = int(text["followingCount"])

dbreader = DBReader(settings.dbname, "sample")
# 取得したい列番号を定義する
column_a = 4# = today
# n列目のデータのリストを取得する
column_data_a = dbreader.get_column(column_a)
#print(column_data_a)

# リストのデータを順番に取り出し、整数値にする。
name1_y = int(column_data_a[0])
name2_y = int(column_data_a[1])
name3_y = int(column_data_a[2])
# 前日比計算
name1_c = name1 - name1_y
name2_c = name2 - name2_y
name3_c = name3 - name3_y

# 投稿系

sql = "SELECT * FROM time_db"
cur.execute(sql)
df = pd.read_sql_query(sql, conn)
df = pd.read_sql_query(sql, conn)
#print(df)
dt1 = (df.iloc[0, 2]) 
dt1 = datetime.datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S.%f')

############Misskey投稿################

def nitizi():
    #api取得
    mk.users_show(user_id=settings.AI_ID)
    #時間取得
    dt_now = datetime.datetime.now()
    def progre_time():
        dt2 = datetime.datetime.now()
        dt3 = dt2- dt1
        days = dt3.days
        hours, remainder = divmod(dt3.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        progre_time2 = f"{days}日と{int(hours)}時間{int(minutes)}分{int(seconds)}秒"
        return  progre_time2
    progre_time2 = progre_time()
    #投稿文作成
    test = ('今日のノート投稿数は' + str(name1_c) + '、今日のフォロワー増加数は' + str(name2_c) + 'でした。\n以上、日次報告を終了します。')
    test_a = ('【日次報告】' + dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒') + "アストロラーベの日次自動メンテナンスが完了しました。\n全機能は正常です。稼働時間は" + progre_time2 + '。\n' + test)
    #print(test)
    #投稿関数
    mk.notes_create(text=test_a, visibility='home')
    logger.info('post_nitizi')
    sql = "SELECT * FROM sample"
    cur.execute(sql)
    cur.execute(f"UPDATE sample SET today = {name1_y} WHERE name = 'notes'")
    cur.execute(f"UPDATE sample SET today = {name2_y} WHERE name = 'followers'")
    cur.execute(f"UPDATE sample SET today = {name3_y} WHERE name = 'following'")
    logger.debug('nitizi_db_write_ok')





nitizi()
# 記録系



df = pd.read_sql_query(sql, conn)
#print(df)




'''

# 挿入するデータをリスト形式で用意する
name4 = 0
data = [name1, name2, name3, name4]

print(data)
print(type(data))


# テーブルのn列目にデータを挿入する
writer = DBWriter(settings.dbname, "sample")

db_writer = DBWriter(dbname=settings.dbname, tablename='sample')
data = [1, 2, 3, 4, 5]
# write_columnメソッドを呼び出してデータを挿入する
db_writer.write_column(column_a=1, data=data)

#writer.write_column(column_a=4, data=data)
'''




'''

##############SQLToday書き込み##############
# CSV展開
#データベース操作
conn = sqlite3.connect(settings.dbname)
cur = conn.cursor()
#数値入力
cur.execute(f"UPDATE sample SET today = {name1} WHERE name = 'notes'")
cur.execute(f"UPDATE sample SET today = {name2} WHERE name = 'followers'")
cur.execute(f"UPDATE sample SET today = {name3} WHERE name = 'following'")
#データベース操作
#sql = "SELECT * FROM sample"
#df = pd.read_sql_query(sql, conn)
#conn.commit()
#conn.close()

#############SQL計算#################

# SQL文でデータを取り出す
sql = "SELECT * FROM sample"
cur.execute(sql)
# DataFrameに変換
df = pd.read_sql_query(sql, conn)
# 縦(colom:0,notes:1), 横（id:0,name:1,ye:2,to:3,）。
# 計算
result = int(df.iloc[1, 3]) - int(df.iloc[1, 2])
# 結果を表示
#print(result)

# データベースとの接続を閉じる
#conn.close()

############時間抽出################


sql = "SELECT * FROM time_db"
cur.execute(sql)
df = pd.read_sql_query(sql, conn)
df = pd.read_sql_query(sql, conn)
#print(df)
# 縦(colom:0,notes:1), 横（id:0,name:1,ye:2,to:3,）。
dt1 = (df.iloc[0, 2]) 
dt1 = datetime.datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S.%f')

############Misskey投稿################

def nitizi():
    #api取得
    mk.users_show(user_id=settings.AI_ID)
    #時間取得
    dt_now = datetime.datetime.now()
    def progre_time():
        dt2 = datetime.datetime.now()
        dt3 = dt2- dt1
        days = dt3.days
        hours, remainder = divmod(dt3.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        progre_time2 = f"{days}日と{int(hours)}時間{int(minutes)}分{int(seconds)}秒"
        return  progre_time2
    progre_time2 = progre_time()
    #投稿文作成
    test = ('今日のノート投稿数は' + str(name1) + '、今日のフォロワー増加数は' + str(name2) + 'でした。\n以上、日次報告を終了します。')
    test_a = ('【日次報告】' + dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒') + "アストロラーベの日次自動メンテナンスが完了しました。\n全機能は正常です。稼働時間は" + progre_time2 + '。\n' + test)
    print(test)
    #投稿関数
    #mk.notes_create(text=test_a, visibility='home')
    
    ############SQLYesterday書き込み################
    #データベース操作
    #数値入力
    cur.execute(f"UPDATE sample SET yesterday = {name1} WHERE name = 'notes'")
    cur.execute(f"UPDATE sample SET yesterday = {name2} WHERE name = 'followers'")
    cur.execute(f"UPDATE sample SET yesterday = {name3} WHERE name = 'following'")
    #データベース操作
    conn.commit()
    conn.close()
    print('fin')
    
nitizi()




'''