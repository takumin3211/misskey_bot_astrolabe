import json
from llama_cpp import Llama
from transformers import pipeline
from misskey import Misskey
import exchange as e
import os
import time
import settings

if e.n == 0:
	e.n = 1

	print('llm_test01')
	llm = Llama(model_path=settings.LLMPATH)
	#input = 'アメリカで一番大きい都市はどこですか'
	#print(input_text)
	print('受け取りデータ')
	print(e.reply)
	e.reply = e.reply.replace('にゃ', 'な')


	je_translator = pipeline("translation", model="staka/fugumt-ja-en")
	reply_a =je_translator(e.reply)
	reply_b = json.dumps(reply_a)
	reply_c = reply_b.replace('[{"translation_text": "', '')
	reply_d = reply_c.replace('"}]', '')
	#print(reply)
	print('翻訳完了')
	print(reply_d)


	prompt = (f'''This is a conversation between {settings.USER_NAME} and his cute and helpful assistant {settings.AI_NAME} through SNS.
	{settings.AI_NAME} is a very helpful assistant and will help {settings.USER_NAME} with anything. They are also very friendly and try to make you feel good.
	{settings.USER_NAME} are often Japanese people.
	{settings.AI_NAME}'s profile reads: "I will go with you to the world you want."
	Hey, it looks like {settings.AI_NAME} got a message.
	{settings.USER_NAME}:{reply_d}
	{settings.AI_NAME}:''')

	print('プロンプト用意完了')
	print(prompt)


	# 推論の実行
		
	output = llm(
		prompt,
		temperature=0.1,
		max_tokens=1024,
		stop=["Instruction:", "Input:", "Response:", "\n"],
		echo=True,
		)
   
	output_a = output["choices"][0]["text"]
	#print(output_a)

	AI = settings.AI_NAME + ''
	print('生成完了（生）')
	print(output_a)
	#output_b = output_a.replace(AI, '')
	#reply_a = json.dumps(reply)#delete
	output_c = output_a.replace(prompt, '')


	#推論
	input_text = output_c
	ej_translator = pipeline("translation", model="staka/fugumt-en-ja")

	print('翻訳投入文')
	print(input_text)

	output_d =ej_translator(input_text)
	'''

	print(output_d)

	output_e = json.dumps(output_d)
	output_f = output_e.replace('[{"translation_text": "test_name:', '')
	output_g = output_f.replace('"}]', 
	'''
	#投稿
	e.output_h = str(output_d).replace("[{'translation_text': 'test_name:", "").replace("'}]", "") + "\n"
	output_h = str(e.output_h).replace("[{'translation_text': '", "").replace("'}]", "") + "\n"

	time.sleep(5)


	#return output_h
	print('最終生成テキスト')
	print(output_h)

	
	
else:
    print('制御を返却します')