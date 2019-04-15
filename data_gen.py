import numpy as np
import string
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

counter = 0

chars = list(string.ascii_letters) + list(string.digits)
for tchar in chars:
  font_name = "LiberationMono-Regular"
  font = ImageFont.truetype(font_name + ".ttf", 16) #eventual loop through all fonts
  size = font.getsize(tchar)
  offset = ((dim_x - size[0]) // 2, (dim_y - size[1]) // 2)
  rez = (dim_x,dim_y)
  f_association = []
  fname = resource_folder + font_name + "_" + tchar +".png"
  MakeImg(tchar,font, fname ,rez,offset)
