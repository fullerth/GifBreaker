import unittest
import src.GifBreaker

class test_GifBreaker(unittest.TestCase):
    def compare_logical_screen(self, lsd, expected):
        self.assertEqual(lsd.canvas_width, expected['canvas_width'])
        self.assertEqual(lsd.canvas_height, expected['canvas_height'])
        self.assertEqual(lsd.color_ctrl_byte, expected['color_ctrl_byte'])
        self.assertEqual(lsd.background_color_index, expected['background_color_index'])
        self.assertEqual(lsd.pixel_aspect_ratio, expected['pixel_aspect_ratio'])

    def test_logical_screen_constructor(self):
        expected = {'canvas_width':'FEDC', 'canvas_height':'BA98', 'color_ctrl_byte':'76', 
                'background_color_index':'54', 'pixel_aspect_ratio':'32',
        }
        lsd = src.GifBreaker.logical_screen_descriptor(
                canvas_width = expected['canvas_width'], canvas_height = expected['canvas_height'],
                color_ctrl_byte = expected['color_ctrl_byte'], 
                background_color_index = expected['background_color_index'],
                pixel_aspect_ratio = expected['pixel_aspect_ratio'],
                )
        self.compare_logical_screen(lsd, expected)
        
    def test_logical_screen_from_element(self):
        expected = {'canvas_width':'0123', 'canvas_height':'4567', 'color_ctrl_byte':'89', 
                'background_color_index':'AB', 'pixel_aspect_ratio':'CD',
        }
        lsd_string = (expected['canvas_width'] + expected['canvas_height'] +
            expected['color_ctrl_byte'] + expected['background_color_index'] +
            expected['pixel_aspect_ratio'])
        lsd = src.GifBreaker.logical_screen_descriptor.fromElement(lsd_string)
        self.compare_logical_screen(lsd, expected)
