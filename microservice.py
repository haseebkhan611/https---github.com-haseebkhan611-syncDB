import sqlite3

connection = sqlite3.connect('UserData.db')

cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users1 (email TEXT PRIMARY KEY, name TEXT, status INTEGER)')

command = "INSERT INTO users1 VALUES ('haseebkhan611@gmail.com', 'Haseeb', 0)"
cursor.execute(command)

result = cursor.execute('SELECT * FROM users1')
print(result.fetchall())

# Commit the changes
connection.commit()

# Close the connection
connection.close()