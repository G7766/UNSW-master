import pandas as pd
from flask import Flask
from flask_restplus import Resource,Api

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

@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        book = dict(df.loc[id])

        return book

if __name__ ==  '__main__':
    file = 'Books.csv'
    df = pd.read_csv(file)
    df = clean_data(df)
    #print(df)
    df.set_index('Identifier', inplace=True)
    print(df)
    app.run(debug='True')