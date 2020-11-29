import sqlite3
import pandas as pd

# Connect to db.
db = sqlite3.connect("san-jose_california.db")
c = db.cursor()

# Create a function to show quries as pandas dataframes.
def query_to_pandas(query, Title):
    c.execute(query)
    rows = c.fetchall()
    df = pd.DataFrame(rows)
    print('')
    print(Title)
    print(df.head(8))

query_to_pandas('select * from nodes', 'Nodes')
query_to_pandas('select * from ways', 'Ways')
query_to_pandas('select * from nodes_tags', 'Nodes tags')
query_to_pandas('select * from ways_tags', 'Ways tags')

# Create a function which executes queries and prints output.
def query_func(query, Title):
    # Execute query and print output.
    c.execute(query)
    rows = c.fetchall()

    # Loop over data.
    print('')
    print(Title)
    for row in rows:
        print(row[0])
        
query_func('SELECT COUNT(*) FROM nodes;', 'Number of nodes')

query_func('SELECT COUNT(*) FROM ways;', 'Number of ways')

query_func('SELECT COUNT(DISTINCT(e.uid)) FROM (SELECT uid FROM nodes \
            UNION ALL SELECT uid FROM ways) as e;', 'Number of unique users')

query_func('SELECT COUNT(*) FROM (SELECT e.user, COUNT(*) as num \
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
            GROUP BY e.user HAVING num=1)  u;', 'Number of users appearing only once')

query_func('SELECT e.user, COUNT(*) as num FROM \
            (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
            GROUP BY e.user ORDER BY num DESC LIMIT 5;', 'Top 5 contributing users')

query_func('SELECT value, COUNT(*) as num FROM nodes_tags \
           WHERE key="amenity" GROUP BY value ORDER BY num DESC LIMIT 5;', 'Top 5 amenities')

query_func('SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags \
           JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="restaurant") as i \
           ON nodes_tags.id = i.id WHERE nodes_tags.key ="cuisine" \
           GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 5;', 'Top 5 cuisine')

query_func('SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags \
           JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="cafe") as i \
           ON nodes_tags.id = i.id WHERE nodes_tags.key ="name" \
           GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 5;', 'Top 5 cafes')

query_func('SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags \
           JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="bank") as i \
           ON nodes_tags.id = i.id WHERE nodes_tags.key ="name" \
           GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 3;', 'Top 3 banks')

query_func('SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags \
           JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value ="place_of_worship") as i \
           ON nodes_tags.id = i.id WHERE nodes_tags.key ="religion" \
           GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 2;', 'Top 2 religions')

# Find the top 10 users contribution percentage.
query1 = 'SELECT SUM(num) FROM (SELECT e.user, COUNT(*) as num FROM \
        (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
        GROUP BY e.user ORDER BY num DESC LIMIT 10);'

query2 = 'SELECT SUM(num) FROM (SELECT e.user, COUNT(*) as num FROM \
        (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as e \
        GROUP BY e.user);'

c.execute(query1)
top10 = c.fetchone()[0]
    
c.execute(query2)
total = c.fetchone()[0]

percentage = round(top10*100/total, 0)
print()
print('Top 10 users contribution percentage: {}%'.format(percentage))


db.close()

