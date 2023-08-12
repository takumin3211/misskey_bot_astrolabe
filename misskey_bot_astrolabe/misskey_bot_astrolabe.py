
from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3

print("main_sys_booting_now!")
# 初期化
api = Misskey('misskey.seitendan.com')
api.token = 'UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a'
# 設定ファイル
text = ("D:\hobby\python\misskey\test.txt")

# ノート
#tsukizi = ('月次報告。')

#api.notes_create(text=)
#'アストロラーベはメンテナンスモードに入りました'
#'アストロラーベの動作が通常モードに切り替わりました'
#'アストロラーベは休止モードに入ります'
#



# 日次スケージュリング投稿(本番)
def nitizi():
    #api取得
    api.users_show(user_id="9ib6lbdave")
    
    #時間取得
    dt_now = datetime.datetime.now()
    #投稿文作成
    test_a = ('日次報告。' + dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒') + "アストロラーベの全機能は正常に動作しています。")
    #投稿関数
    api.notes_create(text=test_a)
#時間判定
schedule.every().days.at("23:59").do(nitizi)
#常駐化

#while True:
    schedule.run_pending()
    sleep(1)


#DB

#取り出し（昨日＆本日）→計算→投稿→上書き
#　　テスト値　昨日値　本日値
#値1
#値2
#値3


