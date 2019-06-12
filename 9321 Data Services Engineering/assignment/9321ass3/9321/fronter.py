
import os,re, glob
from pathlib import Path
from collections import defaultdict
from flask import Flask, render_template, session, request
from datetime import datetime
import requests
import json

app = Flask(__name__)
##

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return render_template('home.html')

@app.route('/', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
	#curl -X GET "http://127.0.0.1:5000/token?username=admin&password=admin" -H "accept: application/json"
    #headers = {'Accept':'application/json'}
    r = requests.get('http://127.0.0.1:5000/token?username=' + str(username) + '&password=' + str(password))
    item = r.json()
    print(item)
    if r.ok:
    	global token
    	token = item['token']
    	return render_template('signin-ok.html', username = username)
    return render_template('form.html', message = 'invalid username or password', username = username)


@app.route('/predictions', methods=['GET'])
def get_pred_list():
    response = requests.get('http://127.0.0.1:5000/predictions', headers={'AUTH-TOKEN':token})
    print(token)
    item = response.json()
    print(item)
    if response.ok:
    	return render_template('signin-ok.html', username='username',data= item)
    return render_template('signin-ok.html', username='username',data=item['message'])

@app.route('/predictions', methods=['POST'])
def post_pred():
	if 'p_id' in request.form:
		p_id = request.form['p_id']
		response = requests.get('http://127.0.0.1:5000/predictions/'+str(p_id), headers={'AUTH-TOKEN':token} )
		item = response.json()
		print(item)
		if response.ok:
			return render_template('signin-ok.html', username='username',data3= item)
		return render_template('signin-ok.html', username='username',data3=item['message'])

	if 'team1' in request.form:
		team1 = request.form['team1']
		team2 = request.form['team2']
		team1speed = request.form['team1speed']
		team2speed = request.form['team2speed']
		team1crossing = request.form['team1crossing']
		team2crossing = request.form['team2crossing']
		global pid
		data = {'prediction_id':pid,
		'team1':team1,
		'team2':team2,
		'team1speed':int(team1speed),
		'team2speed':int(team2speed),
		'team1crossing':int(team1crossing),
		'team2crossing':int(team2crossing)
		}
	    #
	    #'Content-Type': 'application/json'

		print(data)

		response = requests.post('http://127.0.0.1:5000/predictions',headers={'AUTH-TOKEN':token},json=data)
		item = response.json()
		print(item)
		if response.ok:
			return render_template('signin-ok.html', username='username',data2=item)
		return render_template('signin-ok.html', username='username',data2=item['message'])

	if 'delete_id' in request.form:
		delete_id = request.form['delete_id']
		response = requests.delete('http://127.0.0.1:5000/predictions/'+str(delete_id), headers={'AUTH-TOKEN':token} )
		item = response.json()
		print(item)
		if response.ok:
			return render_template('signin-ok.html', username='username',data4= item)
		return render_template('signin-ok.html', username='username',data4=item['message'])


if __name__ == '__main__':
	token = ''
	pid = 0
	app.run(debug=True, port=2424)   #Ive change from 5000 to 2424
