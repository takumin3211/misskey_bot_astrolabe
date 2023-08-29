#!//etc/astrolabe/venv/bin/python3
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO, WARNING, ERROR
from timeit import Timer
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
import os
import psutil
import re
import sys




Ver = 'v.0.04.02'

logger = getLogger('astrolabe_logs')

def dt1():
    #時間取得
    dt1 = datetime.datetime.now()
    #フォルダ生成系
    log_path = settings.PATH + '/log'
    model_path = settings.PATH + '/model'
    new_dir_path_recursive = log_path
    new_dir_path_recursive_a = model_path
    os.makedirs(new_dir_path_recursive, exist_ok=True)
    os.makedirs(new_dir_path_recursive_a, exist_ok=True)
    #ログ準備系
    #dt2 = (str(dt1.strftime('%Y%m%d%H%M%S'))) + '.log'
    dt2 = settings.PATH + '/log/' + (str(dt1.strftime('%Y%m%d%H%M%S'))) + '.log'
    logger.setLevel(DEBUG)
    fl_handler = FileHandler(filename= dt2 , encoding="utf-8")
    fl_handler.setLevel(DEBUG)
    fl_handler.setFormatter(Formatter(settings.FORMAT))
    logger.addHandler(fl_handler)
    logger.info("logging start")
    


    #DB記録系
    conn = sqlite3.connect(settings.dbname)
    cur = conn.cursor()
    cur.execute("UPDATE time_db SET time = ? WHERE name = 'first_time'", (dt1,))
    #print(dt1)
    sql = "SELECT * FROM time_db"
    df = pd.read_sql_query(sql, conn)
    #print(df)
    conn.commit()
    cur.close()
    conn.close()
    #ログ系
    logger.info("def_dt1 clear")
    logger.info("ALos_sys_booting_now!")
    logger.info(Ver)
    print("ALos_sys_booting_now!")
    
dt1()#起動時のみの動作を内部に書く

mk = Misskey(settings.ADRESS, i=settings.TOKEN)

class DBReader:  
    def __init__(self, dbname, tablename):
        # データベース名とテーブル名を属性として保存する
        self.dbname = dbname
        self.tablename = tablename

    def get_column(self, column_a):
        logger.debug('DBReader_read')  
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
	timer = random.randint(0, 50)
	
	await asyncio.sleep(timer)
	
	test_a = (test)
	#投稿関数
	mk.notes_create(text=test_a)
	logger.info("def_ohayou clear")    

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
	
	timer = random.randint(0, 50)
	await asyncio.sleep(timer)    
	test_a = (test)
	#投稿関数
	mk.notes_create(text=test_a)
	timer2 = random.randint(0, 50)
	await asyncio.sleep(timer2)
	import nitizi
	logger.info("def_oyasumi clear")  
	return 'test'


async def rss_a():
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
    
    timer = random.randint(0, 50)
    await asyncio.sleep(timer) 
    
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
                text_a = (test + '\n\n' + title_a + '\n' + url)
                #print(text_a)
                mk.notes_create(text=text_a, visibility='home')
                logger.info("def_rss clear(post)")    
                break
        elif n_a >= 10:
            logger.info("def_rss clear(Over_10)")    
            break    

async def sys_check():
    cpu_per = (psutil.cpu_percent(interval=1, percpu=True))
    cpu_per_a = max(cpu_per)
    usage = (psutil.disk_usage(path='/').percent)
    if usage >= 90.0:
       usage_a = 'ディスク使用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' + usage + '％'
       mk.notes_create(text=usage_a, visibility='home')
       logger.warning("def_sys_check diskuse(Over_90)")
       pass
    else:
       pass
    if cpu_per_a >= 90.0:
       cpu_per_a_a =  'CPU論理プロセッサの最大利用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' +  cpu_per_a + '％'
       mk.notes_create(text=cpu_per_a_a, visibility='home')
       logger.warning("def_sys_check cpu_max_per(Over_90)")
    else:
       logger.debug(cpu_per_a)  
       logger.debug(usage)  
       logger.debug('syscheck_pass')  
       pass



async def asy_test():
    await asyncio.sleep(5)
    print('async test')

   
MY_ID = mk.i()['id']
WS_URL_a = 'wss://' + settings.ADRESS + '?i='
WS_URL = WS_URL_a + settings.TOKEN

async def schedule_coroutine():

    while True:
       #時間管理
       logger.debug('1st_circ')
       ohayou = str('06') + str(random.randint(0, 59))
       oyasumi = str('23') + str(random.randint(0, 59))
       sys_check = '04:00'
       rss_a = str(random.randint(12, 13)) + str(random.randint(0, 59))
       
       #動作制御
       n_a = 0#おはよう
       n_b = 0#おやすみ
       n_c = 0#システムチェック
       n_d = 0#RSS_A
       n_test = 1#async def test直結
       n_date = 1#リセット用(1で正常。23:58に起こす)
       while True:
           dt = datetime.datetime.now()
           dt_a = (str(dt.strftime('%H:%M')))
           if dt_a == ohayou and n_a == 0:
              n_a = n_a + 1
              logger.debug('wakeup_ohayou')
              await ohayou()
           elif dt_a == oyasumi and n_b == 0:
               logger.debug('wakeup_oyasumi')
               n_b = n_b + 1
               await oyasumi()
           elif dt_a == sys_check and n_c == 0:
               n_c = n_c + 1
               logger.debug('wakeup_sys_check')
               await sys_check()
           elif dt_a ==  rss_a and n_d == 0:
               n_d = n_b + 1
               logger.debug('wakeup_rss_a')
               await rss_a()
           elif dt_a == 'test' and n_test == 0:
              print(type(n_test))
              n_test = n_test + 1
              logger.debug('wakeup_asy_test')
              await asy_test()

           #以後周回処理
           elif dt_a == '23:58':
               logger.debug('circle1')  
               n_date = 0
           elif dt_a == '00:00' and n_date == 0:
               logger.debug('circle_break')
               break
           else:
              pass
           await asyncio.sleep(10)
       continue

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

  try:
       data = json.loads(await ws.recv())
       logger.debug(data)    
       if data['type'] == 'channel':
        if data['body']['type'] == 'note':
     
         note = data['body']['body']
         user = data['body']['body']['user']
         await on_note(note, user)
  except websockets.exceptions.ConnectionClosed:
      logger.error('Connection closed_a')
  except websockets.exceptions.ConnectionClosedError:
      logger.error('Connection closed_b')

async def on_note(note,user):
 logger.debug('async_def_onnote')  
 if note.get('mentions'):
  logger.debug('scan_mention')  
  if MY_ID in note['mentions']:
   logger.debug('scan_mention_myid')  
   USER_NAME = 'test_name'
   e.reply = note['text'].replace('@astrolabe ', '')
   logger.debug(e.reply) 
   #mk.notes_create(text='解答を生成しているので少し待っていて下さい！＾＾', reply_id=note['id'])############
   #翻訳
   if e.reply.startswith(('help', 'info', '機能')):
    #time.sleep(4)
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
    logger.debug('help_post')  
   elif e.reply.startswith(('停止', 'stop', '終了')):
       
       mk.notes_create(text='システムを終了します', visibility=note['visibility'] , reply_id=note['id'])
       sys.exit()
   elif e.reply.startswith(('Version', 'バージョン', '世代', '死活')):
       dt1 = datetime.datetime.now()
       dt1 =(str(dt1.strftime('%Y年%m月%d日%H時%M分%S秒')))
       opinion_text = ('アストロラーベは稼働中です\n' + dt1 + '\n' + Ver )
       logger.debug('version_post')  
       mk.notes_create(text=opinion_text, visibility=note['visibility'] , reply_id=note['id'])
   else:
      logger.debug('lmm_start')  
      #print('test04') 
      e.n = 0
      #e.input_text = 'アメリカで一番大きい都市はどこですか？'
      import llm_process
      importlib.reload(llm_process)
   
      logger.debug('receive_control')
      from llm_process import output_h
      
      logger.debug(output_h)
	   #LLMpy = LLM()
	   #output_h = LLMpy.llm(input)
	   #print(output_h)
      mk.notes_create(text=output_h, cw='お待たせしました！丹精込めて答えましたよ～！', visibility=note['visibility'] , reply_id=note['id'])
      logger.info('lmm_post')
 else :
     logger.debug('not_scan_mention')  
     try:
        if 'アストロラーベちゃん' in note['text']:
            test = random.choices([1, 2], weights=[1, 4])
            test = 1
            #print('test')
            logger.debug('detection_astrolabe')
            if test == 1:
                await asyncio.sleep(4)    
                logger.debug('reply_yobidashi')
                mk.notes_create(text='呼びましたか？？', reply_id=note['id'])
                pass
        else:
            logger.debug('not_detection_astrolabe')
            scan_list_ohayou = r'ohayou|おはよう|おきた|起床'
            scan_list_oyasumi = r'ohayou|おはよう|おきた|起床'
            scan_list_kawaii = r'カワイイ|可愛い|かわいい'
            scan_list_oishii = r'美味しい|おいしい|おいしみ'
            scan_list_tiken = r'知見があっぷ|知見がアップ|rs_tiken_up|ちけんがあっぷ|なんだ|らしい|にゃんだ'
            scan_list_gohan = r'ごはん|おひる|よるごはん|あさごはん|朝ご飯|お昼|夜ご飯'
            if (re.compile(scan_list_ohayou)).search(note['text']):
                #print('test')
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_ohayou)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_ohayou')
            elif (re.compile(scan_list_oyasumi)).search(note['text']):
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_oyasumi)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_oyasumi')
            elif (re.compile(scan_list_kawaii)).search(note['text']):
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_kawaii)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_kawaii')
            elif (re.compile(scan_list_oishii)).search(note['text']):
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_oishii)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_oishii')
            elif (re.compile(scan_list_tiken)).search(note['text']):
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_tiken)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_tiken')
            elif (re.compile(scan_list_gohan)).search(note['text']):
                timer = (random.randint(4, 360))
                await asyncio.sleep(timer) 
                test = str(random.choices(settings.note_list_gohan)).replace("['", "").replace("']", "") 
                mk.notes_reactions_create(note_id=note['id'], reaction=test)
                logger.debug('reaction_gohan')
                #mk.notes_reactions_create(note_id=note['id'], reaction=':kawaii_comment:')
            else:
                logger.debug('not_conditions_reaction')
                pass
     except Exception:
         import traceback
         traceback.print_exc()
     
         logger.debug('occurrence_exception')
         pass

async def main():
    await asyncio.gather(runner(), schedule_coroutine())

if __name__ == "__main__":

	asyncio.run(main()) 

logger.info('all_code_read') 
