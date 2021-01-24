import textwrap
from PIL import Image, ImageDraw, ImageFont

def generate_meme(image_path, bottom_text='', font_path='./fonts/Roboto-Bold.ttf', font_size=9):
    # load image
    if len(bottom_text) >= 49:
        raise Exception('bottom_text length should not exceed 48. The length of bottom_text was: {}'.format(len(bottom_text)))
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size + 10) // 4 // (len(bottom_text)))
    print(font.size)
    offset = font.size // 10
    print(offset)
    # convert text to uppercase
    bottom_text = bottom_text.upper()

    # text wrappings
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw bottom lines
    if font.size >= 60:
        y = image_height - char_height * (len(bottom_lines) + len(bottom_lines) / 10) - 135 + offset
    else:
        y = image_height - char_height * (len(bottom_lines) + len(bottom_lines) / 10) - 145 + offset
    # y = image_height - char_height * (len(bottom_lines) + len(bottom_lines) / 10) - 135
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2 + 75
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # save meme
    im.save('meme-' + im.filename.split('/')[-1])