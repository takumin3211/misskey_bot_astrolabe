#! /home/web/astrolabe/venv/bin/python3
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
from llama_cpp import Llama
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
import jaconv

Ver = 'V.01.94.16.26'
'メジャーバージョン（根本的な改変）:マイナーバージョン（大規模な変更）:リビジョン（細かな変更）:ビルド（バグ修正など）'
'V.01.94.00.00 2023/11/28 RSSの拡充(二つ)、Wikipedia記事紹介、スケジュール系のバグ修正、ワードクラウドの動作改善、ログ機能のバグ修正、ログレベルの変更機能、TL勉強機能の実装'
'V.01.94.01.00 2023/11/28 確率系の一部廃止、日次系のトリガー変更'
'V.01.94.02.00 2023/12/04 スクレイピングがサーバ環境で正常に動作していなかった問題を修正、グローバル系取得のバグ修正'
'V.01.94.03.00 2023/12/05 システムチェックとワードクラウドの時間重複による起動問題の修正、グローバル系取得の更なるバグ修正'
'V.01.94.10.00 2023/12/05 翻訳機能の実装、ワードクラウドの件数に関するバグ修正'
'V.01.94.11.00 2023/12/09 RSS系の取得ロジック変更（全数投稿に向けた拡張性確保）、DBメンテナンス（誤字等の修正）'
'V.01.94.12.00 2023/12/09 日次系のロジック変更、学習機能に時差演出を追加'
'V.01.94.13.00 2023/12/09 MisskeyAPI関連の仕様変更、95Updateに向けた準備（投稿予約機能、日次系投稿の大規模改修）'
'V.01.94.14.00 2023/12/10 V.01.94.11以後発生していた様々なバグの修正、安定性の向上'
'V.01.94.15.00 2023/12/11 スケジュール系のバグ修正、スケジュール系の耐障害性向上、【管理者機能】ログ機能の文修正、【試験実装】ふつおた予約機能の試験実装（動作確認）'
'V.01.94.16.00 2023/12/11 【管理者機能】JSONリセット機能の追加'
'Future：V.01.94.17 ふつおたの精査、95Updateへの更なる準備'
'Future：V.01.95.00 【予約系】ふつおたの後尾検出による予約機能（予約機能の動作検証）、内閣府の祝日CSVのDL機能と投稿一括生成機能（wget→with→dataflame→冒頭合致（年）→日次変換→index取得して何の日か→当てはめて一括生成→予約テーブル登録）、リマインダー機能（リプID保持必須）'
'Future：管理者に対して予約テーブルを見る機能、予約テーブルを削除する機能、QRコード生成、削除機能'

#print(Ver)
logger = getLogger("astrolabe_logs")
logrev = DEBUG



dt2_log_path = 0
Master_ID = 0
Master_NAME = 0
AI_ID = 0
AI_NAME = 0
USER_NAME = 0
LLMPATH = 0

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
GTL_CASH_CSV = 0
GTL_CASH_CSV_00to04 = 0
GTL_CASH_CSV_04to08 = 0
GTL_CASH_CSV_08to12 = 0
GTL_CASH_CSV_12to16 = 0
GTL_CASH_CSV_16to20 = 0
GTL_CASH_CSV_20to24 = 0
STUDY_CSV = 0
MECAB_DIR = 0
IMG_SAVE_DIR = 0
PATH = 0
log_date = 0
WS_URL = 0

def sys_exit_force():
    try:
        logger.warning('sys_exit_force')
        Schedule_utils__=Schedule_utils()
        Schedule_utils__.hourly()

        for process in executor._processes.values():
            process.kill()
        
        sys.exit()
    except Exception:
        logger.debug(traceback.format_exc())
        sys.exit()
    
def config_main(ini_header, ini_key):
    try:
        PATH = os.path.dirname(os.path.abspath(__file__)) 
        config_main_ini = configparser.ConfigParser(interpolation=None)
        config_main_ini.read(fr'{PATH}/common.ini', encoding='utf-8-sig')
        ini_header = ini_header.replace('"', '')
        ini_key = ini_key.replace('"', '')

        ini_header.replace('"', '')
        
        read_ini = config_main_ini[f'{ini_header}'][f'{ini_key}']
        return read_ini
    except Exception:
        logger.debug(traceback.format_exc())

def config_accounts(ini_header, ini_key):
    try:
        PATH = os.path.dirname(os.path.abspath(__file__)) 
        config_main_ini = configparser.ConfigParser(interpolation=None)
        config_main_ini.read(fr'{PATH}/accounts.ini', encoding='utf-8-sig')
        ini_header = ini_header.replace('"', '')
        ini_key = ini_key.replace('"', '')
        read_ini = config_main_ini[f'{ini_header}'][f'{ini_key}']
        return read_ini
    except Exception:
        logger.debug(traceback.format_exc())

class Misskey_api:
    def __init__(self):
        self.SERVER_URL = config_main("INSTANCE", "SERVER_URL")
        self.TOKEN = config_accounts("MAIN", "TOKEN")

    def create_note(self, visibility, note_text):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            note_text = note_text.replace('"', '')
            note_text = note_text.replace("'", '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
        'visibility': f'{visibility}',
        "text": f'{note_text}', 
        }
            pyload1 = json.dumps(pyload1)
            r = requests.post(url1, data=pyload1, headers=headers) 
            logger.debug(r)  
        except Exception:
            logger.debug(traceback.format_exc())
    def create_renote(self, visibility, note_text, renote_id):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '').replace("'", '')
            note_text = note_text.replace('"', '').replace("'", '')
            renote_id = renote_id.replace('"', '').replace("'", '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
        'visibility': f'{visibility}',
        "text": f'{note_text}', 
        "renoteId": f'{renote_id}',
        }
            pyload1 = json.dumps(pyload1)
            r = requests.post(url1, data=pyload1, headers=headers) 
            logger.debug(r)  
        except Exception:
            logger.debug(traceback.format_exc())
    def create_note_with_file(self, visibility, note_text, img_id):
        try:
            logger.debug(f'start_create_note_with_file')
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            note_text = note_text.replace('"', '')
            img_id = str(img_id).replace('"', '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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
            
    def create_dm(self, note_text, usr_id):
        try:
            #print('test2')
            headers = {"Content-Type": "application/json"}
            note_text = note_text.replace('"', '')
            usr_id = usr_id.replace('"', '')
            
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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

    def create_dm_cw(self, note_text, cw_text, usr_id):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            note_text = note_text.replace('"', '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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
            
    def create_reply(self, visibility, note_text, note_id):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            note_text = note_text.replace('"', '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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
            
    def create_reply_cw(self, visibility, note_text, cw_text, note_id):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            cw_text = cw_text.replace('"', '')
            note_text = note_text.replace('"', '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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

    def create_note_cw(self, visibility, note_text, cw_text):
        try:
            headers = {"Content-Type": "application/json"}
            visibility = visibility.replace('"', '')
            cw_text = cw_text.replace('"', '')
            note_text = note_text.replace('"', '')
            url1 = f"https://{self.SERVER_URL}/api/notes/create"
            pyload1 = {
        "i": f"{self.TOKEN}",
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
            
    def create_reaction(self, reaction, note_id):
        try:
            headers = {"Content-Type": "application/json"}
            reaction = reaction.replace("'", '')
            #print(reaction)
            url3 = f"https://{self.SERVER_URL}/api/notes/reactions/create"
            pyload3 = {
        "i": f"{self.TOKEN}",
        "noteId": f'{note_id}',
        "reaction": f'{reaction}',
            }
            pyload3 = json.dumps(pyload3)
            r = requests.post(url3, data=pyload3, headers=headers) 
        except Exception:
            logger.debug(traceback.format_exc())
        
    def create_follow(self, usr_id):
        try:
            headers = {"Content-Type": "application/json"}
            #print(reaction)
            url3 = f"https://{self.SERVER_URL}/api/following/create"
            pyload3 = {
        "i": f"{self.TOKEN}",
        "userId": f'{usr_id}',
            }
            pyload3 = json.dumps(pyload3)
            print('follow_ok')
            r = requests.post(url3, data=pyload3, headers=headers) 
        except Exception:
            logger.debug(traceback.format_exc())

    def delete_follow(self, usr_id):
        try:
            headers = {"Content-Type": "application/json"}
            #print(reaction)
            url3 = f"https://{self.SERVER_URL}/api/following/delete"
            pyload3 = {
        "i": f"{self.TOKEN}",
        "userId": f'{usr_id}',
            }
            pyload3 = json.dumps(pyload3)
            r = requests.post(url3, data=pyload3, headers=headers) 
        except Exception:
            logger.debug(traceback.format_exc())

    def create_file(self, img_path):
        try:
            with open(img_path, 'rb') as f:
                #f = f.read()
                #f = base64.b64encode(f)
                logger.debug(f'start_create_file\n{img_path}')
                url1 = f"https://{self.SERVER_URL}/api/drive/files/create"
                headers = {"Content-Type": "multipart/form-data"}
                #print(type(f))
                #print(f)
                params = {
                    'i' : f'{self.TOKEN}',
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

    def get_meta(self):
        pass

    def get_users_show(self):
        try:
            headers = {"Content-Type": "application/json"}
            #print(reaction)
            url3 = f"https://{self.SERVER_URL}/api/users/show"
            pyload3 = {
        "i": f"{self.TOKEN}",
        "userId": f'{AI_ID}',
            }
            pyload3 = json.dumps(pyload3)
            r = requests.post(url3, data=pyload3, headers=headers) 
            return_text = json.loads(r.content)
            return return_text
        
        except Exception:
            logger.debug(traceback.format_exc())
    def get_emoji(self):
        pass           

class Regis_note:
    def __init__(self):
        self.tabelname = 'regis_note'
        self.dbname = dbname
    def regist_write(self, trigger_time, def_name, target_id, note_text, publish_scope, file_id, type_id):
        try:
            logger.debug(f'{trigger_time}, {def_name}, {target_id}, {note_text}, {publish_scope}, {file_id}, {type_id}')
            now = datetime.datetime.now()
            regis_time = now
            id_time = str(now.strftime('%Y%m%d%H%M%S'))
            trigger_time = str(trigger_time)
            regis_time = str(regis_time)
            if trigger_time == None:
                trigger_time = 'Nan'
            elif def_name == None:
                def_name = 'Nan'
            elif target_id == None:
                target_id = 'Nan'
            elif note_text == None:
                note_text = 'Nan'
            elif publish_scope == None:
                publish_scope = 'Nan'
            elif file_id == None:
                file_id = 'Nan'
            elif type_id == None:
                type_id = 'Nan'
            with sqlite3.connect(self.dbname) as conn:
                df = pd.read_sql_query(f'SELECT * FROM {self.tabelname}', conn)
                logger.debug(df)
                #df = df.set_index('index')
                df.loc[id_time] = [regis_time, trigger_time, def_name, target_id, note_text, publish_scope, file_id, type_id]
                #logger.debug(df)
                df.to_sql(self.tabelname, conn, if_exists='replace',index=False)
                logger.debug('clear_regist_write')
        except Exception:
            logger.debug(traceback.format_exc())

    def regist_read(self):
        with sqlite3.connect(self.dbname) as conn:
            df = pd.read_sql_query(f'SELECT * FROM {self.tabelname}', conn)
            df = pd.DataFrame(df)
            #logger.debug('clear_regist_read')
            return df
    def regis_df_write(self, df):
        with sqlite3.connect(self.dbname) as conn:
            df.to_sql(self.tabelname, conn, if_exists='replace',index=False)
        logger.debug('clear_regis_df_write')



class Json_util:
    def __init__(self):
        # データベース名とテーブル名を属性として保存する
        JSON_NAME = config_main("INSTANCE", "JSON_NAME")
        self.JSON_PATH = PATH + "/" + JSON_NAME  

    def json_write(self, key, value):
        try:
            if type(key) == str:
                key = key.replace('"', '')
            if type(value) == str:
                value = value.replace('"', '')
            
            with open(self.JSON_PATH) as f:
                d_update = json.load(f)
            d_update[f'{key}'] = value
            with open(self.JSON_PATH, 'w') as f:
                json.dump(d_update, f, indent=2)
        except Exception:
            logger.debug(traceback.format_exc())
            logger.debug(f'key:{key},value:{value}')
            logger.error('json_write_error')
            sys_exit_force()
            
    def json_read(self, key):
        try:
            if type(key) == str:
                key = key.replace('"', '')
            with open(self.JSON_PATH) as f:
                d_update = json.load(f)
            return d_update[f'{key}']
        except Exception:
            logger.debug(traceback.format_exc())
            logger.debug(f'key:{key}')
            logger.error('json_read_error')
            sys_exit_force()

    def json_all_read(self):
        try:
            with open(self.JSON_PATH) as f:
                d_update = json.load(f)
            return d_update
        except Exception:
            logger.debug(traceback.format_exc())

    def json_all_write(self, json_dic):
        try:
            with open(self.JSON_PATH, 'w') as f:
                json.dump(json_dic, f, indent=2)
        except Exception:
            logger.debug(traceback.format_exc())
            logger.error('json_all_write_error')

    def json_reset(self):
        try:
            global log_date
            log_date = int(log_date)
            d_update = {
            "n_a": 0,
            "n_b": 0,
            "n_c": 0,
            "n_d_0": 0,
            "n_d_1": 0, 
            "n_d_2": 0, 
            "n_d_3": 0, 
            "n_d_4": 0, 
            "n_d_5": 0, 
            "n_d_wiki": 0, 
            "n_e": 0,
            "n_f": 0, 
            "n_g": 0,
            "n_h_1": 0,
            "n_h_2": 0,
            "n_h_3": 0,
            "n_h_4": 0,
            "n_h_5": 0,
            "n_h_6": 0,
            "n_i": 0,
            "wake_up_notification": 1,
            "n_test": 0,
            "end_alos": 0,
            "study": 0,
            "00": 0,
            "01": 0,
            "02": 0,
            "03": 0,
            "04": 0,
            "05": 0,
            "06": 0,
            "07": 0,
            "08": 0,
            "09": 0,
            "10": 0,
            "11": 0,
            "12": 0,
            "13": 0,
            "14": 0,
            "15": 0,
            "16": 0,
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0,
            "22": 0,
            "23": 0,
            "24": 0,
            "log_date": log_date
            }
            with open(self.JSON_PATH, 'w') as f:
                json.dump(d_update, f, indent=2)
        except Exception:
            logger.debug(traceback.format_exc())
            logger.debug(f'date:{log_date}')
            logger.error('json_reset_error')
            sys_exit_force()
    

def log_set(logrev):
    try:
        logger.error(f'log_set_start{logrev}')
        global log_date
        global dt2_log_path
        log_date = str(Json_util().json_read("log_date"))
        FORMAT = config_main("INSTANCE", "format")
        FORMAT = FORMAT.replace('"', '')
        
        dt2_log_path = PATH + '/log/' + log_date + '.log'

        logger.setLevel(logrev)
        fl_handler = FileHandler(filename= dt2_log_path , encoding="utf-8")
        fl_handler.setLevel(logrev)
        fl_handler.setFormatter(Formatter(FORMAT))
        logger.addHandler(fl_handler)
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('log_set_error')
        sys_exit_force()

def dt1():
    try:
        global PATH
        dt1 = datetime.datetime.now()
        PATH = os.path.dirname(os.path.abspath(__file__)).replace(os.sep,'/')
        log_set(logrev)
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
        global STUDY_CSV
        global MECAB_DIR
        global IMG_SAVE_DIR
        
                
        global SERVER_URL
        global TOKEN


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
        STUDY_CSV = config_main("INSTANCE", "STUDY_CSV")
        GTL_CASH_CSV = PATH + "/" + GTL_CASH_CSV  
        GTL_CASH_CSV_00to04 = PATH + "/" + GTL_CASH_CSV_00to04  
        GTL_CASH_CSV_04to08 = PATH + "/" + GTL_CASH_CSV_04to08  
        GTL_CASH_CSV_08to12 = PATH + "/" + GTL_CASH_CSV_08to12  
        GTL_CASH_CSV_12to16 = PATH + "/" + GTL_CASH_CSV_12to16  
        GTL_CASH_CSV_16to20 = PATH + "/" + GTL_CASH_CSV_16to20  
        GTL_CASH_CSV_20to24 = PATH + "/" + GTL_CASH_CSV_20to24  
        STUDY_CSV = PATH + "/" + STUDY_CSV  
        #print(GTL_CASH_CSV_20to24)
        GTL_CASH_CSV = PATH + "/" + GTL_CASH_CSV  
        MECAB_DIR = config_main("INSTANCE", "MECAB_DIR")
        MECAB_DIR = PATH + "/" + MECAB_DIR  
        IMG_SAVE_DIR = config_main("INSTANCE", "IMG_SAVE_DIR")
        IMG_SAVE_DIR = PATH + "/" + IMG_SAVE_DIR
        #print(type(note_list_ohayou))
        global Master_ID
        global Master_NAME

        global AI_ID
        global AI_NAME
        global USER_NAME
        global LLMPATH

        Master_ID = config_accounts("MAIN", "Master_ID")
        Master_NAME = config_accounts("MAIN", "Master_NAME")
        AI_ID = config_accounts("MAIN", "AI_ID")
        AI_NAME = config_accounts("MAIN", "AI_NAME")
        USER_NAME = config_accounts("MAIN", "USER_NAME")
        LLMPATH = config_accounts("MAIN", "LLMPATH")
        LLMPATH = PATH + "/" + LLMPATH
        global WS_URL
        SERVER_URL = config_main("INSTANCE", "SERVER_URL")
        TOKEN = config_accounts("MAIN", "TOKEN")
        WS_URL_a = 'wss://' + SERVER_URL + '/streaming?i='
        WS_URL = WS_URL_a + TOKEN
        #logger.debug(WS_URL)
        opinion_text = ('アストロラーベのシステムが起動しました\n\n' + str(dt1) + '\n' +  Ver)
        time.sleep(2)
        #create_dm(opinion_text, Master_ID)
        #print(opinion_text)
        #os.exit
        
        #args = sys.argv
        #log_date = str(args)


    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('dt1_error')
        sys_exit_force()






###########class###############

class DBReader_next:  
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
        column_data = [row[column_a] for row in results]
        # 接続を閉じる
        conn.close()
        # n列目のデータのリストを返す
        return column_data


class DBReader_name:
    try: 
        def __init__(self, dbname, tablename):
            # データベース名とテーブル名を属性として保存する
            self.dbname = dbname
            self.tablename = tablename


        def get_column(self, column_a):
            #logger.debug('DBReader_read')  
            # データベースに接続する
            conn = sqlite3.connect(self.dbname)
            # カーソルを作成する
            cursor = conn.cursor()
            # テーブルから1列目のデータを取得するSQL文を実行する
            cursor.execute(f"SELECT {column_a} FROM {self.tablename}")
            # 結果をリストとして受け取る
            results = cursor.fetchall()
            # n列目のデータだけを抽出する
            column_data = [row[0] for row in results]
            # 接続を閉じる
            conn.close()
            # n列目のデータのリストを返す
            return column_data
    except Exception:
        logger.debug(traceback.format_exc())

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
                    #sys_exit_force()
        
        except Exception:

            logger.debug(traceback.format_exc())
            logger.error('Connection_closed_global')

            #print('error')
            #sys_exit_force()         #

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
        dbreader = DBReader_name(dbname, "rssqa_1")
        column_a = 'text'
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
                Misskey_api__=Misskey_api()
                Misskey_api__.create_note("public", markov_text)  
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


################################

async def convert_jadge(input_text):
    try:
        logger.debug(f'input{input_text}')
        #input_text = str(input_text).replace(' ', "").replace("　", "")
        pattern = "[a-zA-Z]"
        match = re.search(pattern, input_text[2])
        if match:
            task = asyncio.create_task(ej_convert(input_text))
            logger.debug('match_eng')
        else :
            task = asyncio.create_task(je_convert(input_text))
            logger.debug('match_jpn')
        task = await task 
        return task
    except Exception:
        logger.debug(traceback.format_exc())
        logger.debug('convert_jadge_exception')

async def ej_convert(input_text):
    try:
        input_text = str(input_text)
        ej_translator = pipeline("translation", model="staka/fugumt-en-ja")

        output_d =ej_translator(input_text)
        #output_d = json.dumps(output_d)
        output_d = str(output_d).replace("[{'translation_text': '", "").replace("'}]", "")
        return output_d
    except Exception:
        logger.debug(traceback.format_exc())
        logger.debug('ej_convert_exception')

async def je_convert(input_text):
    try:
        input_text = str(input_text)
        #logger.debug(input_text)
        ej_translator = pipeline("translation", model="staka/fugumt-ja-en")
        
        output_d =ej_translator(input_text)
        #logger.debug(ej_translator)
        #logger.debug(output_d)
        output_d = json.dumps(output_d)
        output_d = str(output_d).replace('[{"translation_text": "', "").replace("}]", "")
        return output_d
    except Exception:
        logger.debug(traceback.format_exc())
        logger.debug('je_convert_exception')
###########schedule_exe#########
###########schedule_exe#########

async def ohayou():
        
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader_next(dbname, "ohayou")
    # 取得したい列番号を定義する
    column_a = 1
    column_b = 2
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
    Misskey_api__=Misskey_api()
    Misskey_api__.create_note("public", test_a)  
    logger.info("def_ohayou clear") 


async def oyasumi():
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader_next(dbname, "oyasumi")
    # 取得したい列番号を定義する
    column_a = 1
    column_b = 2
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
    Misskey_api__=Misskey_api()
    Misskey_api__.create_note("public", test_a)  
    logger.info("def_oyasumi_oyasumi clear")  
    timer2 = random.randint(0, 50)
    timer2 = float(timer2)

    await asyncio.sleep(timer2)
    task = asyncio.create_task(nitizi_main())
    logger.info("def_oyasumi_nitizi clear")  
    return 'test'

async def nitizi_main():
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()



        ##############設定ファイル##############
        df = pd.read_csv(csvname)# 設定ファイル行き
        Misskey_api__=Misskey_api()
        get_users = Misskey_api__.get_users_show()
        #print(text)
        name1 = int(get_users["notesCount"])
        name2 = int(get_users["followersCount"])
        name3 = int(get_users["followingCount"])

        dbreader = DBReader_next(dbname, "sample")
        # 取得したい列番号を定義する
        column_a = 3# = today
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
            Misskey_api__=Misskey_api()
            Misskey_api__.create_note("home", test_a)  
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
    except Exception:
        logger.debug(traceback.format_exc())

async def stady_note(text):
    try:
        text = str(text).replace('"', '')
        tagger = MeCab.Tagger(fr'-chasen -d {MECAB_DIR}')
        tagger = MeCab.Tagger(fr'-chasen -d {MECAB_DIR}')

        text = str(text)
        w = tagger.parse(text)
        node = tagger.parseToNode(text)

        #print(text)
        #print(node)
        node_text = 0
        node = node.next 
        #print(node.surface)
        df2 = pd.read_csv(STUDY_CSV)
        df = pd.DataFrame({'time': [],
                        'text': [],},
                        index=[])
        df = df.set_index('time')
        
        #print(df)
        while node:
            #print(node.surface)
            #print('node surface[%s] feature[%s]' %(node.surface, node.feature))
            #print(node)
            pos = node.feature.split(",")[0]
            #print(pos)
            pos2 = jaconv.kata2hira(node.feature.split(",")[7])
            #print(pos2)
            # if pos == "形容詞" or pos == "名詞" or pos == "動詞":
            
            if  pos == "名詞":
                if len(node.surface) > 1:
                    #print('###################')
                    #print(node.surface)
                    #print('###################')
                    pattern = "[a-zA-Z]"
                    match = re.search(pattern, node.surface)
                    #print('test')
                    if match:
                        pass
                    else:
                        node_text = node.surface
                        node_text = str(node_text)
                        #print(node_text)
                        #print(type(node_text))
                        #print(node_text)
                        #df2.query(f'index.str.contains("{node_text}")', engine='python')
                        #print(df2)
                        #dt2 = (df2.text.str.contains(f"{node_text}"))
                        if df2['text'].str.contains(f"{node_text}").any():
                            #print('test')
                            node = node.next
                            
                                
                        else :
                            #print('test2')
                            dt1 = datetime.datetime.now()
                            dt1 = str(dt1)
                            df.loc[f'{dt1}'] = [f'{node_text}']
                            df.to_csv(STUDY_CSV, mode='a', header=False)
                            node = node.next
                            node_text = (f'{node_text}……{pos2}……覚えました……！！')
                            await asyncio.sleep(random.randint(1, 59))
                            Misskey_api__=Misskey_api()
                            Misskey_api__.create_note("public", node_text) 
                            return
                else:
                    node = node.next
            else :
                node = node.next


    except Exception:
        logger.debug(traceback.format_exc())
        

class Rss_toukatu:#RSSを取得するURL、重複チェックを行う列名を入力する
    try:
        def __init__(self, url, tabelname):
            self.url = url
            self.tabelname = tabelname
            self.column = 'rss_url'
            self.dbname = dbname
        def rss_get(self):#RSSを取得し、重複チェックをし、新規投稿をリスト形式で返す
            #n= random.randint(1, 10)
            self.feed = feedparser.parse(self.url)
            #url = feed.entries[n].link
            #title_a = feed.entries[n].title
            self.urls = [entry['link'] for entry in self.feed['entries']]
            self.titles = [entry['title'] for entry in self.feed['entries']]
            dbreader = DBReader_name(self.dbname, self.tabelname)
            self.column_data_a = dbreader.get_column(self.column)

            rss_compare = list(set(self.column_data_a) & set(self.urls))
            self.rss_compare = list(set(self.urls) - set(rss_compare))
            #print(self.rss_compare)
            if len(self.rss_compare) == 0:
                logger.WARNING(f'RSS_non_new_post,{self.url}')
                return
            return self.rss_compare
            #print(column_data_a)   
            # リストの内容を表示する
        def rss_qa(self):
            dbreader = DBReader_name(self.dbname, "rssqa_1")
            column_a = 'text'
            self.column_data_a = dbreader.get_column(column_a)
            rss_n_len = len(self.rss_compare)
            rss_list = []
            while True:
                if rss_n_len <= 0:
                    break
                rss_n_len = rss_n_len - 1

                rss_compare_only = self.rss_compare[rss_n_len]
                for self.column_data_a in self.column_data_a:
                    if self.column_data_a in rss_compare_only:
                        rss_n_len = rss_n_len - 1
                        #print('qa_clear')
                        continue       
                rss_list.append(rss_compare_only)
            return rss_list
        def rss_publish(self, rss_compare_only):#リストにQAを実施し、更新された中で最古の投稿をリターンする。
            
            dbreader_a = DBReader_name(self.dbname, "rss_reaction_1")

            column_b = 'weights'
            column_c = 'text'

            # Reaction and waight
            column_data_a_a = dbreader_a.get_column(column_b)
            #print(column_data_a_a)
            column_data_a_b = dbreader_a.get_column(column_c)
            #print(column_data_a_b)
            test = random.choices(column_data_a_b, weights=column_data_a_a)
            self.test = str(test).replace("['", "").replace("']", "")     
            rss_n = 0
            
            #print(self.rss_compare)
            #print(rss_n_len)
                
            #print(rss_n_len)
            urls_index = self.urls.index(rss_compare_only)
            rss_title = self.titles[urls_index]
            #print(self.titles)
            urls_index = str(urls_index)
            
            rss_title = str(rss_title)
            text_a = (self.test + '\n\n' + rss_title + '\n' + rss_compare_only)
            #print(text_a)
            
            #create_note("public", text_a) 
            #logger.info("def_rss_a clear(post)") 
            return text_a#差分投稿URLのリスト
        def rss_write(self):
            with sqlite3.connect(self.dbname) as conn:
                df = pd.read_sql_query(f'SELECT * FROM {self.tabelname}', conn)
                df[f'{self.column}'] = self.urls
                #print(df)
                df.to_sql(self.tabelname, conn, if_exists='replace',index=False)
            '''
            with sqlite3.connect(self.dbname) as conn:
                df = pd.read_sql_query(f'SELECT * FROM {self.tabelname}', conn)
            '''
    except Exception:
        logger.debug(traceback.format_exc())

        
async def rss_a():
    try:
        RSS_URL_a = config_main("INSTANCE", "RSS_URL_a")
        Rss_toukatu__ = Rss_toukatu(RSS_URL_a, "rss_post_1")
        Rss_toukatu__.rss_get()
        list = Rss_toukatu__.rss_qa()
        text = (list[len(list) - 1])#最後尾の抽出　全数投稿の場合はforで取り出す。
        text = (Rss_toukatu__.rss_publish(text))
        Rss_toukatu__.rss_write()
        Misskey_api__=Misskey_api()
        Misskey_api__.create_note("public", text)  
    except Exception:
        logger.debug(traceback.format_exc())

async def rss_b():
    try:
        RSS_URL_b = config_main("INSTANCE", "RSS_URL_b")
        Rss_toukatu__ = Rss_toukatu(RSS_URL_b, "rss_post_2")
        Rss_toukatu__.rss_get()
        list = Rss_toukatu__.rss_qa()
        text = (list[len(list) - 1])#最後尾の抽出　全数投稿の場合はforで取り出す。
        text = (Rss_toukatu__.rss_publish(text))
        Rss_toukatu__.rss_write()
        Misskey_api__=Misskey_api()
        Misskey_api__.create_note("public", text)  
    except Exception:
        logger.debug(traceback.format_exc())

async def rss_c():
    try:
        RSS_URL_c = config_main("INSTANCE", "RSS_URL_c")
        Rss_toukatu__ = Rss_toukatu(RSS_URL_c, "rss_post_3")
        Rss_toukatu__.rss_get()
        list = Rss_toukatu__.rss_qa()
        text = (list[len(list) - 1])#最後尾の抽出　全数投稿の場合はforで取り出す。
        text = (Rss_toukatu__.rss_publish(text))
        Rss_toukatu__.rss_write()
        Misskey_api__=Misskey_api()
        Misskey_api__.create_note("public", text)  
    except Exception:
        logger.debug(traceback.format_exc())

async def rss_d():
    try:
        RSS_URL_d = config_main("INSTANCE", "RSS_URL_d")
        Rss_toukatu__ = Rss_toukatu(RSS_URL_d, "rss_post_4")
        Rss_toukatu__.rss_get()
        list = Rss_toukatu__.rss_qa()
        text = (list[len(list) - 1])#最後尾の抽出　全数投稿の場合はforで取り出す。
        text = (Rss_toukatu__.rss_publish(text))
        Rss_toukatu__.rss_write()
        Misskey_api__=Misskey_api()
        Misskey_api__.create_note("public", text)  
    except Exception:
        logger.debug(traceback.format_exc())

async def rss_e():
    try:
        RSS_URL_e = config_main("INSTANCE", "RSS_URL_e")
        Rss_toukatu__ = Rss_toukatu(RSS_URL_e, "rss_post_5")
        Rss_toukatu__.rss_get()
        list = Rss_toukatu__.rss_qa()
        text = (list[len(list) - 1])#最後尾の抽出　全数投稿の場合はforで取り出す。
        text = (Rss_toukatu__.rss_publish(text))
        Rss_toukatu__.rss_write()
        Misskey_api__=Misskey_api()
        Misskey_api__.create_note("public", text)  
    except Exception:
        logger.debug(traceback.format_exc())

async def rss_f():
    pass

async def sys_check_a():
    try:
        cpu_per__ = (psutil.cpu_percent(interval=1, percpu=True))
        cpu_per_a = max(cpu_per__)
        usage__ = (psutil.disk_usage(path='/').percent)
        Misskey_api__=Misskey_api()
        if usage__ >= 90.0 and cpu_per_a >= 90.0:
            usage__ = str(usage__)
            cpu_per_a = str(cpu_per_a)
            cpu_and_disk = 'CPU利用率及びディスク使用率が許容値を超過しました。ディスク使用率：' + usage__ + '％、CPU利用率：' + cpu_per_a + '％'
            Misskey_api__.create_dm(cpu_and_disk, Master_ID)
            logger.warning("def_sys_check_diskuse(Over_90)_and_cpu_max_per(Over_90)")
            return
        elif usage__ >= 90.0:
            usage__ = str(usage__)
            usage_a = 'ディスク使用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' + usage__ + '％'
            Misskey_api__.create_dm(usage_a, Master_ID)
            logger.warning("def_sys_check_diskuse(Over_90)")
            return
        elif cpu_per_a >= 90.0:
            cpu_per_a = str(cpu_per_a)
            cpu_per_a_a =  'CPU論理プロセッサの最大利用率が90％を超過したことを検知しました。\nシステムに影響を及ぼす可能性があります。\n' + '現在使用率:' +  cpu_per_a + '％'
            Misskey_api__.create_dm(cpu_per_a_a, Master_ID)
            logger.warning("def_sys_check_cpu_max_per(Over_90)")
            return
        else:
            logger.debug(cpu_per_a)  
            logger.debug(usage__)  
            sys_check_pass = 'システムチェックの結果問題はありませんでした'
            Misskey_api__.create_dm(sys_check_pass, Master_ID)
            logger.debug('syscheck_pass')  
            #print(cpu_per_a)
            #print(usage__)
    except Exception:
        logger.debug(traceback.format_exc())

async def now_play():
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader_next(dbname, "music")
    column_a = 1 # タイトル
    column_b = 2 # アーティスト
    column_c = 3 # アルバム
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
    Misskey_api__=Misskey_api()
    Misskey_api__.create_note("public", test_a)  
    logger.info("def_now_play_clear")      

async def anime_def():
    	
    # DBReaderクラスのインスタンスを作成する
    dbreader = DBReader_next(dbname, "anime")
    # 取得したい列番号を定義する
    column_a = 5 # title
    column_b = 7 # year
    column_c = 9 # maker
    column_d = 10 # episode
    column_e = 3 # url
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
    Misskey_api__=Misskey_api()
    Misskey_api__.create_note("public", test_a)  
    
async def menu_a():
    try:
        Misskey_api__=Misskey_api()
        # DBReaderクラスのインスタンスを作成する
        dbreader = DBReader_next(dbname, "menu")
        column_a = 1
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
            Misskey_api__.create_note("public", test_a)  
            return test_a
            #投稿関数
        logger.debug('post_menu_dennar')  
        
        Misskey_api__.create_note("public", test_a)  
        timer2 = int(random.randint(39600, 46800))
        timer2 = float(timer2)
        logger.debug(timer2)  
        test_a = 'お腹減ってきたなぁ\nそういえば昨日の夜食べた「' + test + '」冷蔵庫に残ってたかも。\n温め直して食べよっと！'
        logger.debug('post_menu_moning')
        await asyncio.sleep(timer2)
        Misskey_api__.create_note("public", test_a)  
        logger.info("def_menu_clear") 
    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('menu_error')


async def weather_get(url_get, id_get, pref_get):
    try:
        logger.debug('weather_get_start')  
        options = Options()
        #options.binary_location = "/usr/bin/google-chrome"
        #options.add_argument("--headless=new")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")


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
    except Exception:
        logger.error('weather_error')
        logger.debug(traceback.format_exc())
        

async def weather_get_sche():
    try:
        Misskey_api__=Misskey_api()
        dbreader = DBReader_next(dbname, "weather")
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
        Misskey_api__.create_note("public", g_note)  
    except Exception:
        logger.error('weather_get_sche_error')
        logger.debug(traceback.format_exc())

async def asy_test():
    await asyncio.sleep(5)
    print('async test')

async def wikipedia_get(sche_set):
    try:
        Misskey_api__=Misskey_api()
        sche_set = int(sche_set)
        to_get_url = 'https://ja.wikipedia.org/wiki/Special:Randompage'
        res = requests.get(to_get_url)
        wiki_url = res.url
        soup = BeautifulSoup(res.text)
        title = soup.find("title")
        wiki_title = title.text
        wiki_title = wiki_title.replace(' - Wikipedia', '')
        get_text = (soup.find('p'))
        get_text = str(get_text)
        get_text = (BeautifulSoup(get_text, "lxml").text)        
        if sche_set == 0:
            column_data_a = ['Wikipediaってこんな記事もあるんですね！！','知見が深まりますなぁ','面白くてついつい読み込んでしまいました。。','時間が無限に欲しくなります、、', 'とっても面白い記事でした！']
            column_data_a = str(random.choices(column_data_a)).replace("['", "").replace("']", "")
            g_note = f'{column_data_a}\n\nタイトル：{wiki_title}\nURL：{wiki_url}\n>{get_text}'
            Misskey_api__.create_note("public", g_note)  
        elif sche_set == 1:
            g_note = f'ご利用ありがとうございます。ランダムなWikipediaの記事です。\n\nタイトル：{wiki_title}\nURL：{wiki_url}>{get_text}'
            return g_note

    except Exception:
        logger.error('wikipedia_error')
        logger.debug(traceback.format_exc())



async def alos_nitizi():
    try:
        logger.info('alos_nitizi_start')
        Json_util__=Json_util()
        Json_util__.json_reset()
        #await asyncio.sleep(30)
        task = asyncio.create_task(wordcloud_main(999))
        logger.info('alos_nitizi_clear')

    except Exception:
        logger.error('alos_nitizi')
        logger.debug(traceback.format_exc())



###########schedule_ctrl##############
class Schedule_utils:
    def __init__(self):
        self.json_dic = Json_util().json_all_read()
    def random_set_def(self):
        random_set = []
        random_set.append(random.randint(7, 9))#RSS_a
        random_set.append(random.randint(9, 12))#RSS_b
        random_set.append(random.randint(12, 16))#RSS_c
        random_set.append(random.randint(16, 18))#RSS_d
        random_set.append(random.randint(18, 21))#RSS_e
        random_set.append(random.randint(21, 23))#RSS_f
        random_set.append(random.randint(7, 7))#ohayou
        random_set.append(random.randint(22, 23))#oyasumi
        random_set.append(random.randint(10, 15))#anime
        random_set.append(random.randint(17, 20))#nowplay
        random_set.append(random.randint(19, 21))#menu
        random_set.append(random.randint(7, 8))#weather_t
        random_set.append(random.randint(10, 15))#wiki
        self.random_set = random_set

    async def hourly(self):
        Misskey_api__=Misskey_api()
        Json_util().json_all_write(self.json_dic)  
        Regis_note=Regis_note()
        Regis_note.regist_write(self.df)
    def minutely(self):
        try:
            Misskey_api__=Misskey_api()
            now = datetime.datetime.now()
            Regis_note__=Regis_note()
            df = Regis_note__.regist_read()
            #logger.debug(df)
            if df.empty:
                return
            df = df.set_index('regis_time')
            df = df.rename_axis('regis_time')
            #(trigger_time, def_name, target_id, note_text, publish_scope, file_id, type_id)
            '''
            type_id
            1 = ふつおた（CW）:def_nameがCWテキスト。
            2 = 通常投稿（年次系）
            3 = リマインダー（RN）
            4 = 
            '''
            judge_n = 0

            trigger_time = (df.loc[:, 'trigger_time'].tolist())

            type_id = (df.loc[:, 'type_id'].tolist())
            index_1 = df.index.values.tolist()
            index_2 = (df.loc[:, 'publish_scope'].tolist())
            index_3 = (df.loc[:, 'def_name'].tolist())
            index_4 = (df.loc[:, 'note_text'].tolist())
            #index_5 = (df.loc[:, 'regis_time'].tolist())
            del_index = []
            for test in trigger_time:
                time = datetime.datetime.strptime(test, "%Y-%m-%d %H:%M:%S.%f")
                if time <= now:

                    trigger_time_index = trigger_time.index(test)
                    type_id1 = int(type_id[int(trigger_time_index)]) 
                    index_1 = index_1[int(trigger_time_index)]                                            
                    index_2 = index_2[int(trigger_time_index)]
                    index_3 = index_3[int(trigger_time_index)]
                    index_4 = index_4[int(trigger_time_index)]
                    #index_5 = index_5[int(trigger_time_index)]
                    logger.debug(f'clock_in:index_number:{trigger_time_index},typeid:{type_id1},scope:{index_2},cw_text:{index_3},note_text:{index_4},index:{index_1}')

                    if type_id1 == 1:
                        #print(f'Clear_A::{index_2}::')
                        #Misskey_api__.create_note(index_2,data[5])
                        Misskey_api__.create_note_cw(index_2, index_4, index_3)
                        logger.debug(f'clear_note')
                        judge_n = judge_n + 1
                    elif type_id1 == 2:
                        #print(f'Clear_B::{index_2}::')
                        Misskey_api__.create_note(index_2, index_4)
                        judge_n = judge_n + 1
                    elif type_id1 == 3:
                        pass
                        judge_n = judge_n + 1
                        #Misskey_api__.create_renote(data[6], data[5], data[4])
                    del_index.append(index_1)
                        
            #print(del_index)           
            logger.debug(f'del_index:{del_index},judge_n:{judge_n}')
            for del_index1 in del_index:
                #print(f'del_index1::{del_index1}::')
                if judge_n >= 1:
                    df = df.drop(labels=del_index1, axis=0)
                else :
                    break
            logger.debug(df)
            Regis_note__.regis_df_write(df)

        except Exception:
            logger.debug(traceback.format_exc())
    async def schedule_next(self):
        try:
            Misskey_api__=Misskey_api()
            self.random_set_def()
            if logrev == 10:
                logrev_t = 'DEBUG'
            elif logrev == 20:
                logrev_t = 'INFO'
            elif logrev == 30:
                logrev_t = 'WARNING'
            elif logrev == 40:
                logrev_t = 'ERROR'
            elif logrev == 50:
                logrev_t = 'CRITICAL'

            if Json_util().json_read("wake_up_notification") == 0:
                dt = datetime.datetime.now()
                opinion_text = f'アストロラーベが起動されました.。\n（この通知はスケジュール系の起動と同期しています。\n\nVer:{Ver}\n時間:{dt}\nログレベル：{logrev_t}'
                Misskey_api__.create_dm(opinion_text, Master_ID)
                Json_util().json_write("wake_up_notification", 1)
                logger.debug('alos_first_start')
            else:
                start_count = int(Json_util().json_read("wake_up_notification"))
                start_count = start_count + 1
                Json_util().json_write("wake_up_notification", start_count)
                logger.info(f'alos_reboot:{start_count}')
            random_numbers = []
            for _ in range(20):#分乱数生成
                random_numbers.append(random.randint(1, 59))

            minutely = 0
            roop_break = 0
            while True:
                try:
                    while True:
                        try:
                            now = datetime.datetime.now()
                            minutely = minutely + 1
                            #print(now)
                            if minutely > 60:
                                minutely = 0
                                self.minutely()
                            elif now.minute == 00 and self.json_dic[f'{str(now.hour).zfill(2)}'] == 0 :
                                logger.debug(f'wakeup_hourly_{str(now.hour).zfill(2)}:00')
                                Schedule_utils().hourly()
                                self.json_dic[f'{str(now.hour).zfill(2)}'] = 1
                                if now.hour == 4 :
                                    task = asyncio.create_task(wordcloud_main(0))
                                elif now.hour == 8 :
                                    task = asyncio.create_task(wordcloud_main(1))
                                elif now.hour == 12 :
                                    task = asyncio.create_task(wordcloud_main(2))
                                elif now.hour == 16 :
                                    task = asyncio.create_task(wordcloud_main(3))
                                elif now.hour == 20 :
                                    task = asyncio.create_task(wordcloud_main(4))
                                elif now.hour == 00:
                                    task = asyncio.create_task(wordcloud_main(5))
                            #RSS_system
                            elif now.hour == self.random_set[0] and now.minute == random_numbers[1] and self.json_dic[f'n_d_0'] == 0 :
                                logger.debug('wakeup_rss_a')
                                task = asyncio.create_task(rss_a())
                                self.json_dic[f'n_d_0'] = 1
                            elif now.hour == self.random_set[1] and now.minute == random_numbers[2] and self.json_dic[f'n_d_1'] == 0 :
                                logger.debug('wakeup_rss_a')
                                task = asyncio.create_task(rss_b())
                                self.json_dic[f'n_d_1'] = 1
                            elif now.hour == self.random_set[2] and now.minute == random_numbers[3] and self.json_dic[f'n_d_2'] == 0 :
                                logger.debug('wakeup_rss_a')
                                task = asyncio.create_task(rss_c())
                                self.json_dic[f'n_d_2'] = 1
                            elif now.hour == self.random_set[3] and now.minute == random_numbers[4] and self.json_dic[f'n_d_3'] == 0 :
                                logger.debug('wakeup_rss_a')
                                task = asyncio.create_task(rss_d())
                                self.json_dic[f'n_d_3'] = 1
                            elif now.hour == self.random_set[4] and now.minute == random_numbers[5] and self.json_dic[f'n_d_4'] == 0 :
                                logger.debug('wakeup_rss_a')
                                task = asyncio.create_task(rss_e())
                                self.json_dic[f'n_d_4'] = 1
                            elif now.hour == self.random_set[5] and now.minute == random_numbers[6] and self.json_dic[f'n_d_5'] == 0 :
                                logger.debug('wakeup_rss_f')
                                task = asyncio.create_task(rss_f())
                                self.json_dic[f'n_d_5'] = 1
                            #Communicate_system

                            elif now.hour == self.random_set[6] and now.minute == random_numbers[7]  and self.json_dic[f'n_a'] == 0:                  
                                logger.debug('wakeup_ohayou')
                                task = asyncio.create_task(ohayou())
                                self.json_dic[f'n_a'] = 1
                            elif now.hour == self.random_set[7] and now.minute == random_numbers[8]  and self.json_dic[f'n_b'] == 0:
                                logger.debug('wakeup_oyasumi')
                                task = asyncio.create_task(oyasumi())
                                self.json_dic[f'n_b'] = 1
                            elif now.hour == 5 and self.json_dic[f'n_c'] == 0:
                                logger.debug('wakeup_sys_check')
                                task = asyncio.create_task(sys_check_a())
                                self.json_dic[f'n_c'] = 1
                            elif now.hour == self.random_set[8] and now.minute == random_numbers[9]  and self.json_dic[f'n_f'] == 0:
                                logger.debug('wakeup_anime_def')
                                task = asyncio.create_task(anime_def())
                                self.json_dic[f'n_f'] = 1
                            elif now.hour == self.random_set[9] and now.minute == random_numbers[10]  and self.json_dic[f'n_e'] == 0:
                                logger.debug('wakeup_now_play')
                                task = asyncio.create_task(now_play())
                                self.json_dic[f'n_e'] = 1
                            elif now.hour == self.random_set[10] and now.minute == random_numbers[11] and self.json_dic[f'n_g'] == 0:
                                logger.debug('wakeup_menu_a')
                                task = asyncio.create_task(menu_a())
                                self.json_dic[f'n_g'] = 1
                            elif now.hour == self.random_set[11] and now.minute == random_numbers[12] and self.json_dic[f'n_i'] == 0:
                                logger.debug('wakeup_weather_get')
                                task = asyncio.create_task(weather_get_sche())
                                self.json_dic[f'n_i'] = 1
                            elif now.hour == self.random_set[11] and now.minute == random_numbers[13] and self.json_dic[f'n_d_wiki'] == 0:
                                logger.debug('wakeup_wikipedia_get')
                                task = asyncio.create_task(wikipedia_get(0))
                                self.json_dic[f'n_d_wiki'] = 1
                            #MARKOV_system
                            elif now.hour == 10 and now.minute == random_numbers[14] and self.json_dic[f'n_h_1'] == 0 :
                                logger.debug('wakeup_markov')
                                task = asyncio.create_task(post_tl())
                                self.json_dic[f'n_h_1'] = 1
                            elif now.hour == 13 and now.minute == random_numbers[15] and self.json_dic[f'n_h_2'] == 0 :
                                logger.debug('wakeup_markov')
                                task = asyncio.create_task(post_tl())
                                self.json_dic[f'n_h_2'] = 1
                            elif now.hour == 16 and now.minute == random_numbers[16] and self.json_dic[f'n_h_3'] == 0 :
                                logger.debug('wakeup_markov')
                                task = asyncio.create_task(post_tl())
                                self.json_dic[f'n_h_3'] = 1
                            elif now.hour == 19 and now.minute == random_numbers[17] and self.json_dic[f'n_h_4'] == 0 :
                                logger.debug('wakeup_markov')
                                task = asyncio.create_task(post_tl())
                                self.json_dic[f'n_h_4'] = 1
                            elif now.hour == 21 and now.minute == random_numbers[18] and self.json_dic[f'n_h_5'] == 0 :
                                logger.debug('wakeup_markov')
                                task = asyncio.create_task(post_tl())
                                self.json_dic[f'n_h_5'] = 1
                            #Daily_system
                            elif now.hour == 5 and now.minute == 30:
                                self.daily()
                            
                            '''
                            if now.minute == 00 :#日次（時間）毎
                                pass
                            elif now.hour == 12 and now.minute == 31:#日次毎
                                pass
                            elif now.month == 12 and now.day == 31:#特定日毎
                                pass
                            '''
                            await asyncio.sleep(1)
                        except Exception:
                            logger.debug(traceback.format_exc())
                            await asyncio.sleep(10)
                            break 
                except Exception:
                    logger.debug(traceback.format_exc())
                    roop_break = roop_break + 1
                    if roop_break >= 100:
                        logger.error(f'Shedule_error.roop_count:{roop_break}')
                        break
                    await asyncio.sleep(10)

        except Exception:
            logger.debug(traceback.format_exc())

        
    async def monsely():
        try:
            now = datetime.datetime.now()
            'https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv'
        except Exception:
            logger.error('alos_nitizi')
            logger.debug(traceback.format_exc()) 

    async def daily(self):
        try:
            now = datetime.datetime.now()
            if now.day == 1:
                self.monsely()
        except Exception:
            logger.error('alos_nitizi')
            logger.debug(traceback.format_exc()) 

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
        logger.debug('write_csv_gtl_clear')
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
                    if len(node.surface) > 1:
                        pattern = "[a-zA-Z]"
                        match = re.search(pattern, node.surface)
                        if match:
                            pass
                        else:
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

async def process_pool(dataframes):
    try:
        cpu_count = psutil.cpu_count()
        if cpu_count > 1:
            logger.debug(f'get_cpu_core{cpu_count}')
        else:
            logger.error('not_get_cpu_core_count')
            cpu_count = 4
        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            return list(executor.map(wordcloud, dataframes))
    except Exception:
        logger.debug(traceback.format_exc())
    

async def wordcloud_main(toukatsu):
    try:
        time__def_text = ""
        time_sta2 = time.perf_counter()
        tagger = MeCab.Tagger(fr'-chasen -d {MECAB_DIR}')
        logger.debug(f'start_wordcloud_main')
        df = 0
        dt1 = datetime.datetime.now()
        record_time = int(dt1.strftime('%Y'))
        if toukatsu == 999:
            time__def_text = '昨日の0時から23時59分まで24時間'
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
            time__def_text = '0時から3時59分までの4時間'
            df = pd.read_csv(GTL_CASH_CSV_00to04)
        elif toukatsu == 1:
            time__def_text = '4時から7時59分までの4時間'
            df = pd.read_csv(GTL_CASH_CSV_04to08)
        elif toukatsu == 2:
            time__def_text = '8時から11時59分までの4時間'
            df = pd.read_csv(GTL_CASH_CSV_08to12)
        elif toukatsu == 3:
            time__def_text = '12時から15時59分までの4時間'
            df = pd.read_csv(GTL_CASH_CSV_12to16)
        elif toukatsu == 4:
            time__def_text = '16時から19時59分までの4時間'
            df = pd.read_csv(GTL_CASH_CSV_16to20)
        elif toukatsu == 5:
            time__def_text = '20時から23時59分までの4時間'
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
        #print(sec)
        
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
        logger.debug(f'nst_time:{dte1}\ned_time:{dte2}\ncalc_time:{totalling_time}\ncalc_time_sec{sec}\ntotalling_time.days{totalling_time.days}\ntotalling_time_hours{totalling_time_hours}')
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
            #asyncio.get_event_loop().run_until_complete()
            #results = asyncio.run(process_pool(dataframes))
            cpu_count = psutil.cpu_count()
        
            if cpu_count > 1:
                logger.debug(f'get_cpu_core{cpu_count}')
            else:
                logger.error('not_get_cpu_core_count')
                cpu_count = 4
            with ProcessPoolExecutor(max_workers=cpu_count) as executor:
                #Execute the `wordcloud` function on each DataFrame chunk
                #results = list(executor.map(wordcloud, dataframes))
                futures = [executor.submit(wordcloud, dataframe) for dataframe in dataframes]
                results = [future.result() for future in futures]
            #del df
            
            combined_df = pd.concat(results)
            

            # Concatenate the resulting DataFrames
        
            #combined_df.to_csv(mecab_csv_name)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
            #combined_df = pd.read_csv(mecab_csv_name)
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            #print(combined_df)
    

            npt = nlplot.NLPlot(combined_df, target_col='text')
            stopword_top = int(random.randint(0, 10))
            stopwords = npt.get_stopword(top_n=stopword_top, min_freq=0) + ['こと', 'これ', 'それ', 'ない', 'さん', 'もん', 'やつ', 'なん', 'ちゃん', 'くん', '中', 'みたい', '何', 'ん', 'の', 'さ', 'ー', 'そう', '人', '色', 'the', 'of', 'to', 'and', 'in', 'blob', 'meltblob', 'cat', 'with', 'ちんこ', 'まんこ', 'ちんぽ', 'ごみ', 'カス', '死ね', '自殺', 'エッチ', 'エロ', 'グロ', '人身事故', '死', '系', 'nan', '型', '的', 'レイプ', 'a']
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
            logger.debug(f'make_wc_pic_clear_img_file_name:{img_file_name}')
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
            n_calc_text = str(f'全{n}件')
        else :
            n_calc_text = str(f'約{n_calc}万件')
        if toukatsu == 999:
            wc_text = ''
        else :
            wc_text = '、その特徴語が画像のワードクラウドです。'
            
        toukatsu_text = f'''私が{time__def_text}に観測したGTLのデータです。{n_calc_text}の投稿があり{wc_text}
参加インスタンスは{inst_list_count}サーバ、参加ユーザー数は{usr_list_count}人でした。
なお、投稿数第{inst_choice_random}位のサーバは{insetance_choice_name}で{insetance_choice_count}件、投稿数第{usr_choice_random}位のユーザーは{usr_choice_name}さんで{usr_choice_count}件でした。
        '''    
        Misskey_api__=Misskey_api()
        
        if toukatsu == 999:
            Misskey_api__.create_note("public", toukatsu_text)
        else :
            file_id = Misskey_api__.create_file(img_file_name)
            Misskey_api__.create_note_with_file("public", toukatsu_text, file_id)  
            
        df = df.head(0)
        
        if toukatsu == 999:
            #df.to_csv(GTL_CASH_CSV, mode='a', header=False)
            #print(GTL_CASH_CSV_00to04)
            GTL_CASH_CSV_temp = pd.DataFrame(columns=['time','instance','id','text'])
            GTL_CASH_CSV_temp = GTL_CASH_CSV_temp.set_index('time')
            
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_00to04, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_04to08, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_08to12, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_12to16, mode='w')
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_16to20, mode='w')   
            GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_20to24, mode='w')
            logger.debug('del_GTL_CASH_CSV_ALL')
        elif toukatsu == 5:
            task = asyncio.create_task(alos_nitizi())
        #await asyncio.sleep(20)
        #logger.error('word_cloud_main_fin')
        #sys_exit_force()

    except Exception:
        logger.debug(traceback.format_exc())
        logger.error('word_cloud_main_error')

async def cloud_global_runner():#グローバル受信系
    logger.debug(WS_URL)
    #task1 = asyncio.create_task(schedule_a())
    #await task1
    roop_watch = 0
    df = pd.DataFrame({'instance': [],
    'usr_id': [],
    'note': []},
    index=[])
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                g_n = 0
                buf_gr = ''
                buf_gr_1 = ''
                node_cash = str("")
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
                                    roop_watch = 0
                                    if break_parm >= 50:
                                        break_parm = 0
                                        task = asyncio.create_task(write_csv_gtl(df))
                                        df = pd.DataFrame({'instance': [],
                                            'usr_id': [],
                                            'note': []},
                                            index=[])
                                        
                                        #print('fin')

                                        '''
                                        #cloud_gtl_write(node_cash)
                                        table = 'gtl'
                                        task = asyncio.create_task(get_column(dbname, table__, time, instance, usr_id, node_cash))
                                        break_parm = 0
                                        print('fin2')'''
                    except Exception:
                        logger.debug(traceback.format_exc())
                        logger.error(f'Connection_closed_1_global\nroop_watch:{roop_watch}')
                        if roop_watch < 10 :
                            await asyncio.sleep(6)
                            break
                        elif roop_watch < 60 :
                            await asyncio.sleep(60)
                            break
                        else :
                            sys_exit_force()
        except Exception:    
                logger.debug(traceback.format_exc())
                logger.debug()
                logger.error(f'Connection_closed_2_global\nroop_watch:{roop_watch}')
                if roop_watch < 10 :
                    await asyncio.sleep(6)
                elif roop_watch < 60 :
                    await asyncio.sleep(60)
                else :
                    sys_exit_force()


###########home_get##############


async def runner():
     #task1 = asyncio.create_task(schedule_a())
     #await task1
     roop_watch = 0
     logger.debug('start_runner')
     while True: 
        async with websockets.connect(WS_URL) as ws:
            roop_watch = roop_watch + 1
            try:
                await ws.send(json.dumps({
                    "type": "connect",
                    "body": {
                            "channel": "homeTimeline",
                            "id": "test"
                            }
                    }))
                #data = json.loads(await ws.recv())
                #logger.debug(data)    
                while True:
                    try:
                        
                        data = json.loads(await ws.recv())
                        logger.debug('ws_home_catch')    
                        if data['type'] == 'channel':
                            if data['body']['type'] == 'note': 
                                note = data['body']['body']
                                user = data['body']['body']['user']
                                roop_watch = 0
                                task = asyncio.create_task(on_note(note, user))
                    except Exception:
                            logger.debug(traceback.format_exc())
                            logger.error(f'ws_home_1_error\nroop_watch:{roop_watch}')
                            if roop_watch < 10 :
                                await asyncio.sleep(6)
                                break
                            elif roop_watch < 60 :
                                await asyncio.sleep(60)
                                break
                            else :
                                sys_exit_force()

            except Exception:
                logger.debug(traceback.format_exc())
                logger.error(f'ws_home_2_error\nroop_watch:{roop_watch}')
                if roop_watch < 10 :
                    await asyncio.sleep(6)
                    #break
                elif roop_watch < 60 :
                    await asyncio.sleep(60)
                    #break
                else :
                    sys_exit_force()
        
###########main_get##############

async def runner_main():
     Misskey_api__=Misskey_api()
     #task1 = asyncio.create_task(schedule_a())
     #await task1
     roop_watch = 0
     while True:
        async with websockets.connect(WS_URL) as ws:
          
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
                                roop_watch = 0
                                Misskey_api__.create_follow(user)
                                #task = asyncio.create_task(on_follow(user))


                    except Exception:
                        logger.debug(traceback.format_exc())
                        logger.error(f'ws_main_error\nroop_watch:{roop_watch}')
                        if roop_watch < 10:
                    
                            await asyncio.sleep(6)
                            break
                        elif roop_watch < 60:
                            await asyncio.sleep(60)
                            break
                        else:
                            sys_exit_force()
            except Exception:
                  
                logger.debug(traceback.format_exc())
                logger.error(f'ws_main_error\nroop_watch:{roop_watch}')
                if roop_watch < 10:
                    
                    await asyncio.sleep(6)
                    #break
                elif roop_watch < 60:
                    await asyncio.sleep(60)
                    #break
                else:
                    sys_exit_force()



###########home_exe(mention,reaction,call)##############

async def on_note(note,user):
        try:
            Misskey_api__=Misskey_api()
            logger.debug('async_def_onnote')

            if note.get('mentions'):
                logger.debug('scan_mention')  
                if AI_ID in note['mentions']:
                    logger.debug('scan_mention_myid')  
                    USER_NAME = 'test_name'
                    e.reply = note['text'].replace('@astrolabe ', '').replace('@astrolabe　', '').replace('　', ' ')
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
・「ふつおた 任意のペンネーム(省略可) 本文 日時(省略可)」で代理投稿をします
日時はYYYY/MM/DD、YYYY/MM/DD HH:mm、DD日後、HH時間後、mm分後、のそれぞれに対応します。
・「Wiki」「ウィキ」でランダムなWikipediaの記事を投稿します    
・「翻訳」で和英翻訳を実施します。                            
・これらに該当しないリプライは全てLLMによって処理され、必ず何らかの内容を返信します。
      
管理者は「管理者機能」を使って下さい                          
        ......
                                    ''')
                        cw_text = 'わたくしアストロラーベの機能をご紹介します！'
                        Misskey_api__.create_reply_cw(note['visibility'], info_text, cw_text, note['id'])
                        logger.debug('help_post')  
                    elif e.reply.startswith(('Version', 'バージョン', '世代', '死活')):
                        dt1 = datetime.datetime.now()
                        dt1 =(str(dt1.strftime('%Y年%m月%d日%H時%M分%S秒')))
                        opinion_text = ('アストロラーベは稼働中です\n' + dt1 + '\n' +  Ver)
                        logger.debug('version_post')  
                        Misskey_api__.create_reply(note['visibility'], opinion_text, note['id'])
                    elif e.reply.startswith(('Wiki', 'ウィキ', 'wiki')):
                        task = asyncio.create_task(wikipedia_get(1))
                        g_note = await task
                        Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                    elif e.reply.startswith('翻訳'):
                        input1 = e.reply.replace('翻訳', '',1)
                        task = asyncio.create_task(convert_jadge(input1))
                        opinion_text_1 = await task
                        opinion_text = (f'翻訳しました！\n「{opinion_text_1}」')
                        logger.debug(f'convet_post:{opinion_text_1}')  
                        Misskey_api__.create_reply(note['visibility'], opinion_text, note['id'])
                    elif e.reply.startswith(('meal', 'ご飯ガチャ', 'ごはん', 'ご飯', '献立')):
                        dbreader = DBReader_next(dbname, "menu")
                        column_a = 0
                        column_data_a = dbreader.get_column(column_a) 
                        test = str(random.choices(column_data_a)).replace("['", "").replace("']", "")
                        test = '厳正なるご飯ガチャの結果は\n「' + test + '」でした！\nまたのご依頼、お待ちしています。\n（私は現在517の献立をご紹介できます！）'
                        Misskey_api__.create_reply(note['visibility'], test, note['id'])
                    elif e.reply.startswith(('ふつおた', 'おたより', 'お便り', '掲示板')):
                        text = e.reply.replace('ふつおた', '',1).replace('おたより', '',1).replace('お便り', '',1).replace('掲示板', '',1).replace(' ', '',1)
                        # Detect and remove date
                        now = datetime.datetime.now()
                        #print(now)
                        ############予約投稿系#################
                        date_string = None
                        date_pattern = r"\d{4}/\d{2}/\d{2}$"
                        if re.search(date_pattern, text):
                            match = re.search(date_pattern, text)
                            text = re.sub(date_pattern, "", text)
                            
                            if match:
                                date_string = match.group(0)
                            else:
                                date_string = None
                            date_string = date_string.replace('/', '-')
                            date_string = f'{date_string} 00:00:00.000000'
                            date_string =  datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
                        date_pattern = r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}$"
                        if re.search(date_pattern, text):
                            match = re.search(date_pattern, text)
                            text = re.sub(date_pattern, "", text)
                            if match:
                                date_string = match.group(0)
                            else:
                                date_string = None
                            date_string = date_string.replace('/', '-')
                            date_string = f'{date_string}:00.000000'
                            date_string =  datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
                        # Separate pen name and body text
                        date_pattern = r"\d+時間後$"
                        date_pattern2 = r"\d+分後$"
                        date_pattern3 = r"\d+日後$"
                        if re.search(date_pattern, text):
                            match = re.search(date_pattern, text)
                            text = re.sub(date_pattern, "", text)
                            if match:
                                date_string = match.group(0)
                            else:
                                date_string = None
                            time_int = int(re.sub('時間後', "", date_string))
                            print(time_int)
                            print(type(time_int))
                            date_string = now + datetime.timedelta(hours=time_int)
                        elif re.search(date_pattern2, text):
                            match = re.search(date_pattern2, text)
                            text = re.sub(date_pattern2, "", text)
                            if match:
                                date_string = match.group(0)
                            else:
                                date_string = None
                            time_int = int(re.sub('分後', "", date_string))
                            print(time_int)
                            print(type(time_int))
                            date_string = now + datetime.timedelta(minutes=time_int)
                        elif re.search(date_pattern3, text):
                            match = re.search(date_pattern3, text)
                            text = re.sub(date_pattern3, "", text)
                            if match:
                                date_string = match.group(0)
                            else:
                                date_string = None
                            time_int = int(re.sub('日後', "", date_string))
                            print(time_int)
                            print(type(time_int))
                            date_string = now + datetime.timedelta(days=time_int)
                        
                        pen_name_pattern = r"^[^\s]+ "
                        match = re.match(pen_name_pattern, text)
                        if match:
                            body_text = match.group(0)
                            pen_name = text[len(body_text) + 0:]
                        else:
                            body_text = '匿名希望'
                            pen_name = text
                        if date_string == None:
                            input3 = (f'{body_text}さんからのおたよりです')
                            Misskey_api__.create_note_cw("public", input3, pen_name)
                        else :
                            only_time = (f'{body_text}さんからのおたよりです')
                            only_time = only_time.replace(' ', '')
                            trigger_time = date_string
                            def_name = only_time
                            target_id = "Nan"
                            publish_scope = "public"
                            file_id = "Nan"
                            type_id = "1"
                            note_text = pen_name
                            Regis_note__=Regis_note()
                            Regis_note__.regist_write(trigger_time, def_name, target_id, note_text, publish_scope, file_id, type_id)
                        logger.debug(f"ペンネーム: {body_text},本文: {pen_name},日時: {date_string}")
                        '''
                        input2 = re.search(r' (.+) ', input1)
                        input3 = re.search(r' (.+) ', input2)
                        input3 = input1.replace(f'{input2}', '',1)
                        visibility = 'public'
                        #print(input1)
                        #print(input2)
                        #print(input3)
                        if input2 == None:
                            
                            input2 = '匿名希望さんからのおたよりです！'
                            Misskey_api__.create_note_cw("public", input3, input2)
                        
                        else:
                            input2 = input2.group(1)
                            input3 = input1.replace(f'{input2}', '',1)
                            input2 = f'{input2}さんからのおたよりです！'
                            Misskey_api__.create_note_cw("public", input3, input2)
                            '''
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
                        dbreader = DBReader_next(dbname, "weather")
                        # 取得したい列番号を定義する
                        column_a = 2
                        column_b = 5
                        column_c = 13
                        column_d = 1
                        column_e = 6
                        column_f = 7
                        column_g = 8
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
                                Misskey_api__.create_reply(note['visibility'], weather_mk, note['id'])
                                #print(weather_mk)
                            else :
                                #print(url_get)
                                logger.debug('weather_get')  
                                task = asyncio.create_task(weather_get(url_get, id_get, pref_get))
                                g_note = await task
                                Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                                logger.debug('weather_post')  
                        else :
                            g_note = '申し訳ありません。都道府県を認識出来ませんでした。\nこの機能はコマンドの為、「weather 都道府県」「天気 都道府県」の文法を厳守してください。（他に何も書かないでください）\n繰り返し失敗する場合はマスターにご連絡をお願いします。ID:' + Master_NAME
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            logger.debug('none_get_pref')  
                    elif user['id'] == Master_ID:#管理者用リプライ制御機能
                        logger.debug('scan_masterID') 
                        if e.reply.startswith(('停止', 'stop', '終了')):
                            g_note='システムを終了します'
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            Json_util().json_write("end_alos", 1)
                            sys_exit_force()
                        elif e.reply.startswith(('管理者機能')):
                            g_note='''管理者用機能の一覧
ログクリア：ログをクリアします
ログ：ログの末尾2900字を返信します
ログレベル：DEBUG、INFO、WARNING、DEF(起動時の指定レベル)
停止：不可逆的な停止措置を行います
再起動：再起動します
代理：代理投稿をします
テスト：以後に指定された文を実行します
JSONリセット：JSONをリセットします。
予約テーブル参照：【実装中】予約投稿のテーブルを一覧表示します
MP1：【検討中】モジュールプリセット。サーバ維持機能などを内包したバッチファイルの起動。
                            '''
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                        elif e.reply.startswith(('ログクリア')):
                            g_note=f'現在書き込み中のログ「{dt2_log_path}」をクリアします'
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            with open(dt2_log_path , mode='w', encoding='utf-8') as f:
                                f.write('')
                            logger.info('log_clear')

                        elif e.reply.startswith(('ログレベル')):
                            
                            g_note = e.reply.replace('ログレベル ', '',1)
                            g_note2 = f'ログのレベルを{g_note}にセットします'
                            #create_reply(note['visibility'], g_note2, note['id'])
                            if g_note == 'DEBUG':
                                log_set(10)
                                Misskey_api__.create_reply(note['visibility'], g_note2, note['id'])
                                return
                            elif g_note == 'INFO':
                                log_set(20)
                                Misskey_api__.create_reply(note['visibility'], g_note2, note['id'])
                                return
                            elif g_note == 'WARNING':
                                log_set(30)
                                Misskey_api__.create_reply(note['visibility'], g_note2, note['id'])
                                return
                            elif g_note == "DEF":
                                log_set(logrev)
                                Misskey_api__.create_reply(note['visibility'], g_note2, note['id'])
                                return
                            else :
                                g_note = f'ログレベルを認識出来ませんでした。受け取ったレベル：{g_note}'
                                Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                                return
                            
                        elif e.reply.startswith(('ログ')):

                            with open(dt2_log_path , mode='r', encoding='utf-8') as f:
                                text_base = f.read()
                                g_note_0 = str(text_base[-2900:]).replace('@', '')
                                g_note_len = len(text_base) 
                                g_note = (f'ログファイル{dt2_log_path}です。字数は{g_note_len}。\n{g_note_0}')
                                Misskey_api__.create_reply(note['visibility'], g_note, note['id'])                       
                        elif e.reply.startswith(('再起動', 'restart', 'アプデ')):
                            g_note='システムを再起動します'
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            Json_util().json_write("wake_up_notification", 0)
                            sys_exit_force()
                        elif e.reply.startswith(('テスト', 'test', '試験')):
                            e.reply = e.reply.replace('テスト', '',1).replace('test', '',1).replace('試験', '',1)
                            g_note =f"テストとして指定された関数・機能を実行します。実行内容：{e.reply}"
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            eval(f'{e.reply}')
                        elif e.reply.startswith(('JSONリセット')):
                            Json_util__=Json_util()
                            JSON_text1 = Json_util__.json_all_read()
                            Json_util__.json_reset()
                            JSON_text2 = Json_util__.json_all_read()
                            g_note=f'JSONをリセットしました。書き換え前の内容:{JSON_text1}\n#################\n書き換え後の内容{JSON_text2}'
                            Misskey_api__.create_reply(note['visibility'], g_note, note['id'])
                            logger.info('manual_json_reset')
                        elif e.reply.startswith(('代理', '投稿', '代理投稿')):
                            toukou = e.reply.replace('代理', '',1).replace('投稿', '',1).replace('代理投稿', '',1)
                            toukou = toukou.replace('にゃ', 'な')
                            Misskey_api__.create_note('home', toukou)
                            
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
                            Misskey_api__.create_reply_cw(note['visibility'], output_h, cw_text, note['id'])
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
                        Misskey_api__.create_reply_cw(note['visibility'], output_h, cw_text, note['id'])
                        logger.info('lmm_post')

            else :

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
                            Misskey_api__.create_reply(note['visibility'], note_text, note['id'])
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
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_ohayou')
                        elif (re.compile(scan_list_oyasumi)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_oyasumi))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_oyasumi')
                        elif (re.compile(scan_list_kawaii)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_kawaii))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_kawaii')
                        elif (re.compile(scan_list_oishii)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_oishii))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_oishii')
                        elif (re.compile(scan_list_tiken)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_tiken))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_tiken')
                        elif (re.compile(scan_list_gohan)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_gohan))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_gohan')
                        elif (re.compile(scan_list_labe)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_labe))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_labe')
                        elif (re.compile(scan_list_ittekimasu)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_ittekimasu))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_ittekimasu')
                        elif (re.compile(scan_list_kitaku)).search(node_str):
                            timer = (random.randint(4, 360))
                            timer = float(timer)
                            await asyncio.sleep(timer) 
                            test = str(random.choices(eval(note_list_kitaku))).replace("['", "").replace("']", "") 
                            Misskey_api__.create_reaction(test, note['id'])
                            logger.debug('reaction_kitaku')     
                        else:
                            study_r = str(random.randint(0, 40))
                            logger.debug(f'not_conditions_reaction,study_r:{study_r}')
                            
                            if study_r == '0':
                                study_check = Json_util().json_read("study")
                                if study_check == 0 :
                                    #study_text = stady_note(node_str)
                                    Json_util().json_write("study", 1)
                                    task = asyncio.create_task(stady_note(node_str))
                                    
                                

        except Exception:
         
            logger.debug(traceback.format_exc())
            logger.debug('occurrence_exception')

###########manage##############
dt1()#起動時のみの動作を内部に書く

def cloud_global_runner_1():
    try:
        asyncio.run(cloud_global_runner()) 
    except Exception:
        logger.debug(traceback.format_exc())
        sys_exit_force()  
     
def scherdule_runner():
    try:
        Schedule_utils__=Schedule_utils()
        asyncio.run(Schedule_utils__.schedule_next())
    except Exception:
        logger.debug(traceback.format_exc())
        sys_exit_force()  

async def main():
    try:
        #Schedule_utils__=Schedule_utils()
        #await asyncio.gather(runner(), Schedule_utils__.schedule_next(), runner_main())
        await asyncio.gather(runner(), runner_main())
    except Exception:
        logger.debug(traceback.format_exc())
        sys_exit_force()  
def runner_low_load():
    try:
        asyncio.run(main()) 
    except Exception:
        logger.debug(traceback.format_exc())
        sys_exit_force()  
        

if __name__ == "__main__":
    try:
        #asyncio.run(main()) 
        with ProcessPoolExecutor(max_workers=5) as executor:
            executor.submit(cloud_global_runner_1)
            executor.submit(scherdule_runner)
            executor.submit(asyncio.run(main()))
    except Exception:
        logger.debug(traceback.format_exc())
        sys_exit_force()       


