


with open("test2.txt", "r") as f: # ファイルを読み込みモードで開く
    text = f.read() # ファイルの内容を全て読み込む
    print(text) # 読み込んだ内容を表示する
# with文のブロックを抜けると自動的にファイルが閉じられる