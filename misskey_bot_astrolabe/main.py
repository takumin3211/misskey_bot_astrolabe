#!//etc/astrolabe/venv/bin/python
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO, WARNING, ERROR
from timeit import Timer
import datetime
import sqlite3
import pandas as pd
import time
import settings
import os
import sys
import configparser
import subprocess
import json

#logger = getLogger('astrolabe_logs')
logger = getLogger('astrolabe_logs')
JSON_PATH = 0
GTL_CASH_CSV_00to04 = 0
GTL_CASH_CSV_04to08 = 0
GTL_CASH_CSV_08to12 = 0
GTL_CASH_CSV_12to16 = 0
GTL_CASH_CSV_16to20 = 0
GTL_CASH_CSV_20to24 = 0

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
    
    with open(JSON_PATH) as f:
        d_update = json.load(f)
    return d_update[f'{key}']

def dt1():
    #時間取得
    dt1 = datetime.datetime.now()
    PATH = os.path.dirname(os.path.abspath(__file__)) 
    #print(PATH)
    config_ini = configparser.ConfigParser(interpolation=None)
    config_ini.read(fr'{PATH}/common.ini', encoding='utf-8-sig')
    var1 = config_ini['INSTANCE']['python_dir']
    #print('python_dir' + var1)

    #フォルダ生成系
    log_path = PATH + '/log'
    model_path = PATH + '/model'
    cash_path = PATH + '/cash'
    cash_img_path = PATH + '/cash_img'
    new_dir_path_recursive = log_path
    new_dir_path_recursive_a = model_path
    new_dir_path_recursive_b = cash_path
    new_dir_path_recursive_c = cash_img_path
    os.makedirs(new_dir_path_recursive, exist_ok=True)
    os.makedirs(new_dir_path_recursive_a, exist_ok=True)
    os.makedirs(new_dir_path_recursive_b, exist_ok=True)
    os.makedirs(new_dir_path_recursive_c, exist_ok=True)
    GTL_CASH_CSV = config_ini['INSTANCE']['GTL_CASH_CSV']
    GTL_CASH_CSV_00to04 = config_ini['INSTANCE']['GTL_CASH_CSV_00to04']
    GTL_CASH_CSV_04to08 = config_ini['INSTANCE']['GTL_CASH_CSV_04to08']
    GTL_CASH_CSV_08to12 = config_ini['INSTANCE']['GTL_CASH_CSV_08to12']
    GTL_CASH_CSV_12to16 = config_ini['INSTANCE']['GTL_CASH_CSV_12to16']
    GTL_CASH_CSV_16to20 = config_ini['INSTANCE']['GTL_CASH_CSV_16to20']
    GTL_CASH_CSV_20to24 = config_ini['INSTANCE']['GTL_CASH_CSV_20to24']
    GTL_CASH_CSV = PATH + "/" + GTL_CASH_CSV  
    GTL_CASH_CSV_00to04 = PATH + "/" + GTL_CASH_CSV_00to04  
    GTL_CASH_CSV_04to08 = PATH + "/" + GTL_CASH_CSV_04to08  
    GTL_CASH_CSV_08to12 = PATH + "/" + GTL_CASH_CSV_08to12  
    GTL_CASH_CSV_12to16 = PATH + "/" + GTL_CASH_CSV_12to16  
    GTL_CASH_CSV_16to20 = PATH + "/" + GTL_CASH_CSV_16to20  
    GTL_CASH_CSV_20to24 = PATH + "/" + GTL_CASH_CSV_20to24  
    GTL_CASH_CSV_temp = pd.DataFrame(columns=['time','instance','id','text'])
    GTL_CASH_CSV_temp = GTL_CASH_CSV_temp.set_index('time')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV, mode='w')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_00to04, mode='w')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_04to08, mode='w')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_08to12, mode='w')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_12to16, mode='w')
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_16to20, mode='w')   
    GTL_CASH_CSV_temp.to_csv(GTL_CASH_CSV_20to24, mode='w')
    #DB記録系
    dbname = config_ini['INSTANCE']['dbname']
    dbname = PATH + "/" + dbname
    conn = sqlite3.connect(dbname)
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
    FORMAT = config_ini['INSTANCE']['format']
    FORMAT = FORMAT.replace('"', '')
    log_date = str(dt1.strftime('%Y%m%d%H%M%S'))
    dt2 = PATH + '/log/' + log_date + '.log'
    logger.setLevel(INFO)
    fl_handler = FileHandler(filename= dt2 , encoding="utf-8")
    fl_handler.setLevel(INFO)
    fl_handler.setFormatter(Formatter(FORMAT))
    logger.addHandler(fl_handler)
    logger.info("logging start")
    alosname = config_ini['INSTANCE']['alosname']

    global JSON_PATH
    JSON_NAME = config_ini['INSTANCE']['JSON_NAME']
    JSON_PATH = PATH + "/" + JSON_NAME  
    #print(dt1)
    time.sleep(5)
    while True:
        if json_read("end_alos") == 0:
            #startup_command = [fr"{var1}/python", fr"{PATH}/{alosname}", f"{log_date}"]
            startup_command = [fr"{var1}/python", fr"{PATH}/{alosname}", f"{log_date}"]
            print('アストロラーベのメインプロセスが開始されました。\n終了の対応が取られるまで自動再起動により動き続けます')
            #print(startup_command)
            # test1.pyを起動して、終了を待機する
            subprocess.run(startup_command, shell=True)   
        elif json_read("end_alos") ==1 :

            json_write("end_alos", 0)
            print('終了コマンドを受領した為、停止します。停止フラグは初期化されました。end_alos:0')
                
            sys.exit()
        logger.info("Reboot alos")
        time.sleep(5)
      
dt1()#起動時のみの動作を内部に書く
