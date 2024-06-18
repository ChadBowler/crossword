import unittest
from crossword_data import fetch_data


class TestCrosswordData(unittest.TestCase):
    def test_data_fetch(self):
        test_data = fetch_data()
        self.assertNotEqual(test_data, "404: Not Found")


if __name__=="__main__":
    unittest.main()
