from flask import render_template, request, Flask, send_file, url_for
from PIL import Image

import time
import os
from io import BytesIO
import urllib.parse
import json

from create_score_title import create_title
from generate_screenshot import generate_screenshot
from util.get_score import get_score_info, ScoreInfo

# Initialize Flask app
app = Flask(__name__)

app_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(
    app_dir, "static", "scorepost_generator_images", "screenshots"
)

# Initialize messages and default score path
default_title = (
    "Player | Artist - Beatmap Title [Version] (Creator, 0.00*) 0.00% SS | 0pp"
)
default_score_img = "/static/default_score.jpeg"
not_valid_link_msg = (
    "No score found, please enter a valid score link, user link, or username"
)
no_score_found = "No score found to generate screenshot"
no_recent_score = "No recent scores"


@app.route("/how_to_use")
def how_it_works():
    """How it works page

    Returns:
        str: how_to_use.html
    """
    return render_template("how_to_use.html")


@app.route("/contact")
def contact():
    """Contact page

    Returns:
        str: contact.html
    """
    return render_template("contact.html")


@app.route("/screenshot/<screenshot_file_name>/<encoded_json_data>.jpeg")
def screenshot(screenshot_file_name: str, encoded_json_data: str):
    """Screenshot path

    Args:
        screenshot_file_name (str): Screenshot file name
        encoded_json_data (str): Score object as json

    Returns:
        Response: Screenshot data
    """
    screenshot_path = os.path.join(screenshot_dir, screenshot_file_name)
    try:
        ss = Image.open(screenshot_path)
    except FileNotFoundError:
        score_json = urllib.parse.unquote_plus(encoded_json_data)
        j = json.loads(score_json)
        score = ScoreInfo(**j, score_ossapi=None)
        screenshot_path = os.path.join(screenshot_dir, generate_screenshot(score))
        ss = Image.open(screenshot_path)
    ss_io = BytesIO()
    ss.save(ss_io, format="JPEG")
    ss_io.seek(0)
    os.remove(screenshot_path)
    return send_file(ss_io, mimetype="image/jpeg")


@app.route("/", methods=["POST", "GET"])
def home():
    """_summary_

    Returns:
        str: home.html
    """

    # When user submits input
    if request.method == "POST":
        st = time.time()
        # Initialize input content and if screenshot checkbox was checked
        url = request.form["content"]
        checkbox = request.form.getlist("checkbox")
        checked = len(checkbox) > 0
        results = ""

        # Get score information from user input
        score = get_score_info(url)

        # If score is None or -1, do not process
        # score title or score and return with error messages
        if score == None:
            if checked:
                results = no_score_found
            return render_template(
                "home.html",
                score_title=not_valid_link_msg,
                image_src=default_score_img,
                results=results,
                input=url,
                checked=checked,
            )
        elif score == -1:
            if checked:
                results = no_score_found
            return render_template(
                "home.html",
                score_title=no_recent_score,
                image_src=default_score_img,
                results=results,
                input=url,
                checked=checked,
            )

        print("Successfully got ScoreInfo")

        # Get title of score
        title = create_title(score)
        print("Successfully generated title")

        # If checked, get screenshot and path to the screenshot and send
        # the score object as a json to /screenshot
        if checked:
            # TODO: make this better
            screenshot_file_name = generate_screenshot(score)
            print("Successfully generated screenshot")
            score_json = json.dumps(score.__dict__)
            encoded_json_data = urllib.parse.quote(score_json, safe="")
            score_img = url_for(
                "screenshot",
                screenshot_file_name=screenshot_file_name,
                encoded_json_data=encoded_json_data,
            )
            results = "Screenshot successfully generated"
        else:
            score_img = default_score_img
            results = "Title successfully generated"

        et = time.time()
        elapsed_time = et - st
        print(f"Generated scorepost in: {elapsed_time} seconds")
    else:  # Default page
        score_img = default_score_img
        title = default_title
        results = ""
        url = ""
        checked = True
    return render_template(
        "home.html",
        score_title=title,
        image_src=score_img,
        results=results,
        input=url,
        checked=checked,
    )


if __name__ == "__main__":
    app.run(debug=True)
