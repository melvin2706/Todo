import sqlite3

connection = sqlite3.connect('test.db')

with open('schema.sql') as f:
    connection.executescript(f.read())


# cur = connection.cursor()

# cur.executemany(
#     "insert into Task (name, description) values (?,?)",
#     [
#         ('study', 'i have to study everyday'),
#         ('sport', 'i will do sports this evening')
#     ]
# )

connection.commit()
connection.close()