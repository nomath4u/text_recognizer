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
    
def make_specific_image(font_name, tchar):
      font = ImageFont.truetype(font_name , 16)
      size = font.getsize(tchar)
      offset = ((dim_x - size[0]) // 2, (dim_y - size[1]) // 2)
      rez = (dim_x,dim_y)
      fname = resource_folder + font_name[:-4] + "_" + tchar +".png" #Need to cut off file extension
      MakeImg(tchar,font, fname ,rez,offset)
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
        pool.apply_async(make_specific_image, args=(font_name, tchar), callback = associate)
#Done with the pool
pool.close()
pool.join()
