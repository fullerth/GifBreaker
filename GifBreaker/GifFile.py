"""GifFile contains tools to break down a gif file into individual elements"""

class Element():
    """Interface class for gif elements.

    Use Element.get_element() to get the element as a string of hex characters 
    suitable to write to a file.
    """

    def __init__(self, element):
        """Generic method to store an element as a string of hex characters."""
        self.element = element
    def get_element(self):
        """Return this full element composed as a string of hex characters."""
        return self.element

class Header(Element):
    """Represent, but probably don't tweak, a gif file Header."""
    
    def __init__(self, element='474946383961'):
        """Modifying this from default will break rendering on most platforms."""
        self.element = element

class LogicalScreenDescriptor(Element):
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

class ColorTable(Element):
    """Represent and tweak the global color table element of a gif."""

    def __init__(self, color_table_size, color_table):
        """Create a color table of size {0..7}, giving 2 to 256 colors.
      
        IN:
        color_table_size - Logical size of the color table {0..7}
        color_table - Color table in hex string format

        No internal consistency checking performed on these initilization values.
        """
        self.color_table_size = color_table_size
        self.element = color_table

class GraphicsControlExtension(Element):
    """Represent and tweak the values in a graphics control element of a gif."""

    def __init__(self, element):
        """Takes a fully formed graphics control element and stores it."""
        self.element = element

class ImageDescriptor(Element):
    """Represent and tweak an image description in a gif."""

    def __init__(self, element):
        """Takes a fully formed image description and stores it."""
        self.element = element

class ImageData(Element):
    """Represent and tweak image data in a gif."""

    def __init__(self, min_code_size, num_bytes, data, block_terminator="00"):
        """Creates an ImageData element from constituient parts
        
        IN:
        min_code_size - the minimum code size for the existing color table
        num_bytes - the number of bytes in the color table
        data - the actual image data as a string of hex bytes
        block_terminator - 00 in the format, also the default. Change at your own risk."""
        self.min_code_size = min_code_size
        self.num_bytes = num_bytes
        self.data = data
        self.block_terminator = block_terminator
        self.element = min_code_size+num_bytes+data+block_terminator

    @classmethod
    def fromElement(cls, element):
        min_code_size = element[0:2]
        num_bytes = element[2:4]
        #Add 4 to the read index to offset the 4 header ascii characters
        num_bytes_offset = int(num_bytes, 16) + 4
        return cls(min_code_size = min_code_size, num_bytes = element[2:4],
                data = element[4:num_bytes_offset],
                block_terminator = element[num_bytes_offset:num_bytes_offset+2])

class Footer(Element):
    """Represent the gif ending byte of 3B as a class, cause, i dunno. just cause"""

    def __init__(self, element="3B"):
        """Default value is correct, but will store another one if asked."""
        self.element = element

