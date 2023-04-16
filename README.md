# インスタグラム自動操作ツール
## Description
インスタグラムの自動操作ツール

- 実装済み機能
    - 自動いいね
    - 自動フォロー
- アップデート予定
    - 自動アンフォロー
    - 自動投稿(ChatGPT)
    - その他要望に従う

## Requirements
- [Poetry](https://python-poetry.org/)

## Release Notes
- 2023/4/16（v1.0.0）
    - 未管理だったソースコードをリファクタリング
    - 環境変数を`.env`から読み込むよう修正
    - コマンドライン出力を見やすく修正
    - ログファイルを一つに統合
- 2023/4/16（v1.0.1）
    - ログに操作種別を記録するよう修正
    - ログにエラーを記録するよう修正
- 2023/4/16（v1.1.0）
    - 自動フォロー機能を実装
    - 実行方法を微修正(Usageを参照)
- 2023/4/16（v1.1.1）
    - エラー許容数が0に設定されている時、プログラムが開始しない問題を修正

## Usage
- 任意の場所で`$ git clone <ここのURL>`
- `.env_tmp`をリネームもしくはコピーして`.env`を作成
- 以下を設定(quotationは不要)
    - `INSTAGRAM_USERNAME` : インスタグラムログイン時のユーザ名
    - `INSTAGRAM_PASSWORD` : インスタグラムログイン時のパスワード
    - `MAXIMUM_LIKES` : １日の自動いいね上限（デフォルト50）
    - `MAXIMUM_FOLLOWS` : １日の自動フォロー上限（デフォルト20）
    - `MAXIMUM_ERRORS` : １日のエラー許容上限（デフォルト10）
    - `CHROME_DRIVER_PATH` : Chromeドライバーへのパス
- `config/search_words.txt`内にいいね対象／フォロー対象とするハッシュタグを設定
    - 改行区切り
    - 「#」は不要
- 依存パッケージインストール
    - `$ poetry install`
- 実行
    - 自動いいね　　：　`$ poetry run ./main.py --like`
    - 自動フォロー　：　`$ poetry run ./main.py --follow`
