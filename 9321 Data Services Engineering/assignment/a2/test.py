from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
import pymongo
from flask_pymongo import PyMongo


app = Flask(__name__)
api = Api(app)
app.config['MONGO_DBNAME'] = 'ass2_database'
app.config['MONGO_URI'] = 'mongodb://PGhost7:gpg19941011@ds139124.mlab.com:39124/ass2_database'
mongo = PyMongo(app)

if __name__ == '__main__':
    mydict = {"name": "google", "alexa": "10000", "url": "https://www.google.com"}
    user = mongo.db['aaa']
    aaa = user.insert_one(mydict)
    print(aaa.inserted_id)
    print("***************BEFORE******************")
    for x in user.find({}, {"_id": 1}):
        print(x['_id'])
        #print(type(x['_id']))
        #print('!')

    collection_id = '5b9f6a4950914894a548dd89'
    for x in user.find({},{ "_id": 1}):
        if collection_id == str(x['_id']):
            user.delete_one(x)
            print("!!!")
            break
    print('???')
    print("***************AFTER******************")
    for x in user.find():
        print(x)


