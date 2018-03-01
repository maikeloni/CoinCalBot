#!/usr/bin/env python3
# https://github.com/maikeloni/python-coinmarketcal
from coinmarketcal.coinmarketcal import getEvents
import datetime
# https://github.com/kyb3r/dhooks
from dhooks.discord_hooks import Webhook
import re
import requests as r
import sqlite3
import time


def postEvent(event, url):
    if event["date_event"]:
        date = time.strftime("%B %d, %Y", time.strptime(event["date_event"][0:10], "%Y-%m-%d"))
        if event["can_occur_before"]:
            date += " (or earlier)"

    embed = Webhook(url, color=123123)
    if event["coins"]:
        embed.add_field(name="Coin: **" + event["coins"][0]["name"] + " (" + event["coins"][0]["symbol"] + ")**", value=date, inline=False)
    if event["title"] and event["description"]:
        embed.add_field(name=event["title"], value=event["description"], inline=False)
    if event["categories"] != []:
        categories = ""
        for cat in event["categories"]:
            categories += cat + " "
        #  if event["categories"].index(cat) < len(event["categories"])-1:
        #      categories += ", "
        embed.add_field(name="Categories", value=categories, inline=False)
    if event["proof"]:
        embed.set_image(event["proof"])
    if event["source"]:
        embed.add_field(name="Source", value=event["source"] + "\n\n**Proof**", inline=False)
    embed.post()
    return None


def updateDB(event, times=1):
    if times != 0:
        db = sqlite3.connect("coinmarketcal.db")
        cursor = db.cursor()
        cursor.execute("SELECT POSTED FROM events WHERE ID = ?", (event["id"],))
        posted = cursor.fetchone()[0] + times
        cursor.execute("UPDATE events SET POSTED = " + str(posted) + " WHERE id = ?", (event["id"],))
        db.commit()
        db.close()
    return None


def selectPosted(event):
    db = sqlite3.connect("coinmarketcal.db")
    cursor = db.cursor()
    cursor.execute("SELECT POSTED FROM events WHERE ID = ?", (event["id"],))
    posted = cursor.fetchone()[0]
    db.commit()
    db.close()
    return posted


def setPostedInDB(posted):
    db = sqlite3.connect("coinmarketcal.db")
    cursor = db.cursor()
    cursor.execute("UPDATE events SET POSTED = " + str(posted))
    db.commit()
    db.close()
    return None


def fetchCoinMarketCal(days):
    latest_date = datetime.datetime.today() + datetime.timedelta(days=int(days))

    # find max page number
    try:
        cmc_url = "https://coinmarketcal.com"
        startpage = r.get(cmc_url)
        pattern = re.compile("(?<=\?page=)[0-9]*")
        max_page = int(max(pattern.findall(startpage.text)))
    except Exception as e:
        events = []
        return events

    events = []
    for page in range(1, max_page+1):
        events += getEvents(page=page, max=16)
        print("Page number " + str(page) + "/" + str(max_page) + " fetched.")
        print(events[-1]["date_event"][0:10])
        if latest_date < datetime.datetime.strptime(events[-1]["date_event"][0:10], "%Y-%m-%d"):
            print("Event is too far away. Stop fetching.")
            break
    return events


def writeFetchedToDB(event, days_long, days_med, days_short):
    db = sqlite3.connect("coinmarketcal.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS events " +
                   "(ID int, EVENT text, POSTED int)")
    cursor.execute("SELECT * FROM events WHERE ID = ?", (event["id"],))
    entry = cursor.fetchone()

    if entry is None:
        cursor.execute("INSERT INTO events VALUES (?,?,?)", (event["id"], str(event), 0,))
        print("New entry added")
        db.commit()
        db.close()

        # fit "Posted" for new events, which come early - Prints for debugging
        #  posted = selectPosted(event)
        #  print("Posted: " + str(posted))
        if eventIsInTime(event, days_short):
            #  print("Days_short")
            updateDB(event, times=2)
        elif eventIsInTime(event, days_med):
            #  print("Days_med")
            updateDB(event)
        #  posted = selectPosted(event)
        #  print("Posted: " + str(posted))
    else:
        print("Entry found")
        db.commit()
        db.close()
    return None


def eventIsInTime(event, days):
    latest_date = datetime.datetime.today() + datetime.timedelta(days=int(days))
    EVENT_IS_IN_TIME = False
    if latest_date >= datetime.datetime.strptime(event["date_event"][0:10], "%Y-%m-%d"):
        # Event is earlier than latest_date
        EVENT_IS_IN_TIME = True
    return EVENT_IS_IN_TIME


def eventHasCategory(event, categories):
    EVENT_HAS_CATEGORY = False
    if event["categories"] == []:
        EVENT_HAS_CATEGORY = True
    else:
        for category in event["categories"]:
            if category in categories:
                EVENT_HAS_CATEGORY = True
    return EVENT_HAS_CATEGORY


def discord(webhook_url, days_long, categories_long, days_med, categories_med, days_short, categories_short):
    # fetches coinmarketcal and posts the events on discord following the rules set in config.txt
    events = fetchCoinMarketCal(days_long)
    print(str(len(events)) + " events fetched")
    for event in events:
        print("EventID: " + str(event["id"]))
        writeFetchedToDB(event, days_long, days_med, days_short)

        # Check how often posted
        posted = selectPosted(event)
        if posted == 0:
            days = days_long
            categories = categories_long
        elif posted == 1:
            days = days_med
            categories = categories_med
        elif posted == 2:
            days = days_short
            categories = categories_short
        else:
            print("Already " + str(posted) + " times posted.")
            continue

        # Check if event is in the wanted time frame and has correct categories
        EVENT_IS_IN_TIME = False
        EVENT_HAS_CATEGORY = False
        if eventIsInTime(event, days):
            EVENT_IS_IN_TIME = True
        if eventHasCategory(event, categories):
            EVENT_HAS_CATEGORY = True
        if not EVENT_HAS_CATEGORY:
            print("Event won't be posted. Wrong categories.")
        if not EVENT_IS_IN_TIME:
            print("Event won't be posted. Event too far away.")
        if EVENT_HAS_CATEGORY and EVENT_IS_IN_TIME: 
            updateDB(event)
            postEvent(event, webhook_url)
            print("Posted!")
        print("")
    return None
