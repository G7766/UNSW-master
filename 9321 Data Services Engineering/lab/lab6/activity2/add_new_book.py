import pandas as pd
import json
from flask import Flask,request
from flask_restplus import Resource,Api, fields,reqparse, inputs




def clean_data(dataframe):
    # step1:London
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    #print(df['Place of Publication'])

    # step2:
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    df['Date of Publication'] = new_date
    new_date = pd.to_numeric(new_date)
    df['Date of Publication'] = new_date

    # step3:
    new_date = df['Date of Publication'].fillna(0)
    df['Date of Publication'] = new_date
    #print(df['Date of Publication'])

    # step4:
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]

    df.drop(columns_to_drop, inplace=True, axis=1)
    return df






app = Flask(__name__)
api = Api(app)


# The following is the schema of Book
book_model = api.model('Book', {
    'Flickr URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date of Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place of Publication': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in book_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)

#根据这个排序输出

@api.route('/books')
class BooksList(Resource):
    @api.expect(parser, validate=True)
    def get(self):
        # get books as JSON string
        args = parser.parse_args()

        # retrieve the query parameters
        order_by = args.get('order')
        ascending = args.get('ascending', True)

        if order_by:
            df.sort_values(by=order_by, inplace=True, ascending=ascending)

        json_str = df.to_json(orient='index')

        # convert the string JSON to a real JSON
        ds = json.loads(json_str)
        ret = []

        for idx in ds:
            book = ds[idx]
            book['Identifier'] = int(idx)
            ret.append(book)

        return ret

    @api.expect(book_model)
    def post(self):
        book = request.json
        if 'Identifier' not in book:
            return {"message": "Missing Identifier"}, 400
        id = book['Identifier']
        if id in df.index:
            return {"message": "A book with Identifier={} is already in the dataset".format(id)}, 400
        for key in book:
            if key not in book_model.keys():
                # unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = book[key]
        # df.append(book, ignore_index=True)
        return {"message": "Book {} is created".format(id)}, 201



@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        book = dict(df.loc[id])
        return book

    def delete(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        df.drop(id, inplace=True)
        return {"message": "Book {} is removed.".format(id)}, 200

    @api.expect(book_model)
    def put(self, id):

        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        # get the payload and convert it to a JSON
        book = request.json

        # Book ID cannot be changed
        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400

        # Update the values
        for key in book:
            if key not in book_model.keys():
                # unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = book[key]

        df.append(book, ignore_index=True)
        return {"message": "Book {} has been successfully updated".format(id)}, 200

if __name__ ==  '__main__':
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    file = 'Books.csv'
    df = pd.read_csv(file)
    df = clean_data(df)
    print(df)
    df.set_index('Identifier', inplace=True)
    #print(df)
    #print(df.loc[206, 'Place of Publication'])
    app.run(debug='True')