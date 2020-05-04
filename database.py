import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table

conn.execute('''CREATE TABLE ordersss
		(productId INTEGER PRIMARY KEY,
		orderId TEXT,
		orderPlacedOn TEXT,
		productQuantity INTEGER
		)''')

# conn.execute('''CREATE TABLE productss
# 		(productId INTEGER PRIMARY KEY,
# 		name TEXT,
# 		price REAL,
# 		stock INTEGER
# 		)''')

# conn.execute('''CREATE TABLE futuresales
# 		(productId INTEGER PRIMARY KEY,
# 		stock INTEGER
# 		)''')

# conn.execute('''CREATE TABLE futuresales2
# 		(productId INTEGER PRIMARY KEY,
# 		stock INTEGER,
# 		updatedOn TEXT
# 		)''')

# conn.execute('''CREATE TABLE users 
# 		(userId INTEGER PRIMARY KEY, 
# 		password TEXT,
# 		email TEXT,
# 		firstName TEXT,
# 		lastName TEXT,
# 		address1 TEXT,
# 		address2 TEXT,
# 		zipcode TEXT,
# 		city TEXT,
# 		state TEXT,
# 		country TEXT, 
# 		phone TEXT
# 		)''')



conn.close()

