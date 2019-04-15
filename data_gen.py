import numpy as np
import string
import os
from PIL import Image, ImageFont, ImageDraw

dim_x = 32
dim_y = 32
resource_folder = "./font_data/"
def MakeImg(t, f, fn, s = (100, 100), o = (16, 8)):
    '''
    Generate an image of text
    t:      The text to display in the image
    f:      The font to use
    fn:     The file name
    s:      The image size
    o:      The offest of the text in the image
    '''
    img = Image.new('RGB', s, "black")
    draw = ImageDraw.Draw(img)
    draw.text(o, t, (255, 255, 255), font = f)
    img.save(fn)

def get_fonts():
    fonts = []
    for root, dirs, files in os.walk("/usr/share/fonts/truetype"):
        for file in files:
            if file.endswith(".ttf"):
                fonts.append(file)
    return fonts

fonts = get_fonts()
chars = list(string.ascii_letters) + list(string.digits)
f_association = []
for font_name in fonts:
  for tchar in chars:
    font = ImageFont.truetype(font_name , 16) #eventual loop through all fonts
    size = font.getsize(tchar)
    offset = ((dim_x - size[0]) // 2, (dim_y - size[1]) // 2)
    rez = (dim_x,dim_y)
    fname = resource_folder + font_name[:-4] + "_" + tchar +".png" #Need to cut off file extension
    MakeImg(tchar,font, fname ,rez,offset)
    f_association.append(fname + "," + tchar)

with open('Train.csv', 'w') as f:
    f.write('\n'.join(f_association))
