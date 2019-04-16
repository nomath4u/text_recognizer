import multiprocessing as mp
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

#Global association :(
f_association = []

#Beginning ideas yoinked from https://nicholastsmith.wordpress.com/2017/10/14/deep-learning-ocr-using-tensorflow-and-python/

def MakeImg(t, f, fn, s, o, bg_color, text_color):
    '''
    Generate an image of text
    t:      The text to display in the image
    f:      The font to use
    fn:     The file name
    s:      The image size
    o:      The offest of the text in the image
    bg_color: Color of the background 
    text_color: Text color as a tuple (R,G, B) [0-255]
    '''
    img = Image.new('RGB', s, bg_color)
    draw = ImageDraw.Draw(img)
    draw.text(o, t, text_color, font = f)
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
    
def make_specific_image(font_name, tchar, tred, tgreen, tblue, bred, bgreen, bblue):
      font = ImageFont.truetype(font_name , 16)
      size = font.getsize(tchar)
      offset = ((dim_x - size[0]) // 2, (dim_y - size[1]) // 2)
      rez = (dim_x,dim_y)
      color_info = str(tred)+str(tgreen)+str(tblue)+str(bred)+str(bgreen)+str(bblue)
      fname = resource_folder + font_name[:-4] + "_" + tchar + "_" + color_info + ".png"
      text_color = (tred, tgreen, tblue)
      bg_color =  (bred, bgreen, bblue)
      MakeImg(tchar,font, fname ,rez,offset, text_color, bg_color)
      return (fname + "," + tchar)

def associate(f_association):
    with open(training_file, 'a') as f:
        f.write(f_association + "\n")

#Get data for worker threads
fonts = get_fonts()
chars = list(string.ascii_letters) + list(string.digits)
setup_folders()

#Make the pool
pool = mp.Pool(processes=8) #Currently selected for my laptop, is there a better way?
#use apply_async because we have many different arguements to loop over but also needs to be concurrant
for font_name in fonts:
    for tchar in chars:
        for tred in range(255):
            for tgreen in range(255):
                for tblue in range(255):
                    for bred in range(255):
                        for bgreen in range(255):
                            for bblue in range(255):
                                #make_specific_image(font_name, tchar, tred, tgreen, tblue, bred, bgreen, bblue) # This is just useful for debugging
                                pool.apply_async(make_specific_image, args=(font_name, tchar, tred, tgreen, tblue, bred, bgreen, bblue), callback = associate)
#Done with the pool
pool.close()
pool.join()
