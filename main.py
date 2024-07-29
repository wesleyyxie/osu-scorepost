import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join('src')
sys.path.append(module_dir)

from create_score_title import create_title
from screenshot_of_score import screenshot_of_score

# OSU STANDARD

while True:
    url = input("Enter score url:")
    try:
        title = create_title(url)
    except:
        print("Please try again! Invalid url or score does not exist")
    else:
        screenshot_of_score(url)
        print(title)
        break