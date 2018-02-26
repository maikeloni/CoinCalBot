#!/bin/python
import coincalbot.coincalbot as bot
import configparser
import time

config = configparser.ConfigParser()
config.readfp(open('config.txt'))
url = config.get('Discord', 'url')
days_long = config.get('Discord', 'days_long')
categories_long = config.get('Discord', 'categories_long').split(",")
days_med = config.get('Discord', 'days_med')
categories_med = config.get('Discord', 'categories_med').split(",")
days_short = config.get('Discord', 'days_short')
categories_short = config.get('Discord', 'categories_short').split(",")

if days_short >= days_med or days_med >= days_long:
    print("Error: You have to set days_short < days_med < days_long")
else:
    while True:
        bot.discord(url, days_long, categories_long, days_med, categories_med, days_short, categories_short)
        print("Sleep for 1h before next fetching...")
        time.sleep(3600)
