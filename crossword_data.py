import requests as rq
import random

class Data():
    def __init__(self):
        self.json_data = self.fetch_data(5)
        self.across_clues = self.json_data
        self.down_clues = self.json_data
        self.across_answers = self.json_data
        self.down_answers = self.json_data
        self.across_answer_dict = self.craft_across_ans_dict()
        self.down_answer_dict = self.craft_down_ans_dict()
        self.cols = self.json_data
        self.rows = self.json_data
        self.gridnums = self.json_data
        self.grid = self.json_data
        self.author = self.json_data
        self.editor = self.json_data
        self.cpyright = self.json_data
        self.date = self.json_data
        self.publisher = self.json_data
        self.title = self.json_data

    @property
    def across_clues(self):
        return self._across_clues    
    @across_clues.setter
    def across_clues(self, json_data):
        clues = json_data.json()["clues"]
        across_clues = clues["across"]
        # break up clues that are too long
        temp = []
        for clue in across_clues:
            if len(clue) > 45:
                words = clue.split(" ")
                first_half = " ".join(words[0:len(words)*2//3 + 1])
                second_half = " ".join(words[len(words)*2//3 +1:])
                temp.append(first_half)
                temp.append("      " + second_half)
            else:
                temp.append(clue)
        self._across_clues = temp
          
    @property
    def down_clues(self):
        return self._down_clues    
    @down_clues.setter
    def down_clues(self, json_data):
        clues = json_data.json()["clues"]
        down_clues = clues["down"]
        # break up clues that are too long
        temp = []
        for clue in down_clues:
            if len(clue) > 45:
                words = clue.split(" ")
                first_half = " ".join(words[0:len(words)*2//3 + 1])
                second_half = " ".join(words[len(words)*2//3 +1:])
                temp.append(first_half)
                temp.append("      " + second_half)
            else:
                temp.append(clue)
        self._down_clues = temp

    @property
    def across_answers(self):
        return self._across_answers    
    @across_answers.setter
    def across_answers(self, json_data):
        answers = json_data.json()["answers"]
        self._across_answers = answers["across"]

    @property
    def down_answers(self):
        return self._down_answers    
    @down_answers.setter
    def down_answers(self, json_data):
        answers = json_data.json()["answers"]
        self._down_answers = answers["down"]

    @property
    def cols(self):
        return self._cols    
    @cols.setter
    def cols(self, json_data):
        size = json_data.json()["size"]
        self._cols = size["cols"]

    @property
    def rows(self):
        return self._rows    
    @rows.setter
    def rows(self, json_data):
        size = json_data.json()["size"]
        self._rows = size["rows"]

    @property
    def gridnums(self):
        return self._gridnums    
    @gridnums.setter
    def gridnums(self, json_data):
        self._gridnums = json_data.json()["gridnums"]

    @property
    def grid(self):
        return self._grid    
    @grid.setter
    def grid(self, json_data):
        self._grid = json_data.json()["grid"]
    
    @property
    def author(self):
        return self._author    
    @author.setter
    def author(self, json_data):
        self._author = json_data.json()["author"]

    @property
    def editor(self):
        return self._editor    
    @editor.setter
    def editor(self, json_data):
        self._editor = json_data.json()["editor"]

    @property
    def cpyright(self):
        return self.__cpyright    
    @cpyright.setter
    def cpyright(self, json_data):
        self.__cpyright = json_data.json()["copyright"]

    @property
    def date(self):
        return self._date    
    @date.setter
    def date(self, json_data):
        self._date = json_data.json()["date"]

    @property
    def publisher(self):
        return self._publisher    
    @publisher.setter
    def publisher(self, json_data):
        self._publisher = json_data.json()["publisher"]

    @property
    def title(self):
        return self._title    
    @title.setter
    def title(self, json_data):
        self._title = json_data.json()["title"]

    # create a dictionary with numbers as keys and answers as values
    def craft_across_ans_dict(self):
        across_answer_dict = {}
        clues = self.json_data.json()["clues"]
        across_clues = clues["across"]
        for i in range(len(across_clues)):
            clue_key = across_clues[i].split(".")[0]
            across_answer_dict[clue_key] = self.across_answers[i]
        return across_answer_dict

    def craft_down_ans_dict(self):
        down_answer_dict = {}
        clues = self.json_data.json()["clues"]
        down_clues = clues["down"]
        for i in range(len(down_clues)):
            clue_key = down_clues[i].split(".")[0]
            down_answer_dict[clue_key] = self.down_answers[i]
        return down_answer_dict
        
    def fetch_data(self, retries):
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
  