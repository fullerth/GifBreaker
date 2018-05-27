import unittest
from src.GifBreaker import GifBreaker 

class test_GifBreaker(unittest.TestCase):
    def test_add_local_color_table(self):
        gb = GifBreaker()
        gb.add_local_color_table()
        self.assertEqual
