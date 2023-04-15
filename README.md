# インスタグラム自動操作ツール
## Description
インスタグラムの自動操作ツール

- 実装済み機能
    - 自動いいね
- アップデート予定
    - 自動フォロー
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

## Usage
- 任意の場所で`$ git clone <ここのURL>`
- `.env_tmp`をリネームもしくはコピーして`.env`を作成
- 以下を設定(quotationは不要)
    - `INSTAGRAM_USERNAME` : インスタグラムログイン時のユーザ名
    - `INSTAGRAM_PASSWORD` : インスタグラムログイン時のパスワード
    - `MAXIMUM_LIKES` : １日の自動いいね上限（デフォルト50）
    - `MAXIMUM_ERRORS` : １日のエラー許容上限（デフォルト10）
    - `CHROME_DRIVER_PATH` : Chromeドライバーへのパス
- `config/search_words.txt`内にいいね対象とするハッシュタグを設定
    - 改行区切り
    - 「#」は不要
- 実行
    - `$ poetry run ./main.py`