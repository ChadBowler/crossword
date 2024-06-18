import unittest
from crossword_data import fetch_data


class TestCrosswordData(unittest.TestCase):
    def test_data_fetch(self):
        test_data = fetch_data(10)
        data_text = test_data.text
        status_code = test_data.status_code
        self.assertNotEqual(data_text, "404: Not Found")
        self.assertEqual(status_code, 200)


if __name__=="__main__":
    unittest.main()
