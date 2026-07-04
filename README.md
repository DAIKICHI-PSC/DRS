<!DOCTYPE html>
<html lang="ja">
<body>
<div class="container">

<!-- PAGE TITLE -->
<div class="page-title">
  <h1>ＤＲＳ ユーザーズマニュアル <span class="version">V2.5 Python版</span></h1>
</div>

<!-- HERO -->
<div class="hero">
  <h2>測定値自動入力システム</h2>
  <p>「ＤＲＳ」は、製造した製品の日常検査を、極力自動化する為のソフトウェアです。</p>
  <div class="img-wrap" style="margin-top:1.5rem;">
    <img src="https://github.com/DAIKICHI-PSC/DRS/blob/main/manual/manual.files/image074.jpg" style="max-height:260px;border-radius:8px;">
  </div>
</div>

<!-- OVERVIEW -->
<section id="overview">
  <div class="section-header">
    <span class="section-num">概要</span>
    <h2>プログラム概要</h2>
  </div>
  <div class="card">
    2005年にVisual Basic6で作成したプログラムを、AIエージェントとの対話でPythonに移植したソフトウェアです。<br><br>
    RS232Cが付いた、マイクロ、ハイトゲージ、投影機等に対応します。<br>
    作業者が、担当する機番に製品（寸法公差データ）を事前登録する事で、測定結果が自動で保存されます（ファイル名に担当者名、品名品番、機番、測定日が付与されます）。<br>
    測定値は、スペースキーを押すだけで、自動で記録されます。<br><br>
    マニュアル（manual.htm）は、Pythonで再実装された「ＤＲＳ Python版（V2.5）」の操作方法を説明します（画像は旧ソフトウェアのものです）。
  </div>
</section>
<br>
Source Code(ソースコード)<br>
https://github.com/DAIKICHI-PSC/DRS/archive/refs/tags/2.5.zip<br><br>
Excutable files(実行ファイル　ウイルスとして検出された場合は、使用を許可して下さい)<br>
https://github.com/DAIKICHI-PSC/DRS/releases/download/2.5/DRS_Python_2.5.zip
