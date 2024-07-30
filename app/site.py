from flask import Blueprint, render_template, request
from app import flask_app
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from src import create_score_title, screenshot_of_score

default_title = 'Player | Artist - Beatmap Title [Version] +MODS (Creator, 7.27*) 100% SS | 727pp'
default_score_img = '/static/default_score_image.png'

@flask_app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form)
        try:
            url = request.form['content']
            checkbox = request.form.getlist('checkbox')
            title = create_score_title.create_title(url)
            print(len(checkbox))
            if len(checkbox) > 0:
                screenshot_of_score.screenshot_of_score(url)
                score_img = "/static/score.png"
            else:
                score_img = default_score_img
            print(title)
        except:
            title = "Please enter a valid score link"
            score_img = "/static/error_img.png"
    else:
        score_img = default_score_img
        title = default_title
    return render_template('index.html', score_title=title, image_src=score_img)