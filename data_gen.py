import numpy as np
import shutil
import string
import os
from PIL import Image, ImageFont, ImageDraw

dim_x = 32
dim_y = 32
resource_folder = "./font_data/"
font_dir = "/usr/share/fonts/truetype"
data_dir = "./font_data"
training_file = "Train.csv"

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

def setup_folders():
    #Clear it all out if we have done this before
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        os.mkdir(data_dir)
    if os.path.exists(training_file):
        os.remove(training_file)

fonts = get_fonts()
setup_folders()
chars = list(string.ascii_letters) + list(string.digits)
f_association = []

#Do the work
for font_name in fonts:
  for tchar in chars:
    font = ImageFont.truetype(font_name , 16)
    size = font.getsize(tchar)
    offset = ((dim_x - size[0]) // 2, (dim_y - size[1]) // 2)
    rez = (dim_x,dim_y)
    fname = resource_folder + font_name[:-4] + "_" + tchar +".png" #Need to cut off file extension
    MakeImg(tchar,font, fname ,rez,offset)
    f_association.append(fname + "," + tchar)

#Write out the training associations
# Note, we could probably use less ram if we wrote this to disk periodically instead
with open(training_file, 'w') as f:
    f.write('\n'.join(f_association))
