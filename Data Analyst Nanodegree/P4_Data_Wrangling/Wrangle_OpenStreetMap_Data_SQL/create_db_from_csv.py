# Import csv files into sql database.

import csv
import sqlite3

# Create the database.
db = sqlite3.connect('san-jose_california.db')
c = db.cursor()

# Create nodes table.
c.execute("""CREATE TABLE nodes (
                id integer, 
                lat real, 
                lon real, 
                user text, 
                uid integer, 
                version text, 
                changeset integer, 
                timestamp text);"""
         )

with open('nodes.csv','rt') as f:
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])              for i in dr]

c.executemany("""INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)                     VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", to_db)

db.commit()


# Create nodes_tags table.
c.execute("""CREATE TABLE nodes_tags (
                    id integer, 
                    key text, 
                    value text, 
                    type text);"""
         )

with open('nodes_tags.csv','rt') as f:
    dr = csv.DictReader(f) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

c.executemany("""INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);""", to_db)

db.commit()


# Create ways table.
c.execute("""CREATE TABLE ways (
                    id integer, 
                    user text, 
                    uid integer, 
                    version text, 
                    changeset integer, 
                    timestamp text);"""
         )

with open('ways.csv','rt') as f:
    dr = csv.DictReader(f) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

c.executemany("""INSERT INTO ways (id, user, uid, version, changeset, timestamp)                     VALUES (?, ?, ?, ?, ?, ?);""", to_db)

db.commit()


# Create ways_nodes table.
c.execute("""CREATE TABLE ways_nodes (
                    id integer, 
                    node_id integer, 
                    position integer);"""
         )

with open('ways_nodes.csv','rt') as f:
    dr = csv.DictReader(f) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

c.executemany("""INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);""", to_db)

db.commit()


# Create ways_tags table.
c.execute("""CREATE TABLE ways_tags (
                    id integer, 
                    key text, 
                    value text, 
                    type text);"""
         )

with open('ways_tags.csv','rt') as f:
    dr = csv.DictReader(f) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

c.executemany("""INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);""", to_db)

db.commit()


db.close()

