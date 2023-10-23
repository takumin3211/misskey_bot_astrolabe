#!//home/share/venv/bin/python3.11
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
import traceback
import MeCab
import markovify
import emoji
import cv2
from platform import java_ver
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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Ver = 'v.1.01.07'
logger = getLogger('astrolabe_logs')

mk = Misskey(settings.ADRESS, i=settings.TOKEN)

def dt1():
    try:
        #時間取得
        dt1 = datetime.datetime.now()
        #フォルダ生成系
        log_path = settings.PATH + '/log'
        model_path = settings.PATH + '/model'
        model_path = settings.PATH + '/cash'
        new_dir_path_recursive = log_path
        new_dir_path_recursive_a = model_path
        os.makedirs(new_dir_path_recursive, exist_ok=True)
        os.makedirs(new_dir_path_recursive_a, exist_ok=True)
        #DB記録系
        '''
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
        '''
        #dt2 = (str(dt1.strftime('%Y%m%d%H%M%S'))) + '.log'
        dt2 = settings.PATH + '/log/' + (str(dt1.strftime('%Y%m%d%H%M%S'))) + '.log'
        logger.setLevel(ERROR)
        fl_handler = FileHandler(filename= dt2 , encoding="utf-8")
        fl_handler.setLevel(ERROR)
        fl_handler.setFormatter(Formatter(settings.FORMAT))
        logger.addHandler(fl_handler)
        logger.info("logging start")
    



        #ログ系
        #logger.info("def_dt1 clear")
        #logger.info("ALos_sys_booting_now!")
        #logger.info(Ver)
        #print("ALos_sys_booting_now!")
        #(sys.executable)
        #print(settings.alosname)
        #print(sys.argv)
        #print('アストロラーベのプロセスが始動しました。')
        #print(dt1)
        time.sleep(5)

    
        opinion_text = ('アストロラーベのシステムが起動しました\n' + str(dt1) + '\n' +  Ver)
        mk.notes_create(text=opinion_text, visibility='specified' , visible_user_ids=[settings.Master_ID])
    
        #os.exit
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('Connection_closed_global')
        os.execv(sys.executable, ['python'] + sys.argv)
dt1()#起動時のみの動作を内部に書く

###########class###############

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

###########markov##############

async def global_runner():#グローバル受信系

    #task1 = asyncio.create_task(schedule_a())
    #await task1
    async with websockets.connect(WS_URL) as ws:
        g_n = 0
        buf_gr = ''
        buf_gr_1 = ''
        try:
            await ws.send(json.dumps({
            "type": "connect",
            "body": {
                   "channel": "globalTimeline",
                   "id": "test"
                   }
            }))
            data = json.loads(await ws.recv())
            #logger.debug(data)    
            while True:
                   
                try:
                    
                    data = json.loads(await ws.recv())
                    #logger.debug(data)    
                    if data['type'] == 'channel':
                        if data['body']['type'] == 'note': 
                            note = data['body']['body']
                            buf_note =  note['text']
                            if buf_note == None:
                                logger.debug('get_global_note_none')
                            else :
                                buf_note =  note['text']
                            
                                buf_gr_1 += buf_note
                                node = buf_note + '。\n'
                                node = node.replace('。。', '。').replace('$', '')
                                node = re.sub(r'。', '。\n', node, flags=re.MULTILINE)#文中読点の改行
                                node = re.sub(r"https:.*", "", node, flags=re.MULTILINE)#https削除
                                node = re.sub(r"@.*", "", node, flags=re.MULTILINE)
                                node = re.sub(r"<.*>", "", node, flags=re.MULTILINE)
                                node = re.sub(r"[.*]", "", node, flags=re.MULTILINE)
                                node = re.sub(r':', '', node, flags=re.MULTILINE)#短文削除
                                node = re.sub(r'\.*', '', node, flags=re.MULTILINE)#短文削除
                                node = re.sub(r":.*:", "", node, flags=re.MULTILINE)#カスタム絵文字削除<
                                node = re.sub(r"@.* ", "", node, flags=re.MULTILINE)#メンション削除
                                node = re.sub(r"#.* ", "", node, flags=re.MULTILINE)#ハッシュタグ削除
                                node = re.sub(r"#.*", "", node, flags=re.MULTILINE)#ハッシュタグ削除
                                #node = re.sub(r"#", "", node, flags=re.MULTILINE)#ハッシュタグ取り切れないもの削除
                                node = re.sub(r'^.{1,10}$', '', node, flags=re.MULTILINE)#短文削除
                                node = re.sub(r"　", "", node, flags=re.MULTILINE)#空白削除
                                node = re.sub(r'^\s*\n', '', node, flags=re.MULTILINE)#空白行削除
                                node = emoji.replace_emoji(node, replace="")#絵文字削除
                                node = node.replace('にゃ', 'な')
                                buf_gr_1 += node
                                buf_gr += node
                                #print(node)
                                if ():
                                    pass
                                elif ():
                                    pass
                                else :
                                    g_n = g_n + 1     
                                    if g_n > 30:
                                        #print('over10')    
                                        #print('######################処理前######################')
                                        #print(buf_gr_1)
                                        #print('######################処理後######################')
                                        #print(buf_gr)    
                                        logger.debug('get_global_60note')
                                        return buf_gr 
                                        break
                        
                except Exception:

                    logger.debug(traceback.format_exc())
                    logger.error('Connection_closed_global')
                    #os.execv(sys.executable, ['python'] + sys.argv)
        
        except Exception:

            logger.debug(traceback.format_exc())
            logger.error('Connection_closed_global')

            #print('error')
            #os.execv(sys.executable, ['python'] + sys.argv)         #

async def note_captcha():# ノート取得
    try:
        #print('test1')
        #グローバル記録ブロック
        task = asyncio.create_task(global_runner())
        
        g_note = await task
        node = g_note
    
        #print(node) 
        with open(settings.cashtxt, 'a', encoding='utf-8') as f:
            f.writelines(node)
            logger.debug('write_cashtxt')
    except Exception:
        pass                                

async def post_tl():# テキスト処理→テキスト生成→投稿
    try:
        #task = asyncio.create_task(note_captcha())
        await note_captcha()
    
        #print('back captcha')
        with open(settings.cashtxt, "r", encoding = 'utf-8') as f1:
            text1 = f1.read()
            #print(text1)
        with open(settings.home_cashtxt, "r", encoding = 'utf-8') as f2:
            text2 = f2.read()
            #print(text2)
        with open(settings.cash2txt, "w", encoding = 'utf-8') as f3:
            text3 = text1 + text2
            f3.write(text3)

        mecab = MeCab.Tagger('-Owakati')
        text_1 = ''
        # ファイルを開く
        with open(settings.cash2txt, "r", encoding = 'utf-8') as f:
            for line in f:# テキストファイルの品質確保
                node = re.sub(r'\b\w{1,10}\n', '', line)
                text_1 += node
            text_s = text_1.split('\n')
            text_1 = ''
            for text_f in text_s :# 分かち書き
                node = mecab.parse(text_f)
                #print(node)
                text_1 += node
        text_model = markovify.NewlineText(text_1, state_size=1, well_formed=False)#モデル生成
        dbreader = DBReader(settings.dbname, "rssqa_1")
        column_a = 0
        column_data_a = dbreader.get_column(column_a)
        n_a = 0
        while True:
            markov_text = (text_model.make_short_sentence(60)) 
            markov_text = markov_text.replace(' ', '').replace('@astrolabe　', '')
            #print(markov_text)
            '''
            judge = (any(x in markov_text for x in column_data_a))
            if n_a <= 10:
                if judge:
                    n_a = n_a + 1
                    continue'''
            if ():
                pass    
            else :
                mk.notes_create(text=markov_text)
                logger.debug('markov_post')
                #字数制御ブロック（グローバル）
                with open(settings.cashtxt, "r", encoding = 'utf-8') as f:
                    text = f.read()

                if len(text) > 2000:

                    line_count = len(text) // 2
                    new_text = text[line_count:]
                    # テキストファイルを書き換える
                    with open(settings.cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('cashtxt_rewrite')
                elif len(text) > 10000:
                    new_text = ''
                    with open(settings.cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('cashtxt_over10000_clear')
                

                #字数制御ブロック（ホーム）     
                with open(settings.home_cashtxt, "r", encoding = 'utf-8') as f:
                    text = f.read()
                
                if len(text) > 500:
                    # テキストファイルの行数を取得する
                    line_count = len(text) // 2
                
                    # テキストファイルの先頭 half_line_count 行を削除する
                    new_text = text[line_count:]

                    # テキストファイルを書き換える
                    with open(settings.home_cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('home_cashtxt_rewrite')
                elif len(text) > 10000:
                    new_text = ''
                    with open(settings.home_cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('home_cashtxt_over10000_clear')
                #結合用の一時ファイル消去
                with open(settings.cash2txt, "w", encoding = 'utf-8') as f:
                    f.write("")
                    logger.debug('cash2txt_clear')
                break
            
        '''  

        for i in range(1): #文字列生成
            markov_text = (text_model.make_short_sentence(120)) 
            markov_text = markov_text.replace(' ', '').replace('@astrolabe　', '')
            '''
    except Exception:
        logger.debug(traceback.format_exc())
        logger.debug('occurrence_exception')

###########schedule_exe#########

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
	test = str(random.choices(column_data_a, weights=column_data_b)).replace("['", "").replace("']", "") 
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
	timer = float(timer)
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
    test = str(random.choices(column_data_a, weights=column_data_b)).replace("['", "").replace("']", "") 
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
    timer = float(timer)    
    await asyncio.sleep(timer)    
    test_a = (test)
    #投稿関数
    logger.debug(test_a)  
    mk.notes_create(text=test_a)
    logger.info("def_oyasumi_oyasumi clear")  
    timer2 = random.randint(0, 50)
    timer2 = float(timer2)
    await asyncio.sleep(timer2)
    import nitizi
    logger.info("def_oyasumi_nitizi clear")  
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
    timer = float(timer)
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
                mk.notes_create(text=text_a)
                logger.info("def_rss_a clear(post)")    
                break
        elif n_a >= 10:
            logger.info("def_rss_a clear(Over_10)")    
            break    

async def rss_b():
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
    timer = float(timer)
    await asyncio.sleep(timer) 
    
    #print(test)
    n_a = 0
    while True:

        n= random.randint(1, 8)
        feed = feedparser.parse(settings.RSS_URL_b)
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
                mk.notes_create(text=text_a)
                logger.info("def_rss_b clear(post)")    
                break
        elif n_a >= 10:
            logger.info("def_rss_b clear(Over_10)")    
            break    

async def sys_check_a():
    cpu_per__ = (psutil.cpu_percent(interval=1, percpu=True))
    cpu_per_a = max(cpu_per__)
    usage__ = (psutil.disk_usage(path='/').percent)
    if usage__ >= 90.0 and cpu_per_a >= 90.0:
       usage__ = str(usage__)
       cpu_per_a = str(cpu_per_a)
       cpu_and_disk = 'CPU利用率及びディスク使用率が許容値を超過しました。ディスク使用率：' + usage__ + '％、CPU利用率：' + cpu_per_a + '％'
       mk.notes_create(text=cpu_and_disk, visibility='specified' , visible_user_ids=[settings.Master_ID])
       logger.warning("def_sys_check_diskuse(Over_90)_and_cpu_max_per(Over_90)")
       return
    elif usage__ >= 90.0:
       usage__ = str(usage__)
       usage_a = 'ディスク使用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' + usage__ + '％'
       mk.notes_create(text=usage_a, visibility='specified' , visible_user_ids=[settings.Master_ID])
       logger.warning("def_sys_check_diskuse(Over_90)")
       return
    elif cpu_per_a >= 90.0:
       cpu_per_a = str(cpu_per_a)
       cpu_per_a_a =  'CPU論理プロセッサの最大利用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' +  cpu_per_a + '％'
       mk.notes_create(text=cpu_per_a_a, visibility='specified' , visible_user_ids=[settings.Master_ID])
       logger.warning("def_sys_check_cpu_max_per(Over_90)")
       return
    else:
       logger.debug(cpu_per_a)  
       logger.debug(usage__)  
       sys_check_pass = 'システムチェックの結果問題はありませんでした'
       mk.notes_create(text=sys_check_pass, visibility='specified' , visible_user_ids=[settings.Master_ID])
       logger.debug('syscheck_pass')  
       #print(cpu_per_a)
       #print(usage__)
       pass

async def now_play():
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader(settings.dbname, "music")
    column_a = 2 # タイトル
    column_b = 3 # アーティスト
    column_c = 4 # アルバム
    column_data_a = dbreader.get_column(column_a)
    column_data_b = dbreader.get_column(column_b)
    column_data_c = dbreader.get_column(column_c)
    random_title = random.choices(column_data_a)[0]
    index_of_title = column_data_a.index(random_title)
    random_artist = column_data_b[index_of_title]
    random_album = column_data_c[index_of_title]

    text_1 = (str(random_title))
    text_2 = (str(random_artist))
    text_3 = (str(random_album))
    test = text_1 + ' - ' + text_2 + '\n' + '「' + text_3 + '」より\n' + '#NowPlaying'
	#test2 = test2_a.pop(0)
	#test3 = random.randint(0, 10)
	#print(test3)
	#print(test2)
	#sleep_a = test2 + test3 * 60
	#sleep(sleep_a)
	#print(test)
	# Misskey投稿
	
    timer = random.randint(0, 50)
    timer = float(timer)
    await asyncio.sleep(timer)    
    test_a = (test)
    #投稿関数
    logger.debug(test_a)  
    mk.notes_create(text=test_a)
    logger.info("def_now_play_clear")      

async def anime_def():
    	
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader(settings.dbname, "anime")
    # 取得したい列番号を定義する
    column_a = 6 # title
    column_b = 8 # year
    column_c = 10 # maker
    column_d = 11 # episode
    column_e = 4 # url
    column_data_a = dbreader.get_column(column_a)
    column_data_b = dbreader.get_column(column_b)
    column_data_c = dbreader.get_column(column_c)
    column_data_d = dbreader.get_column(column_d)
    column_data_e = dbreader.get_column(column_e)
    random_title = random.choices(column_data_a)[0]
    index_of_title = column_data_a.index(random_title)
    random_year = column_data_b[index_of_title]
    random_maker = column_data_c[index_of_title]
    random_episode = column_data_d[index_of_title]
    random_url = column_data_e[index_of_title]
    text_1 = (str(random_title))
    text_2 = (str(random_year))
    text_3 = (str(random_maker))
    text_4 = (str(random_episode))
    text_5 = (str(random_url))
    if text_2 == 'none':
        test = f'''
むむ、、なんかアニメが見たくなってきました。例えば……
『{text_1}』とか！

でも、Dアニメストアに情報がないみたいなのでこれ以上ご紹介できません。。。
お役に立てず、ごめんなさい！
    '''    
        #print(test)
    elif text_3 == 'Dアニメストアに情報がないか、取得に失敗しました':
        test = f'''
むむ、、なんかアニメが見たくなってきました。例えば……
『{text_1}』とか！
たしか{text_2}年の作品で、全{text_4}話でした。
制作に関する情報は存在しないか、取得に失敗したようです。
    
※この情報はDアニメストアを元に自動収集しています。
誤っている場合があるので注意してください。
作品のページです！：{text_5}
    '''        
        #print(test)    
        
    else :
        test = f'''
むむ、、なんかアニメが見たくなってきました。例えば……
『{text_1}』とか！
たしか{text_2}年の作品で、{text_3}制作、全{text_4}話でした。
    
※この情報はDアニメストアを元に自動収集しています。
誤っている場合があるので注意してください。
作品のページです！：{text_5}
    '''       
        #print(test)     
    #test = str(random.choices(column_data_a)).replace("['", "").replace("']", "") 

    timer = random.randint(0, 50)
    timer = float(timer)
    await asyncio.sleep(timer)
    test_a = (test)
    #print(test)    
    #投稿関数
    mk.notes_create(text=test_a)
    
async def menu_a():
    try:
        # DBReaderクラスのインスタンスを作成する
        dbreader = DBReader(settings.dbname, "menu")
        column_a = 0
        column_data_a = dbreader.get_column(column_a) 
        test = str(random.choices(column_data_a)).replace("['", "").replace("']", "").replace("\u3000", " ")
        timer = random.randint(0, 50)
        timer = float(timer)
        await asyncio.sleep(timer)
        random_a = random.randint(1, 4)
        if random_a == 1:
            test_a = 'なんだか、お腹が空いてきました……ﾋﾟｶｰﾝ☆\nそうだ！今晩はこれを食べます。ででーん「' + test + '」\n美味しく作っちゃいますよ～！'
        elif random_a == 2:
            test_a = 'うーん今晩何食べようかなぁ\n思いつかないので、ご飯ガチャやります！\nででん！「' + test + '」\n頑張って作ります！＾＾'
        elif random_a == 3:
            test_a = '献立って決めるの大変ですよね。そんな時はご飯ガチャを使います！\nということで出てきたのは「' + test + '」！\n出したからには頑張って作ります！'
        elif random_a == 4:
            test_a = 'ば、晩ご飯の時間ですけど、おやつ食べ過ぎちゃって食欲が、、うぅ、、ごめんなさい'
            mk.notes_create(text=test_a)
            return test_a
            #投稿関数
        logger.debug('post_menu_dennar')  
        mk.notes_create(text=test_a)
        timer2 = int(random.randint(39600, 46800))
        timer2 = float(timer2)
        logger.debug(timer2)  
        test_a = 'お腹減ってきたなぁ\nそういえば昨日の夜食べた「' + test + '」冷蔵庫に残ってたかも。\n温め直して食べよっと！'
        logger.debug('post_menu_moning')
        await asyncio.sleep(timer2)
        mk.notes_create(text=test_a)
        logger.info("def_menu_clear") 
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('menu_error')


async def weather_get(url_get, id_get, pref_get):
    logger.debug('weather_get_start')  
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    # set window size

    driver.get(url_get) # URLにアクセスします

    wait = WebDriverWait(driver, 10)#タイムアウト時間の設定
    await asyncio.sleep(10.0)
    driver.implicitly_wait(10) #タイムアウト時間の設定
    element = driver.find_elements(By.XPATH, '//*[@id="bosaitop-bosai_forecast_table_div"]/div[1]/div/div/div[2]/table/tr[3]/td/div') # XPATHで要素を見つけます
    elements_get = []
    for element in element:
        text = element.text
        #print(text)
        elements_get.append(text)
        #print(elements_get)
    # Close Web Browser
    driver.quit()
    dt1 = datetime.datetime.now()
    name0 = (str(dt1.strftime('%Y年%m月%d日')))
    name1 = str(elements_get[0])
    name2 = str(elements_get[1])
    name3 = str(elements_get[2])
    conn = sqlite3.connect(settings.dbname)
    cur = conn.cursor()
    sql = "SELECT * FROM weather"
    cur.execute(sql)
    cur.execute("UPDATE weather SET W_1 = ? WHERE id = ?", (name1, id_get))
    cur.execute("UPDATE weather SET W_2 = ? WHERE id = ?", (name2, id_get))
    cur.execute("UPDATE weather SET W_3 = ? WHERE id = ?", (name3, id_get))
    cur.execute("UPDATE weather SET W_8 = ? WHERE id = ?", (name0, id_get))
    conn.commit()
    conn.close()
    if name1 == name2 and name1 == name3:#毎日同じ場合
        weather_mk = 'ご利用ありがとうございます！\n' + pref_get + 'のお天気は、今日から明後日にかけて連日' + name1 + 'です。\nこれは気象庁から取得した、' + name0 + '時点の予報です。\nこの予報を生命及び財産の保護等に使わないで下さい。\n(正確かつ最新の予報は直接取得して下さい)'
        return weather_mk
    elif name1 == name2:#今日と明日が同じ場合
        weather_mk = 'ご利用ありがとうございます！\n' + pref_get + 'のお天気は、今日は' + name1 + '\n明日も' + name2 + '\n明後日は' + name3 + 'です。これは気象庁から取得した、' + name0 + '時点の予報です。\nこの予報を生命及び財産の保護等に使わないで下さい。\n(正確かつ最新の予報は直接取得して下さい)'
        return weather_mk  
    elif name2 == name3:#明日と明後日同じ場合
        weather_mk = 'ご利用ありがとうございます！\n' + pref_get + 'のお天気は、今日は' + name1 + '\n明日は' + name2 + '\n明後日も' + name3 + 'です。これは気象庁から取得した、' + name0 + '時点の予報です。\nこの予報を生命及び財産の保護等に使わないで下さい。\n(正確かつ最新の予報は直接取得して下さい)'
        return weather_mk  

    else :
        weather_mk = 'ご利用ありがとうございます！\n' + pref_get + 'のお天気は、今日は' + name1 + '\n明日は' + name2 + '\n明後日は' + name3 + 'です。これは気象庁から取得した、' + name0 + '時点の予報です。\nこの予報を生命及び財産の保護等に使わないで下さい。\n(正確かつ最新の予報は直接取得して下さい)'
        return weather_mk
    #print(weather_mk)

async def weather_get_sche():
    dbreader = DBReader(settings.dbname, "weather")
    column_a = 3
    column_b = 6
    column_c = 14
    column_d = 2
    column_data_a = dbreader.get_column(column_a)
    random_pref = random.choices(column_data_a)[0]
    index1 = column_data_a.index(random_pref)
    column_data_b = dbreader.get_column(column_b)
    column_data_c = dbreader.get_column(column_c)
    column_data_d = dbreader.get_column(column_d)
    pref_get =  column_data_a[index1]
    url_get = column_data_b[index1]
    time_get = column_data_c[index1]
    id_get = column_data_d[index1]
    task = asyncio.create_task(weather_get(url_get, id_get, pref_get))
    g_note = await task
    g_note = g_note.replace('ご利用ありがとうございます！\n', '')
    g_note = '今日のランダム地点お天気です！\n\n' + g_note
    mk.notes_create(text=g_note)

async def asy_test():
    await asyncio.sleep(5)
    print('async test')
   
MY_ID = mk.i()['id']
WS_URL_a = 'wss://' + settings.ADRESS + '?i='
WS_URL = WS_URL_a + settings.TOKEN

###########schedule_ctrl##############

async def schedule_coroutine():

    while True:
       try:
           #時間管理
           logger.debug('1st_circ')
           ohayou_r = str(random.randint(0, 59))
           oyasumi_r = str(random.randint(0, 59))
           rss_a_r = str(random.randint(0, 59))
           rss_b_r = str(random.randint(0, 59))
           rss_b_r_1 = str(random.randint(7, 9))
           nowplay_r = str(random.randint(0, 59))
           anime_r = str(random.randint(0, 59))
           anime_r = str(random.randint(0, 59))
           menu_r = str(random.randint(0, 59))
           markov_r = str(random.randint(0, 59))
           
           ohayou_t = str('06') + ':' + (ohayou_r.zfill(2))
           oyasumi_t = str('23') + ':' + (oyasumi_r.zfill(2))
           sys_check_a_t = '04:00'
           rss_a_t = str(random.randint(12, 13)) + ':' + (rss_a_r.zfill(2))
           rss_b_t = (rss_b_r_1.zfill(2)) + ':' + (rss_b_r.zfill(2))
           nowplay = str(random.randint(10, 20)) + ':' + (nowplay_r.zfill(2))
           anime = str(random.randint(18, 21)) + ':' + (anime_r.zfill(2))
           menu = str(random.randint(19, 21)) + ':' + (menu_r.zfill(2))
           weather_t = str('07') + ':' + (nowplay_r.zfill(2))
           
           markov_t_1 = '10' + ':' + (markov_r.zfill(2))
           markov_t_2 = '13' + ':' + (markov_r.zfill(2))
           markov_t_3 = '16' + ':' + (markov_r.zfill(2))
           markov_t_4 = '19' + ':' + (markov_r.zfill(2))
           markov_t_5 = '21' + ':' + (markov_r.zfill(2))
           
           logger.debug(ohayou_t)
           logger.debug(oyasumi_t)
           logger.debug(rss_a_t)
           logger.debug(rss_b_t)
           logger.debug(nowplay)
           logger.debug(anime)
           logger.debug(markov_t_1)
           logger.debug(markov_t_2)
           logger.debug(markov_t_3)
           logger.debug(markov_t_4)
           logger.debug(markov_t_5)
           #動作制御
           n_a = 0#おはよう
           n_b = 0#おやすみ
           n_c = 0#システムチェック
           n_d = 0#RSS_A
           n_d_1 = 0#RSS_B
           n_e = 0#nowplay
           n_f = 0#anime
           n_g = 0#menu
           n_h_1 = 0#markov
           n_h_2 = 0#markov
           n_h_3 = 0#markov
           n_h_4 = 0#markov
           n_h_5 = 0#markov
           n_i = 0#weather

           n_test = 1#async def test直結
           n_date = 1#リセット用(1で正常。23:59に起こす)
           while True:
               dt = datetime.datetime.now()
               dt_a = (str(dt.strftime('%H:%M')))
               if dt_a == ohayou_t and n_a == 0:
                  n_a = n_a + 1
                  logger.debug('wakeup_ohayou')
                  task = asyncio.create_task(ohayou())
               elif dt_a == oyasumi_t and n_b == 0:
                   logger.debug('wakeup_oyasumi')
                   n_b = n_b + 1
                   task = asyncio.create_task(oyasumi())
               elif dt_a == sys_check_a_t and n_c == 0:
                   n_c = n_c + 1
                   logger.debug('wakeup_sys_check')
                   task = asyncio.create_task(sys_check_a())
               elif dt_a ==  rss_a_t and n_d == 0:
                   n_d = n_d + 1
                   logger.debug('wakeup_rss_a')
                   task = asyncio.create_task(rss_a())
                  
               elif dt_a ==  rss_b_t and n_d_1 == 0:
                   n_d_1 = n_d_1 + 1
                   logger.debug('wakeup_rss_b')
                   task = asyncio.create_task(rss_b())
               elif dt_a ==  nowplay and n_e == 0:
                   n_e = n_e + 1
                   logger.debug('wakeup_nowplay_waight')
                   now_r = random.choices([0, 1], weights=[1, 2])
                   logger.debug(now_r)
                   if now_r == [0]:
                       logger.debug('wakeup_nowplay')
                       task = asyncio.create_task(now_play())
               elif dt_a == anime and n_f == 0:
                   pass
                   n_f = n_f + 1
                   logger.debug('wakeup_anime_waight')
                   now_r = random.choices([0, 1], weights=[1, 2])
                   logger.debug(now_r)
                   
                   if now_r == [0]:
                       logger.debug('wakeup_anime_def')
                       task = asyncio.create_task(anime_def())
               elif dt_a == anime and n_g == 0:
                   n_g = n_g + 1
                   logger.debug('wakeup_menu')
                   task = asyncio.create_task(menu_a())
               elif dt_a == markov_t_1  and n_h_1 == 0:
                   n_h_1 = n_h_1 + 1
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
               elif dt_a == markov_t_2 and n_h_2 == 0:
                   n_h_2 = n_h_2 + 1
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
               elif dt_a == markov_t_3 and n_h_3 == 0:
                   n_h_3 = n_h_3 + 1
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
               elif dt_a == markov_t_4 and n_h_4 == 0:
                   n_h_4 = n_h_4 + 1
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
               elif dt_a == markov_t_5 and n_h_5 == 0:
                   n_h_5 = n_h_5 + 1
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
               elif dt_a == weather_t and n_i == 0:
                   n_i = n_i + 1
                   logger.debug('wakeup_weather')
                   task = asyncio.create_task(weather_get_sche())
               elif dt_a == 'test' and n_test == 0:
                  print(type(n_test))
                  n_test = n_test + 1
                  logger.debug('wakeup_asy_test')
                  await asy_test()

               #以後周回処理
               elif dt_a == '23:59':
                   logger.debug('circle1')  
                   n_date = 0
               elif dt_a == '00:00' and n_date == 0:
                   logger.debug('circle_break')
                   break
               else:
                  pass
               await asyncio.sleep(10)
           continue
       except Exception:
            logger.debug(traceback.format_exc())
            logger.info('schedule_coroutine_exception')

###########home_get##############

async def runner():
 #task1 = asyncio.create_task(schedule_a())
 #await task1
 async with websockets.connect(WS_URL) as ws:
  try:
      await ws.send(json.dumps({
          "type": "connect",
          "body": {
                   "channel": "homeTimeline",
                   "id": "test"
                   }
          }))
      data = json.loads(await ws.recv())
      logger.debug(data)    
      while True:
          try:
     
               data = json.loads(await ws.recv())
               logger.debug(data)    
               if data['type'] == 'channel':
                   if data['body']['type'] == 'note': 
                       note = data['body']['body']
                       user = data['body']['body']['user']
                       task = asyncio.create_task(on_note(note, user))
                   elif data['body']['type'] == 'followed':
                       user = data['body']['body']
                       task = asyncio.create_task(on_follow(user))
          except Exception:
               logger.debug(traceback.format_exc())
               logger.error('Connection_closed')
               os.execv(sys.executable, ['python'] + sys.argv)
        
  except Exception:
      logger.debug(traceback.format_exc())
      logger.error('ws_error')
      os.execv(sys.executable, ['python'] + sys.argv)

###########home_folloing#########
      
async def on_follow(user):
    try:
        mk.following_create(user['id'])
        logger.info('refollow_clear')
    except:
        logger.error('refollow_error') 

###########home_exe(mention,reaction,call)##############

async def on_note(note,user):
    logger.debug('async_def_onnote')
    if note.get('mentions'):
        logger.debug('scan_mention')  
        if MY_ID in note['mentions']:
            logger.debug('scan_mention_myid')  
            USER_NAME = 'test_name'
            e.reply = note['text'].replace('@astrolabe ', '').replace('@astrolabe　', '')
            logger.debug(e.reply) 
            if e.reply.startswith(('help', 'info', '機能')):
                info_text = ('''私に興味を持って下さり、ありがとうございます。\n私にはたくさんの機能が搭載されています！！\n
○自動的に様々なノートをします。
・お天気、朝の挨拶、RSS配信、音楽のナウプレイング、アニメの思い出し、ご飯紹介、夜の挨拶、ノート増加数・フォロワー増加数の日次報告、マルコフ連鎖による自動ノート
・「アストロラーベちゃん」とノートするとランダムで返信する機能、特定の文字に反応してカスタム絵文字リアクションをする機能 
○リプライによるコマンド機能もあります。
・「help」「info」「機能」でこの内容を返信します
・「wether 都道府県」「天気 都道府県」でその都道府県の予報を返します。
・「meal」「ごはんガチャ」でご飯ガチャをやります。
・これらに該当しないリプライは全てLLMによって処理され、必ず何らかの内容を返信します。                             
......
                             ''')
                mk.notes_create(text=info_text, cw='わたくしアストロラーベの機能をご紹介します！', visibility=note['visibility'] , reply_id=note['id'])
                logger.debug('help_post')  
            elif e.reply.startswith(('Version', 'バージョン', '世代', '死活')):
                dt1 = datetime.datetime.now()
                dt1 =(str(dt1.strftime('%Y年%m月%d日%H時%M分%S秒')))
                opinion_text = ('アストロラーベは稼働中です\n' + dt1 + '\n' +  Ver)
                logger.debug('version_post')  
                mk.notes_create(text=opinion_text, visibility=note['visibility'] , reply_id=note['id'])
            elif e.reply.startswith(('meal', 'ご飯ガチャ', 'ごはん', 'ご飯', '献立')):
                dbreader = DBReader(settings.dbname, "menu")
                column_a = 0
                column_data_a = dbreader.get_column(column_a) 
                test = str(random.choices(column_data_a)).replace("['", "").replace("']", "")
                test = '厳正なるご飯ガチャの結果は\n「' + test + '」でした！\nまたのご依頼、お待ちしています。\n（私は現在517の献立をご紹介できます！）'
                mk.notes_create(text=test, visibility=note['visibility'] , reply_id=note['id'])
            elif e.reply.startswith(('weather', '天気', '天気予報')):
                input1 = e.reply
                input1 = input1.replace('weather', '').replace('天気', '').replace('天気予報', '')
                input1 = input1.replace(' ', '').replace('　', '')
                #print(input1) 
                if input1.endswith('東京'):
                    input1 = input1 + '都'
                elif input1.endswith(('大阪', '京都')):
                    input1 = input1 + '府'
                elif input1.endswith(('道', '都', '府','県')):
                    pass
                else :
                    input1 = input1 + '県'
                #print(input1)      
                pref_get = input1
                dbreader = DBReader(settings.dbname, "weather")
                # 取得したい列番号を定義する
                column_a = 3
                column_b = 6
                column_c = 14
                column_d = 2
                column_e = 7
                column_f = 8
                column_g = 9
                # n列目のデータのリストを取得する
                column_data_a = dbreader.get_column(column_a)
                column_data_b = dbreader.get_column(column_b)
                column_data_c = dbreader.get_column(column_c)
                column_data_d = dbreader.get_column(column_d)


                input1_test = [input1]
    
                #print(column_data_a)
                if input1 in  column_data_a:
                    dt1 = datetime.datetime.now()
                    name0 = (str(dt1.strftime('%Y年%m月%d日')))
                    index1 = column_data_a.index(input1)
                    url_get = column_data_b[index1]
                    time_get = column_data_c[index1]
                    id_get = column_data_d[index1]

                    
        
                    if name0 == time_get:
                        logger.debug('weather_reuse')  
                        name1 = dbreader.get_column(column_e)
                        name2 = dbreader.get_column(column_f)
                        name3 = dbreader.get_column(column_g)
                        name1 = str(name1[index1]).replace("['", "").replace("']", "")
                        name2 = str(name1[index1]).replace("['", "").replace("']", "")
                        name3 = str(name1[index1]).replace("['", "").replace("']", "")
                        weather_mk = 'ご利用ありがとうございます！\n' + pref_get + 'のお天気は、今日は' + name1 + '\n明日は(も) ' + name2 + '\n明後日は(も)' + name3 + 'です。これは気象庁から取得した、' + name0 + '時点の予報です。\nこの予報を生命及び財産の保護等に使わないで下さい。\n(正確かつ最新の予報は直接取得して下さい)'
                        #print(weather_mk)
                    else :
                        #print(url_get)
                        logger.debug('weather_get')  
                        task = asyncio.create_task(weather_get(url_get, id_get, pref_get))
                        g_note = await task
                        mk.notes_create(text=g_note, visibility=note['visibility'] , reply_id=note['id'])
                        logger.debug('weather_post')  
                else :
                    g_note = '申し訳ありません。都道府県を認識出来ませんでした。\nこの機能はコマンドの為、「weather 都道府県」「天気 都道府県」の文法を厳守してください。（他に何も書かないでください）\n繰り返し失敗する場合はマスターにご連絡をお願いします。ID:' + settings.Master_NAME
                    mk.notes_create(text=g_note, visibility=note['visibility'] , reply_id=note['id'])
                    logger.debug('none_get_pref')  
            elif user['id'] == settings.Master_ID:#管理者用リプライ制御機能
                logger.debug('scan_masterID') 
                if e.reply.startswith(('停止', 'stop', '終了')):
                    mk.notes_create(text='システムを終了します', visibility=note['visibility'] , reply_id=note['id'])
                    sys.exit()
                elif e.reply.startswith(('再起動', 'restart', 'アプデ')):
                    mk.notes_create(text='システムを再起動します', visibility=note['visibility'] , reply_id=note['id'])
                    os.execv(sys.executable, ['python'] + sys.argv)
                elif e.reply.startswith(('テスト', 'test', '試験')):
                    mk.notes_create(text='コードに設定されている関数を実行します', visibility=note['visibility'] , reply_id=note['id'])
                    import nitizi
                elif e.reply.startswith(('代理', '投稿', '代理投稿')):
                    toukou = e.reply.replace('代理', '',1).replace('投稿', '',1).replace('代理投稿', '',1)
                    toukou = toukou.replace('にゃ', 'な')
                    mk.notes_create(text=toukou, visibility='home')
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
        try:

            if user['id'] == settings.AI_ID:
                logger.debug('into_home_else_astrolabe_note')

            else:
                logger.debug('into_home_else_nomal_note')
                node = note['text']
                node = node + '。\n'
                node = node.replace('。。', '。')
                node = re.sub(r'。', '。\n', node, flags=re.MULTILINE)#文中読点の改行
                node = re.sub(r"https:.*", "", node, flags=re.MULTILINE)#https削除
                node = re.sub(r":.*:", "", node, flags=re.MULTILINE)#カスタム絵文字削除
                node = re.sub(r"<.*>", "", node, flags=re.MULTILINE)
                node = re.sub(r"[.*]", "", node, flags=re.MULTILINE)
                node = re.sub(r"@.* ", "", node, flags=re.MULTILINE)#メンション削除
                node = re.sub(r"#.* ", "", node, flags=re.MULTILINE)#ハッシュタグ削除
                node = re.sub(r"#", "", node, flags=re.MULTILINE)#ハッシュタグ取り切れないもの削除
                node = re.sub(r'^.{1,10}$', '', node, flags=re.MULTILINE)#短文削除
                node = re.sub(r"　", "", node, flags=re.MULTILINE)#空白削除
                node = re.sub(r'^\s*\n', '', node, flags=re.MULTILINE)#空白行削除
                node = emoji.replace_emoji(node, replace="")#絵文字削除
                node = node.replace('にゃ', 'な')
                with open(settings.home_cashtxt, 'a', encoding='utf-8') as f:
                    f.writelines(node)
                    logger.debug('record_home_note')
                
                logger.debug('not_scan_mention')
            
                if 'アストロラーベちゃん' in note['text']:
                    logger.debug('call_astrolabe')
                    test_call = random.choices([1, 2], weights=[1, 2])
                    logger.debug(test_call)
                    logger.debug('detection_astrolabe')
                    if test_call == [1]:
                        await asyncio.sleep(10)    
                        logger.debug('reply_yobidashi')
                        mk.notes_create(text='呼びましたか？？', reply_id=note['id'])
                    else :
                    
                        pass
                else:
                    logger.debug('not_detection_astrolabe')
                    scan_list_ohayou = r'ohayou|おはよう|おきた|起床|morning'
                    scan_list_oyasumi = r'oyasumi|おやすみ|寝る|就寝|good night'
                    scan_list_kawaii = r'カワイイ|可愛い|かわいい'
                    scan_list_oishii = r'美味しい|おいしい|おいしみ'
                    scan_list_tiken = r'知見があっぷ|知見がアップ|rs_tiken_up|ちけんがあっぷ|なんだ|らしい|にゃんだ'
                    scan_list_gohan = r'ごはん|おひる|よるごはん|あさごはん|朝ご飯|お昼|夜ご飯'
                    if (re.compile(scan_list_ohayou)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_ohayou)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_ohayou')
                    elif (re.compile(scan_list_oyasumi)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_oyasumi)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_oyasumi')
                    elif (re.compile(scan_list_kawaii)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_kawaii)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_kawaii')
                    elif (re.compile(scan_list_oishii)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_oishii)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_oishii')
                    elif (re.compile(scan_list_tiken)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_tiken)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_tiken')
                    elif (re.compile(scan_list_gohan)).search(note['text']):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(settings.note_list_gohan)).replace("['", "").replace("']", "") 
                        mk.notes_reactions_create(note_id=note['id'], reaction=test)
                        logger.debug('reaction_gohan')
                        #mk.notes_reactions_create(note_id=note['id'], reaction=':kawaii_comment:')
                    else:
                        logger.debug('not_conditions_reaction')
        except Exception:
         
            logger.debug(traceback.format_exc())
            logger.debug('occurrence_exception')

###########manage##############


async def main():
    await asyncio.gather(runner(), schedule_coroutine())

if __name__ == "__main__":
	asyncio.run(main()) 

logger.info('all_code_read') 
