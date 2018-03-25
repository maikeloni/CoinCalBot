# CoinCalBot
A bot fetching coinmarketcal.com and posting the events in discord.

## Requirements
* https://github.com/kyb3r/dhooks
* https://github.com/maikeloni/python-coinmarketcal

## Setup
### Setup coinmarketcal
1. `git clone https://github.com/maikeloni/python-coinmarketcal.git python_coinmarketcal`
2. Set Coinmarketcal `id` and `secret` in config.txt. See https://github.com/maikeloni/python-coinmarketcal for more information.
### Setup discord
Set discord webhook url in config.txt (see https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
### Launch the bot
```python3 launch.py```

## config.txt
* url: Discord webhook url
* ```days_xxx``` and ```categories_xxx```:
  if event is earlier than ```days_xxx``` days in the future and if a category of the event is in ```categories_xxx```, then it will be posted.
 * ```days_short``` < ```days_med``` < ```days_long```
 
 Every event is posted three times respectively the ```days_xxx```
