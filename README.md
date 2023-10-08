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
<p>Misskeyインスタンス「星海天測団Misskey支部」を代表するキャラクターです。Misskeyの慣例に従い「プロキシボット」を名乗っています。</p>
<p>&nbsp;</p>
<h2>機能紹介</h2>
<ul>
  <h3>能動型実行の機能</h3>
<li>マルコフ連鎖機能：ホームTLとグローバルTLを元に自動で文章を生成してノートします。</li>
<li>挨拶：おはよう、おやすみの挨拶が出来ます</li>
<li>日次報告：一日の投稿数や稼働時間をノート出来ます。</li>
<li>RSS投稿：その名の通り一日に何回か、RSSで記事を配信してくれます</li>
<li>システムチェック：空き容量の減少、CPU使用率の上昇を検知すると通知してくれます（一日一回の検出）</li>
<li>ナウプレイング：音楽名とアーティスト、アルバム名をランダムで投稿する機能です。</li>
<li>ご飯紹介：夜にご飯ガチャを自動実行してご飯を紹介してくれます</li>
<li>アニメ紹介：一定の確率でアニメを紹介してくれます</li>
  <h3>受動型実行の機能</h3>
<li>呼び出し：「アストロラーベちゃん」と呼ぶと一定の確率でリプライしてくれます（フォロワー限定）</li>
<li>フォロー返し（フォロー返しの機能）</li>
<li>リアクション：おはよう、おやすみ、ごはん、かわいい、等に反応してカスタム絵文字を付けてくれます（フォロワー限定）</li>
<li>自由トーク：メンションして文章を送ると内容に応じた返信をします。</li>
<li>機能紹介：メンションして「help」「info」「機能」と送ると機能を教えてくれます。</li>
<li>死活報告：メンションして「死活」「世代」「version」と送るとバージョンと時間の乗った返信が来て死活確認等できます</li>
<li>ご飯ガチャ：「献立」「ご飯ガチャ」と送ると517の料理名からランダムで一つ送ってくれます</li>
  <h3>サーバ運用の補佐と、Botの管理をする為の機能</h3>
<li>登録された管理者だけ、停止・再起動が出来ます。また、起動の通知（再起動通知）を受け取れます</li>
</ul>
<h2>実装予定</h2>
<h3>○実装中</h3>
<ul>

</ul>
<h3>○実装予定（順次）</h3>
<ul>
<li>お天気報告機能（リプライ応答型・ランダム地点の併用型）</li>
</ul>
<h3>○実装予定（構想段階・技術調査段階）</h3>
<ul>
<li>翻訳機能</li>
<li>サーバ管理機能（バックアップの報告等）</li>
<li>時間指定のリマインダー</li>
<li>鯖のデータ紹介</li>
<li>トークと選択枝を使って疑似ADVゲームをが出来る機能</li>
<li>メインファイルに鯖のバックアップシステムを組み込み実行・通知をする機能</li>
<li>呼び名登録システム（ID<=>呼び名をDBに登録し順次呼び出す？）</li>
<li>Misskey外実装。主要機能を外部（星海天測団ホームページor独立）に実装する</li>
<li>仮想SSH機能。承認されたユーザにサブプロセスの実行権限と標準出力のノート機能</li>
</ul>
<h2>更新履歴</h2>
  
<ul>
  <li>V1.00.06　2023/09/20　【メイン系（アストロラーベ）】</li>
  <li>V0.07.00　2023/09/20　【メイン系（アストロラーベ）】マルコフ連鎖による自動生成の定期ノート機能（グローバルTLの取得機能）、自動フォロー返し機能</li>
  <li>V0.06.01　2023/09/14　【メイン系】ご飯ガチャ機能（リプライ）、ご飯投稿機能（定期）、アニメ投稿機能（定期）の実装、管理機能の搭載（特定ユーザのみリプライで再起動等が出来る機能）、非同期処理に関する問題の修正、ウェブソケットの例外キャッチの強化【メンテナンス系】簡易的なスクレイピング機能の搭載、CSVの重複データ削除機能の搭載</li>
<li>V05.01　2023/09/07　【通常運用系】ナウプレ機能、初回起動と運用のpyファイルの分離、日次報告ノート機能のコード整理、RSSノート回数の増加、呼び出し機能の回数減少、微細・重大なバグの修正。【メンテナンス系】アストロラーベメンテナンスウィザードのリリース。CSV=>DB、DB=?CSV、m3u=>CSV
、DBのテーブル一覧表示、DBの内容閲覧等の機能を初期から搭載してます</li>
<li>v0.04.00　2023/08/28　呼び出し機能、リアクション機能、システムチェック機能を追加しました。また、定期投稿系の問題を解決し、スケジュール機能を独自実装しました（より柔軟な乱数利用が可能になりました）。新規運用しやすいように、logとmodelフォルダを自動で生成するようにしました。</li>
<li>v0.03.00　2023/08/26　RSS機能を搭載、ログ出力機能を搭載、死活報告機能を追加(「機能紹介」より短く効率的な表示を実現)、各種PATHの自動取得機を追加、時間指定投稿が正常に動作しない問題を解決等</li>
<li>v0.02　2023/08/22　設定項目をsetting.pyに分離し、レポジトリを公開しました。</li>
<li>v0.01　2023/08/21　挨拶投稿、日次投稿、機能紹介、自由トーク機能を搭載して運用を開始しました。</li>
</ul>
<h2>導入時の注意</h2>
  <p>起動するべきメインファイルはmain.pyです。modelフォルダの中にLLM(LLAMA系言語モデル（「chronos-13b.ggmlv3.q4_K_M」を使っています）)を入れて下さい。</p>
  <p>setting.pyの中にMisskeyのトークン、BotのID、管理者のID等を記入して下さい。</p>
　<p>カスタム絵文字等、星海天測団Misskey支部に最適化されている為、適宜api.dbの中を弄る等して調整してください（メンテナンスウィザードに機能が搭載されています）</p>
  <p>cashフォルダの中に、「cash1.txt」「cash2.txt」「cash3.txt」の空ファイルを作って下さい</p>
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
