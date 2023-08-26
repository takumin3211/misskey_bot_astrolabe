import os
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO
logger = getLogger('astrolabe_logs.settings')

PATH = os.path.dirname(os.path.abspath(__file__)) 
logger.info(PATH)

text = "test.txt"
dbname = PATH + '/api.db'
csvname = PATH + './api.csv'
AI_NAME = 'Astrolabe'
AI_ID = '"9ib6lbdave'
TOKEN = 'UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a'
ADRESS = 'misskey.seitendan.com'
USER_NAME = 'test_name'
LLMPATH = PATH + "/model/chronos-13b.ggmlv3.q4_K_M.bin"

FORMAT = "%(levelname)-9s  %(asctime)s [%(filename)s:%(lineno)d] %(message)s"


RSS_URL_a = 'https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml'
