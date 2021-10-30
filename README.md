# human
A Python tool to find human characteristics from an image
(work in progress)

## Installation
```bash
git clone https://github.com/themysticsavages/human.git
cd human
python3 -m pip install -r requirements.txt
```

## Usage
**DISCLAIMER: The image should only have one person in it and the person should be in the center as much as possible.**

Either this:
```bash
# Runs all the functions on picture.png (assuming it exists)
python3 process.py
```
Or this:
```python
from lib.human import Human

# Using the json parameter returns a JSON object: { 'hex': '#hex', 'rgb': [r,g,b], 'round': 'closest basic color to #hex' }
coolguy = Human('cool_guy.png')

coolguy.find_skin_color(json=False\True) # Find skin color
coolguy.find_shirt_color(json=False\True) # Find shirt color
coolguy.find_hair_color(json=False\True) # Find hair color
```

## Examples
```python
from lib.human import Human

person = Human('thisperson.jpg')
shirt = person.find_shirt_color('image', json=True)

if shirt['closest'] == 'green':
  print("Oh nice! You're wearing green!")
elif shirt['closest'] == 'blue':
  print('I like blue!')
```
```python
from lib.human import Human

guy = Human('somebody.png')

skin = guy.find_skin_color(json=True)['hex']
hair = guy.find_hair_color(json=True)['hex']

if skin == hair:
  print('Are you bald?')
```

#

Enjoy the program!
