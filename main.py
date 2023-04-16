#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operations
import schedule
import sys

def main():
    args = sys.argv
    if len(args) == 1:
        print("オプションを指定してください。")
        print("：自動いいね　：\tmain.py --like")
        print("：自動フォロー：\tmain.py --follow")
        exit()
    if args[1] == "--like":
        operator = operations.AutoOperator()
        operator.auto_likes()
    elif args[1] == "--follow":
        operator = operations.AutoOperator()
        operator.auto_follow()
    # schedule.every().day.at("20:10").do(operator.auto_likes)
    
    # while True:
        # schedule.run_pending()
        # time.sleep(1)
        
if __name__ == '__main__':
    main()
