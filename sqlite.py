#!/usr/bin/python3
import sqlite3

# Creates anticarium database if it does not exist
conn = sqlite3.connect('anticarium.db')

# Adds Regimes table to anticarium database
conn.execute('''CREATE TABLE REGIMES (
         ID INT PRIMARY KEY   NOT NULL,
         NAME           TEXT  NOT NULL,
         TEMPERATURE    REAL  NOT NULL,
         MOISTURE       INT   NOT NULL
         );''')

conn.close()

