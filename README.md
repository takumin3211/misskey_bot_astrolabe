<!DOCTYPE html>
<html>

<head>
</head>
<body bgcolor="#212121" text="#DCDCDC">
<h1 style="text-align: center;">星海天測団プロキシボット「アストロラーベ」</h1>

<p>&nbsp;</p>
<p>&nbsp;</p>
<h2>自己紹介</h2>


<p>『太古の昔から、人々の物語を支えた天測航法装置&rdquo;アストロラーベ&rdquo;より生まれました。<br />あなたが望む世界に、あなたと一緒に赴きます。<br />「さて、次はどこに向かいましょうか？」』</p>
<p>弊サークル「星海天測団」及び弊サークルの運営するMisskeyインスタンス「星海天測団Misskey支部」を代表するキャラクターです。Misskeyの慣例に従い「プロキシボット」を名乗っています。</p>
<p>&nbsp;</p>
<h2>機能紹介</h2>
<ul>

<li>挨拶：おはよう、おやすみの挨拶が出来ます</li>
<li>日次報告：一日の投稿数や稼働時間をノート出来ます。</li>
<li>RSS投稿：その名の通り一日に何回か、RSSで記事を配信してくれます</li>
<li>システムチェック：空き容量の減少、CPU使用率の上昇を検知すると通知してくれます（一日一回の検出）</li>
<li>呼び出し：「アストロラーベちゃん」と呼ぶと一定の確率でリプライしてくれます（フォロワー限定）</li>
<li>リアクション：おはよう、おやすみ、ごはん、かわいい、等に反応してカスタム絵文字を付けてくれます（フォロワー限定）</li>
<li>自由トーク：メンションして文章を送ると内容に応じた返信をします。</li>
<li>機能紹介：メンションして「help」「info」「機能」と送ると機能を教えてくれます。</li>
<li>死活報告：メンションして「死活」「世代」「version」と送るとバージョンと時間の乗った返信が来て死活確認等できます</li>

</ul>
<h2>実装予定</h2>
<h3>○実装中</h3>
<ul>
  <li>サーバ管理機能（バックアップの報告等）</li>
</ul>
<h3>○実装予定（順次）</h3>
<ul>

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
<li>v0.04.00　2023/08/28　呼び出し機能、リアクション機能、システムチェック機能を追加しました。また、定期投稿系の問題を解決し、スケジュール機能を独自実装しました（より柔軟な乱数利用が可能になりました）。新規運用しやすいように、logとmodelフォルダを自動で生成するようにしました。</li>
<li>v0.03.00　2023/08/26　RSS機能を搭載、ログ出力機能を搭載、死活報告機能を追加(「機能紹介」より短く効率的な表示を実現)、各種PATHの自動取得機を追加、時間指定投稿が正常に動作しない問題を解決等</li>
<li>v0.02　2023/08/22　設定項目をsetting.pyに分離し、レポジトリを公開しました。</li>
<li>v0.01　2023/08/21　挨拶投稿、日次投稿、機能紹介、自由トーク機能を搭載して運用を開始しました。</li>
</ul>
<h2>導入時の注意</h2>
  <p>起動するべきメインファイルはmisskey_bot_astrolabe.pyです。modelフォルダの中にLLM(LLAMA系言語モデル)を入れて下さい。</p>
  <p>setting.pyの中にMisskeyのトークン等を記入して下さい。</p>
　<p>カスタム絵文字等、星海天測団Misskey支部に最適化されている為、適宜api.dbの中を弄る等して調整してください</p>
  <p>メインファイルのShebangも調整してください。</p>
<h2>既知の問題</h2>
<ul>


</ul>
<h2>修正済みの問題</h2>
<ul>
  <li>【2023/08/26修正済み】2023/08/23　起動時「time_db」が見つからない、というSQLiteのエラー</li>
<p>→何回か挑戦すると起動する（原因特定方法がまず不明）</p>
<li>【2023/08/26修正済み】2023/08/23　LLM後、返答をリプで飛ばすとウェブソケットのコネクションクローズが受信されにゃいエラー</li>
<p>→例外処理で対応できにゃいか試行錯誤中。</p>
<p>※たまにうっかり成功するので検証に時間取られがち</p>
  <li>【2023/08/23修正済み】2023/08/23　全ての返信が「ホーム」に返信されている問題。返信元の公開範囲を引き継げるように変更予定。</li>
</ul>
</body>
</html>
