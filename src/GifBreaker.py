class gif_element():
    def __init__(self, element):
        self.element = element
    def get_element(self):
        return self.element

class header(gif_element):
    def __init__(self, element='474946383961'):
        self.element = element

class logical_screen_descriptor(gif_element):
    def __init__(self, canvas_width, canvas_height, color_ctrl_byte,
           background_color_index, pixel_aspect_ratio):
       self.canvas_width = canvas_width
       self.canvas_height = canvas_height
       self.color_ctrl_byte = color_ctrl_byte
       self.background_color_index = background_color_index
       self.pixel_aspect_ratio = pixel_aspect_ratio
       self.element = canvas_width + canvas_height + color_ctrl_byte + background_color_index + pixel_aspect_ratio 
    @classmethod
    def fromElement(cls, element):
        return cls(element[0:4], element[4:8], element[8:10], element[10:12], element[12:14])

class GifBreaker():
    def __init__(self):
        self.header = header()
        self.logical_screen_descriptor = logical_screen_descriptor(
                canvas_width = 'A000', canvas_height = 'A000', 
                color_ctrl_byte='91', background_color_index='00',
                pixel_aspect_ratio='00')
        self.global_color_table = gif_element('FFFFFFFF00000000FF000000')
        self.graphics_control_extension = gif_element('21F9040000000000')
        self.image_descriptor = gif_element('2C000000000A000A0000')
        self.image_data = gif_element('02168C2D99872A1CDC33A00275EC95FAA8DE608C04914C0100')
        self.trailer = gif_element('3B')

    def write_gif_to_file(self):
        with open("output.gif", "wb") as f:
            f.write(bytes.fromhex(self.header.get_element()))
            f.write(bytes.fromhex(self.logical_screen_descriptor.get_element()))
            f.write(bytes.fromhex(self.global_color_table.get_element()))
            f.write(bytes.fromhex(self.graphics_control_extension.get_element()))
            f.write(bytes.fromhex(self.image_descriptor.get_element()))
            f.write(bytes.fromhex(self.image_data.get_element()))
            f.write(bytes.fromhex(self.trailer.get_element()))
    
if __name__=="__main__":
    gb = GifBreaker()
    gb.write_gif_to_file()
