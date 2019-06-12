import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource,Api, fields





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
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})





@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        book = dict(df.loc[id])

        return book

    def delete(self,id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        df.drop(id, inplace=True)
        return {"message": "Book {} is removed.".format(id)}, 200

    @api.expect(book_model)
    def put(self,id):
        if id not in df.index:
            api.abort(404,"Book {} doesn't exist.".format(id))

        # get the payload and convert it to a JSON
        book = request.json
        #print(book)

        # Book ID cannot be changed
        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400

        # Update the values
        for key in book:
            if key not in book_model.keys():
                #unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = book[key]
        #print(df)


        df.append(book, ignore_index=True)
        return {"message": "Book {} has been successfully updated".format(id)}, 200
'''
@app.route('/add_message/<id>', methods=['GET', 'POST'])
def add_message(id):
    content = request.json
    print('!!!!',content)
    return 'success'
'''


if __name__ ==  '__main__':
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    file = 'Books.csv'
    df = pd.read_csv(file)
    df = clean_data(df)
    #print(df)
    df.set_index('Identifier', inplace=True)
    #print(df)
    #print(df.loc[206, 'Place of Publication'])
    app.run(port = 8081,debug='True')