import unittest
from GifBreaker.GifFile import LogicalScreenDescriptor, ColorTable, ImageData, \
        ImageDescriptor

class test_LogicalScreenDescriptor(unittest.TestCase):
    def compare_LogicalScreenDescriptor(self, lsd, expected):
        self.assertEqual(lsd.canvas_width, expected['canvas_width'])
        self.assertEqual(lsd.canvas_height, expected['canvas_height'])
        self.assertEqual(lsd.color_ctrl_byte, expected['color_ctrl_byte'])
        self.assertEqual(lsd.background_color_index, expected['background_color_index'])
        self.assertEqual(lsd.pixel_aspect_ratio, expected['pixel_aspect_ratio'])

    def test_LogicalScreenDescriptor_constructor(self):
        expected = {'canvas_width':'FEDC', 'canvas_height':'BA98', 'color_ctrl_byte':'76', 
                'background_color_index':'54', 'pixel_aspect_ratio':'32',
        }
        lsd = LogicalScreenDescriptor(
                canvas_width = expected['canvas_width'], canvas_height = expected['canvas_height'],
                color_ctrl_byte = expected['color_ctrl_byte'], 
                background_color_index = expected['background_color_index'],
                pixel_aspect_ratio = expected['pixel_aspect_ratio'],
                )
        self.compare_LogicalScreenDescriptor(lsd, expected)
        
    def test_LogicalScreenDescriptor_from_element(self):
        expected = {'canvas_width':'0123', 'canvas_height':'4567', 'color_ctrl_byte':'89', 
                'background_color_index':'AB', 'pixel_aspect_ratio':'CD',
        }
        lsd_string = (expected['canvas_width'] + expected['canvas_height'] +
            expected['color_ctrl_byte'] + expected['background_color_index'] +
            expected['pixel_aspect_ratio'])
        lsd = LogicalScreenDescriptor.fromElement(lsd_string)
        self.compare_LogicalScreenDescriptor(lsd, expected)

class test_ColorTable(unittest.TestCase):
    def test_ColorTable_constructor(self):
        expected_size = 8
        expected_color_table = "ABCDEF01234567"
        gct = ColorTable(expected_size, expected_color_table)

        self.assertEqual(gct.color_table_size, expected_size)
        self.assertEqual(gct.element, expected_color_table)
        
class test_ImageData(unittest.TestCase):
    def compare_ImageData(self, expected, observed):
        self.assertEqual(expected['min_code_size'], observed.min_code_size)
        self.assertEqual(expected['num_bytes'], observed.num_bytes)
        self.assertEqual(expected['data'], observed.data)
        self.assertEqual(expected['block_terminator'], observed.block_terminator)
        self.assertEqual(expected['element'], observed.element)

    def test_ImageData_constructor(self):
        expected = {}
        expected['min_code_size'] = "02"
        expected['num_bytes'] = "16"
        expected['data'] = "8C2D99872A1CDC33A00275EC95FAA8DE608C04914C01"
        expected['block_terminator'] = "00"
        expected['element'] = (expected['min_code_size'] + expected['num_bytes'] +
                expected['data'] + expected['block_terminator'])

        #Default block terminator
        id = ImageData(min_code_size=expected['min_code_size'],
                num_bytes = expected['num_bytes'],
                data = expected['data'])
        self.compare_ImageData(expected, id)

        expected['block_terminator'] = "AA"
        expected['element'] = (expected['min_code_size'] + expected['num_bytes'] +
                expected['data'] + expected['block_terminator'])
        id = ImageData(min_code_size=expected['min_code_size'],
                num_bytes = expected['num_bytes'], data = expected['data'], 
                block_terminator = expected['block_terminator'])
        self.compare_ImageData(expected, id)

    def test_ImageData_fromElement(self):
        expected = {}
        expected['min_code_size'] = "10"
        expected['num_bytes'] = "40"
        expected['data'] = "ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789"
        expected['block_terminator'] = "BB"
        expected['element'] = (expected['min_code_size'] + expected['num_bytes'] +
                expected['data'] + expected['block_terminator'])

        id = ImageData.fromElement(expected['element'])
        self.compare_ImageData(expected, id)

class test_ImageDescriptor(unittest.TestCase):
    def test_ImageDescriptor_constructor(self):
        expected = {}
        expected['image_separator'] = "2C" # This is always 2C
        expected['image_left'] = "1234"
        expected['image_top'] = "5678"
        expected['image_width'] = "9ABC"
        expected['image_height'] = "DEF0"
        expected['packed_field'] = "20"
        expected['element'] = (expected['image_separator'] + 
                expected['image_left'] + expected['image_top'] + 
                expected['image_width'] + expected['image_height'] + 
                expected['packed_field']) 
        i_d = ImageDescriptor(image_left = expected['image_left'],
                image_top = expected['image_top'],
                image_width = expected['image_width'],
                image_height = expected['image_height'],
                packed_field = expected['packed_field'])

        self.assertEqual(i_d.image_separator, expected['image_separator'])
        self.assertEqual(i_d.image_left, expected['image_left'])
        self.assertEqual(i_d.image_top, expected['image_top'])
        self.assertEqual(i_d.image_width, expected['image_width'])
        self.assertEqual(i_d.image_height, expected['image_height'])
        self.assertEqual(i_d.packed_field, expected['packed_field'])
        self.assertEqual(i_d.element, expected['element'])
