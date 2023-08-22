<!DOCTYPE html>
<html>

<head>
</head>
<body bgcolor="#212121" text="#DCDCDC">
<h1 style="text-align: center;">星海天測団プロキシボット「アストロラーベ」</h1>
<p>&nbsp;</p>
![icontest2](https://github.com/takumin3211/misskey_bot_astrolabe/assets/111957094/767c02a1-4b55-4cd7-b78a-200d4fcf822b)
<p>&nbsp;</p>
<h2>自己紹介</h2>


<p>『太古の昔から、人々の物語を支えた天測航法装置&rdquo;アストロラーベ&rdquo;より生まれました。<br />あなたが望む世界に、あなたと一緒に赴きます。<br />「さて、次はどこに向かいましょうか？」』</p>
<p>弊サークル「星海天測団」及び弊サークルの運営するMisskeyインスタンス「星海天測団Misskey支部」を代表するキャラクターです。Misskeyの慣例に従い「プロキシボット」を名乗っています。</p>
<p>&nbsp;</p>
<h2>機能紹介</h2>
<ul>
<li>挨拶：おはよう、おやすみの挨拶が出来ます</li>
<li>日次報告：一日の投稿数や稼働時間をノート出来ます。</li>
<li>自由トーク：メンションして文章を送ると内容に応じた返信をします。</li>
<li>機能紹介：メンションして「help」「info」「機能」と送ると機能を教えてくれます。</li>
</ul>
<h2>実装予定</h2>
<h3>○実装中</h3>
<p>・RSS投稿する</p>
<p>（「知見がアップ！！」のようなコメントを付けて）</p>
<h3>○実装予定（順次）</h3>
<ul>
<li>アストロラーベちゃん呼び出し（TLで名前を出すと返信してくる）</li>
<li>今日のご飯は〇〇です！（お昼の挨拶機能）</li>
<li>ご飯ガチャ（料理名をランダムで言ってくれる機能）</li>
<li>ナウプレ（音楽名をランダムで投稿する機能）</li>
<li>アニメ思い出し（アニメをランダムで投稿する機能）</li>
<li>フォロー返し（フォロー返しの機能）</li>
</ul>
<h3>○実装予定（構想段階・技術調査段階）</h3>
<ul>
<li>翻訳機能</li>
<li>時間指定のリマインダー</li>
<li>TL学習機能</li>
<li>鯖のデータ紹介</li>
<li>トークと選択枝を使って疑似ADVゲームをが出来る機能</li>
<li>メインファイルに鯖のバックアップシステムを組み込み実行・通知をする機能</li>
<li>呼び名登録システム（ID<=>呼び名をDBに登録し順次呼び出す？）</li>
</ul>
<h2>更新履歴</h2>
<ul>
<li>v0.02　2023/08/22　設定項目をsetting.pyに分離し、レポジトリを公開しました。</li>
<li>v0.01　2023/08/21　挨拶投稿、日次投稿、機能紹介、自由トーク機能を搭載して運用を開始しました。</li>
</ul>
  
<h2>既知の問題</h2>
<ul>
<li>2023/08/23　起動時「time_db」が見つからない、というSQLiteのエラー</li>
<p>→何回か挑戦すると起動する（原因特定方法がまず不明）</p>
<li>2023/08/23　LLM後、返答をリプで飛ばすとウェブソケットのコネクションクローズが受信されにゃいエラー</li>
<p>→例外処理で対応できにゃいか試行錯誤中。</p>
<p>※たまにうっかり成功するので検証に時間取られがち</p>
</ul>
</body>
</html>
