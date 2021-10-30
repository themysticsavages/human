from colorthief import ColorThief
from sty import fg, rs, Style, RgbFg
import numpy as np
import webcolors
import requests
import dotenv
import cv2
import os

'''
Find human characteristics 
'''

phroomkey = dotenv.dotenv_values('.env')['PHOTOROOMAPIKEY']

class Colors():
  '''
  Some internal functions
  '''
  def nearest_color( subjects, query ): 
    return min( subjects, key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )
  colors = ( 
    (255, 255, 255, 'white'),
            (0, 0, 0, 'black'),
          (127, 127, 127, 'gray'),
         (160, 82, 45, 'sienna'),
      (136, 0, 21, 'bordeaux'),
     (237, 28, 36, 'red'),
      (255, 127, 39, 'orange'),
       (255, 242, 0, 'yellow'),
         (34, 177, 76, 'green'),
          (203, 228, 253, 'blue'),
            (0, 162, 232, 'dark blue'),
             (63, 72, 204, 'purple'),
            (255, 255, 255, 'white'),
           (195, 195, 195, 'light gray'),
          (185, 122, 87, 'light brown'),
         (255, 174, 201, 'light pink'),
        (255, 201, 14, 'dark yellow'),
       (239, 228, 176, 'light yellow'),
        (181, 230, 29, 'light green'),
         (153, 217, 234, 'light blue'),
        (224, 255, 255, 'light cyan'),
       (112, 146, 190, 'dark blue'),
    (200, 191, 231, 'light purple')
  )

class BG():
  '''
  BG things
  '''
  def __init__(self, xapikey):
    self.key = xapikey
  def remove_bg(self, f, o):
    '''
    Why do you need this?
    '''
    r= requests.post(
      'https://sdk.photoroom.com/v1/segment',
      headers={'x-api-key': str(self.key)},
      files={'image_file': open(f, 'rb')}
    )
    r.raise_for_status()
    with open(o, 'wb') as f:
      f.write(r.content)

class Human():
  def __init__(self, f):
    '''
    Initiate a new Human object
    '''
    self.f = f
  def find_skin_color(self, json=False):
    BG(phroomkey).remove_bg(self.f, 'transp_'+self.f)
    min_yc = np.array([0,133,77],np.uint8)
    max_yc = np.array([235,173,127],np.uint8)

    image = cv2.imread('transp_'+self.f, cv2.IMREAD_UNCHANGED)
    imageyc = cv2.cvtColor(image,cv2.COLOR_BGR2YCR_CB)
    skinRegionyc = cv2.inRange(imageyc,min_yc,max_yc)
    skinyc = cv2.bitwise_and(image, image, mask = skinRegionyc)

    cv2.imwrite('extskin.png', skinyc)
    color = ColorThief('extskin.png').get_palette(color_count=5)[0]

    r,g,b = color
    fg.color = Style(RgbFg(r,g,b))

    os.remove('extskin.png')
    os.remove('transp_'+self.f)
    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return {'hex': webcolors.rgb_to_hex(color), 'rgb': [r,g,b], 'closest': c }
    else:
      return webcolors.rgb_to_hex(color)+fg.color+' ████'+fg.rs

  def find_shirt_color(self, json=False):
    BG(phroomkey).remove_bg(self.f, 'transp_'+self.f)
    image = cv2.imread('transp_'+self.f, cv2.IMREAD_UNCHANGED)
    h,w,c = image.shape

    bth = image[h//2:h, 0:w]
    cv2.imwrite('extshirt.png', bth)
    color = ColorThief('extshirt.png').get_palette(color_count=5)[0]

    r,g,b = color
    fg.color = Style(RgbFg(r,g,b))

    os.remove('extshirt.png')
    os.remove('transp_'+self.f)
    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return {'hex': webcolors.rgb_to_hex(color), 'rgb': [r,g,b], 'closest': c }
    else:
      return webcolors.rgb_to_hex(color)+fg.color+' ████'+fg.rs
  def find_hair_color(self, json=False):
    BG(phroomkey).remove_bg(self.f, 'transp_'+self.f)
    image = cv2.imread('transp_'+self.f, cv2.IMREAD_UNCHANGED)
    h,w,c = image.shape

    fhc = image[0:-w//2, h//2:h]
    cv2.imwrite('exthair.png', fhc)
    color = ColorThief('exthair.png').get_palette(color_count=5)[0]

    r,g,b = color
    fg.color = Style(RgbFg(r,g,b))

    os.remove('exthair.png')
    os.remove('transp_'+self.f)
    if json:
      r,g,b,c = Colors.nearest_color(Colors.colors, (r, g, b))
      return {'hex': webcolors.rgb_to_hex(color), 'rgb': [r,g,b], 'closest': c }
    else:
      return webcolors.rgb_to_hex(color)+fg.color+' ████'+fg.rs
