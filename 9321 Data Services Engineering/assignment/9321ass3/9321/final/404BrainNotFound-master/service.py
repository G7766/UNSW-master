import json
from functools import wraps
import requests
from time import time
import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from pymongo import *
import datetime
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
import ml
import sqlite3
import numpy as np

class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)

app = Flask(__name__)
api = Api(app,authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="Predictions",  # Default namespace
          title="Match Prediction Dataset",  # Documentation Title
          description="This is just a simple example to show how publish data as a service.")  # Documentation Description


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated


# The following is the schema of match
match_model = api.model('match', {'p_name':fields.String,
                'H_name':fields.String,
                'H_buildUpPlaySpeed':fields.Integer,
                'H_buildUpPlayDribbling':fields.Integer,
                'H_buildUpPlayPassing':fields.Integer,
                'H_chanceCreationPassing':fields.Integer,
                'H_chanceCreationCrossing':fields.Integer,
                'H_chanceCreationShooting':fields.Integer,
                'H_defencePressure':fields.Integer,
                'H_defenceAggression':fields.Integer,
                'A_name':fields.String,
                'A_buildUpPlayDribbling':fields.Integer,
                'A_buildUpPlaySpeed':fields.Integer,
                'A_buildUpPlayPassing':fields.Integer,
                'A_chanceCreationPassing':fields.Integer,
                'A_chanceCreationCrossing':fields.Integer,
                'A_chanceCreationShooting':fields.Integer,
                'A_defencePressure':fields.Integer,
                'A_defenceAggression':fields.Integer
                })

credential_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String
})

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')
        user = db.users.find_one({"_id": username})
        if not user:
            api.abort(404, "Username: {} doesn't exist".format(username))
        if password != user['password']:
            api.abort(401, "Wrong password")
        return {"token": auth.generate_token(username)}


    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def post(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')
        user = {'_id':username,
                'password': password
        }

        posts = db.users
        try:
            posts.insert_one(user)
        except:
            return {"message" : "{} has already been signed".format(username)}, 400
        return { 
            "message" : "{} Register Successfully".format(username), 
            "prediction_id" : username
            }, 200


@api.route('/predictions')
class PredList(Resource):
    @api.response(201, 'Prediction Created Successfully')
    @api.response(200, 'OK')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new prediction")
    @api.expect(match_model, validate=True)
    @requires_auth
    def post(self):
        match = request.json
        match_id = match['p_name']
        match_input = np.array([(match['H_buildUpPlaySpeed'],match['H_buildUpPlayDribbling'],match['H_buildUpPlayPassing'],\
            match['H_chanceCreationPassing'],match['H_chanceCreationCrossing'],match['H_chanceCreationShooting'],\
            match['H_defencePressure'],match['H_defenceAggression'],\
            match['A_buildUpPlayDribbling'],match['A_buildUpPlaySpeed'],match['A_buildUpPlayPassing'],\
            match['A_chanceCreationPassing'],match['A_chanceCreationCrossing'],match['A_chanceCreationShooting'],\
            match['A_defencePressure'],match['A_defenceAggression'])])
        print(f'get post request: {match}')
        p = ml.regression_prediction(regre, match_X_test, match_y_test, match_input)
        print(f'get pred:\n{p}')
        
        time = datetime.datetime.now()
        date_str = time.strftime("%Y-%m-%d %H:%M:%S")
        posts = db.posts
        prediction = {'_id':match['p_name'],
                'H_name':match['H_name'],
                'H_buildUpPlaySpeed':match['H_buildUpPlaySpeed'],
                'H_buildUpPlayDribbling':match['H_buildUpPlayDribbling'],
                'H_buildUpPlayPassing':match['H_buildUpPlayPassing'],
                'H_chanceCreationPassing':match['H_chanceCreationPassing'],
                'H_chanceCreationCrossing':match['H_chanceCreationCrossing'],
                'H_chanceCreationShooting':match['H_chanceCreationShooting'],
                'H_defencePressure':match['H_defencePressure'],
                'H_defenceAggression':match['H_defenceAggression'],

                'A_name':match['A_name'],
                'A_buildUpPlayDribbling':match['A_buildUpPlayDribbling'],
                'A_buildUpPlaySpeed':match['A_buildUpPlaySpeed'],
                'A_buildUpPlayPassing':match['A_buildUpPlayPassing'],
                'A_chanceCreationPassing':match['A_chanceCreationPassing'],
                'A_chanceCreationCrossing':match['A_chanceCreationCrossing'],
                'A_chanceCreationShooting':match['A_chanceCreationShooting'],
                'A_defencePressure':match['A_defencePressure'],
                'A_defenceAggression':match['A_defenceAggression'],

                'result':p['prediction'],
                'accuracy':p['accuracy']
                }
        try:
            rp = posts.insert_one(prediction)
        except:
            print('aaaaaaaa')
            return {"message" : f"{match['p_name']} has already been posted, please use another prediction ID.",
                    "location" : f"/posts/{match['p_name']}" }, 400
        return { 
            "location" : f"/posts/{match['p_name']}", 
            "creation_time": date_str
            }, 201

    @api.response(200, 'Successful')
    @api.doc(description="Get all pred")
    @requires_auth
    def get(self):
        availiable_pred = []
        for item in db.posts.find():      
            p_id = item["_id"] 
            pred = { 
                "location" : "/predictions/{}".format(p_id), 
                "H_name" : item["H_name"],
                "A_name" : item["A_name"]
                }  
            availiable_pred.append(pred)
        return availiable_pred, 200



@api.route('/predictions/<pid>')
@api.param('pid', 'The prediction identifier')
class Pred(Resource):
    @api.response(404, 'prediction was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a detailed prediction by its ID")
    @requires_auth
    def get(self, pid):
        pred = db.posts.find_one({"_id": pid})
        if not pred:
            api.abort(404, "prediction with name: {} doesn't exist".format(pid))
        return pred, 200


    @api.response(404, 'Pred was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Delete a prediction by its ID")
    @requires_auth
    def delete(self, pid):
        delete_id = db.posts.delete_one({"_id": pid})
        if delete_id.deleted_count:
            return { 
                "message" :"prediction = {} is removed from the database!".format(pid)
                }, 200
        # deleted_count = 0, unexisting id 
        api.abort(404, "prediction: {} doesn't exist".format(pid))

if __name__ == '__main__':
    conn = sqlite3.connect("database.sqlite")

    match = ml.getMatch(conn)
    # Split the data into test and train parts
    match_X_train, match_y_train, match_X_test, match_y_test = ml.load_match(match, split_percentage=0.7)
    regre = ml.regression_train(match_X_train, match_y_train)

    client = MongoClient('mongodb://comp9321:comp9321@ds261332.mlab.com:61332/coralsdb')
    db = client['coralsdb']

    # run the application
    app.run(debug=True)
