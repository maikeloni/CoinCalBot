# CoinCalBot
A bot fetching coinmarketcal.com and posting the events in discord.

## Requirements
* https://github.com/kyb3r/dhooks
* https://github.com/maikeloni/python-coinmarketcal

## Setup
1. Set discord webhook url in config.txt (see https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
2. Set other configs in config.txt, if you want.
3. ```python3 launch.py```

## config.txt
* url: Discord webhook url
* ```days_xxx``` and ```categories_xxx```:
  if event is earlier than ```days_xxx``` days in the future and if a category of the event is in ```categories_xxx```, then it will be posted.
 * ```days_short``` < ```days_med``` < ```days_long```
 
 Every event is posted three times respectively the ```days_xxx```
