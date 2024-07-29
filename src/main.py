
from .create_score_title import create_title
from .screenshot_of_score import screenshot_of_score

# OSU STANDARD
def create_scorepost(url):
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
    return title