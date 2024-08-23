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
        "0": "berlin-0.png",
        "1": "berlin-1.png",
        "2": "berlin-2.png",
        "3": "berlin-3.png",
        "4": "berlin-4.png",
        "5": "berlin-5.png",
        "6": "berlin-6.png",
        "7": "berlin-7.png",
        "8": "berlin-8.png",
        "9": "berlin-9.png",
        ".": "berlin-dot.png",
        "%": "berlin-percent.png",
    }

    # Path to skin folder
    path = os.path.join(skin_dir, "Aristia(Edit)", "num/")

    # Start from the left
    left = 0
    space_size = 25

    # IF s is "None", then write 0, else, write the number
    if s == "None":
        char_img = Image.open(os.path.join(path, letters_dict["0"]))
        char_img = resize_image(char_img, size)
        im.paste(char_img, (x + left, y), char_img)
    else:
        # "." and "%" has different space sizes
        for char in s:
            char_img = Image.open(os.path.join(path + letters_dict[char]))
            if char == ".":
                char_img = char_img.resize(
                    (round(dot_width * size), round(dot_height * size))
                )
                im.paste(char_img, (x + left, y), char_img)
                space_size = space_size - 11  # adjust space size for after "."
                left += round(space_size * size)
            elif char == "%":
                char_img = char_img.resize(
                    (round(percent_width * size), round(percent_height * size))
                )
                im.paste(char_img, (x + left, y), char_img)
                left += round(space_size * size)
            else:
                char_img = resize_image(char_img, size)
                im.paste(char_img, (x + left, y), char_img)
                if space_size != 25:  # convert back space size
                    space_size = 25
                left += round(space_size * size)
