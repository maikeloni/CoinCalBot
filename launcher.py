#!/bin/python
import coincalbot.coincalbot as bot
import configparser
import python_coinmarketcal.coinmarketcal.coinmarketcal as coinmarketcal
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
coinmarketcal_id = config.get('Coinmarketcal', 'id')
coinmarketcal_secret = config.get('Coinmarketcal', 'secret')

if int(days_short) >= int(days_med) or int(days_med) >= int(days_long):
    print("Error: You have to set days_short < days_med < days_long")
else:
    while True:
        coinmarketcal_token = coinmarketcal.getToken(coinmarketcal_id, coinmarketcal_secret)['access_token']
        bot.discord(url, days_long, categories_long, days_med, categories_med, days_short, categories_short, coinmarketcal_token)
        print("Sleep for 1h before next fetching...")
        time.sleep(3600)
