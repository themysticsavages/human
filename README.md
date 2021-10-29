# human
A Python tool to find human characteristics from an image
(work in progress)

![img](https://raw.githubusercontent.com/ajskateboarder/stuff/main/usinghumanlib.gif)

## Installation
```bash
git clone https://github.com/themysticsavages/human.git
cd human
python3 -m pip install -r requirements.txt
```

## Usage
**DISCLAIMER: The image should only have one person in it and the person should be in the center.**

Either this:
```bash
# Runs all the functions on picture.png (assuming it exists)
python3 process.py -f image
```
Or this:
```python
from lib.human import Human

# Using the json parameter returns a JSON object: { 'hx': '#hex', 'rgb': [r,g,b], 'round': 'closest basic color to #hex' }
Human().find_skin_color('image', json=False\True) # Find skin color
Human().find_shirt_color('image', json=False\True) # Find shirt color
Human().find_hair_color('image', json=False\True) # Find hair color
```

#

Enjoy!
