import requests
import datetime
import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
import pymongo
from flask_pymongo import PyMongo
import json

class dataOperation():
    def __init__(self):
        #link to mongodb and create db

        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.mydb = self.myclient["Wordbank_db"]
        self.mycollections = self.mydb["collection"]

        #link to local malab
        self.myclient = pymongo.MongoClient
        #mydict = {"name": "google", "alexa": "10000", "url": "https://www.google.com"}
        #x = mycol.insert_one(mydict)

    def print_datadict(self,data):
        print("{")
        for key in data.keys():
            attr = str(key)
            val = str(data[key])
            print("\t"+attr+":"+val)
        print("}")

    def get_data(self):
        datalist = []
        for i in range(1, 3):
            r = requests.get(
                "https://api.worldbank.org/v2/countries/all/indicators/NY.GDP.MKTP.CD?date=2012:2017&format=json&page={}".format(
                    i))
            data = r.json()
            for j in data[1]:
                datalist.append(j)
        return datalist

    def get_target_data(self,data,id):
        datalist = []
        for i in data:
            if i['indicator']['id'] == id:
                for key in i:
                    if key =='indicator':
                        indicator_value = i[key]['value']
                    if key == 'country':
                        p1 = i[key]['value']
                    if key == 'date':
                        p2 = i[key]
                    if key =='value':
                        p3 = i[key]
                t_dict = {'country':p1,
                        'date':p2,
                        'value':p3}
                #change dict to json format
                #t_dict = json.dumps(t_dict)
                datalist.append(t_dict)
        # collection of formatted data
        if datalist == []:
            return
        collection_data = {}
        collection_data['collection_id'] = ""
        collection_data['indicator'] = id
        collection_data['indicator_value'] = indicator_value
        collection_data['creation_time'] ="<creation_time>" #datetime.datetime.now()
        collection_data['entries'] = datalist
        return collection_data


    # insert / delete / query data in local mongodb
    def insert_collection(self, record):
        self.mycollections.insert_one(record)

    def delet_record(self, record):
        self.mycollections.delete(record)

    def find_record(self, record):
        return self.mycollections.find_one(record)



app = Flask(__name__)
api = Api(app,
          default="WorldBank",
          title="WorldBank Data Source",
          description="This is WorldBank Data Source.")
# PyMongo
app.config['MONGO_DBNAME'] = 'ass2_database'
app.config['MONGO_URI'] = 'mongodb://PGhost7:gpg19941011@ds139124.mlab.com:39124/ass2_database'
parser = api.parser()
parser.add_argument('query',type=str)
# mongo
mongo = PyMongo(app)


payload = api.model('Payload',{"indicator_id" : fields.String})

@api.route('/<collections>',methods = ['POST','GET'])
class import_data_Operation(Resource):
    @api.response(201, 'Data Created Successfully')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Data already exist')
    @api.expect(payload, validate=True)
    @api.doc(description="1- Import a collection from the data service")
    def post(self,collections):

        user = mongo.db[collections]

        #print(user)
        coll = dataOperation()
        indicator_id = request.json
        indicator_id = indicator_id['indicator_id']
        #print(indicator_id)
        data = coll.get_data()
        record = coll.get_target_data(data,indicator_id)
        #check if not exist
        if record == None:
            return {"message": "The input indicator id = {} doesn't exist in the data source".format(indicator_id)}, 400

        #check if is already exist
        for x in user.find({},{"indicator":1}):
            if x['indicator'] == indicator_id:
                return {"message": "The input indicator id = {} is already exit".format(indicator_id)}, 200
        # then
        record['indicator'] = indicator_id
        record['creation_time'] = str(datetime.datetime.now())
        #print(record)

        #insert to malab
        collection_id = user.insert_one(record)

        #print(collection_id.inserted_id)

        return_record  ={}
        return_record['location'] ='/'+collections+'/'+ str(collection_id.inserted_id)
        return_record['collection_id'] = str(collection_id.inserted_id)
        return_record['creation_time'] = record['creation_time']
        return_record['indicator'] = indicator_id

        return return_record,201

    @api.response(404, 'Data was not found')
    @api.response(200, 'Successful')
    @api.doc(description="3 - Retrieve the list of available collections")
    def get(self, collections):
        record_list= []

        # check if the name is exit or not
        collist = mongo.db.collection_names()
        if collections not in collist:
            return {"message": "There is not {} collections".format(collections)}, 404

        user = mongo.db[collections]
        for x in user.find():
            if x:
                record = {}
                record['location'] = '/' + collections + '/' + str(x['_id'])
                record['collection_id'] = str(x['_id'])
                record['creation_time'] = str(x['creation_time'])
                record['indicator'] = str(x['indicator'])
                record_list.append(record)

        return record_list,200





@api.route('/aaaa/<collection_id>')
class delete_data_Operation(Resource):
    @api.response(404, 'Data was not found')
    @api.response(200, 'Successful')
    @api.doc(description="2- Deleting a collection with the data service")
    def delete(self,collection_id):
        user = mongo.db['aaaa']
        for x in user.find({}, {"_id": 1}):
            if collection_id == str(x['_id']):
                user.delete_one(x)
                return {"message": "Collection = {} is removed from the database!".format(collection_id)}, 200

        api.abort(404, "Collection = {} is not exit!".format(collection_id))


    @api.response(404, 'Data was not found')
    @api.response(200, 'Successful')
    @api.doc(description="4 - Retrieve a collection")
    def get(self,collection_id):
        user = mongo.db['aaaa']
        for x in user.find():
            if collection_id == str(x['_id']):
                record={}
                record['collection_id'] = collection_id
                record['indicator'] = x['indicator']
                record['indicator_value'] = x['indicator_value']
                record['creation_time'] = x['creation_time']
                record['entries'] = x['entries']
                return record,200
        api.abort(404, "Collection = {} is not exit!".format(collection_id))

@api.route('/aaaa/<collection_id>/<year>/<country>')
class year_country(Resource):
    @api.response(404, 'Data was not found')
    @api.response(200, 'Successful')
    @api.doc(description="5 - Retrieve economic indicator value for given country and a year")
    def get(self,collection_id,year,country):
        user = mongo.db['aaaa']
        for x in user.find():
            if collection_id == str(x['_id']):
                for i in x['entries']:
                    if i['country'] == country and i['date'] == year:
                        record = {}
                        record['collection_id'] = collection_id
                        record['indicator'] = x['indicator']
                        record['country'] = i['country']
                        record['year'] = i['date']
                        record['value'] = i['value']

                        return record,200
        api.abort(404, "The country {} in {} year is not exit!".format(country,year))

@api.route('/aaaa/<collection_id>/<year>')
class Retrive_top_bottom(Resource):
    @api.response(404, 'Data was not found')
    @api.response(200, 'Successful')
    @api.doc(description="6 - Retrieve top/bottom economic indicator values for a given year")
    @api.expect(parser)
    def get(self, collection_id,year):
        user = mongo.db['aaaa']
        args = parser.parse_args()
        query=args['query']

        #query = request.args.get('query')
        #query = request.json()

        if query[:3] == 'top':
            query_type = 'top'
            number = query[3:]
            number = int(number)
            if number<1 or number>100:
                return "The query should be in 1-100", 404
        elif query[:6] == 'bottom':
            query_type = 'bottom'
            number = int(query[6:])
            if number<1 or number>100:
                return "The query should be in 1-100", 404
        else:
            return "top<N> and bottom<N> only.", 404

        for x in user.find():
            if collection_id == str(x['_id']):
                record = []
                for i in x['entries']:
                    if i['date'] == year:
                        record.append(i)
                length = len(record)
                if length == 0:
                    return "The data is not exit!",404

                record = sorted(record,key = lambda a:a['value'])

                record_list={}
                record_list['indicator'] = x['indicator']
                record_list['indicator_value'] = x['indicator_value']

                if query_type == 'top':
                    record = record[::-1]
                    if length < number:
                        record_list['entries'] = record
                        return record_list,200
                    if length >= number:
                        record_list['entries'] = record[:number]
                        return record_list
                if query_type == 'bottom':
                    if length < number:
                        record_list['entries'] = record
                        return record_list,200
                    if length >= number:
                        record_list['entries'] = record[:number]
                        return record_list
        return "The data is not exit!",404




if __name__ == '__main__':
    app.run(port=8081, debug=True)

