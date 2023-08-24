from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3
import pandas as pd
import time
import asyncio
import json
import websockets
from transformers import pipeline
import importlib
import exchange as e
import random
import settings
import feedparser


Ver = 'v.0.02.00'
mk = Misskey(settings.ADRESS, i=settings.TOKEN)

def dt1():

    dt1 = datetime.datetime.now()
    conn = sqlite3.connect(settings.dbname)
    cur = conn.cursor()
    cur.execute("UPDATE time_db SET time = ? WHERE name = 'first_time'", (dt1,))
    print(dt1)
    sql = "SELECT * FROM time_db"
    df = pd.read_sql_query(sql, conn)
    #print(df)
    conn.commit()
    cur.close()
    conn.close()

    print("ALos_sys_booting_now!")
dt1()

class DBReader:
    def __init__(self, dbname, tablename):
        # データベース名とテーブル名を属性として保存する
        self.dbname = dbname
        self.tablename = tablename

    def get_column(self, column_a):
        # データベースに接続する
        conn = sqlite3.connect(self.dbname)
        # カーソルを作成する
        cursor = conn.cursor()
        # テーブルから1列目のデータを取得するSQL文を実行する
        cursor.execute(f"SELECT * FROM {self.tablename}")
        # 結果をリストとして受け取る
        results = cursor.fetchall()
        # n列目のデータだけを抽出する
        column_data = [row[column_a - 1] for row in results]
        # 接続を閉じる
        conn.close()
        # n列目のデータのリストを返す
        return column_data

async def ohayou():
    	
	# DBReaderクラスのインスタンスを作成する
	dbreader = DBReader(settings.dbname, "ohayou")
	# 取得したい列番号を定義する
	column_a = 2
	column_b = 3
	#column_c = 4
	# n列目のデータのリストを取得する
	column_data_a = dbreader.get_column(column_a)
	column_data_b = dbreader.get_column(column_b)
	#column_data_c = dbreader.get_column(column_c)
    # リストの内容を表示する
	#print(column_data_b)
	test = random.choices(column_data_a, weights=column_data_b)
	#test2_a = random.choices(column_data_c)
	#test2 = test2_a.pop(0)
	#test3 = random.randint(0, 10)
	#print(test3)
	#print(test2)
	#sleep_a = test2 + test3 * 60
	#sleep(sleep_a)
	#print(test)
	# Misskey投稿
	
	
	test_a = (test)
	#投稿関数
	mk.notes_create(text=test_a)

async def oyasumi():
		# DBReaderクラスのインスタンスを作成する
	dbreader = DBReader(settings.dbname, "oyasumi")
	# 取得したい列番号を定義する
	column_a = 2
	column_b = 3
	#column_c = 4
	# n列目のデータのリストを取得する
	column_data_a = dbreader.get_column(column_a)
	column_data_b = dbreader.get_column(column_b)
	#column_data_c = dbreader.get_column(column_c)
    # リストの内容を表示する
	#print(column_data_b)
	test = random.choices(column_data_a, weights=column_data_b)
	#test2_a = random.choices(column_data_c)
	#test2 = test2_a.pop(0)
	#test3 = random.randint(0, 10)
	#print(test3)
	#print(test2)
	#sleep_a = test2 + test3 * 60
	#sleep(sleep_a)
	#print(test)
	# Misskey投稿
	
	
	test_a = (test)
	#投稿関数
	mk.notes_create(text=test_a)

async def nitizi():
    import nitizi

def rss_a():
    dbreader = DBReader(settings.dbname, "rssqa_1")
    dbreader_a = DBReader(settings.dbname, "rss_reaction_1")
    # 取得したい列番号を定義する
    column_a = 0
    column_b = 1
    column_c = 2
    # QAWord
    column_data_a = dbreader.get_column(column_a)
    # Reaction and waight
    column_data_a_a = dbreader_a.get_column(column_a)
    #print(column_data_a_a)
    column_data_a_b = dbreader_a.get_column(column_c)
    #print(column_data_a_b)
    test = random.choices(column_data_a_b, weights=column_data_a_a)
    test = str(test).replace("['", "").replace("']", "")
    
    #print(test)
    n_a = 0
    while True:

        n= random.randint(1, 10)
        feed = feedparser.parse(settings.RSS_URL_a)
        url = feed.entries[n].link
        title_a = feed.entries[n].title
        #print(column_data_a)
        # リストの内容を表示する
        judge = (any(x in title_a for x in column_data_a))
        if n_a <= 10:
            if judge:
                #print(title_a)    
                #print('test1') 
                n_a = n_a + 1
                continue
            else :
                #print(title_a)     
                #print('test2')  
                n_a = n_a + 1
                text_a = (test + '\n\n\n' + title_a + '\n' + url)
                #print(text_a)
                mk.notes_create(text=text_a, visibility='home')
                break
        elif n_a >= 10:
            break    

    
    
    
    
   

async def test03():
    print("test03")
	
def get_random_time(start_time, end_time):
  """
  指定された時間範囲内でランダムな時間を生成する。

  Args:
    start_time: 開始時間 (hh:mm)
    end_time: 終了時間 (hh:mm)

  Returns:
    ランダムな時間 (hh:mm)
  """
  start_time_hour, start_time_min = start_time.split(":")
  end_time_hour, end_time_min = end_time.split(":")
  start_time_min = int(start_time_min)
  end_time_min = int(end_time_min)
  random_minute = random.randint(start_time_min, end_time_min)
  return f"{start_time_hour}:{random_minute}"

print('test02')


	

MY_ID = mk.i()['id']
WS_URL_a = 'wss://' + settings.ADRESS + '?i='
WS_URL = WS_URL_a + settings.TOKEN




schedule.every().days.at(get_random_time("06:10", "06:55")).do(ohayou)
schedule.every().days.at(get_random_time("23:10", "23:40")).do(oyasumi)
schedule.every().days.at(get_random_time("23:10", "23:40")).do(nitizi)
schedule.every().days.at("12:53").do(rss_a)

async def schedule_coroutine():
    while True:
        #schedule.every(10).seconds.do(test03)
        schedule.run_pending()
        
        await asyncio.sleep(1)

async def runner():
 #task1 = asyncio.create_task(schedule_a())
 #await task1
 async with websockets.connect(WS_URL) as ws:
  await ws.send(json.dumps({
   "type": "connect",
   "body": {
     "channel": "homeTimeline",
     "id": "test"
   }
  }))

  
  while True:
   schedule.run_pending()#スケジュール投稿用のコマンド。場所借りてる。
   
   try:
       data = json.loads(await ws.recv())
       print(data)
       if data['type'] == 'channel':
        if data['body']['type'] == 'note':
     
         note = data['body']['body']
         user = data['body']['body']['user']
         await on_note(note, user)
   except websockets.exceptions.ConnectionClosed:
      print('Connection closed_a')
   except websockets.exceptions.ConnectionClosedError:
      print('Connection closed_b')

async def on_note(note,user):
 if note.get('mentions'):
  if MY_ID in note['mentions']:
   USER_NAME = 'test_name'
   e.reply = note['text'].replace('@astrolabe ', '')
   print(e.reply)
   #mk.notes_create(text='解答を生成しているので少し待っていて下さい！＾＾', reply_id=note['id'])############
   #翻訳
   if e.reply.startswith(('help', 'info', '機能')):
    time.sleep(4)
    info_text = ('''まず自由にリプライを下されば内容に応じた返信を致します。\n
 次に冒頭のコマンドに応じた機能があります。
・「help」「info」「機能」でこの内容を返信します
・「remind」「リマインダー」でリマインダーを設定します（未実装）
・「trans」「翻訳」で以後の文について日英翻訳します（未実装）
・「wether」「天気」で指示頂いた場所の天気をお教えします（未実装）
・「meal」「ごはんガチャ」でご飯ガチャを実施致します（未実装）
and more......
          
        ''')
    mk.notes_create(text=info_text, cw='わたくしアストロラーベの機能をご紹介します！', visibility=note['visibility'] , reply_id=note['id'])
   elif e.reply.startswith(('Version', 'バージョン', '世代', '死活')):
       dt1 = datetime.datetime.now()
       dt1 = str(dt1)
       opinion_text = ('アストロラーベは稼働中です\n' + dt1 + '\n' + Ver )
       mk.notes_create(text=opinion_text, visibility=note['visibility'] , reply_id=note['id'])
   else:
      print('test04') 
      e.n = 0
      #e.input_text = 'アメリカで一番大きい都市はどこですか？'
      import llm_process
      importlib.reload(llm_process)
   
      print('llmの処理が終了し制御が返却されました。')
      from llm_process import output_h
      print(output_h)
	   #LLMpy = LLM()
	   #output_h = LLMpy.llm(input)
	   #print(output_h)
      mk.notes_create(text=output_h, cw='お待たせしました！丹精込めて答えましたよ～！', visibility=note['visibility'] , reply_id=note['id'])
   


async def main():
    await asyncio.gather(runner(), schedule_coroutine())


if __name__ == "__main__":

	asyncio.run(main()) 


# 日次スケージュリング投稿(本番)
# 時間判定


print('test2')
#常駐化


