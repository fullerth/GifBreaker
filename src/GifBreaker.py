"""GifBreaker wants to help with breaking gifs.

It is a module that connects knobs to the elements of a gif element.
It should allow things like connecting a midi knob to the global color table
"""
class GifElement():
    """Interface class for gif elements.

    Use GifElement.get_element() to get the element as a string of hex characters 
    """

    def __init__(self, element):
        """Generic method to store an element as a string of hex characters."""
        self.element = element
    def get_element(self):
        """Return this full element composed as a string of hex characters."""
        return self.element

class Header(GifElement):
    """Represent, but probably don't tweak, a gif file Header."""
    
    def __init__(self, element='474946383961'):
        """Modifying this from default will break rendering on most platforms."""
        self.element = element

class LogicalScreenDescriptor(GifElement):
    """Represent and tweak a logical screen descriptor."""

    def __init__(self, canvas_width, canvas_height, color_ctrl_byte,
           background_color_index, pixel_aspect_ratio):
        """Create a logical screen descriptor.

        No spaces should be used in these strings.

        IN:
        canvas_width - 2 byte little endian hex character representation of width
        canvas_height - 2 byte little endian hex character representation of height
        color_ctrl_byte - 1 byte bitfield:
            [0:2] - Size of global color table {0..8}
            [3] - Sort Flag, not currently implemented
            [4:7] - Color Resolution {0..8}
            [8] - Global Color Table Flag: if true, Global Color Table follows
        background_color_index - 1 byte color to use for background pixels
        pixel_aspect_ratio - Does not seem to effect gif rendering in testing (Firefox).
        """ 
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.color_ctrl_byte = color_ctrl_byte
        self.background_color_index = background_color_index
        self.pixel_aspect_ratio = pixel_aspect_ratio
        self.element = canvas_width + canvas_height + color_ctrl_byte + background_color_index + pixel_aspect_ratio 
    @classmethod
    def fromElement(cls, element):
        """Decompose a LogicalScreenDescriptor from a string of hex characters."""
        return cls(element[0:4], element[4:8], element[8:10], element[10:12], element[12:14])

class GlobalColorTable(GifElement):
    """Represent and tweak the global color table element of a gif."""

    def __init__(self, color_table_size, color_table):
        """Create a color table of size {0..7}, giving 2 to 256 colors.
       
        No internal consistency checking performed on these initilization values.
        """
        self.color_table_size = color_table_size
        self.element = color_table

class GifBreaker():
    """GifBreaker renders a gif to a file.

    Growing a stock gif from Matthew's example during gif format decomposition
    """

    def __init__(self):
        """Currently we're growing a gif from Matthew's example."""
        self.Header = Header()
        self.LogicalScreenDescriptor = LogicalScreenDescriptor(
                canvas_width = 'A000', canvas_height = 'A000', 
                color_ctrl_byte='91', background_color_index='00',
                pixel_aspect_ratio='00')
        self.global_color_table = GlobalColorTable(2, 'FFFFFFFF00000000FF000000')
        self.graphics_control_extension = GifElement('21F9040000000000')
        self.image_descriptor = GifElement('2C000000000A000A0000')
        self.image_data = GifElement('02168C2D99872A1CDC33A00275EC95FAA8DE608C04914C0100')
        self.trailer = GifElement('3B')

    def write_gif_to_file(self):
        """Write the gif out to a file."""
        with open("output.gif", "wb") as f:
            f.write(bytes.fromhex(self.Header.get_element()))
            f.write(bytes.fromhex(self.LogicalScreenDescriptor.get_element()))
            f.write(bytes.fromhex(self.global_color_table.get_element()))
            f.write(bytes.fromhex(self.graphics_control_extension.get_element()))
            f.write(bytes.fromhex(self.image_descriptor.get_element()))
            f.write(bytes.fromhex(self.image_data.get_element()))
            f.write(bytes.fromhex(self.trailer.get_element()))
    
if __name__=="__main__":
    gb = GifBreaker()
    gb.write_gif_to_file()
