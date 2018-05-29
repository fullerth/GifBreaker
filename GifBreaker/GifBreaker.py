"""GifBreaker wants to help with breaking gifs.

It is a module that connects knobs to the elements of a gif element.
It should allow things like connecting a midi knob to the global color table
"""

from GifBreaker.GifFile import Header, LogicalScreenDescriptor, ColorTable, \
        GraphicsControlExtension, ImageDescriptor, ImageData, Footer

class GifBreaker():
    """GifBreaker renders a gif to a file.

    Growing a stock gif from Matthew's example during gif format decomposition
    """

    def __init__(self):
        """Currently we're growing a gif from Matthew's example."""
        self.header = Header()
        self.logical_screen_descriptor = LogicalScreenDescriptor(
                canvas_width = 'A000', canvas_height = 'A000', 
                color_ctrl_byte='91', background_color_index='00',
                pixel_aspect_ratio='00')
        self.global_color_table = ColorTable(2, 'BBBBBBFFAA0000CCFF002200')
        self.graphics_control_extension = GraphicsControlExtension('21F9040000000000')
        self.image_descriptor = ImageDescriptor(image_left = '0000', 
                image_top = '0000', image_width = '0A00', image_height = '0A00',
                packed_field = '00')
        self.image_data = ImageData(min_code_size = '02', num_bytes = '16',
            data = '8C2D99872A1CDC33A00275EC95FAA8DE608C04914C01')
        self.trailer = Footer()

    def add_local_color_table(self, size, data):
        """Add a static local color table to the one local image_data in this class.
        
        IN:
        size - integer size of the local color table {0..7}. Will be truncated to 3 bits.
        data - a hex string containing the local_color_table data
        """
        local_color_table_flag_mask = 0b10000000
        self.local_color_table = ColorTable(size, data)

        packed_temp = int(self.image_descriptor.packed_field, 16)
        packed_temp |= local_color_table_flag_mask
        packed_temp |= size
        packed_temp_str = "{:X}".format(packed_temp)
        self.image_descriptor.packed_field = packed_temp_str

    def write_gif_to_file(self, filename="output.gif"):
        """Write the gif out to a file."""
        with open(filename, "wb") as f:
            f.write(bytes.fromhex(self.header.get_element()))
            f.write(bytes.fromhex(self.logical_screen_descriptor.get_element()))
            f.write(bytes.fromhex(self.global_color_table.get_element()))
            f.write(bytes.fromhex(self.graphics_control_extension.get_element()))
            f.write(bytes.fromhex(self.image_descriptor.get_element()))
            f.write(bytes.fromhex(self.image_data.get_element()))
            f.write(bytes.fromhex(self.trailer.get_element()))

