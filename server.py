import keywordgenerator
import youtubetool
import aiohttp
import asyncio
from flask import Flask, request, render_template, jsonify,redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from data import math_topics
import os
from dotenv import load_dotenv
from openai import OpenAI
from urllib.parse import unquote
import random 



load_dotenv()
api_key= os.getenv("OPENAI_APIKEY")
YOUTUBE_API_KEY = os.getenv("youtube_api_key")
client = OpenAI(api_key=api_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = "suck my candy"


class LoginForm(FlaskForm):
    name = StringField("enter username",validators=[DataRequired()])
    password = PasswordField("enter Password")
    submit = SubmitField("Submit")



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return render_template("welcomeuser.html",name=name)



@app.route('/login',methods=['GET','POST'])
def login():
    name = None
    password = None
    form = LoginForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("login.html",
                            name=name,
                            password=password,
                            form=form)


@app.route('/signup')
def register():
    
    return render_template("signup.html",)

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/subjects')
def subjects():

    return render_template("subjects.html")


@app.route('/math')
def math():
    
    return render_template("math.html", data = math_topics)




@app.route('/topics/<topic_name>')
def topics(topic_name):
    subtopic_list = math_topics[topic_name]
    return render_template("topics.html",topic_name=topic_name, subtopic_list=subtopic_list)


@app.route('/topics/<topic_name>/<subtopic>/<requirement>')
def topic_subtopic(topic_name,subtopic,requirement):
    
    keywords = unquote(requirement)
    channel_id = 'UCEWpbFLzoYGPfuWUMFPSaoA'
    
    try:
        video = asyncio.run(youtubetool.search_videos(api_key=YOUTUBE_API_KEY, channel_id=channel_id, keywords=keywords ))

    except RuntimeError as e:
        

        loop = asyncio.get_event_loop()
        if loop.is_running():
            video = asyncio.ensure_future(youtubetool.search_videos(api_key=YOUTUBE_API_KEY, channel_id=channel_id, keywords=keywords))
        else:
            raise e
        
    video_url = video[1]


    return render_template("subtopic.html", topic_name=topic_name, requirement=requirement, subtopic = subtopic, word=keywords, video_url=video_url)


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    topic_name = request.form["topic_name"]
    requirement = request.form["requirement"]
    input = msg
    return get_Chat_response(input,topic_name,requirement)


def get_Chat_response(text,topic_name,requirement):


    messages = []
    system_prompt = f"you are a highschool math teacher teaching {requirement} for {topic_name}. Explainations should be clear and concise. Use point form for different points"
    system_msg = system_prompt
    messages.append({"role": "system", "content": system_msg})


    while text != "quit()":
        message = text
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500)
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


@app.route('/topics/<topic_name>/<subtopic>/<requirement>/quiz')
def popquiz(topic_name,requirement,subtopic):
   
    question_list = math_topics[topic_name][subtopic][1]
    question_selected = random.choice(question_list)["question_data"]
    option_a,option_b,option_c = question_selected["optionA"],question_selected["optionB"],question_selected["optionC"]
    question = question_selected["question"]
    rightOption = question_selected["rightOption"]

    return render_template("popquiz.html", topic_name=topic_name, requirement=requirement,question=question,
                           option_a=option_a,option_b=option_b,option_c=option_c,rightOption=rightOption
                            )



@app.route('/mixedquizlist')
def mixedquizlist():

    return render_template("mixedquizlist.html")


@app.route('/mixedquiz/<subject>')
def mixedquiz(subject):
        if subject == "math":
            question_list = []
            for subject, topics in math_topics.items():
                for topic, content in topics.items():
                    for item in content[1]:  # Assuming the questions are always in the second item of the list
                        question_list.append(item['question_data'])
            while True:
                question_selected = question_list[random.randint(0,len(question_list)-1)]
                option_a,option_b,option_c = question_selected["optionA"],question_selected["optionB"],question_selected["optionC"]
                question = question_selected["question"]
                rightOption = question_selected["rightOption"]





    
                return render_template("mixedquiz.html",question=question,option_a=option_a,option_b=option_b,option_c=option_c,rightOption=rightOption)













@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500




if __name__ == '__main__':
    app.run(debug=True)




