<!DOCTYPE html>
<html lang="ja">
<body>
<div class="container">

<!-- PAGE TITLE -->
<div class="page-title">
  <h1>ＤＲＳ ユーザーズマニュアル <span class="version">V2.5 Python版</span></h1>
</div>

<!-- NAV LINKS -->
<nav class="nav-links">
  <a href="#overview">プログラム概要</a>
  <a href="#features">特徴</a>
  <a href="#requirements">必須事項</a>
  <a href="#devices">テスト済機器</a>
  <a href="#ch1">第１章 インストール</a>
  <a href="#ch2">第２章 測定機器の接続</a>
  <a href="#ch3">第３章 フォルダの作成</a>
  <a href="#ch4">第４章 ユーザー管理</a>
  <a href="#ch5">第５章 運用の基本</a>
  <a href="#ch6">第６章 寸法ファイル</a>
  <a href="#ch7">第７章 図面ファイル</a>
  <a href="#ch8">第８章 データ類</a>
  <a href="#ch9">第９章 検査成績表</a>
  <a href="#qa">第１０章 Ｑ＆Ａ集</a>
  <a href="#appendix1">付録１ キー一覧</a>
  <a href="#appendix2">付録２ メイン画面</a>
  <a href="#appendix3">付録３ 図面画面</a>
  <a href="#appendix4">付録４ フローチャート</a>
  <a href="#appendix5">付録５ ユーザー編</a>
  <a href="#appendix6">付録６ データ管理編</a>
</nav>

<!-- HERO -->
<div class="hero">
  <h2>測定値自動入力システム</h2>
  <p>日常検査の記録を効率化し、負荷低減・コスト削減・品質向上に貢献します</p>
</div>

<!-- OVERVIEW -->
<section id="overview">
  <div class="section-header">
    <span class="section-num">概要</span>
    <h2>プログラム概要</h2>
  </div>
  <div class="card">
    「ＤＲＳ」は、製造した製品の日常検査を、極力自動化する為のソフトウェアです。<br>
    RS232Cが付いた、マイクロ、ハイトゲージ、投影機等に対応します。<br>
    作業者が、担当する機番に製品（寸法公差データ）を事前登録する事で、測定結果が自動で保存されます（ファイル名に担当者名、品名品番、機番、測定日が付与されます）。<br>
    測定値は、スペースキーを押すだけで、自動で記録されます。<br><br>
    本マニュアルは、Pythonで再実装された「ＤＲＳ Python版（V2.5）」の操作方法を説明します（画像は旧ソフトウェアのものです）。
  </div>
</section>

<!-- FEATURES -->
<section id="features">
  <div class="section-header">
    <span class="section-num">概要</span>
    <h2>特徴</h2>
  </div>

  <div class="card">
    <h3>測定の効率化</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>１つの製品で最大３００箇所測定可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>測定データはキー１つで入力可能（<kbd>Space</kbd>キー）</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>次に測定する箇所を自動選択</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>測定対象製品は、いつでもキー１つで切り替え可能（最大４８製品）</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>最大限の自動化で測定値記入時間を大幅に短縮可能（当社比４分の１）</li>
    </ul>
  </div>

  <div class="card">
    <h3>品質向上</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>製品の寸法、公差、狙い目を記入したファイルを一度準備すれば、自動で合否を判定し、不良品流出を防止</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>不合格箇所の履歴を記録</li>
    </ul>
  </div>

  <div class="card">
    <h3>測定機器</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>最大１０台の測定器を、１台のＰＣにＲＳ２３２Ｃで接続可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>１０台以上の測定機器を使用したい場合は、２台以上のＰＣで対応可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>測定器は<kbd>Ｆ１</kbd>～<kbd>Ｆ１０</kbd>キーで切り替え可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>豊富な設定項目で様々な測定器に対応</li>
    </ul>
  </div>

  <div class="card">
    <h3>ユーザー関連</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>１つのユーザー名で最大４８個の製品を測定可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>登録出来るユーザー数は無制限</li>
    </ul>
  </div>

  <div class="card">
    <h3>ファイル関連</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>測定データファイルの準備及び保存は全自動</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>一度ＤＲＳを終了しても、再度ＤＲＳを起動すれば、ファイルを自動的に読み込み、測定を再開可能</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>ファイル名に号機、測定者名、製品名、年月日を自動入力</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>ＥＸＣＥＬ不要 — 内部ライブラリ（xlrd/xlwt）で.xlsファイルを直接処理</li>
    </ul>
  </div>

  <div class="card">
    <h3>図面表示</h3>
    <ul style="list-style:none;padding:0;">
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>独立したウィンドウで図面を表示</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>マウスホイールでズーム（マウス位置为中心に拡大・縮小）</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>左クリックドラッグで図面を移動</li>
      <li style="padding:4px 0 4px 1.2rem;position:relative;"><span style="position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--success);"></span>製品登録時に自動表示</li>
    </ul>
  </div>
</section>

<!-- REQUIREMENTS -->
<section id="requirements">
  <div class="section-header">
    <span class="section-num">概要</span>
    <h2>必須事項</h2>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>項目</th><th>要件</th></tr></thead>
      <tbody>
        <tr><td>ＯＳ</td><td>Ｗｉｎｄｏｗｓ １０以上</td></tr>
        <tr><td>ＣＰＵ</td><td>ｉｎｔｅｌ Ｃｏｒｅ ｉ３以上（または同等）</td></tr>
        <tr><td>メモリ</td><td>４ＧＢ以上</td></tr>
        <tr><td>解像度</td><td>１６００×８００以上（推奨：１９２０×１０８０）</td></tr>
        <tr><td>Python</td><td>Python ３．８以上（６４ビット版）</td></tr>
        <tr><td>測定器</td><td>ＰＣ側からの命令で測定器が測定値を出力する事</td></tr>
        <tr><td>データ形式</td><td>測定機器から出力されるデータが固定長である事</td></tr>
        <tr><td>通信プロトコル</td><td>ＰＣ側及び測定機器側の命令が、ＣＲ、ＬＦ，ＣＲ＋ＬＦのいずれかで完了する事</td></tr>
      </tbody>
    </table>
  </div>
  <div class="alert alert-info" style="margin-top:1rem;">
    <strong>注意：</strong>ＥＸＣＥＬのインストールは必須ではありません。ＤＲＳは内部ライブラリ（xlrd/xlwt）を使用して.xlsファイルを直接読み書きします。
  </div>
</section>

<!-- DEVICES -->
<section id="devices">
  <div class="section-header">
    <span class="section-num">概要</span>
    <h2>テスト済測定機器及び中間機器</h2>
  </div>
  <div class="feature-grid">
    <div class="feature-card">
      <h4>ニコン社製</h4>
      <ul>
        <li>デジタルマイクロ表示ユニット ＭＦＣ－１０１（デジタルマイクロ）</li>
        <li>カウンタ ＳＣ－２１３／ＳＣ－２１２（投影機）</li>
      </ul>
    </div>
    <div class="feature-card">
      <h4>ミツトヨ社製</h4>
      <ul><li>ＭＵＸ－１０Ｆ（マイクロメータ等）</li></ul>
    </div>
    <div class="feature-card">
      <h4>ＵＳＢ to シリアルケーブル</h4>
      <ul><li>エレコム社製 ＵＣ－ＳＧＴ</li></ul>
    </div>
  </div>
</section>

<!-- CHAPTER 1 -->
<section id="ch1">
  <div class="section-header">
    <span class="section-num">第１章</span>
    <h2>インストール</h2>
  </div>
  <div class="alert alert-info">
    ＤＲＳ Python版は、ライセンスキーやＵＳＢキーを必要としません。Python環境をインストール後、ＤＲＳを起動するだけで使用可能です。
  </div>
  <div class="steps">
    <div class="step">
      <p>Python ３．８以上をインストールします。Python公式サイト（https://www.python.org/）からダウンロードし、インストーラーを実行して下さい。</p>
      <div class="note">インストール時に「Add Python to PATH」にチェックを入れて下さい。</div>
    </div>
    <div class="step">
      <p>コマンドプロンプトまたはＰｏｗｅｒＳｈｅｌｌを開き、以下のコマンドで必要なライブラリをインストールします。</p>
      <div class="note">
        <code>pip install PySide6 pyserial xlrd xlwt</code>
      </div>
    </div>
    <div class="step">
      <p>ＤＲＳのプログラムフォルダに移動し、以下のコマンドで起動します。</p>
      <div class="note">
        <code>python main.py</code>
      </div>
    </div>
    <div class="step">
      <p>「ユーザー選択画面」が表示されます。必要な設定を行います。</p>
    </div>
  </div>
</section>

<!-- CHAPTER 2 -->
<section id="ch2">
  <div class="section-header">
    <span class="section-num">第２章</span>
    <h2>測定機器の接続・設定</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>ＰＣ側シリアルポートと測定機器側シリアルポートを「測定器メーカー指定のシリアルケーブル」で接続します。</p>
    </div>
    <div class="step">
      <p>Ｗｉｎｄｏｗｓの「デバイス マネージャ」から「ポート（ＣＯＭとＬＰＴ）」を確認し、ＰＣ側シリアルポートの「ＣＯＭ番号」を確認します。</p>
    </div>
    <div class="step">
      <p>「ＤＲＳ」を起動し、ユーザー選択画面の「設定」ボタンを押して、「設定画面」を表示します。</p>
    </div>
    <div class="step">
      <p>「設定画面」の左上のドロップダウンから設定を割り当てたいキー（<kbd>Ｆ１</kbd>～<kbd>Ｆ１０</kbd>）を選びます。</p>
    </div>
    <div class="step">
      <p>先ほど確認した「ＣＯＭ番号」を「ＣＯＭポート」から選択します。</p>
    </div>
    <div class="step">
      <p>測定機器のマニュアルに記載されている通信方式を「ハンドシェイク」から選択します。通信方式が記載されていない場合は <kbd>ＲＴＳ/CTS</kbd> を選択して下さい。</p>
    </div>
    <div class="step">
      <p>測定機器のマニュアルに記載されている、「ボーレート」・「パリティ」・「データ長」・「ストップビット」を選択して下さい。</p>
    </div>
    <div class="step">
      <p>測定機器のマニュアルに記載されている、測定値取得命令を「データ取得コマンド」に入力して下さい。続いて、ＰＣ側・測定機器側の命令完了文字（デリミタ）を「ＰＣ送信終了文字」と「機器送信終了文字」から選択して下さい。</p>
    </div>
    <div class="step">
      <p>測定機器のマニュアルに従い、通信して得たデータから測定値を取り出す設定を行います。測定機器から取得するデータのどの位置から測定値が始まるか確認し、「データ開始位置」に入力します。次に、測定値の終了位置を確認し、「データ終了位置」に入力します。分からない場合は、「通信テスト」ボタンを押し、取得したデータで確認して下さい。</p>
    </div>
    <div class="step">
      <p>「ＤＲＳ」のメイン画面に表示したい測定器名を「表示用機器名」に入力します。使用した測定機器名をＥＸＣＥＬファイルに表示したい場合は、「Ｅｘｃｅｌ用機器名」に測定器名を入力します。</p>
    </div>
    <div class="step">
      <p>「通信テスト」ボタンを押し、測定値が取得出来るか確認して下さい。</p>
    </div>
    <div class="step">
      <p>問題なく通信出来たら、「ＯＫ」ボタンを押し、設定を保存して下さい。</p>
    </div>
    <div class="step">
      <p>測定機器が複数ある場合は、この章の１から繰り返して下さい。</p>
    </div>
  </div>
</section>

<!-- CHAPTER 3 -->
<section id="ch3">
  <div class="section-header">
    <span class="section-num">第３章</span>
    <h2>製品フォルダの作成</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>「寸法ファイル」・「図面ファイル」・「測定記録」の保存先を作成します。任意の場所に、「製品」（任意）と言う名前のフォルダを作成して下さい。</p>
      <div class="note">フォルダ作成場所は、Ｗｉｎｄｏｗｓネットワーク上の共有フォルダでもかまいませんが、測定に使用するＰＣからアクセス出来るようにして下さい。</div>
    </div>
    <div class="step">
      <p>作成した「製品」フォルダの中に、取引先名のフォルダを作成して下さい。</p>
    </div>
    <div class="step">
      <p>作成した取引先名のフォルダの中に、製品名のフォルダを作成して下さい。</p>
    </div>
    <div class="step">
      <p>必要に応じて随時、取引先名・製品名のフォルダを作成して下さい。</p>
    </div>
  </div>
  <div class="card" style="margin-top:1rem;">
    <h3>フォルダ構造例</h3>
    <div style="font-family:monospace;font-size:0.88rem;line-height:1.9;background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:1rem 1.5rem;white-space:pre-wrap;">製品（任意のフォルダ名）
├── サファイア精密（取引先名）
│   ├── Ｆ９１－７７７－０２ シャフト（製品名）
│   │   ├── Ｄａｔａ．ｘｌｓ（寸法ファイル）
│   │   ├── Ｆ９１－７７７－０２ シャフト.jpg（図面ファイル）
│   │   ├── 検査成績表＿原版．ｘｌｓ（検査成績表テンプレート）
│   │   └── Ｄａｔａ（測定データ保存先、自動作成）
│   │       └── 山田太郎_Ｆ９１－７７７－０２ シャフト_0号機_2025年1月15日.xls
│   └── Ｆ９２－８８８－０３ ギア（製品名）
│       ├── Ｄａｔａ．ｘｌｓ
│       ├── Ｆ９２－８８８－０３ ギア.jpg
│       └── Ｄａｔａ
│           └── 山田太郎_Ｆ９２－８８８－０３ ギア_0号機_2025年1月15日.xls
└── ＡＣＳ（取引先名）
    └── 山田太郎_B１２－３４５－０１プレート（製品名）
        ├── Ｄａｔａ．ｘｌｓ
        ├── 山田太郎_B１２－３４５－０１プレート.jpg
        └── Ｄａｔａ
            └── 山田太郎_山田太郎_B１２－３４５－０１ プレート_0号機_2025年1月15日.xls</div>
    <div class="alert alert-info" style="margin-top:0.75rem;">
      <strong>各ファイルの説明：</strong><br>
      ・<strong>Ｄａｔａ．ｘｌｓ</strong> — 寸法・公差・狙い寸法を記述（手動作成）<br>
      ・<strong>製品名.jpg</strong> — 図面ファイル（フォルダ名と同名）<br>
      ・<strong>検査成績表＿原版．ｘｌｓ</strong> — 検査成績表作成用テンプレート（任意）<br>
      ・<strong>Ｄａｔａ/</strong> — 測定データ保存フォルダ（自動作成）<br>
      ・<strong>データファイル</strong> — 測定者名_製品名_号機_日付.xls（自動作成・保存）
    </div>
  </div>
</section>

<!-- CHAPTER 4 -->
<section id="ch4">
  <div class="section-header">
    <span class="section-num">第４章</span>
    <h2>ユーザーの新規作成・削除・新規登録</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>新規にユーザーを登録するには、「ＤＲＳ」を起動後、「ユーザー選択」の「新規作成」ボタンを押します。任意のフォルダを選択後、「ユーザー名」を入力し、「ＯＫ」ボタンを押します。</p>
    </div>
    <div class="step">
      <p>作成したユーザーを「ユーザー選択」のリストから削除するには、ユーザー名を選択後、「削除」ボタンを押します。</p>
      <div class="note">「ユーザー選択」のリストからユーザーを削除しても、フォルダ内のユーザーデータは残ります。ユーザーを完全に削除したい場合には、フォルダ内のユーザーフォルダも手動で削除して下さい。</div>
    </div>
    <div class="step">
      <p>「ユーザー選択」のリストから削除したユーザーを再度登録したい場合や、他のＰＣで作成したユーザー情報を登録したい場合は、「新規登録」を使用します。「新規登録」ボタンを押した後、ユーザーフォルダを選択して下さい。</p>
    </div>
  </div>
</section>

<!-- CHAPTER 5 -->
<section id="ch5">
  <div class="section-header">
    <span class="section-num">第５章</span>
    <h2>運用の基本</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>以上の設定が終われば、製品を登録するだけで「ＤＲＳ」の基本的な運用が可能となります。</p>
    </div>
    <div class="step">
      <p>製品を登録するには、「<strong>測定準備</strong>」状態で、「<strong>製品名</strong>」の「選択」ボタンを押します。製品名のフォルダを選択後、製品名までのパスが表示されたのを確認して下さい。</p>
      <div class="note">測定する必要がなくなった製品は、同じ「選択」ボタンで空のパスを選択し登録解除して下さい。「ＤＲＳ」の起動時間を大幅に短縮する事が出来ます。</div>
    </div>
    <div class="step">
      <p>「ＤＲＳ」のメイン画面を表示するには、「ユーザー選択」でユーザーを選択した後、「決定」ボタンを押します。測定データは１箇所測定する度に保存されますので、メイン画面右上の「Ｘ」ボタンを押す事で、いつでも「ＤＲＳ」を終了させる事が可能です。</p>
      <div class="note">「測定開始」状態では、「Ｘ」ボタンで終了できません。必ず「測定準備」状態（<kbd>ＥＳＣ</kbd>キー）にしてから終了して下さい。</div>
    </div>
    <div class="step">
      <p>測定を開始するには、「開始」ボタンを押し、「<strong>測定開始</strong>」状態にします。<kbd>Space</kbd>キーを押すことで、測定機器から測定値を取得・自動入力する事が可能となります。<kbd>ＥＳＣ</kbd>キーを押すと、「<strong>測定準備</strong>」状態になります。</p>
    </div>
  </div>

  <div style="margin-top:1.5rem;">
    <h3 style="font-size:1.05rem;color:var(--primary-dark);margin-bottom:1rem;">メイン画面各項目の説明</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th style="width:120px;">項目</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td><strong>測定器</strong></td><td>現在選択されている測定器名を表示します。<kbd>Ｆ１</kbd>～<kbd>Ｆ１０</kbd>キーで測定器を変更します。<kbd>Ｆ１１</kbd>キー・<kbd>Ｆ１２</kbd>キーを押す事で、強制的に「ＮＧ」・「ＯＫ」判定が行えます。</td></tr>
          <tr><td><strong>機械番号</strong></td><td>現在の測定対象製品番号（０～４７）を表示します。「測定開始」状態で、キーボードの専用キーを押すと測定対象製品番号が変わります（小文字：０～２３、大文字：２４～４７）。</td></tr>
          <tr><td><strong>製品名</strong></td><td>現在の測定対象製品名を表示します。「測定準備」状態で、「選択」ボタンを押すことで、製品の登録・解除が行えます。</td></tr>
          <tr><td><strong>日付</strong></td><td>選択した日付の測定データを読み込みます。「測定準備」状態で「選択」ボタンを押すとカレンダーが表示されます。日付を変更すると、機械番号は０号機にリセットされ、全てのデータが再読み込みされます。</td></tr>
          <tr><td><strong>測定値リスト</strong></td><td>現在の測定対象製品の測定データが表示されます。最大３００行まで入力可能です。</td></tr>
          <tr><td><strong>開始</strong></td><td>このボタンを押すと、「測定開始」状態になり、<kbd>Space</kbd>キーを押すことで、測定機器から測定値を取得・自動入力する事が可能となります。<kbd>ＥＳＣ</kbd>キーを押すと、「測定準備」状態になります。</td></tr>
          <tr><td><strong>入力先番号</strong></td><td>現在の測定値入力先番号を表示します。「自動」チェックが入った状態では、測定後自動で次の入力先を検索・選択します。「検索」ボタンを押すと、手動で次の入力先番号を検索・選択します。</td></tr>
          <tr><td><strong>手動数値入力</strong></td><td>手動で数値を入力したい場合に使用します。「削除」チェックが入っていると、入力後にテキストボックスがクリアされます。</td></tr>
          <tr><td><strong>手動文字入力</strong></td><td>メモ等を入力したい場合に使用します。「削除」チェックが入っていると、入力後にテキストボックスがクリアされます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- CHAPTER 6 -->
<section id="ch6">
  <div class="section-header">
    <span class="section-num">第６章</span>
    <h2>寸法ファイルの準備</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>測定する際、寸法・公差を表示し、合否判定を行う為には、製品名のフォルダの中に寸法ファイルを準備し、自動的に読み込ませる必要があります。寸法ファイルを作成するためには、ＥＸＣＥＬまたは任意の表計算ソフトを起動します。</p>
    </div>
    <div class="step">
      <p>ＥＸＣＥＬの「Ａ列」に寸法・「Ｂ列」に公差上限値・「Ｃ列」に公差下限値・「Ｄ列」に狙い寸法を入力します。入力する寸法が複数ある場合は、行を変えて同じ様に入力します。また、寸法とは別に、「外観」等のメモも入力可能です。</p>
      <div class="note">効率良く測定する為に、同じ測定器で測定出来る順序で寸法を入力して下さい。また、同じ測定器で測定する際も、極力連続して測定出来る順序で寸法を入力して下さい。</div>
    </div>
    <div class="step">
      <p>入力を終えたら、製品名のフォルダの中に、必ず「Ｄａｔａ．ｘｌｓ」と言うファイル名で保存して下さい（.xls形式）。</p>
    </div>
  </div>
</section>

<!-- CHAPTER 7 -->
<section id="ch7">
  <div class="section-header">
    <span class="section-num">第７章</span>
    <h2>図面ファイルの準備</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>測定する際、図面を表示するには、図面ファイルを準備し、自動的に読み込ませる必要があります。最初に、スキャナー等を使用し、図面を白黒２００ｄｐｉ程度で取り込み、ＪＰＥＧ形式で保存して下さい。</p>
    </div>
    <div class="step">
      <p>図面のファイル名を、製品名のフォルダ名と同じにして下さい。</p>
      <div class="note">例：製品名のフォルダ名が「Ｆ９１－７７７－０２ シャフト」なら、図面ファイル名は「Ｆ９１－７７７－０２ シャフト.jpg」となります。</div>
    </div>
    <div class="step">
      <p>図面ファイルを、製品名のフォルダの中に移動して下さい。</p>
    </div>
    <div class="step">
      <p>一度図面ファイルを準備すれば、製品を登録した際に「図面」ウィンドウが自動で表示されます。</p>
    </div>
  </div>
  <div class="card" style="margin-top:1rem;">
    <h3>図面ウィンドウの操作方法</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th style="width:120px;">操作</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>ズーム</td><td>マウスホイールを回転させる事で図面を拡大・縮小出来ます。マウスカーソルの位置为中心に拡大・縮小されます。</td></tr>
          <tr><td>移動</td><td>左クリックしてドラッグする事で図面を移動出来ます。</td></tr>
          <tr><td>閉じる</td><td>図面ウィンドウは独立したウィンドウとして表示されます。メインウィンドウを閉じると図面ウィンドウも自動的に閉じます。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- CHAPTER 8 -->
<section id="ch8">
  <div class="section-header">
    <span class="section-num">第８章</span>
    <h2>データ類</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>測定データは、製品名のフォルダの中に作られた、「Ｄａｔａ」フォルダの中に保存されます。測定データは.xlsファイルとして保存されており、Ｓｈｅｅｔ１に寸法・公差上限・公差下限・測定器名・測定値・合否判定が記入されています。Ｓｈｅｅｔ２には、寸法・補正値が記入されています。</p>
      <div class="note">ＤＲＳ Python版はＥＸＣＥＬを起動することなく、内部ライブラリで直接.xlsファイルを処理します。そのため、測定中はＥＸＣＥＬを起動する必要も、起動してはいけないという制限もありません。</div>
    </div>
    <div class="step">
      <p>不合格記録は「製品」フォルダの中に作られた、「測定不良\\不良リスト」フォルダの中に保存されます。</p>
    </div>
  </div>
  <div class="card" style="margin-top:1rem;">
    <h3>設定ファイルの保存場所</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th style="width:180px;">ファイル</th><th>内容</th></tr></thead>
        <tbody>
          <tr><td>Ｕｓｅｒｓ．ｄａｔ</td><td>ユーザー名のリスト</td></tr>
          <tr><td>Ｐａｔｈ．ｄａｔ</td><td>ユーザーのフォルダパス</td></tr>
          <tr><td>ＲＳ２３２Ｃ．ｄａｔ</td><td>測定機器の通信設定</td></tr>
          <tr><td>ＰｒｏｄｕｃｔＤｉｒ．ｄａｔ</td><td>製品フォルダのパス</td></tr>
          <tr><td>Ｄｉｒｅｃｔｏｒｙ．ｄａｔ</td><td>号機ごとの製品フォルダパス（ユーザーフォルダ内）</td></tr>
        </tbody>
      </table>
    </div>
    <div class="alert alert-info" style="margin-top:0.5rem;">
      設定ファイルは <code>%USERPROFILE%\AppData\Local\DRS\Config\</code> に保存されます。
    </div>
  </div>
</section>

<!-- CHAPTER 9 検査成績表 -->
<section id="ch9">
  <div class="section-header">
    <span class="section-num">第９章</span>
    <h2>検査成績表の作成</h2>
  </div>
  <div class="alert alert-info">
    検査成績表は、ＤＲＳで収集した測定データを元に、ＥＸＣＥＬマクロを使用して自動作成します。製品名のフォルダ内に「検査成績表＿原版．ｘｌｓ」を配置し、操作パネルシートのボタンでデータを読み込み・加工します。
  </div>
  <div class="steps">
    <div class="step">
      <p>製品名のフォルダ内に「検査成績表＿原版．ｘｌｓ」を配置し、起動します。</p>
    </div>
    <div class="step">
      <p>「図番」・「品番」・「製品名」を記入し、「ファイル」メニューから「上書き保存」後、一旦ＥＸＣＥＬを終了します。</p>
      <div class="note">「ツール」メニューの「マクロ」→「セキュリティー」の設定を「中」以下にして下さい。</div>
    </div>
    <div class="step">
      <p>実際に検査成績表を作成するには、「検査成績表＿原版．ｘｌｓ」を起動し、「操作パネル」シートを表示します。「Ｎｏ．１データ読み込み」～「Ｎｏ．１０データ読み込み」では、個別にデータを読み込む事が出来ます。「連続読み込み」では、指定したフォルダから１０個のファイルを自動で読み込みます。</p>
    </div>
    <div class="step">
      <p>「検査成績表」シートの必要事項を記入後、「操作パネル」シートの「保存」を押すと、「検査成績表」フォルダを自動作成し、作成日のファイル名でファイルを保存します。同日にファイルを保存した場合には、自動連番を付記し、ファイルを保存します。</p>
    </div>
    <div class="step">
      <p>「検査成績表＿原版．ｘｌｓ」を終了する場合は、「操作パネル」シートの「強制終了」を使用して下さい。原版が上書きされるのを防ぎます。</p>
    </div>
    <div class="step">
      <p>必要に応じて、「最大・最小値強調」・「バラツキ判定」・「合否判定」を使用して下さい。「最大・最小値強調」は測定データの最大値・最小値の項目の文字を強調表示させます。「バラツキ判定」は測定データにバラツキ幅を加減算し、規格から外れた項目の背景色を赤色にします。「合否判定」は測定データの合否判定を行い、規格から外れた項目の文字を赤色にします（この機能を使用しなくとも「ＤＲＳ」の判定を元に合否判定は表示されます）。「元に戻す」を使用すると、文字色・背景色は元に戻ります。</p>
    </div>
  </div>
  <div class="card" style="margin-top:1rem;">
    <h3>操作パネルシートの機能</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th style="width:160px;">ボタン</th><th>説明</th></tr></thead>
        <tbody>
          <tr><td>Ｎｏ．１～Ｎｏ．１０データ読み込み</td><td>個別に測定データファイル（.xls）を読み込みます。</td></tr>
          <tr><td>連続読み込み</td><td>指定したフォルダから１０個のファイルを自動で読み込みます。</td></tr>
          <tr><td>保存</td><td>「検査成績表」フォルダに作成日付のファイル名で保存します。</td></tr>
          <tr><td>最大・最小値強調</td><td>測定データの最大値・最小値の項目の文字を強調表示します。</td></tr>
          <tr><td>バラツキ判定</td><td>バラツキ幅を加減算し、規格外項目の背景色を赤色にします。</td></tr>
          <tr><td>合否判定</td><td>規格外項目の文字を赤色にします。</td></tr>
          <tr><td>元に戻す</td><td>文字色・背景色を元に戻します。</td></tr>
          <tr><td>強制終了</td><td>原版を保存せずに終了します。</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- CHAPTER 10 Q&A -->
<section id="qa">
  <div class="section-header">
    <span class="section-num">第１０章</span>
    <h2>Ｑ＆Ａ集</h2>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：１つの製品で測定出来る箇所数は？</div>
    <div class="qa-a">最大３００箇所まで測定可能です。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：ＥＸＣＥＬのインストールは必須ですか？</div>
    <div class="qa-a">いいえ、必須ではありません。ＤＲＳは内部ライブラリ（xlrd/xlwt）を使用して.xlsファイルを直接読み書きします。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：ライセンスキーやＵＳＢキーは必要ですか？</div>
    <div class="qa-a">いいえ、不要です。Python環境をインストールし、ＤＲＳを起動するだけで使用可能です。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：通信完了文字は３種類以外にも対応出来ますか？</div>
    <div class="qa-a">現在はＣＲ、ＬＦ、ＣＲ＋ＬＦの３種類に対応しています。他の文字が必要な場合はご相談下さい。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：ＲＳ２３２Ｃ以外の通信方法を採用した測定機器には対応出来ませんか？</div>
    <div class="qa-a">ご検討させて頂きますので、ご相談下さい。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：ＲＳ２３２Ｃボードの対応は？</div>
    <div class="qa-a">ＲＳ２３２Ｃボードでの実績も御座います。汎用的なＲＳ２３２Ｃボードであれば使用出来ます。ＵＳＢ to シリアル変換ケーブルも使用可能です。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：フットスイッチへの対応は？</div>
    <div class="qa-a">市販ＵＳＢフットスイッチで対応可能かもしれません。キーボードを床に置き代用して下さい。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：バグが見つかったのですが？</div>
    <div class="qa-a">対策を検討させて頂き、修正ファイルを発行する予定です。お手数をお掛け致しますが、ご連絡下さい。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：測定中にウィンドウを閉じようとすると閉じません。</div>
    <div class="qa-a">「測定開始」状態では、誤操作による終了を防ぐ為にウィンドウの閉じを無効にしています。<kbd>ＥＳＣ</kbd>キーで「測定準備」状態にしてから終了して下さい。</div>
  </div>

  <div class="qa">
    <div class="qa-q">Ｑ：図面ウィンドウを閉じたくありませんが、閉じるボタンがありません。</div>
    <div class="qa-a">図面ウィンドウはメインウィンドウと同時に閉じるよう設計されています。メインウィンドウを終了すると図面ウィンドウも自動的に閉じます。</div>
  </div>
</section>

<!-- APPENDIX 1 -->
<section id="appendix1">
  <div class="section-header">
    <span class="section-num">付録１</span>
    <h2>「ＤＲＳ」使用キー一覧</h2>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th style="width:120px;">キー</th><th>機能</th></tr></thead>
      <tbody>
        <tr><td><kbd>ＥＳＣ</kbd></td><td>「測定開始」状態を解除し、「測定準備」状態にします。</td></tr>
        <tr><td><kbd>Ｆ１</kbd>～<kbd>Ｆ１０</kbd></td><td>使用する測定器を変更します（１～１０番）。</td></tr>
        <tr><td><kbd>Ｆ１１</kbd></td><td>強制的に「ＮＧ」判定をします（測定値に「ＮＧ」、判定に「不」を入力）。</td></tr>
        <tr><td><kbd>Ｆ１２</kbd></td><td>強制的に「ＯＫ」判定をします（測定値に「ＯＫ」、判定に「合」を入力）。</td></tr>
        <tr><td><kbd>Space</kbd></td><td>測定値を取り込みます。「測定開始」状態でのみ使用出来ます。</td></tr>
        <tr><td><kbd>q</kbd>～<kbd>]</kbd></td><td>機械番号０～２３に切り替えます（小文字キー）。</td></tr>
        <tr><td><kbd>Q</kbd>～<kbd>}</kbd></td><td>機械番号２４～４７に切り替えます（大文字キー、<kbd>Ｓｈｉｆｔ</kbd>+小文字）。</td></tr>
      </tbody>
    </table>
  </div>
  <div class="card" style="margin-top:1rem;">
    <h3>機械番号切り替えキー一覧</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>機械番号</th><th>キー</th><th>機械番号</th><th>キー</th><th>機械番号</th><th>キー</th><th>機械番号</th><th>キー</th></tr></thead>
        <tbody>
          <tr><td>０</td><td><kbd>q</kbd></td><td>１２</td><td><kbd>a</kbd></td><td>２４</td><td><kbd>Q</kbd></td><td>３６</td><td><kbd>A</kbd></td></tr>
          <tr><td>１</td><td><kbd>w</kbd></td><td>１３</td><td><kbd>s</kbd></td><td>２５</td><td><kbd>W</kbd></td><td>３７</td><td><kbd>S</kbd></td></tr>
          <tr><td>２</td><td><kbd>e</kbd></td><td>１４</td><td><kbd>d</kbd></td><td>２６</td><td><kbd>E</kbd></td><td>３８</td><td><kbd>D</kbd></td></tr>
          <tr><td>３</td><td><kbd>r</kbd></td><td>１５</td><td><kbd>f</kbd></td><td>２７</td><td><kbd>R</kbd></td><td>３９</td><td><kbd>F</kbd></td></tr>
          <tr><td>４</td><td><kbd>t</kbd></td><td>１６</td><td><kbd>g</kbd></td><td>２８</td><td><kbd>T</kbd></td><td>４０</td><td><kbd>G</kbd></td></tr>
          <tr><td>５</td><td><kbd>y</kbd></td><td>１７</td><td><kbd>h</kbd></td><td>２９</td><td><kbd>Y</kbd></td><td>４１</td><td><kbd>H</kbd></td></tr>
          <tr><td>６</td><td><kbd>u</kbd></td><td>１８</td><td><kbd>j</kbd></td><td>３０</td><td><kbd>U</kbd></td><td>４２</td><td><kbd>J</kbd></td></tr>
          <tr><td>７</td><td><kbd>i</kbd></td><td>１９</td><td><kbd>k</kbd></td><td>３１</td><td><kbd>I</kbd></td><td>４３</td><td><kbd>K</kbd></td></tr>
          <tr><td>８</td><td><kbd>o</kbd></td><td>２０</td><td><kbd>l</kbd></td><td>３２</td><td><kbd>O</kbd></td><td>４４</td><td><kbd>L</kbd></td></tr>
          <tr><td>９</td><td><kbd>p</kbd></td><td>２１</td><td><kbd>;</kbd></td><td>３３</td><td><kbd>P</kbd></td><td>４５</td><td><kbd>+</kbd></td></tr>
          <tr><td>１０</td><td><kbd>@</kbd></td><td>２２</td><td><kbd>:</kbd></td><td>３４</td><td><kbd>`</kbd></td><td>４６</td><td><kbd>*</kbd></td></tr>
          <tr><td>１１</td><td><kbd>[</kbd></td><td>２３</td><td><kbd>]</kbd></td><td>３５</td><td><kbd>{</kbd></td><td>４７</td><td><kbd>}</kbd></td></tr>
        </tbody>
      </table>
    </div>
    <div class="alert alert-warn" style="margin-top:0.5rem;">
      <strong>注意：</strong>測定時は必ず <kbd>Ｃａｐｓ Ｌｏｃｋ</kbd> をＯＦＦにして下さい。ＯＮの状態では、小文字キーが大文字として認識され、意図しない機械番号に切り替わります。
    </div>
  </div>
</section>

<!-- APPENDIX 2 -->
<section id="appendix2">
  <div class="section-header">
    <span class="section-num">付録２</span>
    <h2>「ＤＲＳ」メイン画面 機能一覧表</h2>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th style="width:120px;">項目</th><th>説明</th></tr></thead>
      <tbody>
        <tr><td>測定器</td><td>現在選択されている測定器名を表示します。<kbd>Ｆ１</kbd>～<kbd>Ｆ１０</kbd>キーで測定器を変更します。</td></tr>
        <tr><td>機械番号</td><td>現在の測定対象製品番号（０～４７）を表示します。</td></tr>
        <tr><td>製品名</td><td>現在の測定対象製品名を表示します。</td></tr>
        <tr><td>日付</td><td>選択した日付の測定データを読み込みます。「測定準備」状態で使用できます。日付を変更すると機械番号は０号機にリセットされます。</td></tr>
        <tr><td>測定値リスト</td><td>現在の測定対象製品の測定データが表示されます（最大３００行）。</td></tr>
        <tr><td>開始</td><td>このボタンを押すと、「測定開始」状態になります。<kbd>ＥＳＣ</kbd>キーで「測定準備」状態になります。</td></tr>
        <tr><td>入力先番号</td><td>現在の測定値入力先番号を表示します。「自動」チェックで測定後自動で次の行を検索します。</td></tr>
        <tr><td>手動数値入力</td><td>手動で数値を入力したい場合に使用します。「削除」チェックで入力後にクリアします。</td></tr>
        <tr><td>手動文字入力</td><td>メモ等を入力したい場合に使用します。「削除」チェックで入力後にクリアします。</td></tr>
      </tbody>
    </table>
  </div>
</section>

<!-- APPENDIX 3 -->
<section id="appendix3">
  <div class="section-header">
    <span class="section-num">付録３</span>
    <h2>図面画面 機能一覧表</h2>
  </div>
  <div class="card">
    <p>図面画面は、メイン画面とは独立したウィンドウとして表示されます。製品登録時に自動表示され、メイン画面を閉じると自動的に閉じます。</p>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th style="width:140px;">機能</th><th>説明</th></tr></thead>
      <tbody>
        <tr><td>図面表示</td><td>製品フォルダ内のjpgファイルを自動読み込み表示します。</td></tr>
        <tr><td>ズーム</td><td>マウスホイールで拡大・縮小（０．１倍～５．０倍）。マウスカーソル位置为中心に動作します。</td></tr>
        <tr><td>移動</td><td>左クリック＋ドラッグで図面を移動出来ます。</td></tr>
        <tr><td>ウィンドウ</td><td>独立ウィンドウとして表示されます。閉じるボタンは非表示です。</td></tr>
      </tbody>
    </table>
  </div>
</section>

<!-- APPENDIX 4 -->
<section id="appendix4">
  <div class="section-header">
    <span class="section-num">付録４</span>
    <h2>「ＤＲＳ」運用フローチャート</h2>
  </div>
  <div class="steps">
    <div class="step">
      <p>一度だけ、PythonのインストールとＤＲＳのライブラリインストールを行います。</p>
    </div>
    <div class="step">
      <p>必要に応じて、ユーザー作成を行います。</p>
    </div>
    <div class="step">
      <p>測定機器の接続とＲＳ２３２Ｃ設定を行います（「設定」画面）。</p>
    </div>
    <div class="step">
      <p>基本的な運用を行うには、必要に応じて、「製品名」フォルダ作成・製品登録・製品登録解除を行います。</p>
    </div>
    <div class="step">
      <p>日常的には、「開始」→<kbd>Space</kbd>で測定のみ行います。</p>
    </div>
    <div class="step">
      <p>必要に応じて、寸法ファイル（Ｄａｔａ．ｘｌｓ）作成・図面ファイル（.jpg）作成を行います。</p>
    </div>
  </div>
</section>

<!-- APPENDIX 5 -->
<section id="appendix5">
  <div class="section-header">
    <span class="section-num">付録５</span>
    <h2>「ＤＲＳ」運用のヒント — ユーザー編</h2>
  </div>
  <div class="card">
    <h3>１．基本仕様</h3>
    <p>「ＤＲＳ」は、１つのユーザー名で４８個の製品（各製品は３００箇所まで測定可能）の測定データを１日１回入力出来ます。</p>
  </div>
  <div class="card">
    <h3>２．１日複数回の測定</h3>
    <p>現場で日に３回測定データを入力したい場合は、ユーザー名を「山田太郎（朝）」・「山田太郎（昼）」・「山田太郎（夕）」の様に３人分登録し、各ユーザー名に対して同じ製品を登録します。</p>
    <div class="alert alert-warn" style="margin-top:0.5rem;">
      「Ｄａｔａ．ｘｌｓ」に同じ製品の寸法を３回分登録する方法もありますが、この場合は１個の製品で測定出来るのは１００箇所に限定されます。
    </div>
  </div>
  <div class="card">
    <h3>３．協力会社別受け入れ検査</h3>
    <p>様々な協力会社から入荷した製品に対して、受け入れ検査を効率良く行いたい場合は、ユーザー名を、「山田太郎（Ａ精密）」・「山田太郎（Ｂ製作所）」・「山田太郎（Ｃ鉄工所）」の様に登録し、各ユーザー名に対して協力会社の製品を登録します。</p>
    <p style="margin-top:0.5rem;">又、１種類の製品に対して、ｎ＝５の様に何個か抜き取り検査を行う場合、１つのユーザー名に都度対象製品を登録・登録解除します。この方法が面倒な場合は、「山田太郎（Ａ精密 シャフト）」の様に、製品毎にユーザー名を登録する方法もあります。</p>
  </div>
  <div class="card">
    <h3>４．工程管理用データ取得</h3>
    <p>工程管理の為に、単純にデータを取りたい場合は、「ＣＰ値」等、専用の「製品名」フォルダを作成し、０号機に登録します。</p>
  </div>
</section>

<!-- APPENDIX 6 -->
<section id="appendix6">
  <div class="section-header">
    <span class="section-num">付録６</span>
    <h2>「ＤＲＳ」運用のヒント — データ管理編</h2>
  </div>
  <div class="card">
    <h3>１．ネットワーク運用</h3>
    <p>「ＤＲＳ」はネットワーク対応ですので、拠点間による運用も可能です。但し、通信速度によっては、データの読み込み・書き込みに時間がかかる場合があります。極力各拠点にサーバーを設置し、図面等のデータ管理を行う事をお勧めします。</p>
  </div>
  <div class="card">
    <h3>２．図面管理</h3>
    <p>図面表示機能を使用するのであれば、ＩＳＯ９００１の文書管理に関する規定に対応すべく、図面に「制定記号・改定番号・出図印を」を入れてからＰＣに取り込み、図面管理台帳にて管理する事をお勧めします。</p>
  </div>
  <div class="card">
    <h3>３．測定データファイル</h3>
    <p>保存される測定データファイルには、担当者名・号機・製品名・日付が入る為、そのままでＩＳＯ９００１の記録管理に関する規定に対応可能です。また、定期的にバックアップを取る事をお勧めします。</p>
  </div>
  <div class="card">
    <h3>４．不合格ログ</h3>
    <p>不合格のログはデータ分析に使用出来ます。必要に応じて整理する事をお勧めします。</p>
  </div>
</section>

<!-- CREDITS -->
<section id="credits">
  <div class="section-header">
    <span class="section-num">謝辞</span>
    <h2>使用ライブラリ</h2>
  </div>
  <div class="card">
    <h3>Python</h3>
    <p>Developer of Python(programming language)<br>
    Python Software Foundation and the community<br>
    <a href="https://www.python.org/" style="color:var(--primary);">https://www.python.org/</a></p>
  </div>
  <div class="card">
    <h3>pyserial</h3>
    <p>Developer of serial communication module<br>
    pyserial and the community<br>
    <a href="https://github.com/pyserial/pyserial" style="color:var(--primary);">https://github.com/pyserial/pyserial</a></p>
  </div>
  <div class="card">
    <h3>Qt / PySide6</h3>
    <p>Developer of GUI module<br>
    The Qt Company<br>
    <a href="https://www.qt.io/ja-jp/" style="color:var(--primary);">https://www.qt.io/ja-jp/</a></p>
  </div>
  <div class="card">
    <h3>xlrd / xlwt</h3>
    <p>Developer of xlrd and xlwt module<br>
    Portions copyright © 2005-2009, Stephen John Machin, Lingfo Pty Ltd All rights reserved.</p>
  </div>
</section>

</div>
</body>
</html>
