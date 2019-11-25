import os, dialogflow, requests,json, pusher, urllib
from flask import json
from flask import request,redirect,url_for,session
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import make_response
from flask_restplus import Resource, Api
# from weebhook_server import *
import argparse

from functools import wraps
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy


from server import course_info,weather,knowledge_info,recommendation,weebhook_server



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

#user table store user information
class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.name


@app.before_first_request
def create_db():
    if os.path.exists("data.db"):
        return

    db.create_all()

    # create admin, this line cannot be fixed.
    admin = User(name='admin', password='admin')
    db.session.add(admin)


    # insert some user example
    guestes = [User(name='guest1', password='guest1'),
               User(name='guest2', password='guest2')]
    db.session.add_all(guestes)
    db.session.commit()


#check if the user name and password are right
def valid_login(name, password):
    user = User.query.filter(and_(User.name == name, User.password == password)).first()
    if user:
        return True
    else:
        return False

#check if the user name has been registered
def valid_regist(name):
    user = User.query.filter(or_(User.name == name)).first()
    if user:
        return False
    else:
        return True

#for security, make sure some page can only be accessed after login
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('name'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return wrapper

@app.route('/')
def index():
	return render_template('index.html',name=session.get('name'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # login function
    if request.method == 'POST':
        if valid_regist(request.form['name']):
            error = 'account has not been signed up'

        elif valid_login(request.form['name'], request.form['pass']):
            session['name'] = request.form.get('name')
            return redirect(url_for('chatbot'))

        else:
            error = 'wrong name or password！'
    # access login page
    return render_template('login.html', error=error)

# logout api
@app.route('/logout')
def logout():
    # pop user session and return home page
    session.pop('name', None)
    return redirect(url_for('index'))

# user to sign up
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':

        # check if the password are equal
        if request.form['pass'] != request.form['re_pass']:
            error = 'passwords are different！'

        # check if user has been registered
        elif valid_regist(request.form['name']):
            user = User(name=request.form['name'], password=request.form['pass'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:

            error = 'name has been used'

    return render_template('sign_up.html', error=error)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    # login function
    if request.method == 'POST':
        if valid_regist(request.form['name']):
            error = 'Only admin can login.'

        elif valid_login(request.form['name'], request.form['pass']):
            session['name'] = request.form.get('name')
            return redirect(url_for('knowledge_base'))

        else:
            error = 'Wrong name or password！'

    return render_template('admin_login.html',error = error)


@app.route('/knowledge_base', methods=['GET','POST'])
def knowledge_base():
    if request.method == 'GET':
        return render_template('knowledge_base.html')

    keyword = request.form["keyword"]
    description = request.form["description"]
    advantage = request.form["advantage"]
    disadvantage = request.form["disadvantage"]
    example = request.form["example"]

    # create format to save in knowledge.json file
    sim = {}
    sim['description'] = description
    sim['advantages'] = advantage
    sim['disadvantages'] = disadvantage
    sim['example'] = example
    try:
        f = open("data/knowledge/knowledge.json", encoding='utf-8')
        setting = json.load(f)
        setting[keyword] = sim
        jsonData = json.dumps(setting,indent=4)
    except:
        m = {}
        m[keyword] = sim
        jsonData = json.dumps(m,indent=4)
    fileObject = open('data/knowledge/knowledge.json', 'w')
    fileObject.write(jsonData)
    fileObject.close()

    return redirect(url_for('successful'))

@app.route('/success')
def successful():
    return render_template('success.html')


# detect user itents according to question
# dialogflow detect intent function
def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)


        response = session_client.detect_intent(session=session, query_input=query_input)


        return  response.query_result

# chatbot route
@app.route('/chatbot', methods=['GET','POST'])
def chatbot():
    # if GET method caught
    if request.method == 'GET':
        return render_template('chatbot.html')
    # if POST method caught
    message = request.form['question']
    # print(message)

    # setting project id
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    # query_result_model:
    query_result = detect_intent_texts(project_id, "unique", message, 'en')

    # print(query_result)

    # here is some key parameter
    fulfillment_text = query_result.fulfillment_text

    # get action from dialogflow fulfillment_text
    action = query_result.action

    # using action to split into different server
    if fulfillment_text == "":
        if action =="Weather_Info":
            city = query_result.parameters["geo-city"]
            text = weather.weather(city)
        elif action =="Course_Info" or action == "Stream_Info":
            intents = query_result.intent.display_name
            params = query_result.parameters
            text = course_info.course_action(action,intents,params)
            print(text)
        elif action =="Recommendation":
            intents = query_result.intent.display_name
            params = query_result.parameters
            text = recommendation.recommendation_action(action,intents,params)
        elif action =="Google_Knowledge":
            intents = query_result.intent.display_name
            params = query_result.parameters
            text = knowledge_info.knowledge_action(action,intents,params,message)
        else:
            text = "There is not this model"
        response_text = {"message": text}
    else:
        # if not action has been detectd return dialogflow text
        text = fulfillment_text
        response_text = {"message": text}
    return jsonify(response_text)



# Run server
if __name__ == '__main__':
    app.run(debug = True)