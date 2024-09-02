from flask import render_template, request, Flask, send_file, url_for
from PIL import Image
from werkzeug.middleware.profiler import ProfilerMiddleware

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


@app.route("/screenshot/<encoded_json_data>.jpeg")
def screenshot(encoded_json_data: str):
    """Screenshot path

    Args:
        screenshot_file_name (str): Screenshot file name
        encoded_json_data (str): Score object as json

    Returns:
        Response: Screenshot data
    """
    st = time.time()
    score_json = urllib.parse.unquote(encoded_json_data)
    j = json.loads(score_json)
    score = ScoreInfo(**j, score_ossapi=None)

    screenshot = generate_screenshot(score)
    ss_io = BytesIO()
    screenshot.save(ss_io, format="jpeg")
    ss_io.seek(0)
    print(f"screenshot link: {time.time() - st}")
    return send_file(ss_io, mimetype="image/jpeg")


@app.route("/", methods=["POST", "GET"])
def home():
    """_summary_

    Returns:
        str: home.html
    """

    # When user submits input
    st = time.time()
    if request.method == "POST":
        # Initialize input content and if screenshot checkbox was checked
        url = request.form["content"]
        checkbox_list = request.form.getlist("checkbox")

        screenshot_checked = "get screenshot" in checkbox_list

        custom_message_input = request.form["custom_message_content"]

        results = ""

        # Get score information from user input
        # ValueError is input is invalid
        try:
            score = get_score_info(url)
        except ValueError:
            if screenshot_checked:
                results = no_score_found
            return render_template(
                "home.html",
                score_title=not_valid_link_msg,
                image_src=default_score_img,
                results=results,
                input=url,
                screenshot_checked=screenshot_checked,
                custom_message_input=custom_message_input,
            )
        except IndexError:
            if screenshot_checked:
                results = no_score_found
            return render_template(
                "home.html",
                score_title=no_recent_score,
                image_src=default_score_img,
                results=results,
                input=url,
                screenshot_checked=screenshot_checked,
                custom_message_input=custom_message_input,
            )

        print("Successfully got ScoreInfo")

        # Get title of score
        title = create_title(score)
        print("Successfully generated title")

        # Insert custom message
        custom_message_input = request.form["custom_message_content"]
        if custom_message_input and not custom_message_input.isspace():
            title += f" | {custom_message_input}"

        # If checked, get screenshot and path to the screenshot and send
        # the score object as a json to /screenshot
        if screenshot_checked:
            # TODO: make this better
            score_json = json.dumps(score.__dict__)
            encoded_json_data = urllib.parse.quote(score_json, safe="")
            score_img = url_for(
                "screenshot",
                encoded_json_data=encoded_json_data,
            )
            results = "Screenshot successfully generated"
        else:
            score_img = default_score_img
            results = "Title successfully generated"

    else:  # Default page
        score_img = default_score_img
        title = default_title
        results = ""
        url = ""
        custom_message_input = ""
        screenshot_checked = True
    et = time.time()
    elapsed_time = et - st
    print(f"Generated scorepost in: {elapsed_time} seconds")
    return render_template(
        "home.html",
        score_title=title,
        image_src=score_img,
        results=results,
        input=url,
        screenshot_checked=screenshot_checked,
        custom_message_input=custom_message_input,
    )


if __name__ == "__main__":
    app.run(debug=True)
