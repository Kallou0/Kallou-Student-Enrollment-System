import sqlite3

conn = sqlite3.connect('sample.db')
print("Opened database successfully");

conn.execute('''CREATE TABLE students 
       (name TEXT  NOT NULL,
       reg_num TEXT  NOT NULL,
       id_num  TEXT  NOT NULL,
       year TEXT NOT NULL,
       course  TEXT);''')
print("Table created successfully");

conn.execute('''CREATE TABLE courses 
       (course_name TEXT  NOT NULL,
       abrv TEXT  NOT NULL);''')
print("Table created successfully");




