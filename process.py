import argparse
from lib.human import Human

parser = argparse.ArgumentParser(description='Find human characteristics from image')
parser.add_argument('-f', help='File to search')
args = parser.parse_args()

print('Hair color - '+Human().find_hair_color(args.f))
print('Skin color - '+Human().find_skin_color(args.f))
print('Shirt color - '+Human().find_shirt_color(args.f))