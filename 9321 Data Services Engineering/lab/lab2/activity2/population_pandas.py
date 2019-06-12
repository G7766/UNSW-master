import sqlite3
import pandas as pd


conn = sqlite3.connect('population.sqlite')
cur = conn.cursor()
query = 'select country from Population where population > 50000000;'
z = cur.execute(query)
zz=[ i for i in z.fetchall() ]
#names = [tup[1] for tup in c.fetchall()]
print('z:',z)
print('zz:',zz)

print('~~~~~~~~~~~~~~~~~~')
df = pd.read_sql_query(query,conn) #The line that converts SQLite data to a Panda data frame
for country in df['country']:
    print(country)



