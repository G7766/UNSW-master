import sqlite3

sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_3'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Retrieve column information
# Every column will be represented by a tuple with the following attributes:
# (id, name, type, notnull, default_value, primary_key)
c.execute('PRAGMA TABLE_INFO({})'.format(table_name))

'''
z=c.fetchall()
print(z)
print('')
[(0, 'id', 'TEXT', 0, None, 1), (1, 'date', '', 0, None, 0), (2, 'time', '', 0, None, 0), (3, 'date_time', '', 0, None, 0)]
'''
# collect names in a list
names = [tup[1] for tup in c.fetchall()]
print(names)
# e.g., ['id', 'date', 'time', 'date_time']

# Closing the connection to the database file
conn.close()