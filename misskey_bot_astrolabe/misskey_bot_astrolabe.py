#!//home/share/venv/bin/python3.11
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO, WARNING, ERROR
from timeit import Timer
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
import configparser
import subprocess
from concurrent.futures import ProcessPoolExecutor
import nlplot
import plotly
from plotly.subplots import make_subplots
from plotly.offline import iplot
import matplotlib.pyplot as plt

Ver = 'v.1.92.00'
"v.1.91.00:ふつおた機能の実装、投稿管理の外部化(JSON)、設定のINI化、リフォロー機能の修正、MisskeyAPI利用の内製化、コード見直しによるウェブソケット切断時の再読込範囲の削減"
"v.1.92.00:ワードクラウド機能の実装。再読込の際、処理が高速に行われる問題の修正、起動メッセージの修正、起動報告のDMが複数回送られる問題の修正"
#print(Ver)
logger = getLogger("astrolabe_logs")
TOKEN = 0
Master_ID = 0
Master_NAME = 0
TOKEN = 0
AI_ID = 0
AI_NAME = 0
USER_NAME = 0
LLMPATH = 0


SERVER_URL = 0
RSS_URL_a = 0
RSS_URL_b = 0
cashtxt = 0
home_cashtxt = 0
cash2txt = 0
note_list_ohayou = 0
note_list_oyasumi = 0
note_list_kawaii = 0
note_list_oishii = 0
note_list_tiken = 0
note_list_gohan = 0
note_list_labe = 0
note_list_ittekimasu = 0
note_list_kitaku = 0
csvname = 0
dbname = 0
JSON_PATH = 0
GTL_CASH_CSV = 0
GTL_CASH_CSV_00to04 = 0
GTL_CASH_CSV_04to08 = 0
GTL_CASH_CSV_08to12 = 0
GTL_CASH_CSV_12to16 = 0
GTL_CASH_CSV_16to20 = 0
GTL_CASH_CSV_20to24 = 0
MECAB_DIR = 0
IMG_SAVE_DIR = 0
PATH = 0

WS_URL = 0

def config_main(ini_header, ini_key):
    
    PATH = os.path.dirname(os.path.abspath(__file__)) 
    config_main_ini = configparser.ConfigParser(interpolation=None)
    config_main_ini.read(fr'{PATH}/common.ini', encoding='utf-8-sig')
    ini_header = ini_header.replace('"', '')
    ini_key = ini_key.replace('"', '')

    ini_header.replace('"', '')
    
    read_ini = config_main_ini[f'{ini_header}'][f'{ini_key}']
    return read_ini

def config_accounts(ini_header, ini_key):
    PATH = os.path.dirname(os.path.abspath(__file__)) 
    config_main_ini = configparser.ConfigParser(interpolation=None)
    config_main_ini.read(fr'{PATH}/accounts.ini', encoding='utf-8-sig')
    ini_header = ini_header.replace('"', '')
    ini_key = ini_key.replace('"', '')
    read_ini = config_main_ini[f'{ini_header}'][f'{ini_key}']
    return read_ini

def create_note(visibility, note_text):
    try:
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        note_text = note_text.replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': f'{visibility}',
    "text": f'{note_text}', 
    }
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r)  
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()

def create_note_with_file(visibility, note_text, img_id):
    try:
        logger.debug(f'start_create_note_with_file')
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        note_text = note_text.replace('"', '')
        img_id = str(img_id).replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': f'{visibility}',
    "text": f'{note_text}', 
    "fileIds": [f'{img_id}'], 
    
    }
        
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(pyload1)  
        logger.debug(r)  
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
        
def create_dm(note_text, usr_id):
    try:
        #print('test2')
        headers = {"Content-Type": "application/json"}
        note_text = note_text.replace('"', '')
        usr_id = usr_id.replace('"', '')
        
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': 'specified',
    "text": f'{note_text}', 
    "visibleUserIds": [usr_id]
    }
        
        #print(url1)
        #print(pyload1)
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r.text)  
        #print(r.text)
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()

def create_dm_cw(note_text, cw_text, usr_id):
    try:
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        note_text = note_text.replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': 'specified',
    "text": f'{note_text}', 
    "visibleUserIds": [usr_id], 
    "cw": f'{cw_text}'
    
    }
        
        #print(url1)
        #print(pyload1)
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r.text)  
        #print(r.text)
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
        
def create_reply(visibility, note_text, note_id):
    try:
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        note_text = note_text.replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': f'{visibility}',
    "text": f'{note_text}', 
    "replyId": f'{note_id}'
    }
        
        #print(url1)
        #print(pyload1)
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r.text)  
        #print(r.text)
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
        
def create_reply_cw(visibility, note_text, cw_text, note_id):
    try:
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        cw_text = cw_text.replace('"', '')
        note_text = note_text.replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': f'{visibility}',
    "text": f'{note_text}', 
    "cw": f'{cw_text}',
    "replyId": f'{note_id}'
    }
        
        #print(url1)
        #print(pyload1)
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r.text)  
        #print(r.text)
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()

def create_note_cw(visibility, note_text, cw_text):
    try:
        headers = {"Content-Type": "application/json"}
        visibility = visibility.replace('"', '')
        cw_text = cw_text.replace('"', '')
        note_text = note_text.replace('"', '')
        url1 = f"https://{SERVER_URL}/api/notes/create"
        pyload1 = {
    "i": f"{TOKEN}",
    'visibility': f'{visibility}',
    "text": f'{note_text}', 
    "cw": f'{cw_text}',
    }
        
        #print(url1)
        #print(pyload1)
        pyload1 = json.dumps(pyload1)
        r = requests.post(url1, data=pyload1, headers=headers) 
        logger.debug(r.text)  
        #print(r.text)
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
        
def create_reaction(reaction, note_id):
    try:
        headers = {"Content-Type": "application/json"}
        reaction = reaction.replace("'", '')
        #print(reaction)
        url3 = f"https://{SERVER_URL}/api/notes/reactions/create"
        pyload3 = {
    "i": f"{TOKEN}",
    "noteId": f'{note_id}',
    "reaction": f'{reaction}',
        }
        pyload3 = json.dumps(pyload3)
        r = requests.post(url3, data=pyload3, headers=headers) 
    except Exception:
        pass
    
def create_follow(usr_id):
    try:
        headers = {"Content-Type": "application/json"}
        #print(reaction)
        url3 = f"https://{SERVER_URL}/api/following/create"
        pyload3 = {
    "i": f"{TOKEN}",
    "userId": f'{usr_id}',
        }
        pyload3 = json.dumps(pyload3)
        print('follow_ok')
        r = requests.post(url3, data=pyload3, headers=headers) 
    except Exception:
        pass

def delete_follow(usr_id):
    try:
        headers = {"Content-Type": "application/json"}
        #print(reaction)
        url3 = f"https://{SERVER_URL}/api/following/delete"
        pyload3 = {
    "i": f"{TOKEN}",
    "userId": f'{usr_id}',
        }
        pyload3 = json.dumps(pyload3)
        r = requests.post(url3, data=pyload3, headers=headers) 
    except Exception:
        pass

def create_file(img_path):
    try:
        with open(img_path, 'rb') as f:
            #f = f.read()
            #f = base64.b64encode(f)
            logger.debug(f'start_create_file\n{img_path}')
            url1 = f"https://{SERVER_URL}/api/drive/files/create"
            headers = {"Content-Type": "multipart/form-data"}
            print(type(f))
            #print(f)
            params = {
                  'i' : f'{TOKEN}',
                  }
            #print(type(params))
            #print('########################################################')
            #pyload1 = json.dumps(params)
            r = requests.post(
                url1, 
                data=params,
                files={'img' : f},
                #headers=headers,
                )
            logger.debug(f'{r}\n{r.text}')
            #print(r.text)
            #print(r)
            #print(r.text)
            #print(r.content)
            media_id = json.loads(r.content)
            
            media_id = media_id['id']

            logger.info(f'create_fila\nimg_path:{img_path}\nmedia_id:{media_id}')
            return media_id
        #logger.debug(r) 
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
    

def get_meta():
    pass

def get_users_show():
    try:
        headers = {"Content-Type": "application/json"}
        #print(reaction)
        url3 = f"https://{SERVER_URL}/api/users/show"
        pyload3 = {
    "i": f"{TOKEN}",
    "userId": f'{AI_ID}',
        }
        pyload3 = json.dumps(pyload3)
        r = requests.post(url3, data=pyload3, headers=headers) 
        return_text = json.loads(r.content)
        return return_text
    
    except Exception:
        pass
def get_emoji():
    pass

def json_write(key, value):
    if type(key) == str:
        key = key.replace('"', '')
    if type(value) == str:
        value = value.replace('"', '')
    
    with open(JSON_PATH) as f:
        d_update = json.load(f)
    d_update[f'{key}'] = value
    with open(JSON_PATH, 'w') as f:
        json.dump(d_update, f, indent=2)
        
def json_read(key):
    pass
    if type(key) == str:
        key = key.replace('"', '')
    with open(JSON_PATH) as f:
        d_update = json.load(f)
    return d_update[f'{key}']

def json_reset():
    pass
    d_update = {
    "n_a": 0,
    "n_b": 0,
    "n_c": 0,
    "n_d_0": 0,
    "n_d_1": 0, 
    "n_d_2": 0, 
    "n_e": 0,
    "n_f": 0, 
    "n_g": 0,
    "n_h_1": 0,
    "n_h_2": 0,
    "n_h_3": 0,
    "n_h_4": 0,
    "n_h_5": 0,
    "n_i": 0,
    "n_test": 0,
    "end_alos": 0
}
    with open(JSON_PATH, 'w') as f:
        json.dump(d_update, f, indent=2)
        

def dt1():
    try:
        global PATH
        dt1 = datetime.datetime.now()
        PATH = os.path.dirname(os.path.abspath(__file__)).replace(os.sep,'/')
        

        FORMAT = config_main("INSTANCE", "format")
        FORMAT = FORMAT.replace('"', '')
        args = sys.argv
        log_date = args[1]
        dt2 = PATH + '/log/' + log_date + '.log'
        logger.setLevel(DEBUG)
        fl_handler = FileHandler(filename= dt2 , encoding="utf-8")
        fl_handler.setLevel(DEBUG)
        fl_handler.setFormatter(Formatter(FORMAT))
        logger.addHandler(fl_handler)
        global SERVER_URL
        global RSS_URL_a
        global RSS_URL_b 
        global RSS_URL_c
        global cashtxt
        global home_cashtxt
        global cash2txt
        global note_list_ohayou
        global note_list_oyasumi
        global note_list_kawaii
        global note_list_oishii
        global note_list_tiken
        global note_list_gohan
        global note_list_labe
        global note_list_ittekimasu
        global note_list_kitaku
        global dbname
        global csvname
        global JSON_PATH
        global GTL_CASH_CSV
        global GTL_CASH_CSV_00to04
        global GTL_CASH_CSV_04to08
        global GTL_CASH_CSV_08to12
        global GTL_CASH_CSV_12to16
        global GTL_CASH_CSV_16to20
        global GTL_CASH_CSV_20to24
        global MECAB_DIR
        global IMG_SAVE_DIR
        
        SERVER_URL = config_main("INSTANCE", "SERVER_URL")
        RSS_URL_a = config_main("INSTANCE", "RSS_URL_a")
        RSS_URL_b = config_main("INSTANCE", "RSS_URL_b")
        RSS_URL_c = config_main("INSTANCE", "RSS_URL_c")
        cashtxt = config_main("INSTANCE", "cashtxt")
        cashtxt = PATH + "/" + cashtxt
        home_cashtxt = config_main("INSTANCE", "home_cashtxt")
        home_cashtxt = PATH + "/" + home_cashtxt
        cash2txt = config_main("INSTANCE", "cash2txt")
        cash2txt = PATH + "/" + cash2txt
        note_list_ohayou = config_main("INSTANCE", "note_list_ohayou")
        note_list_oyasumi = config_main("INSTANCE", "note_list_oyasumi")
        note_list_kawaii = config_main("INSTANCE", "note_list_kawaii")
        note_list_oishii = config_main("INSTANCE", "note_list_oishii")
        note_list_tiken = config_main("INSTANCE", "note_list_tiken")
        note_list_gohan = config_main("INSTANCE", "note_list_gohan")
        note_list_labe = config_main("INSTANCE", "note_list_labe")
        note_list_ittekimasu = config_main("INSTANCE", "note_list_ittekimasu")
        note_list_kitaku = config_main("INSTANCE", "note_list_kitaku")
        dbname = config_main("INSTANCE", "dbname")
        dbname = PATH + "/" + dbname
        csvname = config_main("INSTANCE", "csvname")
        csvname = PATH + "/" + csvname
        JSON_NAME = config_main("INSTANCE", "JSON_NAME")
        JSON_PATH = PATH + "/" + JSON_NAME  
        GTL_CASH_CSV = config_main("INSTANCE", "GTL_CASH_CSV")
        GTL_CASH_CSV_00to04 = config_main("INSTANCE", "GTL_CASH_CSV_00to04")
        GTL_CASH_CSV_04to08 = config_main("INSTANCE", "GTL_CASH_CSV_04to08")
        GTL_CASH_CSV_08to12 = config_main("INSTANCE", "GTL_CASH_CSV_08to12")
        GTL_CASH_CSV_12to16 = config_main("INSTANCE", "GTL_CASH_CSV_12to16")
        GTL_CASH_CSV_16to20 = config_main("INSTANCE", "GTL_CASH_CSV_16to20")
        GTL_CASH_CSV_20to24 = config_main("INSTANCE", "GTL_CASH_CSV_20to24")
        GTL_CASH_CSV = PATH + "/" + GTL_CASH_CSV  
        GTL_CASH_CSV_00to04 = PATH + "/" + GTL_CASH_CSV_00to04  
        GTL_CASH_CSV_04to08 = PATH + "/" + GTL_CASH_CSV_04to08  
        GTL_CASH_CSV_08to12 = PATH + "/" + GTL_CASH_CSV_08to12  
        GTL_CASH_CSV_12to16 = PATH + "/" + GTL_CASH_CSV_12to16  
        GTL_CASH_CSV_16to20 = PATH + "/" + GTL_CASH_CSV_16to20  
        GTL_CASH_CSV_20to24 = PATH + "/" + GTL_CASH_CSV_20to24  
        GTL_CASH_CSV = PATH + "/" + GTL_CASH_CSV  
        MECAB_DIR = config_main("INSTANCE", "MECAB_DIR")
        MECAB_DIR = PATH + "/" + MECAB_DIR  
        IMG_SAVE_DIR = config_main("INSTANCE", "IMG_SAVE_DIR")
        IMG_SAVE_DIR = PATH + "/" + IMG_SAVE_DIR
        #print(type(note_list_ohayou))
        global Master_ID
        global Master_NAME
        global TOKEN
        global AI_ID
        global AI_NAME
        global USER_NAME
        global LLMPATH


        TOKEN = config_accounts("MAIN", "TOKEN")
        Master_ID = config_accounts("MAIN", "Master_ID")
        Master_NAME = config_accounts("MAIN", "Master_NAME")
        AI_ID = config_accounts("MAIN", "AI_ID")
        AI_NAME = config_accounts("MAIN", "AI_NAME")
        USER_NAME = config_accounts("MAIN", "USER_NAME")
        LLMPATH = config_accounts("MAIN", "LLMPATH")
        LLMPATH = PATH + "/" + LLMPATH
        global WS_URL
        WS_URL_a = 'wss://' + SERVER_URL + '/streaming?i='
        WS_URL = WS_URL_a + TOKEN
        #print(WS_URL)
        opinion_text = ('アストロラーベのシステムが起動しました\n\n' + str(dt1) + '\n' +  Ver)
        time.sleep(2)
        #create_dm(opinion_text, Master_ID)
        #print(opinion_text)
        #os.exit

    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('Connection_closed_global')
        sys.exit()
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
                    #sys.exit()
        
        except Exception:

            logger.debug(traceback.format_exc())
            logger.error('Connection_closed_global')

            #print('error')
            #sys.exit()         #

async def note_captcha():# ノート取得
    try:
        #print('test1')
        #グローバル記録ブロック
        task = asyncio.create_task(global_runner())
        
        g_note = await task
        node = g_note
    
        #print(node) 
        with open(cashtxt, 'a', encoding='utf-8') as f:
            f.writelines(node)
            logger.debug('write_cashtxt')
    except Exception:
        pass                                

async def post_tl():# テキスト処理→テキスト生成→投稿
    try:
        #task = asyncio.create_task(note_captcha())
        await note_captcha()
    
        #print('back captcha')
        with open(cashtxt, "r", encoding = 'utf-8') as f1:
            text1 = f1.read()
            #print(text1)
        with open(home_cashtxt, "r", encoding = 'utf-8') as f2:
            text2 = f2.read()
            #print(text2)
        with open(cash2txt, "w", encoding = 'utf-8') as f3:
            text3 = text1 + text2
            f3.write(text3)

        mecab = MeCab.Tagger('-Owakati')
        text_1 = ''
        # ファイルを開く
        with open(cash2txt, "r", encoding = 'utf-8') as f:
            for line in f:# テキストファイルの品質確保
                node = re.sub(r'\b\w{1,10}\n', '', line)
                text_1 += node
            text_s = text_1.split('\n')
            text_1 = ''
            for text_f in text_s :# 分かち書き
                node = mecab.parse(text_f)
                #print(node)
                text_1 += node
        text_model = markovify.NewlineText(text_1, state_size=2, well_formed=False)#モデル生成
        dbreader = DBReader(dbname, "rssqa_1")
        column_a = 0
        column_data_a = dbreader.get_column(column_a)
        n_a = 0
        while True:
            markov_text = (text_model.make_short_sentence(40)) 
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
                create_note("public", markov_text)  
                logger.debug('markov_post')
                #字数制御ブロック（グローバル）
                with open(cashtxt, "r", encoding = 'utf-8') as f:
                    text = f.read()

                if len(text) > 2000:

                    line_count = len(text) // 2
                    new_text = text[line_count:]
                    # テキストファイルを書き換える
                    with open(cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('cashtxt_rewrite')
                elif len(text) > 10000:
                    new_text = ''
                    with open(cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('cashtxt_over10000_clear')
                

                #字数制御ブロック（ホーム）     
                with open(home_cashtxt, "r", encoding = 'utf-8') as f:
                    text = f.read()
                
                if len(text) > 500:
                    # テキストファイルの行数を取得する
                    line_count = len(text) // 2
                
                    # テキストファイルの先頭 half_line_count 行を削除する
                    new_text = text[line_count:]

                    # テキストファイルを書き換える
                    with open(home_cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('home_cashtxt_rewrite')
                elif len(text) > 10000:
                    new_text = ''
                    with open(home_cashtxt, "w", encoding = 'utf-8') as f:
                        f.write(new_text)
                        logger.debug('home_cashtxt_over10000_clear')
                #結合用の一時ファイル消去
                with open(cash2txt, "w", encoding = 'utf-8') as f:
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
###########schedule_exe#########

async def ohayou():
    	
	# DBReaderクラスのインスタンスを作成する
	dbreader = DBReader(dbname, "ohayou")
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
	create_note("public", test_a)  
	logger.info("def_ohayou clear")    

async def oyasumi():
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader(dbname, "oyasumi")
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
    create_note("public", test_a)  
    logger.info("def_oyasumi_oyasumi clear")  
    timer2 = random.randint(0, 50)
    timer2 = float(timer2)
    
    await asyncio.sleep(timer2)
    task = asyncio.create_task(nitizi_main())
    logger.info("def_oyasumi_nitizi clear")  
    return 'test'

async def nitizi_main():

    conn = sqlite3.connect(dbname)
    cur = conn.cursor()



    ##############設定ファイル##############
    df = pd.read_csv(csvname)# 設定ファイル行き
    get_users = get_users_show()
    #print(text)
    name1 = int(get_users["notesCount"])
    name2 = int(get_users["followersCount"])
    name3 = int(get_users["followingCount"])

    dbreader = DBReader(dbname, "sample")
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
        #get_users = get_users_show()
        #時間取得
        dt_now = datetime.datetime.now()
        def progre_time():
            dt2 = datetime.datetime.now()
            dt3 = dt2- dt1
            days = dt3.days
            hours, remainder = divmod(dt3.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            hours_cale = int(hours) - days*24
            progre_time2 = f"{days}日と{hours_cale}時間{int(minutes)}分{int(seconds)}秒"
            return  progre_time2
        progre_time2 = progre_time()
        #投稿文作成
        test = ('今日のノート投稿数は' + str(name1_c) + '、今日のフォロワー増加数は' + str(name2_c) + 'でした。\n以上、日次報告を終了します。')
        test_a = ('【日次報告】' + dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒') + "アストロラーベの日次自動メンテナンスが完了しました。\n全機能は正常です。稼働時間は" + progre_time2 + '。\n' + test)
        #print(test)
        #投稿関数
        create_note("home", test_a)  
        logger.info('post_nitizi')
        sql = "SELECT * FROM sample"
        cur.execute(sql)
        cur.execute(f"UPDATE sample SET today = {name1} WHERE name = 'notes'")
        cur.execute(f"UPDATE sample SET today = {name2} WHERE name = 'followers'")
        cur.execute(f"UPDATE sample SET today = {name3} WHERE name = 'following'")
        df = pd.read_sql_query(sql, conn)
        logger.debug(df)
        conn.commit()
        cur.close()
        conn.close()
        logger.debug('nitizi_db_write_ok')
    nitizi()

async def rss_a():
    dbreader = DBReader(dbname, "rssqa_1")
    dbreader_a = DBReader(dbname, "rss_reaction_1")
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
        feed = feedparser.parse(RSS_URL_a)
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
                create_note("public", text_a) 
                logger.info("def_rss_a clear(post)")    
                break
        elif n_a >= 10:
            logger.info("def_rss_a clear(Over_10)")    
            break    

async def rss_b():
    dbreader = DBReader(dbname, "rssqa_1")
    dbreader_a = DBReader(dbname, "rss_reaction_1")
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
    #print(RSS_URL_b)
    #print(test)
    n_a = 0
    while True:

        n= random.randint(1, 8)
        feed = feedparser.parse(RSS_URL_b)
        #print(feed)
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
                create_note("public", text_a)  
                logger.info("def_rss_b clear(post)")    
                break
        elif n_a >= 10:
            logger.info("def_rss_b clear(Over_10)")    
            break    


async def rss_c():
    dbreader = DBReader(dbname, "rssqa_1")
    dbreader_a = DBReader(dbname, "rss_reaction_1")
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
        feed = feedparser.parse(RSS_URL_c)
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
                create_note("public", text_a)  
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
       create_dm(cpu_and_disk, Master_ID)
       logger.warning("def_sys_check_diskuse(Over_90)_and_cpu_max_per(Over_90)")
       return
    elif usage__ >= 90.0:
       usage__ = str(usage__)
       usage_a = 'ディスク使用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' + usage__ + '％'
       create_dm(usage_a, Master_ID)
       logger.warning("def_sys_check_diskuse(Over_90)")
       return
    elif cpu_per_a >= 90.0:
       cpu_per_a = str(cpu_per_a)
       cpu_per_a_a =  'CPU論理プロセッサの最大利用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' +  cpu_per_a + '％'
       create_dm(cpu_per_a_a, Master_ID)
       logger.warning("def_sys_check_cpu_max_per(Over_90)")
       return
    else:
       logger.debug(cpu_per_a)  
       logger.debug(usage__)  
       sys_check_pass = 'システムチェックの結果問題はありませんでした'
       create_dm(sys_check_pass, Master_ID)
       logger.debug('syscheck_pass')  
       #print(cpu_per_a)
       #print(usage__)
       pass

async def now_play():
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader(dbname, "music")
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
    create_note("public", test_a)  
    logger.info("def_now_play_clear")      

async def anime_def():
    	
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader(dbname, "anime")
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
    create_note("public", test_a)  
    
async def menu_a():
    try:
        # DBReaderクラスのインスタンスを作成する
        dbreader = DBReader(dbname, "menu")
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
            create_note("public", test_a)  
            return test_a
            #投稿関数
        logger.debug('post_menu_dennar')  
        create_note("public", test_a)  
        timer2 = int(random.randint(39600, 46800))
        timer2 = float(timer2)
        logger.debug(timer2)  
        test_a = 'お腹減ってきたなぁ\nそういえば昨日の夜食べた「' + test + '」冷蔵庫に残ってたかも。\n温め直して食べよっと！'
        logger.debug('post_menu_moning')
        await asyncio.sleep(timer2)
        create_note("public", test_a)  
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
    conn = sqlite3.connect(dbname)
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
    dbreader = DBReader(dbname, "weather")
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
    create_note("public", g_note)  

async def asy_test():
    await asyncio.sleep(5)
    print('async test')

async def alos_nitizi():
    json_reset()
    await sleep(30)
    wordcloud_main(999)
    logger.info('alos_nitizi_clear')

###########schedule_ctrl##############

async def schedule_coroutine():
    dt = datetime.datetime.now()
    opinion_text = f'アストロラーベが起動されました.。\n（この通知はスケジュール系の起動と同期しています。\n\nVer:{Ver}\n時間:{dt}'
    create_dm(opinion_text, Master_ID)
    while True:
       try:
           
           with open(JSON_PATH) as f:
               d_update = json.load(f)
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
           rss_c_t = str(random.randint(15, 18)) + ':' + (anime_r.zfill(2))
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
           logger.debug(rss_c_t)

           logger.debug(nowplay)
           logger.debug(anime)
           logger.debug(markov_t_1)
           logger.debug(markov_t_2)
           logger.debug(markov_t_3)
           logger.debug(markov_t_4)
           logger.debug(markov_t_5)
           #動作制御

           n_date = 1#リセット用(1で正常。23:59に起こす)
           while True:
               dt = datetime.datetime.now()
               dt_a = (str(dt.strftime('%H:%M')))
               if dt_a == ohayou_t and json_read("n_a") == 0:                  
                  logger.debug('wakeup_ohayou')
                  task = asyncio.create_task(ohayou())
                  json_write("n_a", 1)
               elif dt_a == oyasumi_t and json_read("n_b") == 0:
                   logger.debug('wakeup_oyasumi')
                   task = asyncio.create_task(oyasumi())
                   json_write("n_b", 1)
               elif dt_a == sys_check_a_t and json_read("n_c") == 0:
                   logger.debug('wakeup_sys_check')
                   task = asyncio.create_task(sys_check_a())
                   json_write("n_c", 1)
               elif dt_a ==  rss_a_t and json_read("n_d_0") == 0:
                   logger.debug('wakeup_rss_a')
                   task = asyncio.create_task(rss_a())
                   json_write("n_d_0", 1)
               elif dt_a ==  rss_b_t and json_read("n_d_1") == 0:
                   logger.debug('wakeup_rss_b')
                   task = asyncio.create_task(rss_b())
                   json_write("n_d_1", 1)
               elif dt_a ==  rss_c_t and json_read("n_d_2") == 0:
                   logger.debug('wakeup_rss_c')
                   task = asyncio.create_task(rss_c())
                   json_write("n_d_2", 1)
               elif dt_a ==  nowplay and json_read("n_e") == 0:
                   logger.debug('wakeup_nowplay_waight')
                   now_r = random.choices([0, 1], weights=[1, 0.5])
                   logger.debug(now_r)
                   json_write("n_e", 1)
                   if now_r == [0]:
                       logger.debug('wakeup_nowplay')
                       task = asyncio.create_task(now_play())
                       
               elif dt_a == anime and json_read("n_f") == 0:
                   pass
                   logger.debug('wakeup_anime_waight')
                   now_r = random.choices([0, 1], weights=[1, 1.5])
                   logger.debug(now_r)
                   json_write("n_f", 1)
                   if now_r == [0]:
                       logger.debug('wakeup_anime_def')
                       task = asyncio.create_task(anime_def())
               elif dt_a == anime and json_read("n_g") == 0:
                   logger.debug('wakeup_menu')
                   task = asyncio.create_task(menu_a())
                   json_write("n_g", 1)
               elif dt_a == markov_t_1  and json_read("n_h_1") == 0:
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
                   json_write("n_h_1", 1)
               elif dt_a == markov_t_2 and json_read("n_h_2") == 0:
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
                   json_write("n_h_2", 1)
               elif dt_a == markov_t_3 and json_read("n_h_3") == 0:
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
                   json_write("n_h_3", 1)
               elif dt_a == markov_t_4 and json_read("n_h_4") == 0:
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
                   json_write("n_h_4", 1)
               elif dt_a == markov_t_5 and json_read("n_h_5") == 0:
                   logger.debug('wakeup_markov')
                   task = asyncio.create_task(post_tl())
                   json_write("n_h_5", 1)
               elif dt_a == weather_t and json_read("n_i") == 0:
                   logger.debug('wakeup_weather')
                   task = asyncio.create_task(weather_get_sche())
                   json_write("n_i", 1)
               elif dt_a == 'test' and json_read("n_test") == 0:
                  logger.debug('wakeup_asy_test')
                  json_write("n_test", 1)
                  await asy_test()
               elif dt_a == '04:00':
                  wordcloud_main(0)
               elif dt_a == '08:00':
                  wordcloud_main(1)
               elif dt_a == '12:00':
                  wordcloud_main(2)
               elif dt_a == '16:00':
                  wordcloud_main(3)
               elif dt_a == '20:00':
                  wordcloud_main(4)
               elif dt_a == '00:00':
                  wordcloud_main(5)
               #以後周回処理
               elif dt_a == '23:59':
                   logger.debug('circle1')  
                   n_date = 0
               elif dt_a == '00:00' and n_date == 0:
                   task = asyncio.create_task(alos_nitizi())
                   logger.debug('circle_break')
                   break
               await asyncio.sleep(60)
           continue
       except Exception:
            logger.debug(traceback.format_exc())
            logger.info('schedule_coroutine_exception')


###########Wordcloud##############
async def write_csv_gtl(df):
    try:    
        dt1 = datetime.datetime.now()
        record_time = int(dt1.strftime('%H'))
        if record_time == 0 or record_time == 1 or record_time == 2 or record_time == 3:
            df.to_csv(GTL_CASH_CSV_00to04, mode='a', header=False)
            
        elif record_time == 4 or record_time == 5 or record_time == 6 or record_time == 7:
            df.to_csv(GTL_CASH_CSV_04to08, mode='a', header=False)
        elif record_time == 8 or record_time == 9 or record_time == 10 or record_time == 11:
            df.to_csv(GTL_CASH_CSV_08to12, mode='a', header=False)
        elif record_time == 12 or record_time == 13 or record_time == 14 or record_time == 15:
            df.to_csv(GTL_CASH_CSV_12to16, mode='a', header=False)
        elif record_time == 16 or record_time == 17 or record_time == 18 or record_time == 19:
            df.to_csv(GTL_CASH_CSV_16to20, mode='a', header=False)
        elif record_time == 20 or record_time == 21 or record_time == 22 or record_time == 23:
            df.to_csv(GTL_CASH_CSV_20to24, mode='a', header=False)
    except Exception:
        logger.debug(traceback.format_exc())
        logger.info('write_csv_gtl_error')
            
async def csv_gtl_connect():
    pass
    

def wordcloud(df):
    try:
        tagger = MeCab.Tagger(fr'-chasen -d {MECAB_DIR}')
        text_list = df["text"].tolist()
        word_df = pd.DataFrame({'text': []}, index=[])
        # word_df["text"] = word_df["text"].astype("object")
        id_s = 0
        for text in text_list:
            text = str(text)
            word_list = []
            w = tagger.parse(text)
            node = tagger.parseToNode(text)
            while node:
                pos = node.feature.split(",")[0]
                # if pos == "形容詞" or pos == "名詞" or pos == "動詞":
                if pos == "形容詞" or pos == "名詞":

                    word_list.append(node.surface)
                node = node.next
            word_list = str(word_list).replace('[', '').replace(']', '').replace(',', ' ').replace("'", ' ')
            word_df.loc[f'{id_s}'] = [f'{word_list}']
            id_s = id_s + 1
        # print(word_list)
        # word_df = pd.DataFrame(word_list, columns=["Text"])
        # print(word_df)
        return word_df
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('wordcloud_error')
        
def wordcloud_main(toukatsu):
    try:
        time_sta2 = time.perf_counter()
        tagger = MeCab.Tagger(fr'-chasen -d {MECAB_DIR}')
        logger.debug(f'start_wordcloud_main')
        df = 0
        dt1 = datetime.datetime.now()
        record_time = int(dt1.strftime('%Y'))
        if toukatsu == 999:
            df0 = pd.read_csv(GTL_CASH_CSV_00to04)
            df1 = pd.read_csv(GTL_CASH_CSV_04to08)
            df0 = pd.concat([df0, df1])
            del df1
            df2 = pd.read_csv(GTL_CASH_CSV_08to12)
            df0 = pd.concat([df0, df2])
            del df2
            df3 = pd.read_csv(GTL_CASH_CSV_12to16)
            df0 = pd.concat([df0, df3])
            del df3
            df4 = pd.read_csv(GTL_CASH_CSV_16to20)
            df0 = pd.concat([df0, df4])
            del df4
            df5 = pd.read_csv(GTL_CASH_CSV_20to24)
            df0 = pd.concat([df0, df5])
            del df5
            df = df0

        elif toukatsu == 0:
            df = pd.read_csv(GTL_CASH_CSV_00to04)
        elif toukatsu == 1:
            df = pd.read_csv(GTL_CASH_CSV_04to08)
        elif toukatsu == 2:
            df = pd.read_csv(GTL_CASH_CSV_08to12)
        elif toukatsu == 3:
            df = pd.read_csv(GTL_CASH_CSV_12to16)
        elif toukatsu == 4:
            df = pd.read_csv(GTL_CASH_CSV_16to20)
        elif toukatsu == 5:
            df = pd.read_csv(GTL_CASH_CSV_20to24)
            
        inst_list = (df['instance'].value_counts(sort=True).index.tolist())
        inst_dict = (df['instance'].value_counts(sort=True).to_dict())
        inst_list_count = int(len(inst_list))
        inst_choice_random = random.randint(0, inst_list_count)
        #print(inst_list_count)
        #print(inst_choice_random)
        insetance_choice_name = inst_list[inst_choice_random]
        insetance_choice_count = inst_dict[insetance_choice_name]
        #print(insetance_choice_name)
        #print(insetance_choice_count)
        logger.debug(f'inst_list_count:{inst_list_count}\ninst_choice_random:{inst_choice_random}')
        usr_list = (df['id'].value_counts(sort=True).index.tolist())
        usr_dict = (df['id'].value_counts(sort=True).to_dict())
        usr_list_count = int(len(usr_list))
        #print(usr_list_count)
        usr_choice_random = random.randint(0, usr_list_count)
        #print(random__)
        usr_choice_name = usr_list[usr_choice_random]
        usr_choice_count = usr_dict[usr_choice_name]
        logger.debug(f'usr_list_count:{usr_list_count}\nusr_choice_random:{usr_choice_random}')
        #print(usr_choice_name)
        #print(usr_choice_count)


        start_time = df.iloc[0]['time']
        time__ = start_time.replace('T', ' ').replace('Z', '')
        dte1 = datetime.datetime.strptime(time__, '%Y-%m-%d %H:%M:%S.%f')

        end_time = df.iloc[-1]['time']
        time__ = end_time.replace('T', ' ').replace('Z', '')
        dte2 = datetime.datetime.strptime(time__, '%Y-%m-%d %H:%M:%S.%f')

        totalling_time = dte2 - dte1
        sec = totalling_time.total_seconds()
        print(sec)
        totalling_time_hours = int(sec // 3600)
        cale_time = 0
        cale_time_text = 0
        #print()
        if totalling_time.days >= 1:
            cale_time = totalling_time_hours + 24
        elif totalling_time.days == 0:
            cale_time = totalling_time_hours
        if cale_time == 0:
            cale_time = int(sec // 360)
            cale_time_text = str(f'{cale_time}分間')
        else :
            cale_time_text = str(f'{cale_time}時間')
        # print(df)
        split_n = 10000
        n = len(df)
        dfs = []
        df_count = n / split_n
        df_count = int(df_count)
        df_count = df_count + 1
        logger.debug(f'GTL_count{n}')
        #print(df_count)
        if toukatsu == 999:
            pass
        else :
            dataframes = [pd.DataFrame({'text': []}, index=[]) for _ in range(df_count)]
            for i in range(df_count):
                start = i * split_n
                end = start + split_n
                dataframes[i] = df.iloc[start:end]
            cpu_count = psutil.cpu_count()
        
            if cpu_count > 1:
                logger.debug(f'get_cpu_core{cpu_count}')
            else:
                logger.error('not_get_cpu_core_count')
                cpu_count = 4
            with ProcessPoolExecutor(max_workers=cpu_count) as executor:
                # Execute the `wordcloud` function on each DataFrame chunk
                results = list(executor.map(wordcloud, dataframes))
            #del df
            
            combined_df = pd.concat(results)
            

            # Concatenate the resulting DataFrames
        
            #combined_df.to_csv(mecab_csv_name)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
            #combined_df = pd.read_csv(mecab_csv_name)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            #print(combined_df)
    

            npt = nlplot.NLPlot(combined_df, target_col='text')
    
            stopwords = npt.get_stopword(top_n=0, min_freq=0) + ['こと', 'これ', 'それ', 'ない', 'さん', 'もん', 'やつ', 'なん', 'ちゃん', 'くん', '中', 'みたい', '何', 'ん', 'の', 'さ', 'ー', 'そう', '人', '色', 'the', 'of', 'to', 'and', 'in', 'blob', 'meltblob', 'cat', 'with', 'ちんこ', 'まんこ', 'ちんぽ', 'ごみ', 'カス', '死ね', '自殺', 'エッチ', 'エロ', 'グロ', '人身事故', '死', '系', 'nan', '型', '的', 'レイプ', 'a']
            '''
            fig_unigram = npt.bar_ngram(
            title='uni-gram',
            xaxis_label='word_count',
            yaxis_label='word',
            ngram=1,
            top_n=50,
            width=800,
            height=1100,
            color=None,
            horizon=True,
            stopwords=stopwords,
            verbose=False,
            save=False,
            )
            fig_unigram.show()
            '''
        
            #fig_unigram.write_image() 
    
            fig_wc = npt.wordcloud(
            width=1000,
            height=600,
            max_words=100,
            max_font_size=100,
            colormap='tab20_r',
            stopwords=stopwords,
            mask_file=None,
            save=False
            )
            plt.figure(figsize=(16, 9))
            plt.imshow(fig_wc, interpolation="bilinear")
            plt.axis("off")
            dt1 = datetime.datetime.now()
            file_name_time = str(dt1.strftime('%Y%m%d%H%M%S'))
            img_file_name = (f"{IMG_SAVE_DIR}/{file_name_time}.png") 
            plt.savefig(img_file_name) 
            
            #plt.show()
            '''
            test = npt.build_graph(stopwords=stopwords, min_edge_frequency=25)
            print(test)
    
            fig_co_network = npt.co_network(
            title='Co-occurrence network',
            sizing=100,
            node_size='adjacency_frequency',
            color_palette='hls',
            width=1100,
            height=700,
            save=False
            )
            test_plot = iplot(fig_co_network)
            '''
            #test_plot.write_image('test3.png')

            #df = pd.read_csv(GTL_CASH_CSV)

            
            #dataDelete = df.head(0)
            
            #del df
            #pass   

        n_calc = (n // 10000)
        n_calc_text = 0
        wc_text = 0
        if n_calc == 0 :
            n_calc_text = str(f'全{n_calc}件')
        else :
            n_calc_text = str(f'約{n_calc}万件')
        if toukatsu == 999:
            wc_text = ''
        else :
            wc_text = '、その特徴語が画像のワードクラウドです。'
            
        toukatsu_text = f'''私が直近{cale_time_text}に観測したGTLのデータです。{n_calc}万件の投稿があり{wc_text}
参加インスタンスは{inst_list_count}サーバ、参加ユーザー数は{usr_list_count}人でした。
なお、投稿数第{inst_choice_random}位のサーバは{insetance_choice_name}で{insetance_choice_count}件、投稿数第{usr_choice_random}位のユーザーは{usr_choice_name}さんで{usr_choice_count}件でした。
        '''    
        file_id = create_file(img_file_name)
        create_note_with_file("public", toukatsu_text, file_id)  
        df = df.head(0)
        
        if toukatsu == 999:
            df.to_csv(GTL_CASH_CSV, mode='a', header=False)
            GTL_CASH_CSV_temp = pd.DataFrame(columns=['time','instance','id','text'])
            GTL_CASH_CSV_temp = GTL_CASH_CSV_temp.set_index('time')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_00to04, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_04to08, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_08to12, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_12to16, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_16to20, mode='w')   
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_20to24, mode='w')
            logger.debug('del_GTL_CASH_CSV_ALL')
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('word_cloud_main_error')

async def cloud_global_runner():#グローバル受信系

    #task1 = asyncio.create_task(schedule_a())
    #await task1
    async with websockets.connect(WS_URL) as ws:
        g_n = 0
        buf_gr = ''
        buf_gr_1 = ''
        node_cash = str("")
        while True:
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
                break_parm = int(0)
                df = pd.DataFrame({'instance': [],
                                   'usr_id': [],
                                   'note': []},
                                  index=[])
                while True:
                   
                    try:
                    
                        data = json.loads(await ws.recv())
                        #logger.debug(data)    
                        #print('get_global')
                        #print(data)
                        if data['type'] == 'channel':
                            if data['body']['type'] == 'note': 
                                #print('gtl_get')
                                note = data['body']['body']
                                #print(note)
                                time = data['body']['body']['createdAt']
                                name = data['body']['body']['user']['name']
                                try:
                                     instance = data['body']['body']['user']['instance']['name']
                                except Exception:
                                     continue
                                if time == None:
                                    continue
                                elif name == None:
                                    continue
                                elif instance == None:
                                    continue
                                time = str(time)
                                usr_id = str(name)
                                instance =  str(instance)
                                buf_note =  note['text']
                                if buf_note == None:
                                    continue
                                else :
                                    #print('test2')
                            
                                
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
                                    #node = re.sub(r'^.{1,10}$', '', node, flags=re.MULTILINE)#短文削除
                                    node = re.sub(r"　", "", node, flags=re.MULTILINE)#空白削除
                                    node = re.sub(r'^\s*\n', '', node, flags=re.MULTILINE)#空白行削除
                                    node = emoji.replace_emoji(node, replace="")#絵文字削除
                                    node = node.replace('にゃ', 'な')
                                
                                    #print(type(node))
                                
                                    #node_cash = node_cash + node
                                    #print(node)
                                    break_parm = break_parm + 1
                                    #print(node_cash)
                                    #======================================本番はiniに収容する変数
                                    #生成系をdt1に追記。既存があれば上書きしない形。日次から貰ったyyyymmddデータをf{}で収容。削除系は検討。結果データだけあれば良いのはそう。
                                
                                    #======================================
                                
                                    #print(break_parm)
                                    #print(df)

                                    df.loc[f'{time}'] = [f'{instance}', f'{usr_id}', f'{node}']
                                    #print(df)


                                
                                    test_time = "23:59"
                                    dt = datetime.datetime.now()
                                    dt_a = (str(dt.strftime('%H:%M')))
                                    #if dt_a == test_time:
                                    if break_parm >= 50:
                                        break_parm = 0
                                        logger.debug('gtl_record')
                                        task = asyncio.create_task(write_csv_gtl(df))
                                    
                                        #print('fin')

                                        '''
                                        #cloud_gtl_write(node_cash)
                                        table = 'gtl'
                                        task = asyncio.create_task(get_column(dbname, table__, time, instance, usr_id, node_cash))
                                        break_parm = 0
                                        print('fin2')'''
                    except Exception:
                        pass
            except Exception:
                logger.debug(traceback.format_exc())
                logger.error('Connection_closed_global')
                await sleep(5)
                break


###########home_get##############


async def runner():
     #task1 = asyncio.create_task(schedule_a())
     #await task1
     async with websockets.connect(WS_URL) as ws:
          while True: 
              try:
                  await ws.send(json.dumps({
                      "type": "connect",
                      "body": {
                               "channel": "homeTimeline",
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
                                   user = data['body']['body']['user']
                                   task = asyncio.create_task(on_note(note, user))
                      except Exception:
                           logger.debug(traceback.format_exc())
                           logger.error('Connection_closed')
                           pass
        
              except Exception:
                  logger.debug(traceback.format_exc())
                  logger.error('ws_error')
                  await sleep(5)
                  break
      
###########main_get##############

async def runner_main():
     #task1 = asyncio.create_task(schedule_a())
     #await task1
     async with websockets.connect(WS_URL) as ws:
          while True:
              try:
                  await ws.send(json.dumps({
                      "type": "connect",
                      "body": {
                               "channel": "main",
                               "id": "test"
                               }
                      }))
                  data = json.loads(await ws.recv())
                  #rint("test2")
                  while True:
                      #print("test3")
                      try:
     
     
                           data = json.loads(await ws.recv())
                           #print(data)
               
                           if data['type'] == 'channel':
                               #print('channel')
                               test = data['body']['type']
                               #print(test)
                               if data['body']['type'] == 'followed': 
                                   #print('follow')
                                   user = data['body']['body']['id']
                                   #print(user)
                                   create_follow(user)
                                   #task = asyncio.create_task(on_follow(user))


                      except Exception:
                           logger.debug(traceback.format_exc())
                           logger.error('ws_main_error')
                           pass
                           #print((traceback.format_exc()))

        
              except Exception:
                  logger.debug(traceback.format_exc())
                  logger.error('ws_main_error')
                  await sleep(5)
                  break



###########home_exe(mention,reaction,call)##############

async def on_note(note,user):
    logger.debug('async_def_onnote')
    if note.get('mentions'):
        logger.debug('scan_mention')  
        if AI_ID in note['mentions']:
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
                cw_text = 'わたくしアストロラーベの機能をご紹介します！'
                create_reply_cw(note['visibility'], info_text, cw_text, note['id'])
                logger.debug('help_post')  
            elif e.reply.startswith(('Version', 'バージョン', '世代', '死活')):
                dt1 = datetime.datetime.now()
                dt1 =(str(dt1.strftime('%Y年%m月%d日%H時%M分%S秒')))
                opinion_text = ('アストロラーベは稼働中です\n' + dt1 + '\n' +  Ver)
                logger.debug('version_post')  
                create_reply(note['visibility'], opinion_text, note['id'])
            elif e.reply.startswith(('meal', 'ご飯ガチャ', 'ごはん', 'ご飯', '献立')):
                dbreader = DBReader(dbname, "menu")
                column_a = 0
                column_data_a = dbreader.get_column(column_a) 
                test = str(random.choices(column_data_a)).replace("['", "").replace("']", "")
                test = '厳正なるご飯ガチャの結果は\n「' + test + '」でした！\nまたのご依頼、お待ちしています。\n（私は現在517の献立をご紹介できます！）'
                create_reply(note['visibility'], test, note['id'])
            elif e.reply.startswith(('ふつおた', 'おたより', 'お便り', '掲示板')):
                input1 = e.reply.replace('ふつおた', '',1).replace('おたより', '',1).replace('お便り', '',1).replace('掲示板', '',1)
                input2 = re.search(r' (.+) ', input1)
                input3 = input1.replace(f'{input2}', '',1)
                visibility = 'public'
                #print(input1)
                #print(input2)
                #print(input3)
                if input2 == None:
                    
                    input2 = '匿名希望さんからのおたよりです！'
                    create_note_cw("public", input3, input2)
                else:
                    input2 = input2.group(1)
                    input3 = input1.replace(f'{input2}', '',1)
                    input2 = f'{input2}さんからのおたよりです！'
                    create_note_cw("public", input3, input2)
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
                dbreader = DBReader(dbname, "weather")
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
                        create_reply(note['visibility'], weather_mk, note['id'])
                        #print(weather_mk)
                    else :
                        #print(url_get)
                        logger.debug('weather_get')  
                        task = asyncio.create_task(weather_get(url_get, id_get, pref_get))
                        g_note = await task
                        create_reply(note['visibility'], g_note, note['id'])
                        logger.debug('weather_post')  
                else :
                    g_note = '申し訳ありません。都道府県を認識出来ませんでした。\nこの機能はコマンドの為、「weather 都道府県」「天気 都道府県」の文法を厳守してください。（他に何も書かないでください）\n繰り返し失敗する場合はマスターにご連絡をお願いします。ID:' + Master_NAME
                    create_reply(note['visibility'], g_note, note['id'])
                    logger.debug('none_get_pref')  
            elif user['id'] == Master_ID:#管理者用リプライ制御機能
                logger.debug('scan_masterID') 
                if e.reply.startswith(('停止', 'stop', '終了')):
                    g_note='システムを終了します'
                    create_reply(note['visibility'], g_note, note['id'])
                    json_write("end_alos", 1)
                    sys.exit()
                elif e.reply.startswith(('再起動', 'restart', 'アプデ')):
                    g_note='システムを再起動します'
                    create_reply(note['visibility'], g_note, note['id'])
                    for process in executor._processes.values():
                        process.kill()
                    sys.exit()
                elif e.reply.startswith(('テスト', 'test', '試験')):
                    e.reply = e.reply.replace('テスト', '',1).replace('test', '',1).replace('試験', '',1)
                    g_note =f"テストとして指定された関数・機能を実行します。実行内容：{e.reply}"
                    create_reply(note['visibility'], g_note, note['id'])
                    eval(f'{e.reply}')
                    
                    #########################
                    #########################
                elif e.reply.startswith(('代理', '投稿', '代理投稿')):
                    toukou = e.reply.replace('代理', '',1).replace('投稿', '',1).replace('代理投稿', '',1)
                    toukou = toukou.replace('にゃ', 'な')
                    create_note('home', toukou)
                    
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
                    cw_text='お待たせしました！丹精込めて答えましたよ～！'
                    create_reply_cw(note['visibility'], output_h, cw_text, note['id'])
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
                cw_text='お待たせしました！丹精込めて答えましたよ～！'
                create_reply_cw(note['visibility'], output_h, cw_text, note['id'])
                logger.info('lmm_post')
    else :
        try:

            if user['id'] == AI_ID:
                logger.debug('into_home_else_astrolabe_note')

            else:
                logger.debug('into_home_else_nomal_note')
                node = note['text']
                node = str(node)  + '。\n'
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
                with open(home_cashtxt, 'a', encoding='utf-8') as f:
                    f.writelines(node)
                    logger.debug('record_home_note')
                
                logger.debug('not_scan_mention')
                node_str = str(note['text'])
                if 'アストロラーベちゃん' in node_str:
                    logger.debug('call_astrolabe')
                    test_call = random.choices([1, 2], weights=[1, 2])
                    logger.debug(test_call)
                    logger.debug('detection_astrolabe')
                    if test_call == [1]:
                        await asyncio.sleep(10)    
                        logger.debug('reply_yobidashi')
                        note_text = '呼びましたか？？'
                        create_reply(note['visibility'], note_text, note['id'])
                    else :
                    
                        pass
                else:
                    logger.debug('not_detection_astrolabe')
                    scan_list_ohayou = r'ohayou|おはよう|おきた|起床|morning'
                    scan_list_oyasumi = r'oyasumi|おやすみ|寝る|就寝|good night'
                    scan_list_kawaii = r'カワイイ|可愛い|かわいい'
                    scan_list_oishii = r'美味しい|おいしい|おいしみ'
                    scan_list_tiken = r'知見があっぷ|知見がアップ|rs_tiken_up|ちけんがあっぷ|知らなかった|知見|なんだ$|なのか$'
                    scan_list_gohan = r'ごはん|おひる|よるごはん|あさごはん|朝ご飯|お昼|夜ご飯'
                    scan_list_labe = r'ラーベちゃん'
                    scan_list_ittekimasu = r'出勤|行ってきます|頑張ってきます|行ってくる|頑張ってくる'
                    scan_list_kitaku = r'退勤|仕事終わった|しごおわ|帰った|KITAKU|ただいま|帰宅'
                    
                    if (re.compile(scan_list_ohayou)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_ohayou))).replace("['", "").replace("']", "") 
                        #print(test)
                        create_reaction(test, note['id'])
                        logger.debug('reaction_ohayou')
                    elif (re.compile(scan_list_oyasumi)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_oyasumi))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_oyasumi')
                    elif (re.compile(scan_list_kawaii)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_kawaii))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_kawaii')
                    elif (re.compile(scan_list_oishii)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_oishii))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_oishii')
                    elif (re.compile(scan_list_tiken)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_tiken))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_tiken')
                    elif (re.compile(scan_list_gohan)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_gohan))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_gohan')
                    elif (re.compile(scan_list_labe)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_labe))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_labe')
                    elif (re.compile(scan_list_ittekimasu)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_ittekimasu))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_ittekimasu')
                    elif (re.compile(scan_list_kitaku)).search(node_str):
                        timer = (random.randint(4, 360))
                        timer = float(timer)
                        await asyncio.sleep(timer) 
                        test = str(random.choices(eval(note_list_kitaku))).replace("['", "").replace("']", "") 
                        create_reaction(test, note['id'])
                        logger.debug('reaction_kitaku')     
                    else:
                        logger.debug('not_conditions_reaction')
        except Exception:
         
            logger.debug(traceback.format_exc())
            logger.debug('occurrence_exception')

###########manage##############


def cloud_global_runner_1():
    try:
        asyncio.run(cloud_global_runner()) 
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()  
     


async def main():
    try:
        await asyncio.gather(runner(), schedule_coroutine(), runner_main())
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()  
def runner_low_load():
    try:
        asyncio.run(main()) 
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()  
        

if __name__ == "__main__":
    try:
        #asyncio.run(main()) 
        with ProcessPoolExecutor(max_workers=5) as executor:
            executor.submit(cloud_global_runner_1)
            executor.submit(asyncio.run(main()))
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()       


