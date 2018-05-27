import unittest
from GifBreaker.GifBreaker import GifBreaker

class test_GifBreakerModule(unittest.TestCase): 
    def test_write_to_file(self):
        """ Look at the gif file that's generated. Is it what you expected?"""
        filename = "write_to_file.gif"
        gb = GifBreaker()
        gb.write_gif_to_file(filename=filename)

    def test_add_local_color_table(self):
        """ Look at the gif file that's generated.
        It should be a color shifted version of the initial write_to_file test"""
        filename = "local_color_table.gif"
        gb = GifBreaker()
        gb.add_local_color_table(2, 'DDDDDD112233445566778800')
        gb.write_gif_to_file(filename=filename)
