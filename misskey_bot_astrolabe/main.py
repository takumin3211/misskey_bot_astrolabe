#!//etc/astrolabe/venv/bin/python
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO, WARNING, ERROR
from timeit import Timer
from misskey import Misskey
import datetime
from time import sleep
import sqlite3
import pandas as pd
import time
import exchange as e
import random
import settings
import os
import re
import sys

#print('test')

#logger = getLogger('astrolabe_logs')

def dt1():
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
    #logger.info("def_dt1 clear")
    #logger.info("ALos_sys_booting_now!")
    #logger.info(Ver)
    #print("ALos_sys_booting_now!")
    #(sys.executable)
    #print(settings.alosname)
    #print(sys.argv)
    print('アストロラーベのプロセスが始動しました。')
    print(dt1)
    time.sleep(5)
    os.execv(sys.executable, ['python '] + [settings.alosname])
    
    #os.exit
    
dt1()#起動時のみの動作を内部に書く
