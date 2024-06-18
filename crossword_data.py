import requests as rq
import random

class Data():
    def __init__(self, json_data):
        self.json_data = json_data
        self.across_clues = []
        self.down_clues = []
        self.across_answers = []
        self.down_answers = []
        self.gridnums = []
        self.grid = []
        self.author = ""
        self.editor = ""
        self.copyright = ""
        self.date = ""
        self.publisher = ""
        self.title = ""

    def get_clues(self):
        self.across_clues = self.json_data["clues"]["across"]
        self.down_clues = self.json_data["clues"]["down"]
        

    def get_answers(self):
        self.across_answers = self.json_data["answers"]["across"]
        self.down_answers = self.json_data["answers"]["down"]
        

    def get_puzzle_info(self):
        self.author = self.json_data["author"]
        self.editor = self.json_data["editor"]
        self.copyright = self.json_data["copyright"]
        self.date = self.json_data["date"]
        self.publisher = self.json_data["publisher"]
        self.title = self.json_data["title"]

    def get_grids(self):
        self.gridnums = self.json_data["gridnums"]
        self.grid = self.json_data["grid"]

    


def fetch_data(retries):
    while True:
        retries -= 1
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
            if retries < 1:
                return f"Error fetching data: {xword_data.status_code}"
            continue
        else:
            return xword_data
    

def generate_new_puzzle():
    new_puzzle = Data(fetch_data())
    new_puzzle.get_clues()
    new_puzzle.get_answers()
    new_puzzle.get_grids()
    new_puzzle.get_puzzle_info()
    return new_puzzle