import requests as rq
import random

def fetch_data():
    while True:
        year = str(random.randint(1988, 2018))
        month = random.randint(1, 12)
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        day = random.randint(1, 31)
        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)
        xword_data = rq.get(f'https://raw.githubusercontent.com/doshea/nyt_crosswords/master/{year}/{month}/{day}.json')
       
        if xword_data.status_code != 200:
            continue
        else:
            return xword_data

def parse_data():
    pass


