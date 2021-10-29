from colorthief import ColorThief
from sty import Style, RgbFg, fg
import numpy as np
import webcolors
import cv2
import sys
import os

'''
Find human characteristics from image
'''

class Colors():
  '''
  Some internal functions
  '''
  def nearest_color( subjects, query ): 
    return min( subjects, key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )
  colors = ( (255, 255, 255, "white"),
              (255, 0, 0, "red"),
              (128, 0, 0, "dark red"),
              (0, 255, 0, "green") )

class Human():
  '''
  Initiate a new 'Human' class
  '''
  def __init__(self):
    os.chdir(os.getcwd())
  def find_skin_color(self, f, json=False):
    '''
    Find skin color from image
    '''
    min_YCrCb, max_YCrCb = np.array([0,133,77],np.uint8), np.array([235,173,127],np.uint8)

    image = cv2.imread(f)
    imageYCrCb = cv2.cvtColor(image,cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)
    skinYCrCb = cv2.bitwise_and(image, image, mask = skinRegionYCrCb)

    cv2.imwrite('extskin.png', np.hstack([skinYCrCb]))
    thief = ColorThief('extskin.png')
    palette = thief.get_palette(color_count=10, quality=10)[0]
    r,g,b = palette
    fg.color = Style(RgbFg(r,g,b))

    os.remove('extskin.png')
    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return { 'skin_hx': webcolors.rgb_to_hex(palette), 'skin_rgb': [r, g, b],  'round': c }
    else:
      return str(webcolors.rgb_to_hex(palette)+' '+fg.color+'████'+fg.rs)
  def find_shirt_color(self, f, json=False):
    '''
    Find shirt color from image
    '''
    image = cv2.imread(f)
    h,w,c = image.shape
    body = image[0:int(round(w*2)), 100:int(round(w*2))]

    cv2.imwrite('extshirt.png', body)
    thief = ColorThief('extshirt.png')
    palette = thief.get_palette(color_count=10, quality=10)[0]
    r,g,b = palette
    fg.color = Style(RgbFg(r,g,b))

    os.remove('extshirt.png')
    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return { 'shirt_hx': webcolors.rgb_to_hex(palette), 'shirt_rgb': [r, g, b], 'round': c }
    else:
      return str(webcolors.rgb_to_hex(palette)+' '+fg.color+'████'+fg.rs)
  def find_hair_color(self, f, json=False):
    '''
    Find hair color from image
    '''
    image = cv2.imread(f)
    h,w,c = image.shape
    body = image[0:int(round(h/5)), 100:int(round(w/3))]

    cv2.imwrite('exthair.png', body)
    thief = ColorThief('exthair.png')
    palette = thief.get_palette(color_count=10, quality=10)[1]
    r,g,b = palette
    fg.color = Style(RgbFg(r,g,b))

    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return { 'hair_hx': webcolors.rgb_to_hex(palette), 'hair_rgb': [r, g, b], 'round': c }
    else:
      return str(webcolors.rgb_to_hex(palette)+' '+fg.color+'████'+fg.rs)

#print(human.find_skin_color(sys.argv[1]))
#print(human.find_shirt_color(sys.argv[1]))