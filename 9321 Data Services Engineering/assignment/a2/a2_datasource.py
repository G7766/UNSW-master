import requests
import datetime
import pymongo


def print_datadict(data):
    print("{")
    for key in data.keys():
        attr = str(key)
        val = str(data[key])
        print("\t"+attr+":"+val)
    print("}")

def print_datalist(data):
    for i in data:
        print_datadict(i)

def get_data():
    datalist = []
    for i in range(1,3):
        r = requests.get("https://api.worldbank.org/v2/countries/all/indicators/NY.GDP.MKTP.CD?date=2012:2017&format=json&page={}".format(i))
        data = r.json()
        for j in data[1]:
            datalist.append(j)
    return datalist


def get_target_data(data,id):
    datalist = []
    for i in data:
        if i['indicator']['id'] == id:
            for key in i:
                #print(key)
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
            #print_datadict(t_dict)
            datalist.append(t_dict)
    # collection of formatted data
    if datalist == []:
        return
    collection_data = {}
    #collection_data['collection_id'] = "<collection_id>"
    collection_data['indicator'] = id
    collection_data['indicator_value'] = indicator_value
    collection_data['creation_time'] = datetime.datetime.now()
    collection_data['entries'] = datalist
    # id plus 1
    return collection_data

def mydbOperation_insert(mydict):
    # connect to mongodb and creadte db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ass2"]
    mycol = mydb["collection"]

    # delete
    mycol.drop()

    # show all database name
    # dblist = myclient.list_database_names()

    #insert data
    x = mycol.insert_one(mydict)


def get_data_from_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ass2"]
    mycol = mydb["collection"]


if __name__ == '__main__':
    #print(datetime.datetime.now())

    # get resource data
    data = get_data()


    # let user to input  indicator id and get target data collection

    collection_data = get_target_data(data,"NY.GDP.MKTP.CD")
    print_datadict(collection_data)



    # connect to mongodb and create database
    # store connection_data to mongodb
    #mydict = collection_data
    #mydbOperation_insert(mydict)

