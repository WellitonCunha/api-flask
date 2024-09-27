import psycopg2

conn = psycopg2.connect(database="python", host="localhost", user="postgres", password="root", port="5432")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE USERS (ID SERIAL PRIMARY KEY, NAME VARCHAR);''')
cursor.execute('''INSERT INTO USERS (NAME) VALUES ('WELLITON'),('JOÃO'),('MARIA');''')

conn.commit()
cursor.close()
conn.close()