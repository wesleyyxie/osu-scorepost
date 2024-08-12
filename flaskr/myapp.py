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

default_title = 'Player | Artist - Beatmap Title [Version] (Creator, 0.00*) 0.00% SS | 0pp'
default_score_img = '/static/default_score.png'

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        not_valid_link_msg = "Please enter a valid score link"
        print(request.form)
        url = request.form['content']
        try:
            title = create_score_title.create_title(url)
        except:
            title = not_valid_link_msg
        print(title)
        checkbox = request.form.getlist('checkbox')
        print(checkbox)
        if len(checkbox) > 0 and title != not_valid_link_msg:
            try:
                generate_screenshot.generate_ss(url)
                time.sleep(1)
                score_img = "/static/scorepost_generator_images/score.png"
                results = "Screenshot successfully generated"
            except:
                score_img = default_score_img
                results = "There was a problem generating your screenshot"
        else:
            score_img = default_score_img
            results = ""
    else:
        score_img = default_score_img
        title = default_title
        results = ""
    return render_template('home.html', score_title=title, image_src=score_img, results=results)

if __name__ == "__main__":
    app.run(debug=True)