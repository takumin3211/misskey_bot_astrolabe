import os
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO
logger = getLogger('astrolabe_logs.settings')

PATH = os.path.dirname(os.path.abspath(__file__)) 
logger.info(PATH)

text = "test.txt"
dbname = PATH + '/api.db'
csvname = PATH + '/api.csv'
m3uname = PATH + '/list.m3u'
alosname = PATH +'/misskey_bot_astrolabe.py'
AI_NAME = 'Astrolabe'
AI_ID = '9ib6lbdave'
Master_ID = ''
TOKEN = 'UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a'
ADRESS = 'misskey.seitendan.com'
USER_NAME = 'test_name'
LLMPATH = PATH + "/model/chronos-13b.ggmlv3.q4_K_M.bin"

FORMAT = "%(levelname)-9s  %(asctime)s [%(filename)s:%(lineno)d] %(message)s"


RSS_URL_a = 'https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml'
RSS_URL_b = 'https://gigazine.net/news/rss_2.0/'


note_list_ohayou = [':ohayoo:']
note_list_oyasumi = [':oyasumi2:', ':neru_purikone_anime:']
note_list_kawaii = [':emoemo2_nizigasaki_anime:', ':kawaii_comment:', ':kawwa_comment:']
note_list_oishii = [':oishimi_text:', ':unnmenya_wug_anime:']
note_list_tiken = [':rs_tiken_up:']
note_list_gohan = [':taberux2_kouhuku_anime:', ':oishimi_text:', ':gokugoku_comment:', ':unnmenya_wug_anime:']

