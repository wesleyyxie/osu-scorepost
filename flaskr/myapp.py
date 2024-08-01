from flask import Blueprint, render_template, request, Flask
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
path_to_src = os.path.join(parent_dir, "src", "statistics")
sys.path.append(parent_dir)
sys.path.append(path_to_src)
from src import create_score_title, generate_screenshot
import time
app = Flask(__name__)

default_title = 'Player | Artist - Beatmap Title [Version] +MODS (Creator, 7.27*) 100% SS | 727pp'
default_score_img = '/static/default_score_image.png'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        not_valid_link_msg = "Please enter a valid score link"
        print(request.form)
        url = request.form['content']
        title = create_score_title.create_title(url)
        print(title)
        checkbox = request.form.getlist('checkbox')
        print(checkbox)
        if len(checkbox) > 0 and title != not_valid_link_msg:
            generate_screenshot.generate_ss(url)
            time.sleep(1)
            score_img = "/static/scorepost_generator_images/score.png"
        else:
            score_img = "/static/error_img.png"
       
    else:
        score_img = default_score_img
        title = default_title
    return render_template('index.html', score_title=title, image_src=score_img)

if __name__ == "__main__":
    app.run(debug=True)