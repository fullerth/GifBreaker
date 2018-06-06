import unittest
from GifBreaker.GifBreaker import GifBreaker 

class test_GifBreaker(unittest.TestCase):
    def test_add_local_color_table(self):
        color_table_size = 1 
        expected_color_table_data = "QQQ"
        local_color_table_flag_mask = 0b10000000
        local_color_table_size_mask = 0b00000111
        gb = GifBreaker()
        gb.add_local_color_table(size=color_table_size, 
                data=expected_color_table_data)
        self.assertEqual(gb.local_color_table.get_element(), expected_color_table_data)

        packed_byte = int(gb.image_descriptor.packed_field, 16)
        packed_element = int(gb.image_descriptor.get_element()[7])
        # Check the Packed Field in the image descriptor to ensure that the
        # local color table flag and size are set correctly
        self.assertEqual(packed_byte & local_color_table_flag_mask, 
                local_color_table_flag_mask, "packed_field attribute value incorrect")
        self.assertEqual(packed_element & local_color_table_flag_mask,
                local_color_table_flag_mask, "element value incorrect")
        # Explicitly not shifting because the size of the local color table
        # is the last three bits of the packed byte
        self.assertEqual(packed_byte & local_color_table_size_mask, color_table_size, 
                "packed_field attribute value incorrect")
        self.assertEqual(packed_element & local_color_table_size_mask, color_table_size,
                "element value incorrect")

    def test_add_local_color_table_ValueError(self):
        color_table_size = 99
        expected_color_table_data = "QQQ"
        gb = GifBreaker()
        with self.assertRaises(ValueError):
            gb.add_local_color_table(size=color_table_size, 
                    data=expected_color_table_data)
