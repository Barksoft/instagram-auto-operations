#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operations
import schedule

def main():
    operator = operations.AutoOperator()
    operator.auto_likes()
    # schedule.every().day.at("20:10").do(operator.auto_likes)
    
    # while True:
        # schedule.run_pending()
        # time.sleep(1)
        
if __name__ == '__main__':
    main()
