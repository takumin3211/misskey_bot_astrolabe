
from misskey import Misskey
import datetime
import schedule
from time import sleep
import sqlite3

print("main_sys_booting_now!")
# ������
api = Misskey('misskey.seitendan.com')
api.token = 'UeZEaJ09jR9FKI7NHh5vtMaNYKfBxR0a'
# �ݒ�t�@�C��
text = ("D:\hobby\python\misskey\test.txt")

# �m�[�g
#tsukizi = ('�����񍐁B')

#api.notes_create(text=)
#'�A�X�g�����[�x�̓����e�i���X���[�h�ɓ���܂���'
#'�A�X�g�����[�x�̓��삪�ʏ탂�[�h�ɐ؂�ւ��܂���'
#'�A�X�g�����[�x�͋x�~���[�h�ɓ���܂�'
#



# �����X�P�[�W�������O���e(�{��)
def nitizi():
    #api�擾
    api.users_show(user_id="9ib6lbdave")
    
    #���Ԏ擾
    dt_now = datetime.datetime.now()
    #���e���쐬
    test_a = ('�����񍐁B' + dt_now.strftime('%Y�N%m��%d�� %H��%M��%S�b') + "�A�X�g�����[�x�̑S�@�\�͐���ɓ��삵�Ă��܂��B")
    #���e�֐�
    api.notes_create(text=test_a)
#���Ԕ���
schedule.every().days.at("23:59").do(nitizi)
#�풓��

#while True:
    schedule.run_pending()
    sleep(1)


#DB

#���o���i������{���j���v�Z�����e���㏑��
#�@�@�e�X�g�l�@����l�@�{���l
#�l1
#�l2
#�l3


