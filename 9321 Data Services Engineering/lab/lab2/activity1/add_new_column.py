import sqlite3
sqlite_file = 'my_first_db.sqlite'
table_name = 'my_table_2'
id_column = 'my_1st_column'
new_column1 = 'my_4nd_column'  # name of the new column
new_column2 = 'my_5nd_column'
column_type = 'TEXT'
default_val = 'Hello World'


# Connecting to the database file
conn =sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
          .format (tn=table_name, cn=new_column1, ct=column_type))

# B) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' '{ct}' DEFAULT '{df}'"\
        .format(tn=table_name, cn=new_column2, ct=column_type, df=default_val))

conn.commit()
conn.close()
