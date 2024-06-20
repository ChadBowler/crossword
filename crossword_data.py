import requests as rq
import random

class Data():
    def __init__(self, json_data):
        self.json_data = json_data
        self.across_clues = []
        self.down_clues = []
        self.across_answers = []
        self.down_answers = []
        self.cols = 0
        self.rows = 0
        self.gridnums = []
        self.grid = []
        self.author = ""
        self.editor = ""
        self.copyright = ""
        self.date = ""
        self.publisher = ""
        self.title = ""

    def get_clues(self):
        clues = self.json_data.json()["clues"]
        self.across_clues = clues["across"]
        self.down_clues = clues["down"]
        

    def get_answers(self):
        answers = self.json_data.json()["answers"]
        self.across_answers = answers["across"]
        self.down_answers = answers["down"]
        

    def get_puzzle_info(self):
        self.author = self.json_data.json()["author"]
        self.editor = self.json_data.json()["editor"]
        self.copyright = self.json_data.json()["copyright"]
        self.date = self.json_data.json()["date"]
        self.publisher = self.json_data.json()["publisher"]
        self.title = self.json_data.json()["title"]

    def get_size(self):
        size = self.json_data.json()["size"]
        self.cols = size["cols"]
        self.rows = size["rows"]

    def get_grids(self):
        self.gridnums = self.json_data.json()["gridnums"]
        self.grid = self.json_data.json()["grid"]

    


def fetch_data(retries):
    # random.seed(0)
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
    new_puzzle = Data(fetch_data(5))
    if new_puzzle:
        new_puzzle.get_clues()
        new_puzzle.get_answers()
        new_puzzle.get_size()
        new_puzzle.get_grids()
        new_puzzle.get_puzzle_info()
        return new_puzzle
    else:
        raise Exception("Puzzle failed to generate.")