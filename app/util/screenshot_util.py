import os
from PIL import Image


# paths to current directory and skin directory
current_dir = os.path.dirname(os.path.abspath(__file__))
skin_dir = os.path.join(current_dir, "assets", "skin")


def resize_image(im: Image.Image, n: float):
    """Returns a copy of the resized image where the dimensions
    are multiplied by n

    Args:
        im (Image.Image): Image
        n (float): multiplier

    Returns:
        Image.Image: Resized copy of im
    """

    # Dimensions of im
    w, h = im.size
    return im.resize((round(w * n), round(h * n)))


def write_with_img(s: str, x: int, y: int, size: float, im: Image.Image):
    """Writes string s in x,y coordinates with font size of multiple of size
    onto im.

    Args:
        s (str): String
        x (int): x-coordinate
        y (int): y-coordinate
        size (float): size multiplier
        im (Image.Image): Image
    """

    # Special size cases for dot and percent
    dot_width = 15
    dot_height = 35
    percent_width = 33
    percent_height = 35

    # Number to corresponding image file
    letters_dict = {
        "0": "berlin-0x",
        "1": "berlin-1x",
        "2": "berlin-2x",
        "3": "berlin-3x",
        "4": "berlin-4x",
        "5": "berlin-5x",
        "6": "berlin-6x",
        "7": "berlin-7x",
        "8": "berlin-8x",
        "9": "berlin-9x",
        ".": "berlin-dot.png",
        "%": "berlin-percent.png",
    }

    # Path to skin folder
    path = os.path.join(skin_dir, "Aristia", "num")

    # Start from the left
    left = 0
    space_size = 25

    # IF s is "None", then write 0, else, write the number
    if s == "None":
        char_name = f"{letters_dict["0"]}{size}.png"
        char_img = Image.open(os.path.join(path, char_name))
        im.paste(char_img, (x + left, y), char_img)
    else:
        # "." and "%" has different space sizes
        for char in s:
            if char == ".":
                char_img = Image.open(os.path.join(path, letters_dict[char]))
                im.paste(char_img, (x + left, y), char_img)
                space_size = space_size - 11  # adjust space size for after "."
                left += round(space_size * size)
            elif char == "%":
                char_img = Image.open(os.path.join(path, letters_dict[char]))
                im.paste(char_img, (x + left, y), char_img)
                left += round(space_size * size)
            else:
                char_img = Image.open(os.path.join(path, f"{letters_dict[char]}{size}.png"))
                im.paste(char_img, (x + left, y), char_img)
                if space_size != 25:  # convert back space size
                    space_size = 25
                left += round(space_size * size)
