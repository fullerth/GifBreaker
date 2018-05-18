class GifBreaker():
    header = '474946383961'
    logical_screen_descriptor = '0A000A00910000'
    global_color_table = 'FFFFFFFF00000000FF000000'
    graphics_control_extension = '21F9040000000000'
    image_descriptor = '2C000000000A000A0000'
    image_data = '02168C2D99872A1CDC33A00275EC95FAA8DE608C04914C0100'
    trailer = '3B'

    def write_gif_to_file(self):
        with open("output.gif", "wb") as f:
            f.write(bytes.fromhex(self.header))
            f.write(bytes.fromhex(self.logical_screen_descriptor))
            f.write(bytes.fromhex(self.global_color_table))
            f.write(bytes.fromhex(self.graphics_control_extension))
            f.write(bytes.fromhex(self.image_descriptor))
            f.write(bytes.fromhex(self.image_data))
            f.write(bytes.fromhex(self.trailer))
    
if __name__=="__main__":
    gb = GifBreaker()
    gb.write_gif_to_file()
