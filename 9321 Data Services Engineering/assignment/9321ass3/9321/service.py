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
match_model = api.model('match', {
    'prediction_id': fields.Integer,
    'team1': fields.String,
    'team2': fields.String,
    'team1speed': fields.Integer,
    'team2speed': fields.Integer,
    'team1crossing': fields.Integer,
    'team2crossing': fields.Integer,
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

        if username == 'admin' and password == 'admin':
            return {"token": auth.generate_token(username)}

        return {"message": "authorization has been refused for those credentials."}, 401




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
        print(f'get post request: {match}')
#############################################
######## ML: give match_model, get prediction
#############################################
        prediction = {
        '_id': 3,
        'team1':'team1_name',
        'team2':'team2_name',
        'team1speed':60,
        'team2speed':71,
        'team1crossing':39,
        'team2crossing':45,
        'pred':'0:0'
        }

        time = datetime.datetime.now()
        date_str = time.strftime("%Y-%m-%d %H:%M:%S")
        posts = db.posts        
        prediction_id = prediction['_id']
        try:
            posts.insert_one(prediction)
        except:
            return {"message" : "{} has already been posted".format(prediction_id),
                    "location" : "/posts/{}".format(prediction_id)}, 200
        return { 
            "location" : "/predictions/{}".format(prediction_id), 
            "prediction_id" : prediction_id,  
            "creation_time": date_str
            }, 201



    @api.response(200, 'Successful')
    @api.doc(description="Get all books")
    @requires_auth
    def get(self):
        availiable_pred = []
        for item in db.posts.find():      
            p_id = item["_id"] 
            pred = { 
                "location" : "/posts/{}".format(p_id), 
                "prediction_id" : p_id,
                "team1": item['team1'],
                "team2": item['team2']
                }  
            availiable_pred.append(pred)
        return availiable_pred, 200




@api.route('/predictions/<pid>')
@api.param('pid', 'The prediction identifier')
class Pred(Resource):
    @api.response(404, 'prediction was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a prediction by its ID")
    @requires_auth
    def get(self, pid):
        pred = db.posts.find_one({"_id": int(pid)})
        if not pred:
            api.abort(404, "prediction with id {} doesn't exist".format(pid))
        return pred, 200


    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Delete a prediction by its ID")
    @requires_auth
    def delete(self, pid):
        delete_id = db.posts.delete_one({"_id": int(pid)})
        if delete_id.deleted_count:
            return { 
                "message" :"prediction = {} is removed from the database!".format(pid)
                }, 200
        # deleted_count = 0, unexisting id 
        api.abort(404, "prediction: {} doesn't exist".format(pid))

if __name__ == '__main__':

    client = MongoClient('mongodb://comp9321:comp9321@ds261332.mlab.com:61332/coralsdb')
    db = client['coralsdb']

    # run the application
    app.run(debug=True)
