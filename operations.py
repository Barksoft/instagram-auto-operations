#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
import sys
import datetime
import time
import traceback
import pandas as pd
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

LOGIN_URL = "https://www.instagram.com/" # ログインURL
TAG_SEARCH_URL = "https://www.instagram.com/explore/tags/{}/?hl=ja"
FILE_WORDS = "config/search_words.txt" # いいねしたいワードの一覧ファイル
FILE_AUTO_LIKES_LOG = "logs/auto_likes_log.csv" # 自動いいねのログファイル

class AutoOperator:
    def __init__(self):
        print("\033[1m\033[045mインスタグラム自動操作プログラム\033[0m")
        print()
        load_dotenv()
        driver_path = os.getenv("CHROME_DRIVER_PATH")
        # Chromeの起動
        service = Service(executable_path=driver_path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def __get_search_words(self):
        file_check = os.path.isfile(FILE_WORDS)
        if file_check:
            print(f"\033[1m\033[046m以下ワードのハッシュタグ付き投稿をいいねします。\033[0m")
            words = []
            with open(FILE_WORDS,'r',encoding='utf-8') as f:
                for row in f:
                    if row != "":
                        word = row.strip()
                        words.append(word)
            print(f"\033[1m\033[096m#{', #'.join(words)}\033[0m")
            print()
        else:
            print(f"\033[1m\033[041m{FILE_WORDS}が見つかりません。処理を終了します。\033[041m" )
            exit()
        return words
    
    def __login(self, username, password):
        # Instagramを開く
        self.driver.get(LOGIN_URL)
        time.sleep(3)
        # ログイン処理
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys(username)
        time.sleep(1)
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)
        if "アカウントが不正使用されました" in self.driver.page_source:
            print(self.driver.page_source)
            print("ブロックされました。パスワードを変更する必要があります。")
            print("処理を終了します。")
            exit()
    
    def __get_post_hrefs_by_hashtag(self, word):
        # ハッシュタグの検索
        self.driver.get(TAG_SEARCH_URL.format(urllib.parse.unquote(word)))
        time.sleep(3)
        self.driver.implicitly_wait(10)
        # href要素を取得して投稿を抽出
        media_list = self.driver.find_elements(By.TAG_NAME, "a")
        href_list = []
        for media in media_list:
            href = media.get_attribute("href")
            if "/p/" in href:
                href_list.append(href)
        return href_list
    
    def auto_likes(self):
        # 環境変数の読み込み
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        max_likes = os.getenv("MAXIMUM_LIKES")
        max_errors = os.getenv("MAXIMUM_ERRORS")

        print("\033[1m\033[045m以下の設定で自動いいねを開始します。\033[0m")
        print(f"\033[1m\033[095mユーザ名　　　：  {username}\033[0m")
        print(f"\033[1m\033[095mパスワード　　：  {'*'*len(str(password))}\033[0m")
        print(f"\033[1m\033[095m最大いいね数　：  {max_likes}\033[0m")
        print(f"\033[1m\033[095m許容エラー数　：  {max_errors}\033[0m")
        print()

        # 動作環境依存変数
        today = str(datetime.date.today())

        # 検索ワード／ログファイルからデータの読み込み
        search_words = self.__get_search_words()
        logs = pd.read_csv(FILE_AUTO_LIKES_LOG)
        todays_rows = logs['date'] == today
        likes_rows = logs['operation'] == 'LIKE'
        executable_likes_left = int(max_likes) - logs.loc[todays_rows & likes_rows].shape[0] if int(max_likes) - logs.loc[todays_rows & likes_rows].shape[0] > 0 else 0
        print(f"\033[1m\033[096m本日（{today}）の自動実行済いいね！数 : \033[4m{logs.loc[todays_rows & likes_rows].shape[0]}（あと{executable_likes_left}回実行可能）\033[0m\n")
        if (logs['date'] == today).sum() >= int(max_likes):
            print(f"\n\033[1m\033[041m既に１日のいいね！の上限回数({max_likes})を超えています。処理を終了します。\033[0m")
            exit()

        self.__login(username, password)

        off = False
        error_count = 0
        for word in search_words:
            if off:
                break
            print(f"\033[1m\033[046m「#{word}」の自動いいね！を開始します。\033[0m\n")

            href_list = self.__get_post_hrefs_by_hashtag(word)
            for href in href_list:
                # いいね済みはパス
                if logs['url'].isin([href]).any():
                    print(f"\033[1m\033[043m[いいね！済]：\033[0m\033[1m\033[033m　{href}\033[0m")
                    continue

                # 投稿ページへ遷移
                self.driver.get(href)
                time.sleep(2)

                # いいね処理
                try:
                    dbl_clickable = self.driver.find_element(By.CLASS_NAME, "_aagw")
                    ActionChains(self.driver).double_click(dbl_clickable).perform()
                    time.sleep(2)

                    if "ブロックされています" in self.driver.page_source:
                        print("\033[1m\033[041mブロックされました。処理を終了します。\033[0m")
                        off = True
                        break

                    new_log = pd.DataFrame({
                        'date': [today],
                        'time': [datetime.datetime.now().time()],
                        'operation': 'LIKE',
                        'url': [href]
                    })
                    logs = pd.concat([logs, new_log])
                    todays_rows = logs['date'] == today
                    likes_rows = logs['operation'] == 'LIKE'
                    print(f"\033[1m\033[042m[本日{logs.loc[todays_rows & likes_rows].shape[0]}回目のいいね]：\033[0m\033[1m\033[032m　{href}\033[0m")

                    #BAN防止
                    if logs.loc[todays_rows & likes_rows].shape[0] >= int(max_likes):
                        print(f"\n\033[1m\033[041m１日のいいね！の上限回数({max_likes})を超えました。処理を終了します。\033[0m")
                        off = True

                except Exception as e:
                    ex, ms, tb = sys.exc_info()
                    print(ex)
                    print(ms)
                    traceback.print_tb(tb)
                    error_count += 1
                    time.sleep(5)
                    if error_count > int(max_errors):
                        print(f"\n\033[1m\033[041mエラーが{max_errors}回を超えました。処理を終了します。\033[0m")
                        off = True
                if off:
                    break
        logs.to_csv(FILE_AUTO_LIKES_LOG, index=False)
        print(f"\n\033[1m\033[096m[本日のいいね！回数]:　\033[4m{logs.loc[todays_rows & likes_rows].shape[0]}\033[0m")
