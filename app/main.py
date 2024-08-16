from flask import render_template, request, Flask
from .scorepost.create_score_title import create_title
from .scorepost.generate_screenshot import generate_ss
from .scorepost.util.get_score import get_score_info
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
        st = time.time()
        not_valid_link_msg = "No score found, please enter a valid score link, user link, or username"
        url = request.form['content']
        checkbox = request.form.getlist('checkbox')
        checked = len(checkbox) > 0
        try:
            score = get_score_info(url)
            print("successfully got score!")
        except Exception as e:
            print(e)
            score = False
            print("error did not get score!")

        if score != False:
            try:
                title = create_title(score)
                generated_title = True
                print("successfully created title!")
            except Exception as e: 
                print(e)
                title = not_valid_link_msg
                generated_title = False
                print("ERROR IN CREATING TITLE!")
            
            if checked and generated_title:
                try:    
                    screenshot_file_name = generate_ss(score)
                    score_img = f"/static/scorepost_generator_images/{screenshot_file_name}"
                    results = "Screenshot successfully generated"
                    print("successfully made ss!")
                except Exception as e: 
                    print(e)
                    score_img = default_score_img
                    results = "There was a problem generating your screenshot"
                    print("ERROR IN MAKING SS!")
            else:
                score_img = default_score_img
                results = ""
        else:
            score_img = default_score_img
            results = ""
            title = not_valid_link_msg
            
        et = time.time()
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')
    else:
        score_img = default_score_img
        title = default_title
        results = ""
        url=""
        checked=True
    return render_template("home.html", score_title=title, image_src=score_img, results=results, input=url, checked=checked)